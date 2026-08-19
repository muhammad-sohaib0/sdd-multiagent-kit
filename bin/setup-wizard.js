#!/usr/bin/env node
"use strict";
// SDD Multi-Agent Kit setup wizard (bin: sdd-setup).
// Collects the three API keys in one pass (masked entry), offers the reserved
// "Guide for Pakistani users" slot under the NVIDIA prompt, detects installed
// tools, lets the user choose which to install into, installs, and confirms
// triggers.
// Exit codes: 0 all chosen installed+confirmed (or nothing detected); 1 partial
// (some failed/not confirmed); 2 usage/config error before any install;
// 130 aborted by the user (Ctrl-C).

const fs = require("fs");
const os = require("os");
const path = require("path");
const readline = require("readline");

const KEY_NAMES = ["NVIDIA_NIM_API_KEY", "GOOGLE_AISTUDIO_API_KEY", "OLLAMA_API_KEY"];
const GUIDE_SLOT = "docs/GUIDE.md#guide-for-pakistani-users"; // reserved location

// Adapter discovery: every .js directly under installers/ is an adapter. A
// tool's "registration" is its file exporting name/detect/install/confirmEnabled.
const adapters = {};
(function discoverAdapters() {
  const dir = path.join(__dirname, "..", "installers");
  let files;
  try {
    files = fs.readdirSync(dir);
  } catch (e) {
    console.error(`error: installers/ not found or unreadable (${e.message})`);
    process.exit(2);
  }
  const js = files.filter((f) => f.endsWith(".js"));
  if (js.length === 0) {
    console.error("error: installers/ contains no .js adapters");
    process.exit(2);
  }
  for (const f of js) {
    let ad;
    try {
      ad = require(path.join(dir, f));
    } catch (e) {
      console.error(`error: adapter ${f} failed to load (${String(e && e.message ? e.message : e)})`);
      process.exit(2);
    }
    if (!ad || typeof ad.detect !== "function" || typeof ad.install !== "function" ||
        typeof ad.confirmEnabled !== "function" || typeof ad.name !== "string") {
      console.error(`error: adapter ${f} must export name, detect(), install(), confirmEnabled()`);
      process.exit(2);
    }
    if (adapters[ad.name]) {
      console.error(`error: duplicate adapter name "${ad.name}" in ${adapters[ad.name].__file} and ${f}`);
      process.exit(2);
    }
    ad.__file = f;
    adapters[ad.name] = ad;
  }
})();

// readline is created lazily and only for the piped/non-TTY fallback. On a TTY
// the wizard uses its own raw-mode reader exclusively — mixing readline's
// terminal machinery with raw mode would double-echo input and leak masked
// key entry into the terminal.
let rl = null;
let stdinClosed = false;
function getRl() {
  if (!rl) {
    rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.on("close", () => {
      stdinClosed = true;
    });
    rl.on("SIGINT", () => {
      console.log("\nAborted by user.");
      process.exit(130);
    });
  }
  return rl;
}
// EOF with a pending question: readline never invokes the callback, so race
// the question against 'close' — on close the prompt resolves empty and the
// caller's stdinClosed check turns that into the user-abort path (exit 130).
const q = (prompt) => new Promise((res) => {
  const r = getRl();
  const onClose = () => res("");
  r.once("close", onClose);
  try {
    r.question(prompt, (ans) => {
      r.removeListener("close", onClose);
      res(ans);
    });
  } catch (e) {
    r.removeListener("close", onClose);
    res("");
  }
});

// Single raw-mode line reader for TTY prompts (masked when hidden). Bytes are
// buffered and decoded as UTF-8 at line end, so non-ASCII keys survive intact.
function line(prompt, hidden) {
  if (!process.stdin.isTTY) {
    return q(prompt);
  }
  return new Promise((resolve) => {
    const stdin = process.stdin;
    stdin.setRawMode(true);
    stdin.resume();
    process.stdout.write(prompt);
    let buf = Buffer.alloc(0);
    const cleanup = () => {
      stdin.setRawMode(false);
      stdin.pause();
      stdin.removeListener("data", onData);
    };
    const onData = (chunk) => {
      for (const byte of chunk) {
        if (byte === 3 || byte === 4) { // Ctrl-C / Ctrl-D (EOF) abort at any point
          cleanup();
          console.log("\nAborted by user.");
          process.exit(130);
        }
        if (byte === 13 || byte === 10) {
          process.stdout.write("\n");
          cleanup();
          resolve(buf.toString("utf8"));
          return;
        }
        if (byte === 127 || byte === 8) {
          if (buf.length > 0) {
            const chars = Array.from(buf.toString("utf8"));
            chars.pop();
            buf = Buffer.from(chars.join(""), "utf8");
            if (!hidden) process.stdout.write("\b \b");
          }
        } else if (byte >= 32) {
          buf = Buffer.concat([buf, Buffer.from([byte])]);
          if (!hidden) process.stdout.write(Buffer.from([byte]));
        }
      }
    };
    stdin.on("data", onData);
  });
}

// Kit source discovery: walk parent directories from this file's location
// until a package.json with name: sdd-multiagent-kit AND a sibling kit/SKILL.md
// is found (both conditions — robust under npm bin symlinks, local checkouts,
// and monorepo/workspace installs). Errors (exit 2) if no match is found.
function kitDir() {
  let dir = __dirname;
  while (true) {
    const pkg = path.join(dir, "package.json");
    try {
      const name = JSON.parse(fs.readFileSync(pkg, "utf8")).name;
      const skill = path.join(dir, "kit", "SKILL.md");
      if (name === "sdd-multiagent-kit" && fs.existsSync(skill)) {
        return path.join(dir, "kit");
      }
    } catch (e) {
      /* not this package root — keep walking */
    }
    const parent = path.dirname(dir);
    if (parent === dir) {
      console.error("error: could not locate the sdd-multiagent-kit package root (no matching package.json with kit/SKILL.md)");
      process.exit(2);
    }
    dir = parent;
  }
}

async function collectKeys() {
  const keys = {};
  // Key entry requires a TTY (masked, no echo). Off-TTY the prompts are
  // skipped and the env-var names are printed instead — a key is never echoed
  // in cleartext.
  if (!process.stdin.isTTY) {
    console.log("Key entry skipped (no interactive terminal). Set these in your shell profile or .env before using the kit:");
    for (const name of KEY_NAMES) console.log(`  export ${name}=...`);
    return keys;
  }
  for (let i = 0; i < KEY_NAMES.length; i++) {
    const prior = process.env[KEY_NAMES[i]] ? " (existing value found; skip to keep it)" : " [skip]";
    let value = "";
    while (true) {
      value = await line(`Enter your ${KEY_NAMES[i]} API key${prior}: `, true);
      if (value.trim() && /[\s\x00-\x1f\x7f]/.test(value)) {
        console.log("  Keys cannot contain whitespace or control characters — try again, or leave empty to skip.");
        continue;
      }
      break;
    }
    keys[KEY_NAMES[i]] = value.trim();
    if (i === 0) {
      const guide = await line("  NVIDIA has a regional signup gap. [Learn more] about the Guide for Pakistani users? (y/N): ", false);
      if (/^y/i.test(guide)) {
        console.log(`  -> See ${GUIDE_SLOT} (reserved; content supplied by the maintainer).`);
      }
    }
    if (!keys[KEY_NAMES[i]]) {
      console.log(`  Warning: ${KEY_NAMES[i]} skipped. Tools needing it may fail at runtime.`);
    }
  }
  return keys;
}

// Final reminder: fixed key order with per-key status. Printed on every run,
// TTY and non-TTY alike, including the nothing-detected early exit.
function printReminder(keys) {
  console.log("Env vars — set these in your shell profile or .env before using the kit:");
  for (const name of KEY_NAMES) {
    let status;
    if (process.env[name]) status = "set in env";
    else if (keys[name]) status = "entered this session (not persisted) — add it to your shell profile or .env";
    else status = "not set — add it to your shell profile or .env";
    console.log(`  ${name}: ${status}`);
  }
}

async function main() {
  const nodeMajor = parseInt(process.versions.node.split(".")[0], 10);
  if (nodeMajor < 18) {
    console.error(`error: sdd-setup requires Node >= 18 (found ${process.version})`);
    return 2;
  }
  if (process.argv.includes("--help") || process.argv.includes("-h")) {
    console.log(`sdd-setup — SDD Multi-Agent Kit setup wizard (v0.1.0)

Usage: sdd-setup
  Interactive wizard. Collects the three API keys in one pass
  (NVIDIA_NIM_API_KEY, GOOGLE_AISTUDIO_API_KEY, OLLAMA_API_KEY), detects
  supported tools, installs the kit into the chosen ones, and confirms
  the /sdd trigger.

Options:
  -h, --help      show this help and exit
      --version   print the package version and exit`);
    return 0;
  }
  if (process.argv.includes("--version")) {
    console.log("0.1.0");
    return 0;
  }
  if (process.argv.length > 2) {
    console.error("error: sdd-setup takes no arguments or flags (see --help)");
    return 2;
  }
  const kit = kitDir();
  if (!fs.existsSync(path.join(kit, "SKILL.md"))) {
    console.error("error: kit/SKILL.md not found; install from the package root");
    return 2;
  }
  if (!os.homedir()) {
    console.error("error: home directory could not be resolved (HOME/USERPROFILE unset)");
    return 2;
  }

  const keys = await collectKeys();
  for (const name of Object.keys(keys)) {
    if (keys[name]) console.log(`Collected ${name} (onboarding only — not persisted; add it to your shell profile or .env).`);
  }
  const detected = [];
  for (const [name, ad] of Object.entries(adapters)) {
    try {
      const d = ad.detect();
      if (d.installed) detected.push({ name, ad });
      else console.log(`  - ${name}: not detected, skipped.`);
    } catch (e) {
      console.log(`  - ${name}: detect() error (${e.message}), skipped.`);
    }
  }
  if (detected.length === 0) {
    console.log("No supported tools detected. Nothing to install.");
    printReminder(keys);
    return 0;
  }

  console.log("\nDetected tools: " + detected.map((d) => d.name).join(", "));
  let chosen = [];
  while (true) {
    const pick = await line("Install into which? (comma-separated list, or 'all'; Ctrl-C aborts): ", false);
    const trimmed = pick.trim();
    if (!trimmed) {
      if (stdinClosed) {
        console.log("\nEOF on stdin with no input — aborted.");
        return 130;
      }
      console.log("  Nothing selected — pick a tool name, 'all', or abort with Ctrl-C.");
      continue;
    }
    if (/all/i.test(trimmed)) {
      chosen = detected;
      break;
    }
    chosen = detected.filter((d) => trimmed.toLowerCase().split(",").map((s) => s.trim()).includes(d.name.toLowerCase()));
    if (chosen.length > 0) break;
    if (stdinClosed) {
      console.log("\nEOF on stdin — aborted.");
      return 130;
    }
    console.log(`  No match for "${trimmed}". Detected: ${detected.map((d) => d.name).join(", ")}`);
  }

  let allOk = true;
  for (const { name, ad } of chosen) {
    try {
      const dest = ad.install(kit);
      const ok = ad.confirmEnabled();
      const okB = ok && ok.installed === true;
      console.log(`  [${okB ? "OK" : "WARN"}] ${name}: installed to ${dest}, trigger ${okB ? "active" : "not confirmed"}.`);
      if (!okB) allOk = false;
    } catch (e) {
      console.log(`  [FAIL] ${name}: ${String(e && e.message ? e.message : e)}`);
      allOk = false;
    }
  }
  console.log("\nSetup complete." + (allOk ? "" : " Some tools were not confirmed."));
  printReminder(keys);
  return allOk ? 0 : 1;
}

main().then((code) => {
  if (rl) rl.close();
  process.exitCode = code;
}).catch((e) => {
  console.error("error:", e.message);
  if (rl) rl.close();
  process.exitCode = 2;
});
