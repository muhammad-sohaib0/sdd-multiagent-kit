#!/usr/bin/env node
"use strict";
// Asserts the two workflows agree on the npm version they install.
//
// This exists because they did not, and it cost a failed publish on main. ci.yml
// ran Node's bundled npm 10 while publish.yml installed npm@latest (12), and
// npm 12 had changed `npm pack --json` from an array to an object — so CI was
// green while the publish step crashed. Pinning alone is not enough: `npm@latest`
// is a moving target, and two files can be pinned to two different things.
//
// Run: node scripts/check-workflows.js
// Exit: 0 they agree, 1 they do not, 2 a file or the pin could not be read.

const fs = require("fs");
const path = require("path");

const WORKFLOWS = path.join(__dirname, "..", ".github", "workflows");
const FILES = ["ci.yml", "publish.yml"];

// Matches `npm install -g npm@<spec>`. A bare `npm install -g npm` (no @spec)
// is itself a floating install and is reported as unpinned.
const INSTALL_RE = /npm\s+install\s+-g\s+npm(@([^\s"']+))?/;

function pinOf(file) {
  const full = path.join(WORKFLOWS, file);
  let text;
  try {
    text = fs.readFileSync(full, "utf8");
  } catch (e) {
    console.error(`error: cannot read ${file} (${e.message})`);
    process.exit(2);
  }
  const m = INSTALL_RE.exec(text);
  if (!m) {
    console.error(`error: ${file} does not install npm globally; both workflows must run the same npm`);
    process.exit(2);
  }
  return m[2] || null;
}

const pins = FILES.map((f) => ({ file: f, pin: pinOf(f) }));

const floating = pins.filter((p) => p.pin === null || p.pin === "latest");
if (floating.length) {
  console.error("error: npm must be pinned, not floating — `npm@latest` silently changed major and broke publish:");
  for (const p of floating) console.error(`  ${p.file}: ${p.pin === null ? "no @spec" : p.pin}`);
  process.exit(1);
}

const distinct = [...new Set(pins.map((p) => p.pin))];
if (distinct.length !== 1) {
  console.error("error: workflows disagree on the npm version, so a green CI would not imply a working publish:");
  for (const p of pins) console.error(`  ${p.file}: npm@${p.pin}`);
  process.exit(1);
}

console.log(`OK: ${FILES.join(" and ")} both install npm@${distinct[0]}`);
