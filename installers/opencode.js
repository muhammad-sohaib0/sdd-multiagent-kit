"use strict";
// OpenCode adapter. Per PLAN.md §10.3, OpenCode reads .claude/skills/ directly,
// so it shares Claude Code's user-level location and needs NO separate copy
// when the kit is already present. detect() checks for OpenCode itself (config
// directory and/or executable on PATH). install() is a no-op verification when
// the shared folder is populated, and performs the copy when it is absent
// (OpenCode installed but the kit never installed for Claude Code).

const fs = require("fs");
const path = require("path");
const os = require("os");

const FOLDER = "sdd-multiagent-kit";

exports.name = "OpenCode";

function sharedDir() {
  return path.join(os.homedir(), ".claude", "skills", FOLDER);
}

function opencodeInstalled() {
  try {
    const candidates = [
      path.join(os.homedir(), ".opencode"),
      path.join(os.homedir(), ".config", "opencode"),
    ];
    if (process.env.XDG_CONFIG_HOME) {
      candidates.push(path.join(process.env.XDG_CONFIG_HOME, "opencode"));
    }
    if (candidates.some((p) => fs.existsSync(p) && fs.readdirSync(p).length > 0)) return true;
    const PATH = (process.env.PATH || "").split(path.delimiter);
    const names = process.platform === "win32" ? ["opencode.exe", "opencode.cmd", "opencode.bat"] : ["opencode"];
    return PATH.some((dir) => names.some((n) => fs.existsSync(path.join(dir, n))));
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
// the registration check (name: sdd-multiagent-kit) looks inside that block.
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
    const dest = sharedDir();
    const populated = fs.existsSync(dest) && fs.readdirSync(dest).length > 0;
    return {
      installed: opencodeInstalled(),
      location: populated ? dest : null,
    };
  } catch (e) {
    console.warn(`opencode: detect() error (${e.message}) — treated as not installed`);
    return { installed: false, location: null };
  }
};

exports.install = function (kitDir) {
  try {
    // Shared location: no-op only when already populated WITH the kit (its
    // SKILL.md carries the kit name); otherwise a real copy refreshes it.
    const dest = sharedDir();
    if (kitMarked(dest)) {
      return dest;
    }
    copyDir(kitDir, dest);
    return dest;
  } catch (e) {
    throw new Error(`opencode: ${e.message}`);
  }
};

exports.confirmEnabled = function () {
  const dest = sharedDir();
  const installed = kitMarked(dest);
  return { installed, location: installed ? dest : null };
};