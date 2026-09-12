import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { IDS } from "../lattice.ts";
import { RARES, OFFICE_RARE, rareAt, supply } from "../rares.ts";

test("each temple references a distinct recorded Counterparty asset and original artwork", () => {
  assert.equal(RARES.length, 10);
  assert.equal(new Set(Object.values(OFFICE_RARE)).size, 10);
  for (const id of IDS) {
    const r = rareAt(id);
    assert(r);
    assert.match(r.assetId, /^\d+$/);
    assert.equal(
      r.api,
      "https://api.counterparty.io:4000/v2/assets/" + r.name + "/",
    );
    assert.equal(r.explorer, "https://tokenscan.io/asset/" + r.name);
    assert(readFileSync("vortex/web/public" + r.image).length > 1000);
  }
});
test("divisible supply stays exact instead of rounding a Rare Pepe quantity", () => {
  assert.equal(supply(RARES.find((r) => r.name === "LORDKEK")!), "9.9999995");
  assert.equal(supply(RARES.find((r) => r.name === "RAREPEPE")!), "298");
});
