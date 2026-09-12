import test from "node:test";
import assert from "node:assert/strict";
import { IDS, NODES, neighbors, place } from "../lattice.ts";
import { PATH_LETTERS, pathKey } from "../paths.ts";
import {
  activeSeeker,
  addSeeker,
  transition,
  status,
  isBound,
  readyToRoot,
} from "../session.ts";
import type { Action } from "../session.ts";
import { parseWorld } from "../storage.ts";
import { looksLikeSecret, safeText, escapeHtml } from "../safety.ts";
import { newGame, finish, travel } from "./helpers.ts";

test("ten offices, 22 unique undirected paths, connected in both directions", () => {
  assert.equal(IDS.length, 10);
  assert.equal(PATH_LETTERS.length, 22);
  assert.equal(new Set(PATH_LETTERS.map((p) => p.id)).size, 22);
  for (const p of PATH_LETTERS) {
    assert.equal(p.id, pathKey(p.from, p.to));
    assert(neighbors(p.from).includes(p.to));
    assert(neighbors(p.to).includes(p.from));
  }
  assert.deepEqual(
    IDS.filter((id) => NODES[id].ledgerFloor),
    ["malkhut"],
  );
  assert.deepEqual(
    IDS.filter((id) => NODES[id].creationUnlock),
    ["hod", "yesod", "malkhut"],
  );
});
test("ties and empty profiles start at the heart", () => {
  for (const scores of [
    { mercy: 0, severity: 0, balance: 0 },
    { mercy: 0.5, severity: 0.5, balance: 0.5 },
    { mercy: 0.8, severity: 0.8, balance: 0.1 },
  ])
    assert.equal(place(scores, true).node.id, "tiferet");
});
test("every one of 729 questionnaire combinations can finish without a wallet", () => {
  for (let n = 0; n < 729; n++) {
    let x = n;
    const answers = Array.from({ length: 6 }, () => {
      const a = x % 3;
      x = Math.floor(x / 3);
      return a;
    });
    const w = finish(answers),
      s = activeSeeker(w)!;
    assert(s.rooted);
    assert(!isBound(s));
    assert(readyToRoot(s));
    assert.equal(s.visited.length, 10);
    assert.deepEqual(parseWorld(JSON.stringify(w)), w);
  }
});
test("invalid actions never mutate the world or advance its clock", () => {
  const w = newGame(),
    original = JSON.stringify(w);
  for (const a of [
    { type: "walk", to: "malkhut" },
    { type: "rite", choice: 0 },
    { type: "sigil", text: "hello" },
    { type: "root" },
    { type: "unknown" },
  ])
    assert.throws(() => transition(w, a as Action));
  assert.equal(JSON.stringify(w), original);
});
test("Crown opens only after both pillars meet at the heart", () => {
  let w = newGame([0, 0, 0, 0, 0, 0]);
  assert.equal(status(w, activeSeeker(w)!, "keter"), "veiled");
  w = transition(w, { type: "sit" });
  assert.equal(activeSeeker(w)!.harmony, false);
  w = travel(w, "tiferet");
  assert.equal(activeSeeker(w)!.harmony, true);
  assert.equal(status(w, activeSeeker(w)!, "keter"), "open");
});
test("Qoph stays veiled in both directions until this seeker Looks at Netzach", () => {
  let w = travel(newGame(), "netzach");
  assert.equal(status(w, activeSeeker(w)!, "malkhut"), "veiled");
  w = transition(w, { type: "look" });
  assert.equal(status(w, activeSeeker(w)!, "malkhut"), "open");
  w = transition(w, { type: "walk", to: "malkhut" });
  assert.equal(status(w, activeSeeker(w)!, "netzach"), "open");
});
test("a return reveals a stream once, and repeated rites/rests cannot farm progress", () => {
  let w = newGame();
  w = transition(w, { type: "walk", to: "hod" });
  w = transition(w, { type: "walk", to: "tiferet" });
  const s = activeSeeker(w)!;
  assert.equal(s.crossings[pathKey("hod", "tiferet")], 2);
  assert(s.journal.some((j) => j.text.includes("reveals its meaning")));
  w = transition(w, { type: "look" });
  w = transition(w, { type: "rite", choice: 0 });
  assert.throws(() => transition(w, { type: "rite", choice: 1 }));
  w = transition(w, { type: "sit" });
  const scores = { ...activeSeeker(w)!.pillars };
  w = transition(w, { type: "sit" });
  assert.deepEqual(activeSeeker(w)!.pillars, scores);
});
test("the Watcher changes shared water but never speaks or traps a seeker", () => {
  let w = newGame();
  for (const to of ["hod", "tiferet", "chesed"] as const)
    w = transition(w, { type: "walk", to });
  assert.equal(Object.keys(w.darkness).length, 1);
  assert(
    neighbors(activeSeeker(w)!.current).some(
      (to) => status(w, activeSeeker(w)!, to) === "open",
    ),
  );
  assert(!activeSeeker(w)!.journal.some((j) => j.speaker === "Watcher"));
  const first = structuredClone(activeSeeker(w)!);
  w = addSeeker(
    w,
    "Second Frog",
    "classical",
    { mercy: 0.5, severity: 0.5, balance: 0.5 },
    1,
    "second",
  );
  w = transition(w, { type: "sit" });
  assert.deepEqual(w.darkness, {});
  assert.deepEqual(w.seekers[0], first);
});
test("sigil changes invalidate a previous root and proof", () => {
  let w = travel(finish(), "hod");
  assert(activeSeeker(w)!.rooted);
  w = transition(w, { type: "sigil", text: "Try another tomorrow" });
  assert.equal(activeSeeker(w)!.rooted, false);
  assert.equal(activeSeeker(w)!.proof, null);
});
test("questions stay out of saves; speaker identity survives dialect changes", () => {
  let w = newGame();
  const old = activeSeeker(w)!.journal[1].speaker;
  w = transition(w, {
    type: "talk",
    text: "I worry about a very specific fictional meeting tomorrow.",
  });
  assert(!JSON.stringify(w).includes("specific fictional meeting"));
  w = transition(w, { type: "dialect", dialect: "classical" });
  assert.equal(activeSeeker(w)!.journal[1].speaker, old);
});
test("long random walks always produce reloadable bounded saves", () => {
  let w = newGame(),
    seed = 8731;
  for (let n = 0; n < 3000; n++) {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    const s = activeSeeker(w)!,
      choices = neighbors(s.current).filter(
        (to) => status(w, s, to) === "open",
      );
    const actions: Action[] = [
      { type: "look" },
      { type: "sit" },
      ...choices.map((to) => ({ type: "walk" as const, to })),
    ];
    w = transition(w, actions[seed % actions.length]);
    if (n % 50 === 0) assert.deepEqual(parseWorld(JSON.stringify(w)), w);
  }
  assert(activeSeeker(w)!.journal.length <= 80);
});
test("secret-shaped input is rejected before storage and markup is escaped", () => {
  for (const text of [
    "a".repeat(64),
    "abandon ".repeat(11) + "about",
    "sk-" + "x".repeat(24),
  ]) {
    assert(looksLikeSecret(text));
    assert.throws(() => safeText(text, 500));
  }
  assert.equal(
    escapeHtml('<img src=x onerror="x">'),
    "&lt;img src=x onerror=&quot;x&quot;&gt;",
  );
  assert.throws(() => safeText("two\nlines", 500));
});
