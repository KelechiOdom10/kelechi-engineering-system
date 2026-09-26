#!/usr/bin/env node
// Enforces the dependency rule declared in boundaries.json. Zero dependencies.
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";

const SKIP = new Set(["node_modules", "dist", "build", "coverage", ".output", ".wrangler", ".tanstack", ".vinxi", ".turbo", "fixtures"]);
const SOURCE = /\.(m|c)?(t|j)sx?$/;
const SPECIFIERS = [
  /\b(?:import|export)\s[^'"`;]*?\sfrom\s*['"]([^'"]+)['"]/g,
  /\bimport\s*['"]([^'"]+)['"]/g,
  /\bimport\(\s*['"]([^'"]+)['"]\s*\)/g,
  /\brequire\(\s*['"]([^'"]+)['"]\s*\)/g,
];

const root = resolve(process.argv[2] ?? ".");
const configPath = resolve(process.argv[3] ?? join(root, "boundaries.json"));
if (!existsSync(configPath)) {
  console.error(`No boundary config at ${configPath}`);
  process.exit(2);
}
const { rules } = JSON.parse(readFileSync(configPath, "utf8"));

function* sourceFiles(dir) {
  for (const entry of readdirSync(dir)) {
    if (SKIP.has(entry) || entry.startsWith(".")) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) yield* sourceFiles(full);
    else if (SOURCE.test(entry) && !entry.endsWith(".d.ts")) yield full;
  }
}

function packageName(specifier) {
  if (specifier.startsWith("node:")) return specifier;
  const parts = specifier.split("/");
  return specifier.startsWith("@") ? parts.slice(0, 2).join("/") : parts[0];
}

function matches(name, pattern) {
  return pattern.endsWith("*") ? name.startsWith(pattern.slice(0, -1)) : name === pattern;
}

function lineOf(text, index) {
  return text.slice(0, index).split("\n").length;
}

const violations = [];
for (const [scope, rule] of Object.entries(rules)) {
  const scopeDir = join(root, scope);
  if (!existsSync(scopeDir)) {
    violations.push(`${scope}: declared in boundaries.json but missing on disk`);
    continue;
  }
  for (const file of sourceFiles(scopeDir)) {
    const text = readFileSync(file, "utf8");
    for (const pattern of SPECIFIERS) {
      for (const match of text.matchAll(pattern)) {
        const specifier = match[1];
        const where = `${relative(root, file)}:${lineOf(text, match.index)}`;
        if (specifier.startsWith(".")) {
          const target = resolve(dirname(file), specifier);
          if (!(target + sep).startsWith(scopeDir + sep) && target !== scopeDir) {
            violations.push(`${where}: relative import "${specifier}" leaves ${scope}; import the package instead`);
          }
          continue;
        }
        const name = packageName(specifier);
        if (rule.deny?.some((p) => matches(name, p))) {
          violations.push(`${where}: "${name}" is denied in ${scope}`);
        } else if (rule.allow && !rule.allow.some((p) => matches(name, p))) {
          violations.push(`${where}: "${name}" is not in ${scope}'s allow list`);
        }
      }
    }
  }
}

if (violations.length > 0) {
  console.error(`Boundary violations (${violations.length}):\n  ${violations.join("\n  ")}`);
  process.exit(1);
}
const count = Object.keys(rules).length;
console.log(`Boundaries hold across ${count} scope${count === 1 ? "" : "s"}.`);
