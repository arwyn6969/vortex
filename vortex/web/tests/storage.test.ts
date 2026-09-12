import test from "node:test";
import assert from "node:assert/strict";
import {
  SAVE_KEY,
  parseWorld,
  loadWorld,
  saveWorld,
  importWorld,
} from "../storage.ts";
import { activeSeeker, addSeeker, transition } from "../session.ts";
import { MemoryStorage, newGame, finish } from "./helpers.ts";

test("save and reload preserve the completed journey exactly", async () => {
  const store = new MemoryStorage(),
    w = finish();
  saveWorld(store, w, 0);
  assert.deepEqual(await loadWorld(store), w);
});
test("stale writers and full storage preserve previous progress", () => {
  const store = new MemoryStorage(),
    w = newGame();
  saveWorld(store, w, 0);
  const before = store.getItem(SAVE_KEY);
  assert.throws(
    () => saveWorld(store, transition(w, { type: "look" }), 0),
    /Another tab/,
  );
  store.setItem = () => {
    throw new Error("quota");
  };
  assert.throws(
    () => saveWorld(store, transition(w, { type: "sit" }), w.revision),
    /quota/,
  );
  assert.equal(store.getItem(SAVE_KEY), before);
});
test("malformed and future saves are retained verbatim", async () => {
  for (const raw of [
    "not json",
    '{"version":9}',
    JSON.stringify({ ...newGame(), activeId: "missing" }),
  ]) {
    const store = new MemoryStorage();
    store.setItem(SAVE_KEY, raw);
    await assert.rejects(loadWorld(store));
    assert.equal(store.getItem(SAVE_KEY), raw);
  }
});
test("forged states, prototype keys, impossible progress and oversized input fail", () => {
  const mutations = [
    (w: any) => (w.seekers[0].current = "__proto__"),
    (w: any) => (w.seekers[0].pillars.mercy = 2),
    (w: any) => (w.seekers[0].rites.hod = 0),
    (w: any) => (w.seekers[0].rooted = true),
    (w: any) => (w.darkness.not_a_path = 3),
  ];
  for (const change of mutations) {
    const w = newGame();
    change(w);
    assert.throws(() => parseWorld(JSON.stringify(w)));
  }
  assert.throws(() => parseWorld("x".repeat(1_000_001)), /too large/);
});
test("imports merge new identities but cannot silently rewind an existing journey", async () => {
  const store = new MemoryStorage(),
    w = newGame();
  saveWorld(store, w, 0);
  const other = addSeeker(
    { ...w, seekers: [], activeId: null },
    "Other Frog",
    "folk",
    { mercy: 0.2, severity: 0.2, balance: 0.5 },
    1,
    "other",
  );
  const merged = await importWorld(store, JSON.stringify(other));
  assert.equal(merged.seekers.length, 2);
  assert.deepEqual(merged.seekers[0], activeSeeker(w));
  const original = store.getItem(SAVE_KEY);
  await assert.rejects(
    importWorld(store, JSON.stringify(transition(w, { type: "look" }))),
    /different version/,
  );
  assert.equal(store.getItem(SAVE_KEY), original);
});
