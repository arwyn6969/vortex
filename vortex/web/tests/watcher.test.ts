import assert from "node:assert/strict";
import test from "node:test";
import { authoredDirective, senseWatcher } from "../watcher.ts";
import { transition } from "../session.ts";
import { newGame } from "./helpers.ts";

test("haste only after several walks with another open stream", () => {
  const w = newGame();
  const s = w.seekers[0]!;
  assert.equal(authoredDirective(w, s), "still");
  s.walks = 2;
  assert.equal(authoredDirective(w, s), "haste");
  assert.equal(senseWatcher(w, s).darkSoon, true);
  assert.doesNotMatch(senseWatcher(w, s).water, /watcher/i);
});

test("tilt when one pillar dominates", () => {
  const w = newGame();
  const s = w.seekers[0]!;
  s.pillars.mercy = 0.7;
  s.pillars.severity = 0.1;
  s.pillars.balance = 0.1;
  assert.equal(authoredDirective(w, s), "tilt");
});

test("thin when many offices are passed without looking", () => {
  const w = newGame();
  const s = w.seekers[0]!;
  s.visited = ["tiferet", "hod", "yesod", "netzach"];
  s.looked = ["tiferet"];
  assert.equal(authoredDirective(w, s), "thin");
});

test("sit clears haste darkness without naming the Watcher", () => {
  let w = newGame();
  w = transition(w, { type: "walk", to: "hod" });
  w = transition(w, { type: "walk", to: "yesod" });
  w = transition(w, { type: "walk", to: "malkhut" });
  w = transition(w, { type: "sit" });
  assert.deepEqual(w.darkness, {});
});

test("hosted override may change water copy but not darkness", () => {
  const w = newGame();
  const s = w.seekers[0]!;
  const still = senseWatcher(w, s, "haste");
  assert.equal(still.directive, "haste");
  assert.equal(still.darkSoon, false);
  assert.match(still.water, /current is running/i);
  assert.doesNotMatch(still.water, /watcher/i);
  s.walks = 2;
  const warned = senseWatcher(w, s, "still");
  assert.equal(warned.directive, "still");
  assert.equal(warned.darkSoon, true);
  assert.equal(warned.water, "");
});
