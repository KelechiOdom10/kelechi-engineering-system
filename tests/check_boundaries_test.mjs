// node --test tests/check_boundaries_test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const script = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", "kickoff", "assets", "check-boundaries.mjs");

function repo(files, rules) {
  const root = mkdtempSync(join(tmpdir(), "boundaries-"));
  for (const [path, text] of Object.entries(files)) {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    writeFileSync(join(root, path), text);
  }
  writeFileSync(join(root, "boundaries.json"), JSON.stringify({ rules }));
  return root;
}

function check(root) {
  const out = spawnSync(process.execPath, [script, root], { encoding: "utf8" });
  return { code: out.status, text: out.stdout + out.stderr };
}

const rules = {
  "packages/core": { allow: ["zod"] },
  "apps/web": { deny: ["@app/db", "postgres"] },
};

test("passes when every import respects its scope", () => {
  const root = repo({
    "packages/core/src/plan.ts": 'import { z } from "zod";\nimport { helper } from "./helper";\n',
    "packages/core/src/helper.ts": "export const helper = 1;\n",
    "apps/web/src/app.tsx": 'import { useQuery } from "@tanstack/react-query";\nimport type { App } from "@app/api";\n',
  }, rules);
  const result = check(root);
  assert.equal(result.code, 0, result.text);
  assert.match(result.text, /Boundaries hold across 2 scopes/);
});

test("fails on a denied package with its file and line", () => {
  const root = repo({
    "packages/core/src/plan.ts": 'import { z } from "zod";\n',
    "apps/web/src/leak.ts": '\n\nimport { db } from "@app/db";\n',
  }, rules);
  const result = check(root);
  assert.equal(result.code, 1);
  assert.match(result.text, /apps\/web\/src\/leak\.ts:3: "@app\/db" is denied in apps\/web/);
});

test("fails when an allow-listed scope imports anything else, including multi-line imports", () => {
  const root = repo({
    "packages/core/src/plan.ts": 'import {\n  drizzle,\n  sql,\n} from "drizzle-orm/pg-core";\n',
    "apps/web/src/app.tsx": "",
  }, rules);
  const result = check(root);
  assert.equal(result.code, 1);
  assert.match(result.text, /"drizzle-orm" is not in packages\/core's allow list/);
});

test("fails when a relative import escapes its scope", () => {
  const root = repo({
    "packages/core/src/plan.ts": 'import { db } from "../../../apps/web/src/secret";\n',
    "apps/web/src/secret.ts": "export const db = 1;\n",
  }, rules);
  const result = check(root);
  assert.equal(result.code, 1);
  assert.match(result.text, /relative import .* leaves packages\/core/);
});

test("fails when a declared scope is missing, so a rename cannot silently disable a rule", () => {
  const root = repo({ "apps/web/src/app.tsx": "" }, rules);
  const result = check(root);
  assert.equal(result.code, 1);
  assert.match(result.text, /packages\/core: declared in boundaries\.json but missing on disk/);
});
