import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { activeSeeker, transition } from "../session.ts";
import type { Action, World } from "../session.ts";
import { parseWorld } from "../storage.ts";
import { nextStep } from "../navigation.ts";
import { pathKey } from "../paths.ts";
import { worldDetail, worldVignette } from "../world-view.ts";
import { boardingHelper, suggestedBoarding } from "../boarding.ts";
import type { BoardingPlan } from "../boarding.ts";
import { registerJourneyTools, journeySnapshot } from "../webmcp.ts";
import type { JourneyTool } from "../webmcp.ts";
import { finish, newGame, travel } from "./helpers.ts";

function completeMercy(w: World): World {
  w = travel(w, "chesed");
  w = transition(w, { type: "story-start", story: "chesed", choice: 2 });
  w = travel(w, "gevurah");
  w = transition(w, { type: "story-deliver", story: "chesed" });
  w = travel(w, "chesed");
  return transition(w, { type: "story-resolve", story: "chesed", choice: 1 });
}
function readyToBoard(choice = 0): World {
  let w = travel(finish(), "tiferet");
  w = transition(w, { type: "story-start", story: "tiferet", choice });
  return travel(w, "netzach");
}

test("all 48 boarding arrangements enforce capacity, companionship and the player's promise atomically", () => {
  for (let choice = 0; choice < 3; choice++) {
    const w = readyToBoard(choice),
      before = JSON.stringify(w);
    let accepted = 0;
    for (let bits = 0; bits < 16; bits++) {
      const boarding = {
        novices: bits & 1,
        apprentice: (bits >> 1) & 1,
        cook: (bits >> 2) & 1,
        drummer: (bits >> 3) & 1,
      } as BoardingPlan;
      const action: Action = {
        type: "story-deliver",
        story: "tiferet",
        boarding,
      };
      // The only two safe partitions are [novices, apprentice] / [cook, drummer].
      // A quiet-first promise rules out the reversed order.
      const valid = bits === 12 || (choice !== 0 && bits === 3);
      if (!valid) assert.throws(() => transition(w, action));
      else {
        accepted++;
        const next = transition(w, action),
          s = activeSeeker(next)!;
        assert.equal(s.stories.tiferet!.delivered, true);
        assert.equal(s.turns, activeSeeker(w)!.turns + 1);
        assert.equal(next.revision, w.revision + 1);
        assert.deepEqual(s.pillars, activeSeeker(w)!.pillars);
        assert.deepEqual(parseWorld(JSON.stringify(next)), next);
        assert.throws(() => transition(next, action), /before delivering/);
      }
      assert.equal(JSON.stringify(w), before);
    }
    assert.equal(accepted, choice === 0 ? 1 : 2);
  }
});

test("malformed manifests cannot deliver, while a prior kindness and delegation both continue the same story", () => {
  const w = readyToBoard(),
    before = JSON.stringify(w);
  for (const boarding of [
    null,
    undefined,
    [],
    {},
    { ...suggestedBoarding(), extra: 0 },
    { ...suggestedBoarding(), cook: "1" },
    { ...suggestedBoarding(), novices: 2 },
  ]) {
    assert.throws(() =>
      transition(w, {
        type: "story-deliver",
        story: "tiferet",
        boarding,
      } as Action),
    );
    assert.equal(JSON.stringify(w), before);
  }
  assert(!boardingHelper(activeSeeker(w)!));
  let helped = completeMercy(w);
  assert(boardingHelper(activeSeeker(helped)!));
  helped = travel(helped, "netzach");
  const planned = transition(helped, {
    type: "story-deliver",
    story: "tiferet",
    boarding: suggestedBoarding(),
  });
  const delegated = transition(helped, {
    type: "story-deliver",
    story: "tiferet",
  });
  assert.deepEqual(
    activeSeeker(planned)!.stories,
    activeSeeker(delegated)!.stories,
  );
  for (const delivered of [planned, delegated]) {
    const home = transition(travel(delivered, "tiferet"), {
      type: "story-resolve",
      story: "tiferet",
      choice: 2,
    });
    assert.equal(activeSeeker(home)!.stories.tiferet!.resolution, 2);
    assert.deepEqual(parseWorld(JSON.stringify(home)), home);
  }
  let other = travel(finish(), "chesed");
  other = transition(other, {
    type: "story-start",
    story: "chesed",
    choice: 0,
  });
  other = travel(other, "gevurah");
  assert.throws(
    () =>
      transition(other, {
        type: "story-deliver",
        story: "chesed",
        boarding: suggestedBoarding(),
      }),
    /solar boat/,
  );
  assert.throws(
    () =>
      transition(travel(w, "hod"), {
        type: "story-deliver",
        story: "tiferet",
        boarding: suggestedBoarding(),
      }),
    /destination/,
  );
});

test("released v5 progress loads unchanged and its visible consequences survive journal rollover", () => {
  const raw = readFileSync(
    new URL("./fixtures/living-v5.json", import.meta.url),
    "utf8",
  );
  let w = parseWorld(raw);
  assert.deepEqual(w, JSON.parse(raw));
  assert.equal(activeSeeker(w)!.festival, 2);
  assert.deepEqual(activeSeeker(w)!.inquiries, {
    seen: ["stamps", "nisaba", "neti"],
    testimony: true,
    tablet: 1,
    gate: 2,
  });
  const before = worldVignette(activeSeeker(w)!);
  assert.match(before, /chorus/);
  assert.match(before, /Spare stools/);
  for (let i = 0; i < 90; i++) w = transition(w, { type: "sit" });
  w = parseWorld(JSON.stringify(w));
  assert.equal(worldVignette(activeSeeker(w)!), before);
  for (const [office, kind, variant] of [
    ["hod", "desk", 1],
    ["netzach", "gate", 2],
    ["tiferet", "boat", 0],
  ] as const) {
    w = travel(w, office);
    assert.equal(worldDetail(activeSeeker(w)!)!.kind, kind);
    assert.equal(worldDetail(activeSeeker(w)!)!.variant, variant);
  }
  assert.equal(worldVignette(activeSeeker(newGame())!), "");
});

test("all tablet, gate and festival illustrations follow saved choices without changing progress", () => {
  const root = completeMercy(finish());
  for (let choice = 0; choice < 3; choice++) {
    let w = root;
    for (const entry of ["stamps", "nisaba", "neti"])
      w = transition(w, { type: "study", entry });
    w = transition(travel(w, "yesod"), {
      type: "inquiry",
      task: "testimony",
      choice: 0,
    });
    w = transition(travel(w, "hod"), {
      type: "inquiry",
      task: "tablet",
      choice,
    });
    const before = JSON.stringify(w);
    assert.equal(worldDetail(activeSeeker(w)!)!.variant, choice);
    assert.match(worldVignette(activeSeeker(w)!), /role="img" aria-label=/);
    assert.equal(JSON.stringify(w), before);
    w = transition(travel(w, "netzach"), {
      type: "inquiry",
      task: "gate",
      choice,
    });
    assert.equal(worldDetail(activeSeeker(w)!)!.variant, choice);
    assert.deepEqual(parseWorld(JSON.stringify(w)), w);
    // Use the released fixture's legitimately completed Chapter II prerequisites.
    const festival = parseWorld(
      readFileSync(
        new URL("./fixtures/living-v5.json", import.meta.url),
        "utf8",
      ),
    );
    activeSeeker(festival)!.festival = null;
    const ended = transition(festival, { type: "festival", choice });
    assert.equal(worldDetail(activeSeeker(ended)!)!.variant, choice);
    assert.deepEqual(parseWorld(JSON.stringify(ended)), ended);
  }
});

test("a followed encounter has one legal route, clears temporary darkness and leads to its prerequisites", () => {
  let w = readyToBoard();
  let s = activeSeeker(w)!;
  assert.equal(nextStep(w, s, "tiferet", "hod").target, "hod");
  const action = nextStep(w, s, "tiferet", "hod").action!;
  assert.equal(action.type, "walk");
  if (action.type !== "walk") throw new Error("expected crossing");
  w.darkness[pathKey(s.current, action.to)] = w.clock + 2;
  assert.equal(nextStep(w, s, "tiferet", "hod").action!.type, "sit");
  w = transition(w, { type: "sit" });
  assert.equal(
    nextStep(w, activeSeeker(w)!, "tiferet", "hod").action!.type,
    "walk",
  );
  w = travel(w, "hod");
  assert.equal(
    nextStep(w, activeSeeker(w)!, "tiferet", "hod").panel,
    "inquiry",
  );
  let fresh = travel(newGame(), "hod");
  assert.equal(
    nextStep(fresh, activeSeeker(fresh)!, null, "hod").action!.type,
    "look",
  );
  fresh = transition(fresh, { type: "look" });
  assert.equal(
    nextStep(fresh, activeSeeker(fresh)!, null, "hod").panel,
    "rite",
  );
  assert.equal(
    nextStep(readyToBoard(), activeSeeker(readyToBoard())!).panel,
    "story",
  );
});

test("browser tools validate boarding before commit and share the visible encounter priority", async () => {
  let w = readyToBoard();
  const registered = new Map<string, JourneyTool>();
  const dispose = registerJourneyTools(
    {
      registerTool: (t) => {
        registered.set(t.name, t);
      },
    },
    () => w,
    async (action) => {
      w = transition(w, action);
    },
    undefined,
    (world, seeker) => nextStep(world, seeker, "tiferet", "hod"),
  );
  try {
    const state = registered
      .get("get_journey_state")!
      .execute({}) as ReturnType<typeof journeySnapshot>;
    assert.equal(state.next?.target, "hod");
    assert.equal(state.boarding?.novicesFirst, true);
    assert.equal(state.boarding?.canDelegate, true);
    const action = registered.get("take_journey_action")!;
    const before = JSON.stringify(w);
    for (const boarding of [
      { ...suggestedBoarding(), extra: 0 },
      { novices: 1, apprentice: 1, cook: 0, drummer: 0 },
    ]) {
      await assert.rejects(
        Promise.resolve().then(() =>
          action.execute({
            action: "story-deliver",
            story: "tiferet",
            seekerId: w.activeId,
            revision: w.revision,
            boarding,
          }),
        ),
      );
      assert.equal(JSON.stringify(w), before);
    }
    await action.execute({
      action: "story-deliver",
      story: "tiferet",
      seekerId: w.activeId,
      revision: w.revision,
      boarding: suggestedBoarding(),
    });
    assert.equal(activeSeeker(w)!.stories.tiferet!.delivered, true);
    assert.equal(journeySnapshot(w).boarding, null);
  } finally {
    dispose();
  }
});
