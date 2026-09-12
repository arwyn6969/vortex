import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { ATLAS, RELATIONS, ATLAS_SOURCES, searchAtlas } from "../atlas.ts";
import { atlasView, emptyAtlasView } from "../atlas-view.ts";
import { emptyInquiries, inquiryMemory } from "../inquiries.ts";
import { transition, activeSeeker } from "../session.ts";
import {
  parseWorld,
  saveWorld,
  loadWorld,
  restoreBackup,
  recoveryWorld,
  SAVE_KEY,
  BACKUP_KEY,
  RECOVERY_KEY,
} from "../storage.ts";
import { finish, travel, newGame, MemoryStorage } from "./helpers.ts";
import { safeText } from "../safety.ts";
import { withJourneyLock } from "../journey-lock.ts";

test("atlas identifiers and source references are complete; aliases and untrusted search remain inert", () => {
  assert.equal(new Set(ATLAS.map((x) => x.id)).size, ATLAS.length);
  assert.equal(new Set(RELATIONS.map((x) => x.id)).size, RELATIONS.length);
  for (const entry of ATLAS) {
    assert(ATLAS_SOURCES[entry.source]);
    assert(entry.locator);
    assert(entry.distinction);
    if (entry.kind === "Asset")
      assert.match(ATLAS_SOURCES[entry.source].url, /^https:\/\/xcp\.io\//);
  }
  for (const r of RELATIONS) {
    assert(ATLAS.some((x) => x.id === r.from));
    assert(ATLAS.some((x) => x.id === r.to));
    assert(ATLAS_SOURCES[r.source]);
  }
  assert(searchAtlas("Nidaba").some((x) => x.id === "nisaba"));
  assert(searchAtlas("Hunahpu").some((x) => x.id === "hero-twins"));
  assert(searchAtlas("KEVIN").some((x) => x.id === "kevin-saga"));
  assert(!searchAtlas("Xiuhtecuhtli").length);
  const html = atlasView(activeSeeker(newGame())!, {
    ...emptyAtlasView(),
    query: '<img src=x onerror="alert(1)">',
  });
  assert(!html.includes("<img src=x"));
  assert(html.includes("&lt;img"));
});
test("released v4 journeys migrate without losing fields and v5 rejects missing or forged atlas progress", () => {
  const raw = readFileSync(
    new URL("./fixtures/enduring-v4.json", import.meta.url),
    "utf8",
  );
  const old = JSON.parse(raw),
    migrated = parseWorld(raw);
  assert.equal(migrated.version, 5);
  const restored: any = structuredClone(migrated);
  restored.version = 4;
  for (const s of restored.seekers) delete s.inquiries;
  assert.deepEqual(restored, old);
  assert.deepEqual(migrated.seekers[0].inquiries, emptyInquiries());
  for (const bad of [
    undefined,
    { ...emptyInquiries(), seen: ["invented"] },
    { ...emptyInquiries(), tablet: 1 },
    { ...emptyInquiries(), gate: 2 },
    { ...emptyInquiries(), seen: ["nisaba", "nisaba"] },
  ]) {
    const w: any = structuredClone(migrated);
    w.seekers[0].inquiries = bad;
    assert.throws(() => parseWorld(JSON.stringify(w)));
  }
  const older: any = structuredClone(migrated);
  older.version = 4;
  assert.throws(() => parseWorld(JSON.stringify(older)));
});
test("all tablet and gate branches persist and rejected choices are atomic", () => {
  for (let tablet = 0; tablet < 3; tablet++)
    for (let gate = 0; gate < 3; gate++) {
      let w = finish();
      for (const entry of ["stamps", "nisaba", "hero-twins"])
        w = transition(w, { type: "study", entry });
      w = travel(w, "yesod");
      w = transition(w, { type: "inquiry", task: "testimony", choice: 0 });
      w = travel(w, "hod");
      w = transition(w, { type: "inquiry", task: "tablet", choice: tablet });
      if (gate === 2 && tablet !== 0) {
        w = travel(w, "chesed");
        w = transition(w, { type: "story-start", story: "chesed", choice: 0 });
        w = travel(w, "gevurah");
        w = transition(w, { type: "story-deliver", story: "chesed" });
        w = travel(w, "chesed");
        w = transition(w, {
          type: "story-resolve",
          story: "chesed",
          choice: 0,
        });
      }
      w = travel(w, "netzach");
      w = transition(w, { type: "inquiry", task: "gate", choice: gate });
      const before = JSON.stringify(w);
      assert.throws(() =>
        transition(w, { type: "inquiry", task: "gate", choice: 0 }),
      );
      assert.equal(JSON.stringify(w), before);
      for (let i = 0; i < 90; i++) w = transition(w, { type: "sit" });
      w = travel(w, "malkhut");
      assert(
        activeSeeker(w)!.journal.some(
          (x) => x.text === inquiryMemory(activeSeeker(w)!, "malkhut"),
        ),
      );
      assert.deepEqual(parseWorld(JSON.stringify(w)), w);
      assert(activeSeeker(w)!.rooted);
      assert.equal(activeSeeker(w)!.proof, null);
    }
  const w = newGame(),
    before = JSON.stringify(w);
  for (const action of [
    { type: "study", entry: "__proto__" },
    { type: "inquiry", task: "tablet", choice: 0 },
    { type: "inquiry", task: "fake", choice: 1 },
  ])
    assert.throws(() => transition(w, action as any));
  assert.equal(JSON.stringify(w), before);
});
test("recovery preserves damaged originals, rechecks conflicts, and fails safely at either storage write", async () => {
  const store = new MemoryStorage(),
    first = newGame();
  saveWorld(store, first, 0);
  const second = transition(first, { type: "look" });
  saveWorld(store, second, first.revision);
  assert.deepEqual(await recoveryWorld(store), first);
  store.setItem(SAVE_KEY, "broken json");
  const recovered = await restoreBackup(store, "broken json");
  assert.equal(store.getItem(RECOVERY_KEY), "broken json");
  assert.deepEqual(recovered.seekers, first.seekers);
  assert.deepEqual(await loadWorld(store), recovered);
  await assert.rejects(restoreBackup(store, "stale"), /changed/);
  store.setItem(SAVE_KEY, '{"version":99}');
  await assert.rejects(restoreBackup(store, '{"version":99}'), /newer edition/);
  for (const failKey of [BACKUP_KEY, SAVE_KEY]) {
    const st = new MemoryStorage();
    saveWorld(st, first, 0);
    const original = st.getItem(SAVE_KEY);
    st.setItem = (key, value) => {
      if (key === failKey) throw new Error("quota");
      st.data.set(key, value);
    };
    assert.throws(() => saveWorld(st, second, first.revision), /quota/);
    assert.equal(st.getItem(SAVE_KEY), original);
  }
});
test("ordinary twelve-word questions work while mnemonic-shaped input remains blocked", () => {
  const sentence =
    "please tell me about the temple and the frogs beside this river";
  assert.equal(safeText(sentence, 500), sentence);
  assert.throws(() => safeText("abandon ".repeat(11) + "about", 500));
  const w = transition(newGame(), { type: "talk", text: sentence });
  assert(!JSON.stringify(w).includes(sentence));
});
test("browser writes serialize through Web Locks; unsupported browsers cannot silently race", async () => {
  const previous = Object.getOwnPropertyDescriptor(globalThis, "navigator");
  try {
    Object.defineProperty(globalThis, "navigator", {
      configurable: true,
      value: {},
    });
    let written = false;
    await assert.rejects(
      withJourneyLock(async () => {
        written = true;
      }),
      /safely coordinate/,
    );
    assert(!written);
    let queue = Promise.resolve();
    const order: number[] = [];
    Object.defineProperty(globalThis, "navigator", {
      configurable: true,
      value: {
        locks: {
          request: (_name: string, work: () => Promise<any>) => {
            const next = queue.then(work);
            queue = next.catch(() => {});
            return next;
          },
        },
      },
    });
    await Promise.all([
      withJourneyLock(async () => {
        order.push(1);
        await new Promise((r) => setImmediate(r));
        order.push(2);
      }),
      withJourneyLock(async () => {
        order.push(3);
      }),
    ]);
    assert.deepEqual(order, [1, 2, 3]);
  } finally {
    if (previous) Object.defineProperty(globalThis, "navigator", previous);
    else Reflect.deleteProperty(globalThis, "navigator");
  }
});
