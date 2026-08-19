"use strict";
// Claude Code adapter (Agent-Skills standard, PLAN.md §10.3).
// Location: ~/.claude/skills/sdd-multiagent-kit/ (user-level).
// Trigger: native /sdd slash command derived from the folder name.

const fs = require("fs");
const path = require("path");
const os = require("os");

const FOLDER = "sdd-multiagent-kit";

exports.name = "Claude Code";

function skillsDir() {
  return path.join(os.homedir(), ".claude", "skills");
}
function destPath() {
  return path.join(skillsDir(), FOLDER);
}

function toolPresent() {
  try {
    if (fs.existsSync(path.join(os.homedir(), ".claude"))) return true;
    const PATH = (process.env.PATH || "").split(path.delimiter);
    return PATH.some((dir) => fs.existsSync(path.join(dir, "claude")));
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
// the native slash command derives from the skill name, so the registration
// check must look inside that block, not anywhere in the file.
function frontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  return m ? m[1] : "";
}

function kitMarked(dest) {
  const master = path.join(dest, "SKILL.md");
  try {
    return fs.existsSync(master) && /name:\s*sdd-multiagent-kit/.test(frontmatter(fs.readFileSync(master, "utf8")));
  } catch {
    return false;
  }
}

exports.detect = function () {
  try {
    const dest = destPath();
    const populated = fs.existsSync(dest) && fs.readdirSync(dest).length > 0;
    return { installed: toolPresent(), location: populated ? dest : null };
  } catch (e) {
    console.warn(`claude-code: detect() error (${e.message}) — treated as not installed`);
    return { installed: false, location: null };
  }
};

exports.install = function (kitDir) {
  try {
    const dest = destPath();
    copyDir(kitDir, dest);
    return dest;
  } catch (e) {
    throw new Error(`claude-code: ${e.message}`);
  }
};

exports.confirmEnabled = function () {
  const dest = destPath();
  const installed = kitMarked(dest);
  return { installed, location: installed ? dest : null };
};