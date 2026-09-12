import test from "node:test";
import assert from "node:assert/strict";
import { IDS } from "../lattice.ts";
import type { SefirahId } from "../lattice.ts";
import { activeSeeker, transition, addSeeker, status } from "../session.ts";
import type { World, Action } from "../session.ts";
import {
  STORIES,
  completedStories,
  activeStories,
  readyForFestival,
  FESTIVAL_ENDINGS,
  returnMemory,
} from "../stories.ts";
import { rareAt } from "../rares.ts";
import { nextStep, route } from "../navigation.ts";
import { pathKey } from "../paths.ts";
import { readFileSync } from "node:fs";
import { storyPanel, storyBook, festivalPanel } from "../story-view.ts";
import { parseWorld, importWorld, SAVE_KEY } from "../storage.ts";
import { finish, newGame, travel, MemoryStorage } from "./helpers.ts";

function completeStory(
  w: World,
  id: SefirahId,
  choice = 0,
  resolution = 0,
): World {
  w = travel(w, id);
  w = transition(w, { type: "story-start", story: id, choice });
  w = travel(w, STORIES[id].destination);
  w = transition(w, { type: "story-deliver", story: id });
  w = travel(w, id);
  return transition(w, {
    type: "story-resolve",
    story: id,
    choice: resolution,
  });
}
test("all ten real-token stories support every outward and return choice without altering the canon", () => {
  assert.equal(new Set(IDS.map((id) => rareAt(id).assetId)).size, 10);
  for (const id of IDS)
    for (let choice = 0; choice < 3; choice++)
      for (let resolution = 0; resolution < 3; resolution++) {
        const w = completeStory(finish(), id, choice, resolution),
          s = activeSeeker(w)!;
        assert.deepEqual(s.stories[id], {
          choice,
          delivered: true,
          resolution,
        });
        assert.equal(returnMemory(s, id), STORIES[id].aftermath[resolution]);
        assert(s.rooted);
        assert.equal(s.proof, null);
        assert.equal(s.visited.length, 10);
        assert(
          s.journal.some((j) =>
            j.text.includes(STORIES[id].aftermath[resolution]),
          ),
        );
        assert.deepEqual(parseWorld(JSON.stringify(w)), w);
      }
});
test("story actions require their actual location, rite, delivery and a free story slot; rejected actions are atomic", () => {
  let w = finish();
  const reject = (action: unknown) => {
    const before = JSON.stringify(w);
    assert.throws(() => transition(w, action as Action));
    assert.equal(JSON.stringify(w), before);
  };
  reject({ type: "story-start", story: "chokhmah", choice: 0 });
  reject({ type: "story-start", story: "__proto__", choice: 0 });
  reject({ type: "story-start", story: "malkhut", choice: NaN });
  reject({ type: "story-deliver", story: "malkhut" });
  reject({ type: "story-resolve", story: "malkhut", choice: 0 });
  for (const id of ["malkhut", "tiferet", "chesed"] as const) {
    w = travel(w, id);
    w = transition(w, { type: "story-start", story: id, choice: 1 });
  }
  assert.equal(activeStories(activeSeeker(w)!).length, 3);
  w = travel(w, "hod");
  reject({ type: "story-start", story: "hod", choice: 0 });
  w = travel(w, "gevurah");
  w = transition(w, { type: "story-deliver", story: "chesed" });
  reject({ type: "story-deliver", story: "chesed" });
  reject({ type: "story-resolve", story: "chesed", choice: 1 });
  w = travel(w, "chesed");
  w = transition(w, { type: "story-resolve", story: "chesed", choice: 1 });
  reject({ type: "story-resolve", story: "chesed", choice: 2 });
  w = travel(w, "hod");
  w = transition(w, { type: "story-start", story: "hod", choice: 0 });
  assert.equal(activeStories(activeSeeker(w)!).length, 3);
  let fresh = newGame();
  assert.throws(() =>
    transition(fresh, { type: "story-start", story: "tiferet", choice: 0 }),
  );
  fresh = transition(fresh, { type: "look" });
  fresh = transition(fresh, { type: "rite", choice: 0 });
  fresh = transition(fresh, {
    type: "story-start",
    story: "tiferet",
    choice: 0,
  });
  fresh = travel(fresh, "netzach");
  assert.throws(() =>
    transition(fresh, { type: "story-deliver", story: "tiferet" }),
  );
});
test("all festival endings reflect actual completed choices and remain wallet-free", () => {
  let w = finish();
  assert.throws(() => transition(w, { type: "festival", choice: 0 }));
  for (const [i, id] of (["chokhmah", "chesed", "tiferet"] as const).entries())
    w = completeStory(w, id, i, i);
  assert(readyForFestival(activeSeeker(w)!));
  assert.throws(() => transition(w, { type: "festival", choice: 0 })); // must return to Kingdom
  w = travel(w, "malkhut");
  for (let i = 0; i < 3; i++) {
    const end = transition(w, { type: "festival", choice: i }),
      s = activeSeeker(end)!;
    assert.equal(s.festival, i);
    assert.equal(s.proof, null);
    assert(s.rooted);
    assert(festivalPanel(s).includes(FESTIVAL_ENDINGS[i]));
    assert.equal(completedStories(s).length, 3);
    assert.throws(() =>
      transition(end, { type: "festival", choice: (i + 1) % 3 }),
    );
    assert.deepEqual(parseWorld(JSON.stringify(end)), end);
    const renewed = transition(travel(end, "hod"), {
      type: "sigil",
      text: "Make room for another season",
    });
    assert.equal(activeSeeker(renewed)!.festival, null);
    assert.equal(completedStories(activeSeeker(renewed)!).length, 3);
  }
});
test("save extension preserves Nile v3 journeys, rejects impossible story state, and survives export/import", async () => {
  // Captured by running the prior released c71650e source, not by guessing its shape.
  const original = readFileSync(
    new URL("./fixtures/nile-v3.json", import.meta.url),
    "utf8",
  );
  const old = JSON.parse(original);
  const migrated = parseWorld(original);
  assert.equal(migrated.version, 4);
  const restored = structuredClone(migrated) as any;
  restored.version = 3;
  delete restored.seekers[0].stories;
  delete restored.seekers[0].festival;
  assert.deepEqual(restored, old);
  assert.deepEqual(activeSeeker(migrated)!.stories, {});
  assert.equal(activeSeeker(migrated)!.festival, null);
  const w = completeStory(migrated, "chokhmah", 2, 1),
    s = activeSeeker(w)!;
  const storage = new MemoryStorage();
  await importWorld(storage, JSON.stringify(w));
  assert.deepEqual(parseWorld(storage.getItem(SAVE_KEY)!).seekers, w.seekers);
  const invalid = [
    { stories: { chokhmah: { choice: 3, delivered: true, resolution: 1 } } },
    { stories: { chokhmah: { choice: 1, delivered: false, resolution: 0 } } },
    {
      stories: { chokhmah: { choice: 1, delivered: "yes", resolution: null } },
    },
    { stories: { alien: { choice: 1, delivered: false, resolution: null } } },
    { stories: null },
    { festival: 0 },
    { festival: 3 },
    { stories: undefined },
    { festival: undefined },
  ];
  for (const fields of invalid) {
    const bad = structuredClone(w);
    Object.assign(activeSeeker(bad)!, fields);
    assert.throws(() => parseWorld(JSON.stringify(bad)));
  }
  const before = structuredClone(s);
  const second = addSeeker(
    w,
    "Different Frog",
    "folk",
    { mercy: 0.5, severity: 0.5, balance: 0.5 },
    1,
    "second",
  );
  assert.deepEqual(second.seekers[0], before);
  assert.deepEqual(activeSeeker(second)!.stories, {});
  assert.equal(activeSeeker(second)!.festival, null);
});
test("return scenes and Stories retain consequences after the journal rolls over", () => {
  let w = completeStory(finish(), "chokhmah", 0, 2);
  w = travel(w, "hod");
  assert.equal(
    returnMemory(activeSeeker(w)!, "hod"),
    STORIES.chokhmah.delivery[0],
  );
  for (let i = 0; i < 100; i++) w = transition(w, { type: "sit" });
  w = travel(w, "chokhmah");
  const s = activeSeeker(w)!;
  assert(s.journal.some((j) => j.text === STORIES.chokhmah.aftermath[2]));
  assert(storyBook(s).includes(STORIES.chokhmah.aftermath[2]));
  assert(storyPanel(s).includes(STORIES.chokhmah.aftermath[2]));
  assert.equal(s.journal.length, 80);
});
test("following the next-step guide completes both chapters from all 729 placements", () => {
  for (let n = 0; n < 729; n++) {
    let x = n;
    const answers = Array.from({ length: 6 }, () => {
      const a = x % 3;
      x = Math.floor(x / 3);
      return a;
    });
    let w = newGame(answers);
    for (
      let turn = 0;
      turn < 250 && activeSeeker(w)!.festival === null;
      turn++
    ) {
      const s = activeSeeker(w)!,
        hint = nextStep(w, s);
      if (hint.action) {
        if (hint.action.type === "walk")
          assert.equal(status(w, s, hint.action.to), "open");
        w = transition(w, hint.action);
      } else if (hint.panel === "rite")
        w = transition(w, { type: "rite", choice: n % 3 });
      else if (hint.panel === "sigil")
        w = transition(w, {
          type: "sigil",
          text: "A practical little promise",
        });
      else if (hint.panel === "festival")
        w = transition(w, { type: "festival", choice: n % 3 });
      else {
        const id = hint.target!,
          p = s.stories[id];
        w = transition(
          w,
          !p
            ? { type: "story-start", story: id, choice: n % 3 }
            : p.delivered
              ? { type: "story-resolve", story: id, choice: n % 3 }
              : { type: "story-deliver", story: id },
        );
      }
    }
    assert.notEqual(
      activeSeeker(w)!.festival,
      null,
      "Placement " + n + ": " + JSON.stringify(nextStep(w, activeSeeker(w)!)),
    );
    assert.deepEqual(parseWorld(JSON.stringify(w)), w);
  }
});
test("tracking an unstarted story leads to its temple; Crown and darkness never become illegal shortcuts", () => {
  let w = finish();
  let s = activeSeeker(w)!;
  const hint = nextStep(w, s, "chokhmah");
  assert.equal(hint.target, "chokhmah");
  assert(hint.action?.type === "walk");
  w.darkness = { [pathKey(s.current, hint.action.to)]: w.clock + 5 };
  assert.equal(nextStep(w, s, "chokhmah").action?.type, "sit");
  w = newGame([0, 0, 0, 0, 0, 0]);
  w = transition(w, { type: "look" });
  w = transition(w, { type: "rite", choice: 1 });
  s = activeSeeker(w)!;
  assert.equal(route(s, "keter"), null);
  assert.equal(nextStep(w, s, "keter").action?.type, "sit");
});
