#!/usr/bin/env python3
"""M3 verification suite — NT1..NT8 + E2E walkthrough per
outputs/milestones/milestone_3/tests_milestone_3.md.

Run:  python3 verify_milestone_3.py
Exit 0 = all nodes pass, 1 = any failure. The suite is hermetic: every run uses
a temp package tree (copied wizard + adapters + kit) and a temp HOME, so the
user's real tool installs are never touched. PTY tests drive the real wizard
over a pseudo-terminal (masked key entry, guide slot, key-entry rules).
"""
import json
import os
import pty
import re
import select
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
WIZARD = os.path.join(REPO, "bin", "setup-wizard.js")
INSTALLERS = os.path.join(REPO, "installers")
KIT = os.path.join(REPO, "kit")
PKG = os.path.join(REPO, "package.json")

NODE = shutil.which("node")
if not NODE:
    sys.stderr.write("node not found on PATH — M3 verification requires Node >= 18\n")
    sys.exit(2)

ADAPTERS = ["claude-code.js", "claude-desktop.js", "opencode.js", "antigravity.js"]
ADAPTER_NAMES = ["Claude Code", "Claude Desktop", "OpenCode", "Antigravity"]
KEY_NAMES = ["NVIDIA_NIM_API_KEY", "GOOGLE_AISTUDIO_API_KEY", "OLLAMA_API_KEY"]
KIT_MARK = "name: sdd-multiagent-kit"
INVOCATION = "Invocation: /sdd"

# The package version is read from package.json, never hard-coded here. Pinning
# a literal made a correct release bump fail this suite, which would deadlock
# version-driven publishing; what these tests must assert instead is that every
# place carrying a version *agrees with the manifest*, whatever it says.
PKG_VERSION = json.load(open(PKG))["version"]

# A minimal but *valid* kit-marked SKILL.md for fixtures that pre-populate a
# destination folder. The adapters read the registration marker from inside the
# '---'-delimited frontmatter block, so a bare `name:` line is NOT kit-marked —
# a fixture missing the delimiters makes the kit-identity guards read the folder
# as stale content and re-copy, which is not the state these tests set up.
KIT_SKILL_STUB = f"---\n{KIT_MARK}\ndescription: fixture\nversion: {PKG_VERSION}\n---\n\n# fixture\n"

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"Bearer [A-Za-z0-9._-]{20,}"),
]

# --------------------------------------------------------------------------
# Harness helpers
# --------------------------------------------------------------------------

def base_env(home, extra=None):
    env = {
        "HOME": home,
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "TERM": "xterm",
        "LANG": "C",
        "USER": "m3verify",
    }
    if extra:
        env.update(extra)
    return env


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def make_pkg_tree(adapters=None, with_kit=True, with_installers=True, pkg_name=None,
                  pkg_version=None):
    """A hermetic package root: bin/setup-wizard.js + installers/ + kit/.

    pkg_version defaults to the real manifest's version. Pass a different value
    to prove the wizard reads its version from package.json rather than
    carrying a copy of it.
    """
    tree = tempfile.mkdtemp(prefix="m3pkg-")
    os.makedirs(os.path.join(tree, "bin"))
    shutil.copy2(WIZARD, os.path.join(tree, "bin", "setup-wizard.js"))
    write_file(os.path.join(tree, "package.json"), json.dumps({
        "name": pkg_name or "sdd-multiagent-kit",
        "version": pkg_version or PKG_VERSION,
        "bin": {"sdd-setup": "bin/setup-wizard.js"},
    }))
    if with_kit:
        shutil.copytree(KIT, os.path.join(tree, "kit"))
    if with_installers:
        os.makedirs(os.path.join(tree, "installers"))
        for fn in (adapters or ADAPTERS):
            shutil.copy2(os.path.join(INSTALLERS, fn), os.path.join(tree, "installers", fn))
    return tree


def run_wizard(tree, env, stdin=None, args=None):
    argv = [NODE, os.path.join(tree, "bin", "setup-wizard.js")] + (args or [])
    r = subprocess.run(argv, env=env, input=stdin, capture_output=True, text=True,
                       cwd=tree, timeout=60)
    return r.returncode, r.stdout, r.stderr


class PtySession:
    """Drive the wizard over a pseudo-terminal."""

    def __init__(self, argv, env, cwd=None):
        self.pid, self.fd = pty.fork()
        if self.pid == 0:
            os.chdir(cwd or "/")
            os.execvpe(argv[0], argv, env)
        self.buf = b""
        self.rc = None

    def _drain(self, timeout=0.2):
        end = time.time() + timeout
        while time.time() < end:
            r, _, _ = select.select([self.fd], [], [], 0.05)
            if not r:
                break
            try:
                data = os.read(self.fd, 65536)
            except OSError:
                break
            if not data:
                break
            self.buf += data

    def expect(self, pat, timeout=15):
        if isinstance(pat, str):
            pat = pat.encode()
        end = time.time() + timeout
        while pat not in self.buf:
            if time.time() > end:
                raise AssertionError(
                    "timeout waiting for %r; output so far: %r" % (pat, self.buf[-400:]))
            self._drain(0.2)
        return self.buf

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        os.write(self.fd, data)

    def keyline(self, text):
        """Send a masked key entry: the text + Enter. Returns nothing (the
        key must never be echoed back, so the caller checks self.buf)."""
        self.send(text + "\r")

    def expect_exit(self, timeout=20):
        end = time.time() + timeout
        while self.rc is None:
            if time.time() > end:
                raise AssertionError("timeout waiting for wizard exit")
            self._drain(0.2)
            try:
                pid, status = os.waitpid(self.pid, os.WNOHANG)
                if pid:
                    if os.WIFEXITED(status):
                        self.rc = os.WEXITSTATUS(status)
                    elif os.WIFSIGNALED(status):
                        self.rc = 128 + os.WTERMSIG(status)
            except ChildProcessError:
                break
        return self.rc


def probe(adapter_file, home, op, kit_dir=None, env_extra=None):
    """Run one adapter operation in a node probe with HOME isolated."""
    probe_src = r"""
const a = require(process.argv[2]);
const op = process.argv[3];
let out = {};
try {
  if (op === "detect") out = a.detect();
  else if (op === "install") out = { dest: a.install(process.argv[4]) };
  else if (op === "confirm") out = a.confirmEnabled();
} catch (e) {
  out = { error: String(e && e.message ? e.message : e) };
}
process.stdout.write(JSON.stringify(out));
"""
    fd, probe_path = tempfile.mkstemp(suffix=".js")
    with os.fdopen(fd, "w") as f:
        f.write(probe_src)
    try:
        argv = [NODE, probe_path, adapter_file, op] + ([kit_dir] if kit_dir else [])
        r = subprocess.run(argv, env=base_env(home, env_extra),
                           capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            raise AssertionError("probe failed: %s" % r.stderr)
        return json.loads(r.stdout)
    finally:
        os.unlink(probe_path)


def copy_tree(src, dest):
    if os.path.isdir(src):
        os.makedirs(dest, exist_ok=True)
        for ent in os.listdir(src):
            copy_tree(os.path.join(src, ent), os.path.join(dest, ent))
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)


# --------------------------------------------------------------------------
# NT1 — adapter interface (AC-1)
# --------------------------------------------------------------------------

class NT1AdapterInterface(unittest.TestCase):

    def test_exports_and_shapes(self):
        for fn in ADAPTERS:
            home = tempfile.mkdtemp(prefix="m3home-")
            d = probe(os.path.join(INSTALLERS, fn), home, "detect")
            self.assertIsInstance(d, dict, fn)
            self.assertIn("installed", d, fn)
            self.assertIn("location", d, fn)
            self.assertIs(d["installed"], False, fn + " must not detect tools in an empty HOME")
            self.assertIsNone(d["location"], fn + " location must be null when the kit is absent")

    def test_detect_location_when_tool_present_but_kit_absent(self):
        home = tempfile.mkdtemp(prefix="m3home-")
        os.makedirs(os.path.join(home, ".claude"))
        os.makedirs(os.path.join(home, ".opencode"))
        open(os.path.join(home, ".opencode", "config.json"), "w").write("{}")
        os.makedirs(os.path.join(home, ".agents", "skills"))
        if sys.platform == "darwin":
            os.makedirs(os.path.join(home, "Library", "Application Support", "Claude"))
        elif sys.platform.startswith("linux"):
            os.makedirs(os.path.join(home, ".config", "Claude"))
        d = probe(os.path.join(INSTALLERS, "claude-code.js"), home, "detect")
        self.assertIs(d["installed"], True)
        self.assertIsNone(d["location"])
        d = probe(os.path.join(INSTALLERS, "claude-desktop.js"), home, "detect")
        self.assertIs(d["installed"], True)
        self.assertIsNone(d["location"])
        d = probe(os.path.join(INSTALLERS, "opencode.js"), home, "detect")
        self.assertIs(d["installed"], True)
        self.assertIsNone(d["location"])
        d = probe(os.path.join(INSTALLERS, "antigravity.js"), home, "detect")
        self.assertIs(d["installed"], True)
        self.assertIsNone(d["location"])

    def test_orphaned_install_location_without_tool(self):
        home = tempfile.mkdtemp(prefix="m3home-")
        shared = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        os.makedirs(shared)
        write_file(os.path.join(shared, "SKILL.md"), KIT_SKILL_STUB)
        d = probe(os.path.join(INSTALLERS, "opencode.js"), home, "detect")
        self.assertIs(d["installed"], False, "no opencode signal must mean not installed")
        self.assertEqual(d["location"], shared, "populated kit folder must still be reported")

    def test_non_stub(self):
        files = [WIZARD] + [os.path.join(INSTALLERS, f) for f in ADAPTERS]
        for p in files:
            self.assertTrue(os.path.exists(p), p)
            text = open(p).read()
            self.assertGreater(len(text), 500, "%s looks like a stub" % p)
            self.assertNotIn("TODO", text, p)
            self.assertNotIn("NotImplemented", text, p)


# --------------------------------------------------------------------------
# NT2 — keys + guide slot (AC-2)
# --------------------------------------------------------------------------

class NT2KeysAndSlot(unittest.TestCase):

    def _wizard_session(self, env_extra=None):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        env = base_env(home, env_extra)
        return PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                          env, cwd=tree), tree, home

    def test_keys_in_one_pass_masked_with_guide_slot(self):
        s, tree, home = self._wizard_session()
        keys = ["NVIDIAKEY-abc-123", "GOOGLEKEY-abc-456", "OLLAMAKEY-abc-789"]
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.keyline(keys[0])
        self.assertNotIn(keys[0], s.buf.decode(errors="replace"),
                         "masked key must never be echoed")
        s.expect("Learn more")  # guide slot directly under the NVIDIA prompt
        s.send("y\r")
        s.expect("docs/GUIDE.md#guide-for-pakistani-users")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.keyline(keys[1])
        self.assertNotIn(keys[1], s.buf.decode(errors="replace"))
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.keyline(keys[2])
        self.assertNotIn(keys[2], s.buf.decode(errors="replace"))
        s.expect("No supported tools detected. Nothing to install.")
        rc = s.expect_exit()
        self.assertEqual(rc, 0)
        out = s.buf.decode(errors="replace")
        for k in keys:
            self.assertNotIn(k, out, "key value must not appear anywhere in the session output")
        self.assertIn("NVIDIA_NIM_API_KEY: entered this session (not persisted)", out)
        self.assertIn("GOOGLE_AISTUDIO_API_KEY: entered this session (not persisted)", out)
        self.assertIn("OLLAMA_API_KEY: entered this session (not persisted)", out)

    def test_guide_slot_default_no_and_existing_value_hint(self):
        s, tree, home = self._wizard_session(
            {"NVIDIA_NIM_API_KEY": "pre-existing-env-value"})
        s.expect("Enter your NVIDIA_NIM_API_KEY API key (existing value found; skip to keep it):")
        s.send("\r")  # skip to keep the env value
        s.expect("Learn more")  # still offered every interactive run
        s.send("\r")  # default-No: no link printed
        s.expect("Warning: NVIDIA_NIM_API_KEY skipped.")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.send("gk\r")
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("No supported tools detected. Nothing to install.")
        s.expect_exit()
        out = s.buf.decode(errors="replace")
        self.assertNotIn("docs/GUIDE.md", out, "declining the guide must not print the link")
        self.assertIn("NVIDIA_NIM_API_KEY: set in env", out)
        self.assertIn("GOOGLE_AISTUDIO_API_KEY: entered this session (not persisted)", out)
        self.assertIn("OLLAMA_API_KEY: not set", out)

    def test_non_tty_skips_keys_and_guide(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 0)
        self.assertIn("Key entry skipped (no interactive terminal)", out)
        for name in KEY_NAMES:
            self.assertIn("export %s=" % name, out)
        self.assertNotIn("Learn more", out, "guide prompt is TTY-only")
        self.assertNotIn("Enter your", out, "no key prompts off-TTY")
        self.assertIn("No supported tools detected. Nothing to install.", out)
        self.assertIn("NVIDIA_NIM_API_KEY: not set", out)


# --------------------------------------------------------------------------
# NT3 — graceful detection / install failure (AC-3)
# --------------------------------------------------------------------------

class NT3Graceful(unittest.TestCase):

    def test_absent_tools_skipped(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 0, err)
        for name in ADAPTER_NAMES:
            self.assertIn("%s: not detected, skipped." % name, out)
        self.assertIn("No supported tools detected. Nothing to install.", out)

    def test_failing_install_reported_per_tool_and_run_continues(self):
        good = '"use strict";\n' \
               'const os = require("os");\n' \
               'exports.name = "Good Tool";\n' \
               'exports.detect = function () { return { installed: true, location: null }; };\n' \
               'exports.install = function () { return os.tmpdir() + "/good-tool"; };\n' \
               'exports.confirmEnabled = function () { return { installed: true, location: os.tmpdir() + "/good-tool" }; };\n'
        bad = '"use strict";\n' \
              'exports.name = "Bad Tool";\n' \
              'exports.detect = function () { return { installed: true, location: null }; };\n' \
              'exports.install = function () { throw new Error("bad-tool: boom"); };\n' \
              'exports.confirmEnabled = function () { throw new Error("unreachable"); };\n'
        crasher = '"use strict";\n' \
                  'exports.name = "Crasher";\n' \
                  'exports.detect = function () { throw new Error("detect exploded"); };\n' \
                  'exports.install = function () { return "x"; };\n' \
                  'exports.confirmEnabled = function () { return { installed: true, location: "x" }; };\n'
        tree = make_pkg_tree(adapters=["good.js", "bad.js", "crasher.js"],
                             with_installers=False)
        for fn, src in (("good.js", good), ("bad.js", bad), ("crasher.js", crasher)):
            write_file(os.path.join(tree, "installers", fn), src)
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="all\n")
        self.assertEqual(rc, 1, "a failed tool must contribute exit 1; output:\n" + out)
        self.assertIn("[FAIL] Bad Tool: bad-tool: boom", out)
        self.assertIn("[OK] Good Tool:", out)
        self.assertIn("Crasher: detect() error (detect exploded), skipped.", out)
        self.assertIn("Setup complete. Some tools were not confirmed.", out)


# --------------------------------------------------------------------------
# NT4 — locations + trigger per §10.3 (AC-4)
# --------------------------------------------------------------------------

class NT4LocationsAndTrigger(unittest.TestCase):

    def _home(self):
        return tempfile.mkdtemp(prefix="m3home-")

    def test_claude_code_location_and_trigger(self):
        home = self._home()
        os.makedirs(os.path.join(home, ".claude"))
        ad = os.path.join(INSTALLERS, "claude-code.js")
        d = probe(ad, home, "detect")
        self.assertEqual(d, {"installed": True, "location": None})
        r = probe(ad, home, "install", KIT)
        dest = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        self.assertEqual(r["dest"], dest)
        master = os.path.join(dest, "SKILL.md")
        self.assertTrue(os.path.exists(master), "SKILL.md must be copied")
        self.assertIn(KIT_MARK, open(master).read())
        c = probe(ad, home, "confirm")
        self.assertEqual(c, {"installed": True, "location": dest})
        # in-place overwrite: marker is replaced by the re-copy
        marker = os.path.join(dest, "config", "providers.yaml")
        with open(marker, "a") as f:
            f.write("\n# MARKERXYZ\n")
        r = probe(ad, home, "install", KIT)
        self.assertNotIn("MARKERXYZ", open(marker).read(),
                         "Claude Code re-install must overwrite in place")

    def test_claude_desktop_shared_folder_and_noop(self):
        home = self._home()
        if sys.platform == "darwin":
            appdir = os.path.join(home, "Library", "Application Support", "Claude")
        elif sys.platform.startswith("linux"):
            appdir = os.path.join(home, ".config", "Claude")
        else:
            appdir = None
        ad = os.path.join(INSTALLERS, "claude-desktop.js")
        if appdir:
            os.makedirs(appdir)
            d = probe(ad, home, "detect")
            self.assertEqual(d, {"installed": True, "location": None})
        else:
            src = open(ad).read()
            self.assertIn("AppData", src, "win32 %APPDATA%\\Claude path must exist")
            self.assertIn("opencode", src, "sanity")
        # install copies only if the shared folder is not kit-populated
        shared = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        os.makedirs(shared)
        write_file(os.path.join(shared, "SKILL.md"), KIT_SKILL_STUB)
        marker = os.path.join(shared, "config", "providers.yaml")
        os.makedirs(os.path.dirname(marker))
        open(marker, "w").write("version: 1\n# MARKERXYZ\n")
        r = probe(ad, home, "install", KIT)
        self.assertEqual(r["dest"], shared)
        self.assertIn("MARKERXYZ", open(marker).read(),
                      "Desktop install must no-op when the shared folder is kit-populated")
        c = probe(ad, home, "confirm")
        self.assertEqual(c, {"installed": True, "location": shared})
        # non-kit content in the shared folder -> real copy refreshes
        write_file(os.path.join(shared, "SKILL.md"), "# stale non-kit\n")
        open(marker, "w").write("# MARKERXYZ\n")
        r = probe(ad, home, "install", KIT)
        self.assertIn(KIT_MARK, open(os.path.join(shared, "SKILL.md")).read())
        self.assertNotIn("MARKERXYZ", open(marker).read())

    def test_opencode_detection_and_refresh_semantics(self):
        home = self._home()
        ad = os.path.join(INSTALLERS, "opencode.js")
        # config-dir signal (non-empty)
        os.makedirs(os.path.join(home, ".opencode"))
        open(os.path.join(home, ".opencode", "config.json"), "w").write("{}")
        d = probe(ad, home, "detect")
        self.assertEqual(d, {"installed": True, "location": None})
        # PATH signal alone (no config dir)
        home2 = self._home()
        bindir = tempfile.mkdtemp(prefix="m3bin-")
        open(os.path.join(bindir, "opencode"), "w").write("#!/bin/sh\n")
        d = probe(ad, home2, "detect", env_extra={"PATH": bindir})
        self.assertEqual(d, {"installed": True, "location": None})
        # XDG_CONFIG_HOME signal
        home3 = self._home()
        xdg = tempfile.mkdtemp(prefix="m3xdg-")
        os.makedirs(os.path.join(xdg, "opencode"))
        open(os.path.join(xdg, "opencode", "config.json"), "w").write("{}")
        d = probe(ad, home3, "detect", env_extra={"XDG_CONFIG_HOME": xdg})
        self.assertEqual(d, {"installed": True, "location": None})
        # Windows executable variants present in the adapter (static)
        src = open(ad).read()
        for win in ["opencode.exe", "opencode.cmd", "opencode.bat"]:
            self.assertIn(win, src)
        # install no-op only when the shared folder is kit-marked
        shared = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        os.makedirs(shared)
        write_file(os.path.join(shared, "SKILL.md"), KIT_SKILL_STUB)
        marker = os.path.join(shared, "config", "providers.yaml")
        os.makedirs(os.path.dirname(marker))
        open(marker, "w").write("version: 1\n# MARKERXYZ\n")
        r = probe(ad, home, "install", KIT)
        self.assertEqual(r["dest"], shared)
        self.assertIn("MARKERXYZ", open(marker).read(),
                      "OpenCode install must no-op on a kit-marked shared folder")
        # stale/partial shared folder -> real copy refreshes
        os.remove(os.path.join(shared, "SKILL.md"))
        open(marker, "w").write("# MARKERXYZ\n")
        r = probe(ad, home, "install", KIT)
        self.assertIn(KIT_MARK, open(os.path.join(shared, "SKILL.md")).read())
        self.assertNotIn("MARKERXYZ", open(marker).read())

    def test_antigravity_location_and_embedded_trigger(self):
        home = self._home()
        os.makedirs(os.path.join(home, ".agents", "skills"))
        ad = os.path.join(INSTALLERS, "antigravity.js")
        d = probe(ad, home, "detect")
        self.assertEqual(d, {"installed": True, "location": None})
        r = probe(ad, home, "install", KIT)
        dest = os.path.join(home, ".agents", "skills", "sdd-multiagent-kit")
        self.assertEqual(r["dest"], dest)
        master = os.path.join(dest, "SKILL.md")
        self.assertIn(INVOCATION, open(master).read())
        c = probe(ad, home, "confirm")
        self.assertEqual(c, {"installed": True, "location": dest})
        # stale Invocation line is replaced, re-runs converge to the canonical line
        write_file(master, open(master).read().replace(INVOCATION, "Invocation: /old-stale"))
        r = probe(ad, home, "install", KIT)
        txt = open(master).read()
        self.assertIn(INVOCATION, txt)
        self.assertNotIn("Invocation: /old-stale", txt)
        c = probe(ad, home, "confirm")
        self.assertEqual(c["installed"], True)
        # version-key append path: a copy with no Invocation line at all
        home2 = self._home()
        os.makedirs(os.path.join(home2, ".agents", "skills"))
        r = probe(ad, home2, "install", KIT)
        txt = open(os.path.join(home2, ".agents", "skills", "sdd-multiagent-kit", "SKILL.md")).read()
        self.assertIn(f"version: {PKG_VERSION}\n" + INVOCATION, txt)
        self.assertIn(KIT_MARK, txt)


# --------------------------------------------------------------------------
# NT5 — package.json + secrets (AC-5)
# --------------------------------------------------------------------------

class NT5PackageAndSecrets(unittest.TestCase):

    def test_package_json_contract(self):
        pkg = json.load(open(PKG))
        self.assertEqual(pkg["name"], "sdd-multiagent-kit")
        # The version is deliberately NOT asserted against a literal. Pinning one
        # made every correct release bump fail this suite. What matters is that it
        # is well-formed semver and that every other copy agrees with it — see
        # test_version_is_consistent_everywhere.
        self.assertRegex(pkg["version"], r"^\d+\.\d+\.\d+([-+].+)?$")
        self.assertEqual(pkg["license"], "MIT")
        self.assertEqual(pkg["bin"], {"sdd-setup": "bin/setup-wizard.js"})
        self.assertNotIn("dependencies", pkg, "no runtime dependencies allowed")
        self.assertNotIn("devDependencies", pkg, "no development dependencies allowed")
        self.assertEqual(pkg["engines"]["node"], ">=18")
        files = pkg["files"]
        self.assertIn("kit/", files)
        self.assertIn("bin/", files)
        self.assertIn("installers/", files)
        self.assertIn("LICENSE", files)
        self.assertIn("README.md", files)
        # docs/ must ship: README links docs/GUIDE.md and the wizard prints the
        # reserved guide location there, so both dangle in a global install
        # unless the directory is in the allowlist.
        self.assertIn("docs/", files)
        # Python bytecode must not ship. npm honors negations inside "files";
        # a .npmignore cannot override an allowlist, so the exclusion lives here.
        self.assertIn("!kit/**/__pycache__", files)
        self.assertIn("!**/*.pyc", files)

    def test_no_secret_writes_anywhere(self):
        scan_dirs = [os.path.join(REPO, "bin"), os.path.join(REPO, "installers"),
                     os.path.join(REPO, "kit"), HERE]
        hits = []
        for d in scan_dirs:
            for root, _dirs, names in os.walk(d):
                for n in names:
                    if n.endswith((".js", ".py", ".yaml", ".md", ".json")):
                        text = open(os.path.join(root, n), "r", errors="replace").read()
                        for pat in SECRET_PATTERNS:
                            hits.extend("%s: %s" % (os.path.join(root, n), m)
                                        for m in pat.findall(text))
        self.assertEqual(hits, [], "secret-shaped values found: %r" % hits)

    def test_kit_and_logs_contain_no_key_values_after_e2e(self):
        # The E2E test feeds keys into the wizard; nothing may persist them.
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        for d in (".claude", ".opencode"):
            os.makedirs(os.path.join(home, d))
        open(os.path.join(home, ".opencode", "config.json"), "w").write("{}")
        rc, out, err = run_wizard(tree, base_env(home), stdin="all\n")
        self.assertEqual(rc, 0, out + err)
        blob = out + err + open(os.path.join(tree, "kit", "SKILL.md")).read()
        for needle in ["NVIDIAKEY", "GOOGLEKEY", "OLLAMAKEY"]:
            self.assertNotIn(needle, blob)


# --------------------------------------------------------------------------
# NT6 — runnable (AC-6)
# --------------------------------------------------------------------------

class NT6Runnable(unittest.TestCase):

    def test_bin_metadata(self):
        self.assertTrue(os.path.exists(WIZARD))
        first = open(WIZARD).readline()
        self.assertIn("#!/usr/bin/env node", first)
        st = os.stat(WIZARD)
        self.assertTrue(st.st_mode & stat.S_IXUSR, "wizard must carry the executable bit")
        self.assertIn(">= 18", open(WIZARD).read(), "Node < 18 must error at startup")

    def test_help_version_and_bad_args(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        env = base_env(home)
        rc, out, err = run_wizard(tree, env, stdin="", args=["--help"])
        self.assertEqual(rc, 0)
        self.assertIn("Usage: sdd-setup", out)
        rc, out, err = run_wizard(tree, env, stdin="", args=["-h"])
        self.assertEqual(rc, 0)
        rc, out, err = run_wizard(tree, env, stdin="", args=["--version"])
        self.assertEqual(rc, 0)
        self.assertEqual(out.strip(), PKG_VERSION)
        rc, out, err = run_wizard(tree, env, stdin="", args=["--bogus"])
        self.assertEqual(rc, 2)

    def test_version_comes_from_the_manifest_not_a_copy(self):
        """FR-5 — `--version` prints *the package version*, read from package.json.

        The fixture writes a version the wizard has never seen, so a wizard
        carrying its own copy of the number cannot pass. Asserting against the
        real version instead would pass either way and prove nothing — that is
        exactly how the previous hard-coded literal survived unnoticed until a
        release bump broke this suite.
        """
        tree = make_pkg_tree(pkg_version="9.9.9")
        env = base_env(tempfile.mkdtemp(prefix="m3home-"))
        rc, out, err = run_wizard(tree, env, stdin="", args=["--version"])
        self.assertEqual(rc, 0, err)
        self.assertEqual(out.strip(), "9.9.9")
        rc, out, err = run_wizard(tree, env, stdin="", args=["--help"])
        self.assertEqual(rc, 0, err)
        self.assertIn("(v9.9.9)", out)
        # A version it cannot determine is reported as an error, never invented:
        # the walk requires a package.json named sdd-multiagent-kit, so a foreign
        # manifest yields exit 2 rather than a fabricated number.
        tree = make_pkg_tree(pkg_name="not-the-kit")
        rc, out, err = run_wizard(tree, env, stdin="", args=["--version"])
        self.assertEqual(rc, 2, out)
        self.assertIn("could not read the package version", err)

    def test_version_is_consistent_everywhere(self):
        """One version, one source. Every shipped copy must match package.json.

        These files ship together in a single tarball, so a mismatch means the
        installed skill advertises a version the package is not. `scripts/
        bump-version.js --check` enforces the same rule for the release
        workflow; this test is the suite-level guarantee.
        """
        skills = [os.path.join(KIT, "SKILL.md")] + sorted(
            os.path.join(KIT, "skills", d, "SKILL.md")
            for d in os.listdir(os.path.join(KIT, "skills"))
            if os.path.exists(os.path.join(KIT, "skills", d, "SKILL.md")))
        self.assertEqual(len(skills), 12, "master skill + 11 sub-skills")
        for path_ in skills:
            fm = re.match(r"^---\r?\n(.*?)\r?\n---", open(path_).read(), re.S)
            self.assertIsNotNone(fm, f"{path_} has no frontmatter block")
            found = re.search(r"^version:[ \t]*(\S+)[ \t]*$", fm.group(1), re.M)
            self.assertIsNotNone(found, f"{path_} has no version: key")
            self.assertEqual(found.group(1), PKG_VERSION,
                             f"{os.path.relpath(path_, REPO)} is {found.group(1)}, "
                             f"package.json is {PKG_VERSION}")

    def test_wizard_begins(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 0, err)
        self.assertIn("Key entry skipped (no interactive terminal)", out)
        self.assertIn("NVIDIA_NIM_API_KEY: not set", out)


# --------------------------------------------------------------------------
# NT7 — key-entry rules (AC-2)
# --------------------------------------------------------------------------

class NT7KeyEntryRules(unittest.TestCase):

    def test_whitespace_rejected_then_valid(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        s = PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                       base_env(home), cwd=tree)
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.keyline("bad key with spaces")
        s.expect("cannot contain whitespace or control characters")
        s.expect("Enter your NVIDIA_NIM_API_KEY API key")  # re-prompted
        s.keyline("goodkey-1")
        s.expect("Learn more")
        s.send("n\r")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("No supported tools detected. Nothing to install.")
        s.expect_exit()
        out = s.buf.decode(errors="replace")
        self.assertIn("NVIDIA_NIM_API_KEY: entered this session (not persisted)", out)
        self.assertNotIn("bad key with spaces", out, "rejected key must not be echoed")
        self.assertIn("GOOGLE_AISTUDIO_API_KEY: not set", out)
        self.assertIn("OLLAMA_API_KEY: not set", out)

    def test_non_ascii_key_accepted(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        s = PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                       base_env(home), cwd=tree)
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.keyline("\u043a\u043b\u044e\u0447-\U0001f511")  # ключ-🔑
        s.expect("Learn more")
        s.send("n\r")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("No supported tools detected. Nothing to install.")
        s.expect_exit()
        out = s.buf.decode(errors="replace")
        self.assertNotIn("whitespace", out)
        self.assertIn("NVIDIA_NIM_API_KEY: entered this session (not persisted)", out)

    def test_empty_entry_is_a_skip(self):
        tree = make_pkg_tree()
        home = tempfile.mkdtemp(prefix="m3home-")
        s = PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                       base_env(home), cwd=tree)
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("Learn more")
        s.send("n\r")
        s.expect("Warning: NVIDIA_NIM_API_KEY skipped.")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.send("\r")
        s.expect("No supported tools detected. Nothing to install.")
        s.expect_exit()
        out = s.buf.decode(errors="replace")
        self.assertIn("NVIDIA_NIM_API_KEY: not set", out)


# --------------------------------------------------------------------------
# NT8 — discovery guards (AC-1)
# --------------------------------------------------------------------------

class NT8DiscoveryGuards(unittest.TestCase):

    def _guard(self, adapters=None, with_installers=True, with_kit=True, pkg_name=None):
        tree = make_pkg_tree(adapters=adapters, with_installers=with_installers,
                             with_kit=with_kit, pkg_name=pkg_name)
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        return rc, out, err

    def test_missing_installers_dir(self):
        rc, out, err = self._guard(with_installers=False)
        self.assertEqual(rc, 2)
        self.assertIn("installers/", err)

    def test_installers_with_no_js(self):
        tree = make_pkg_tree(with_installers=False)
        write_file(os.path.join(tree, "installers", "README.md"), "# installers\n")
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 2)
        self.assertIn("no .js adapters", err)

    def test_malformed_adapter(self):
        tree = make_pkg_tree(with_installers=False)
        write_file(os.path.join(tree, "installers", "broken.js"),
                   '"use strict";\nexports.name = "Broken";\nexports.detect = function () { return { installed: true }; };\n')
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 2)
        self.assertIn("broken.js", err)
        self.assertIn("name, detect(), install(), confirmEnabled()", err)

    def test_adapter_require_throw(self):
        tree = make_pkg_tree(with_installers=False)
        write_file(os.path.join(tree, "installers", "syntax-broken.js"),
                   '"use strict";\nthis is not valid javascript (((\n')
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 2)
        self.assertIn("syntax-broken.js", err)
        self.assertIn("failed to load", err)

    def test_duplicate_adapter_name(self):
        a = '"use strict";\nexports.name = "Dup";\nexports.detect = function () { return { installed: false, location: null }; };\nexports.install = function () { return "x"; };\nexports.confirmEnabled = function () { return { installed: false, location: null }; };\n'
        tree = make_pkg_tree(with_installers=False)
        write_file(os.path.join(tree, "installers", "dup-a.js"), a)
        write_file(os.path.join(tree, "installers", "dup-b.js"), a.replace("Dup", "Dup"))
        home = tempfile.mkdtemp(prefix="m3home-")
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 2)
        self.assertIn("duplicate adapter name", err)
        self.assertIn("dup-a.js", err)
        self.assertIn("dup-b.js", err)

    def test_kit_source_missing(self):
        rc, out, err = self._guard(with_kit=False)
        self.assertEqual(rc, 2)
        self.assertIn("could not locate", err)


# --------------------------------------------------------------------------
# E2E walkthrough (tests §3)
# --------------------------------------------------------------------------

class E2EWalkthrough(unittest.TestCase):

    def _fake_home(self):
        home = tempfile.mkdtemp(prefix="m3home-")
        os.makedirs(os.path.join(home, ".claude"))
        os.makedirs(os.path.join(home, ".opencode"))
        open(os.path.join(home, ".opencode", "config.json"), "w").write("{}")
        os.makedirs(os.path.join(home, ".agents", "skills"))
        if sys.platform == "darwin":
            os.makedirs(os.path.join(home, "Library", "Application Support", "Claude"))
        elif sys.platform.startswith("linux"):
            os.makedirs(os.path.join(home, ".config", "Claude"))
        return home

    def _run_e2e(self, home, select_input="all\r"):
        tree = make_pkg_tree()
        s = PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                       base_env(home), cwd=tree)
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.keyline("NVIDIAKEY-e2e-111")
        s.expect("Learn more")
        s.send("n\r")
        s.expect("Enter your GOOGLE_AISTUDIO_API_KEY API key [skip]:")
        s.keyline("GOOGLEKEY-e2e-222")
        s.expect("Enter your OLLAMA_API_KEY API key [skip]:")
        s.keyline("OLLAMAKEY-e2e-333")
        s.expect("Detected tools: Antigravity, Claude Code, Claude Desktop, OpenCode")
        s.send(select_input)
        return s, tree

    def test_full_flow(self):
        home = self._fake_home()
        s, tree = self._run_e2e(home)
        for name in ADAPTER_NAMES:
            s.expect("[OK] %s: installed to" % name)
            s.expect("trigger active")
        s.expect("Setup complete.")
        s.expect("Env vars")
        rc = s.expect_exit()
        self.assertEqual(rc, 0)
        out = s.buf.decode(errors="replace")
        # destinations per §10.3
        shared = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        ag = os.path.join(home, ".agents", "skills", "sdd-multiagent-kit")
        self.assertIn(shared, out)
        self.assertIn(ag, out)
        self.assertTrue(os.path.exists(os.path.join(shared, "SKILL.md")))
        self.assertIn(KIT_MARK, open(os.path.join(shared, "SKILL.md")).read())
        self.assertIn(INVOCATION, open(os.path.join(ag, "SKILL.md")).read())
        # no key values anywhere: session output, temp HOME, temp package tree
        for needle in ["NVIDIAKEY-e2e-111", "GOOGLEKEY-e2e-222", "OLLAMAKEY-e2e-333"]:
            self.assertNotIn(needle, out)
            for root, _dirs, names in os.walk(home):
                for n in names:
                    self.assertNotIn(needle, open(os.path.join(root, n), errors="replace").read())
        # re-run: idempotent, in-place overwrite
        marker = os.path.join(shared, "config", "providers.yaml")
        with open(marker, "a") as f:
            f.write("\n# MARKERXYZ\n")
        s2, tree2 = self._run_e2e(home)
        s2.expect("Setup complete.")
        self.assertEqual(s2.expect_exit(), 0)
        self.assertNotIn("MARKERXYZ", open(marker).read(),
                         "re-run must overwrite in place (Claude Code/Desktop copy)")

    def test_opencode_only_rerun_noop(self):
        home = self._fake_home()
        s, tree = self._run_e2e(home)
        s.expect("Setup complete.")
        self.assertEqual(s.expect_exit(), 0)
        shared = os.path.join(home, ".claude", "skills", "sdd-multiagent-kit")
        marker = os.path.join(shared, "config", "providers.yaml")
        with open(marker, "a") as f:
            f.write("\n# MARKERXYZ\n")
        s2, tree2 = self._run_e2e(home, select_input="opencode\r")
        s2.expect("Setup complete.")
        self.assertEqual(s2.expect_exit(), 0)
        self.assertIn("MARKERXYZ", open(marker).read(),
                      "OpenCode-only re-run must no-op on a kit-marked shared folder")
        self.assertNotIn("[OK] Claude Code", s2.buf.decode(errors="replace"))

    def test_ctrl_c_aborts_cleanly_exit_130(self):
        home = self._fake_home()
        tree = make_pkg_tree()
        s = PtySession([NODE, os.path.join(tree, "bin", "setup-wizard.js")],
                       base_env(home), cwd=tree)
        s.expect("Enter your NVIDIA_NIM_API_KEY API key [skip]:")
        s.send("\x03")
        s.expect("Aborted by user.")
        rc = s.expect_exit()
        self.assertEqual(rc, 130)
        self.assertFalse(os.path.exists(os.path.join(home, ".claude", "skills")),
                         "abort must not leave partial install state")

    def test_piped_eof_and_complete_selection(self):
        home = self._fake_home()
        tree = make_pkg_tree()
        # EOF with no pending input = user abort, exit 130
        rc, out, err = run_wizard(tree, base_env(home), stdin="")
        self.assertEqual(rc, 130, out + err)
        self.assertIn("aborted", out)
        # EOF after a complete selection proceeds normally, exit 0
        rc, out, err = run_wizard(tree, base_env(home), stdin="all\n")
        self.assertEqual(rc, 0, out + err)
        self.assertIn("[OK] Claude Code", out)
        self.assertIn("trigger active", out)
        self.assertIn("Setup complete.", out)
        # invalid selection re-prompts until valid; EOF during the re-prompt
        # (readline drops unread pipe content on close) is the user abort, 130
        rc, out, err = run_wizard(tree, base_env(home), stdin="bogus\n")
        self.assertEqual(rc, 130, out + err)
        self.assertIn("No match for", out)
        self.assertIn("aborted", out)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)