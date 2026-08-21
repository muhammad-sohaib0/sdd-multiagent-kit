#!/usr/bin/env node
"use strict";
// Version bump tool. Sets one version across every place that carries it:
// package.json and the `version:` frontmatter of kit/SKILL.md plus each
// kit/skills/*/SKILL.md. Skill versions stay in lockstep with the package
// because they ship in the same tarball.
//
// This file is a repo tool, not shipped content — scripts/ is deliberately
// absent from package.json "files", so users never receive it. Node stdlib
// only, matching the package's no-dependencies rule.
//
// Usage:  node scripts/bump-version.js 0.2.0
//         node scripts/bump-version.js --check     (verify agreement, change nothing)
//
// Exit codes: 0 success (or --check found agreement), 1 --check found a
// mismatch, 2 usage error.
//
// It deliberately does NOT touch CHANGELOG.md — release notes are prose a
// human writes, and generating them would produce a plausible-looking record
// nobody actually verified.

const fs = require("fs");
const path = require("path");

const REPO = path.join(__dirname, "..");
const PKG = path.join(REPO, "package.json");
const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;

// Every SKILL.md that carries a `version:` frontmatter key: the master skill
// plus each sub-skill. Discovered, not hard-coded, so a new sub-skill is picked
// up automatically instead of being silently skipped.
function skillFiles() {
  const files = [path.join(REPO, "kit", "SKILL.md")];
  const skills = path.join(REPO, "kit", "skills");
  for (const name of fs.readdirSync(skills).sort()) {
    const f = path.join(skills, name, "SKILL.md");
    if (fs.existsSync(f)) files.push(f);
  }
  return files;
}

// The `version:` line inside the leading `---` frontmatter block only. Anchored
// to the block so a `version:` mentioned in prose further down is never touched.
function frontmatterVersion(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!m) return null;
  const v = /^version:[ \t]*(\S+)[ \t]*$/m.exec(m[1]);
  return v ? v[1] : null;
}

function setFrontmatterVersion(text, version) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (!m) return null;
  if (!/^version:[ \t]*\S+[ \t]*$/m.test(m[1])) return null;
  const block = m[1].replace(/^version:[ \t]*\S+[ \t]*$/m, `version: ${version}`);
  return text.slice(0, m.index) + "---\n" + block + "\n---" + text.slice(m.index + m[0].length);
}

function readPkg() {
  return JSON.parse(fs.readFileSync(PKG, "utf8"));
}

// Reports every place whose version differs from package.json's.
function findMismatches(version) {
  const bad = [];
  for (const f of skillFiles()) {
    const found = frontmatterVersion(fs.readFileSync(f, "utf8"));
    if (found !== version) {
      bad.push(`${path.relative(REPO, f)}: ${found === null ? "no version: key in frontmatter" : found}`);
    }
  }
  return bad;
}

function main(argv) {
  const arg = argv[2];
  if (!arg || arg === "-h" || arg === "--help") {
    console.log("usage: node scripts/bump-version.js <new-version> | --check");
    return arg ? 0 : 2;
  }

  if (arg === "--check") {
    const version = readPkg().version;
    const bad = findMismatches(version);
    if (bad.length) {
      console.error(`error: version mismatch — package.json is ${version} but:`);
      for (const b of bad) console.error(`  ${b}`);
      return 1;
    }
    console.log(`OK: package.json and ${skillFiles().length} SKILL.md files all at ${version}`);
    return 0;
  }

  if (argv.length > 3) {
    console.error("error: takes exactly one version (see --help)");
    return 2;
  }
  if (!SEMVER.test(arg)) {
    console.error(`error: "${arg}" is not a semver version (expected e.g. 0.2.0)`);
    return 2;
  }

  const pkg = readPkg();
  const from = pkg.version;

  // package.json: rewrite the version string in place rather than
  // re-serializing the whole object, so key order and formatting survive.
  const raw = fs.readFileSync(PKG, "utf8");
  const next = raw.replace(/("version":\s*")[^"]*(")/, `$1${arg}$2`);
  if (next === raw && from !== arg) {
    console.error('error: could not locate the "version" field in package.json');
    return 2;
  }
  if (next !== raw) fs.writeFileSync(PKG, next);

  let changed = raw === next ? 0 : 1;
  for (const f of skillFiles()) {
    const text = fs.readFileSync(f, "utf8");
    const updated = setFrontmatterVersion(text, arg);
    if (updated === null) {
      console.error(`error: ${path.relative(REPO, f)} has no version: key in its frontmatter`);
      return 2;
    }
    if (updated !== text) {
      fs.writeFileSync(f, updated);
      changed++;
    }
  }

  console.log(`${from} -> ${arg}  (${changed} file${changed === 1 ? "" : "s"} changed, ${skillFiles().length + 1} checked)`);
  if (changed === 0) console.log("already at this version — nothing to do");
  console.log("next: update CHANGELOG.md, then merge to main to publish");
  return 0;
}

process.exit(main(process.argv));
