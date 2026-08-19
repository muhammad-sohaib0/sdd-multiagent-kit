"use strict";
// Claude Desktop adapter. Per PLAN.md §10.3, Claude Desktop shares Claude Code's
// configuration (same user-level skills folder). detect() verifies Claude
// Desktop's own presence via its app config directory; install() copies only if
// the shared folder is not already populated.

const fs = require("fs");
const path = require("path");
const os = require("os");

const FOLDER = "sdd-multiagent-kit";

exports.name = "Claude Desktop";

function sharedDir() {
  return path.join(os.homedir(), ".claude", "skills", FOLDER);
}

function desktopAppDir() {
  const h = os.homedir();
  if (process.platform === "darwin") return path.join(h, "Library", "Application Support", "Claude");
  if (process.platform === "win32") return path.join(process.env.APPDATA || path.join(h, "AppData", "Roaming"), "Claude");
  return path.join(h, ".config", "Claude");
}

function desktopPresent() {
  try {
    return fs.existsSync(desktopAppDir());
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
    return { installed: desktopPresent(), location: populated ? dest : null };
  } catch (e) {
    console.warn(`claude-desktop: detect() error (${e.message}) — treated as not installed`);
    return { installed: false, location: null };
  }
};

exports.install = function (kitDir) {
  try {
    const dest = sharedDir();
    if (kitMarked(dest)) {
      return dest;
    }
    copyDir(kitDir, dest);
    return dest;
  } catch (e) {
    throw new Error(`claude-desktop: ${e.message}`);
  }
};

exports.confirmEnabled = function () {
  const dest = sharedDir();
  const installed = kitMarked(dest);
  return { installed, location: installed ? dest : null };
};