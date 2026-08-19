"use strict";
// Antigravity adapter. Per PLAN.md §10.3: a SEPARATE copy is required, into
// ~/.agents/skills/sdd-multiagent-kit/. There is no native slash-command
// registry, so the canonical invocation line is (re-)asserted into the copied
// SKILL.md description on every install; confirmEnabled() checks that phrase.

const fs = require("fs");
const path = require("path");
const os = require("os");

const FOLDER = "sdd-multiagent-kit";
const INVOCATION_LINE = "Invocation: /sdd";

exports.name = "Antigravity";

function destDir() {
  return path.join(os.homedir(), ".agents", "skills", FOLDER);
}

function toolPresent() {
  try {
    return fs.existsSync(path.join(os.homedir(), ".agents", "skills"));
  } catch {
    return false;
  }
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const ent of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, ent.name);
    const d = path.join(dest, ent.name);
    if (ent.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

// The YAML frontmatter is the '---'-delimited block at the top of SKILL.md;
// the canonical invocation line is adapter-owned content layered on the
// kit-owned copy, kept inside that block so it never touches the body.
function frontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  return m ? m[1] : "";
}

function reassertInvocation(master) {
  const txt = fs.readFileSync(master, "utf8");
  const fm = frontmatter(txt);
  if (!fm) return;
  let next = fm;
  if (/^Invocation:.*$/m.test(next)) {
    next = next.replace(/^Invocation:.*$/gm, INVOCATION_LINE);
  } else {
    next = next.replace(/^(\s*version:.*)$/m, `$1\n${INVOCATION_LINE}`);
  }
  if (next !== fm) fs.writeFileSync(master, txt.replace(fm, next));
}

exports.detect = function () {
  try {
    const dest = destDir();
    const populated = fs.existsSync(dest) && fs.readdirSync(dest).length > 0;
    return { installed: toolPresent(), location: populated ? dest : null };
  } catch (e) {
    console.warn(`antigravity: detect() error (${e.message}) — treated as not installed`);
    return { installed: false, location: null };
  }
};

exports.install = function (kitDir) {
  try {
    const dest = destDir();
    copyDir(kitDir, dest);
    reassertInvocation(path.join(dest, "SKILL.md"));
    return dest;
  } catch (e) {
    throw new Error(`antigravity: ${e.message}`);
  }
};

exports.confirmEnabled = function () {
  const dest = destDir();
  const master = path.join(dest, "SKILL.md");
  try {
    const fm = fs.existsSync(master) ? frontmatter(fs.readFileSync(master, "utf8")) : "";
    const installed = fm.includes(INVOCATION_LINE);
    return { installed, location: installed ? dest : null };
  } catch {
    return { installed: false, location: null };
  }
};