#!/usr/bin/env node
"use strict";
// Asserts what the published tarball will contain. Used by both
// .github/workflows/ci.yml and publish.yml so the two cannot drift — the
// previous copies were duplicated inline and diverged the moment they ran
// against different npm majors (see below).
//
// This file is a repo tool, not shipped content: scripts/ is deliberately
// absent from package.json "files", and this script asserts that too.
//
// Usage:  node scripts/check-package-contents.js
// Exit:   0 all assertions hold, 1 a violation, 2 could not read npm's output.
//
// `npm pack --json` has TWO output shapes and the difference is silent:
//   npm <= 11:  [ { id, name, files: [{path, size}, ...] } ]
//   npm >= 12:  { "<pkg-name>": { id, name, files: [...] } }
// Reading `[0].files` throws `TypeError: Cannot read properties of undefined`
// under npm 12. Both shapes are normalized here rather than pinning an npm
// version, since publish.yml must track npm >= 11.5.1 for trusted publishing.

const { execFileSync } = require("child_process");
const path = require("path");

const REPO = path.join(__dirname, "..");

// Directories every install needs. docs/ is included because README's guide
// link and the wizard's printed guide pointer both resolve into it, so omitting
// it ships two dangling references.
const REQUIRED_DIRS = ["kit/", "bin/", "installers/", "docs/"];
const REQUIRED_FILES = ["LICENSE", "README.md", "CHANGELOG.md", "package.json"];
// Repo-only paths that must never reach a user's node_modules.
const FORBIDDEN_PREFIXES = ["scripts/", ".github/", "outputs/", "examples/"];

function packJson() {
  let raw;
  try {
    raw = execFileSync("npm", ["pack", "--dry-run", "--json"], {
      cwd: REPO,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
      maxBuffer: 32 * 1024 * 1024,
    });
  } catch (e) {
    console.error(`error: \`npm pack --dry-run --json\` failed (${e.message})`);
    process.exit(2);
  }
  // npm may prepend warnings on stdout in some configurations; take the JSON
  // from the first structural character so a warning line cannot break parsing.
  const start = raw.search(/[[{]/);
  if (start === -1) {
    console.error("error: npm pack produced no JSON on stdout");
    process.exit(2);
  }
  try {
    return JSON.parse(raw.slice(start));
  } catch (e) {
    console.error(`error: could not parse npm pack output as JSON (${e.message})`);
    process.exit(2);
  }
}

// Returns the file path list, whichever shape npm used.
function filePaths(parsed) {
  const entry = Array.isArray(parsed)
    ? parsed[0] // npm <= 11
    : parsed && typeof parsed === "object"
      ? Object.values(parsed)[0] // npm >= 12, keyed by package name
      : undefined;
  if (!entry || !Array.isArray(entry.files)) {
    console.error("error: npm pack output had neither the array nor the keyed-object shape");
    console.error(`  got: ${JSON.stringify(parsed).slice(0, 200)}`);
    process.exit(2);
  }
  return entry.files.map((f) => f.path);
}

function main() {
  const files = filePaths(packJson());
  const fail = [];

  for (const dir of REQUIRED_DIRS) {
    if (!files.some((f) => f.startsWith(dir))) fail.push(`missing ${dir}`);
  }
  for (const f of REQUIRED_FILES) {
    if (!files.includes(f)) fail.push(`missing ${f}`);
  }
  for (const f of files) {
    // The verification suites import kit/scripts/*.py, which leaves
    // interpreter-specific bytecode beside it; a directory allowlist would
    // otherwise sweep it in.
    if (f.endsWith(".pyc") || f.includes("__pycache__")) fail.push(`bytecode shipped: ${f}`);
    for (const p of FORBIDDEN_PREFIXES) {
      if (f.startsWith(p)) fail.push(`repo-only path shipped: ${f}`);
    }
  }

  if (fail.length) {
    console.error("error: tarball contents violate the package contract:");
    for (const f of [...new Set(fail)]) console.error(`  ${f}`);
    process.exit(1);
  }
  console.log(`OK: ${files.length} files, contents as declared`);
  return 0;
}

// --selftest exercises the shape normalizer against both npm majors' output
// without needing either installed, because the whole point is that one shape
// silently produced a crash that CI could not see.
if (process.argv.includes("--selftest")) {
  const cases = [
    ["npm<=11 array", [{ name: "x", files: [{ path: "bin/a.js" }] }], ["bin/a.js"]],
    ["npm>=12 object", { x: { name: "x", files: [{ path: "bin/a.js" }] } }, ["bin/a.js"]],
  ];
  let bad = 0;
  for (const [label, input, expected] of cases) {
    const got = filePaths(input);
    const ok = JSON.stringify(got) === JSON.stringify(expected);
    console.log(`  ${ok ? "OK  " : "FAIL"} ${label} -> ${JSON.stringify(got)}`);
    if (!ok) bad++;
  }
  process.exit(bad ? 1 : 0);
}

process.exit(main());
