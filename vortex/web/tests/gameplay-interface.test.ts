import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { activeSeeker, transition } from "../session.ts";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { finish, travel } from "./helpers.ts";

test("boarding drafts, cooperative help, route selection and Atlas bookmarks stay in the right journey", async () => {
  let w = travel(finish(), "chesed");
  w = transition(w, { type: "story-start", story: "chesed", choice: 0 });
  w = transition(travel(w, "gevurah"), {
    type: "story-deliver",
    story: "chesed",
  });
  w = transition(travel(w, "chesed"), {
    type: "story-resolve",
    story: "chesed",
    choice: 1,
  });
  w = transition(travel(w, "tiferet"), {
    type: "story-start",
    story: "tiferet",
    choice: 0,
  });
  w = travel(w, "netzach");
  const second = structuredClone(activeSeeker(w)!);
  second.id = "another-boarder";
  second.name = "Another boarder";
  w.seekers.push(second);
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<div id="app"></div><div id="journey-announcement"></div>';
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(w));
  Object.defineProperty(window.navigator, "locks", {
    value: { request: async (_: string, work: () => unknown) => work() },
  });
  for (const key of [
    "window",
    "document",
    "navigator",
    "localStorage",
    "FormData",
    "MouseEvent",
    "HTMLElement",
    "HTMLInputElement",
  ])
    Object.defineProperty(globalThis, key, {
      configurable: true,
      writable: true,
      value: key === "window" ? window : (window as any)[key],
    });
  const settle = async () => {
    for (let i = 0; i < 8; i++) await new Promise((r) => setImmediate(r));
  };
  const click = async (selector: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    assert(!el.disabled, selector);
    el.click();
    await settle();
  };
  const saved = () => window.localStorage.getItem(SAVE_KEY)!;
  try {
    await import("../bootstrap.ts");
    await settle();
    const before = saved();
    for (const id of ["novices", "apprentice", "cook", "drummer"])
      await click(`#boarding-${id}-0`);
    await click('#boarding-form button[type="submit"]');
    assert.match(
      window.document.querySelector(".toast.error")!.textContent,
      /boat holds three/,
    );
    assert.equal(saved(), before);
    await click("[data-boarding-help]");
    assert.equal(window.document.activeElement?.id, "boarding-title");
    assert.equal(saved(), before, "asking for help is not a reward");
    await click('[data-view="atlas"]');
    await click('[data-cluster="return"]');
    await click('[data-atlas-connections="return"]');
    const detail = window.document.querySelector(
      ".atlas-connections details",
    ) as any;
    detail.open = true;
    const detailId = detail.id;
    window.scrollTo({ top: 617 });
    await click('[data-view="tree"]');
    assert.equal(
      window.document.querySelectorAll("#boarding-form input:checked").length,
      4,
    );
    await click('[data-view="atlas"]');
    assert.equal(window.scrollY, 617);
    assert((window.document.getElementById(detailId) as any).open);
    await click('[data-atlas-route="hod"]');
    assert.equal(window.document.querySelectorAll("[data-next]").length, 1);
    assert.match(
      window.document.querySelector(".journey-compass")!.textContent,
      /Following Meme Studio/,
    );
    await click('[data-view="stories"]');
    await click('[data-track="tiferet"]');
    assert.equal(window.document.querySelectorAll("[data-next]").length, 1);
    assert(!window.document.querySelector(".journey-compass.atlas-route"));
    await click('[data-modal="journeys"]');
    await click(`[data-switch="${second.id}"]`);
    assert.equal(
      window.document.querySelectorAll("#boarding-form input:checked").length,
      0,
    );
    await click("[data-boarding-help]");
    await click("[data-boarding-reset]");
    assert.equal(
      window.document.querySelectorAll("#boarding-form input:checked").length,
      0,
    );
    await click("[data-boarding-help]");
    await click('#boarding-form button[type="submit"]');
    const world = parseWorld(saved());
    assert.equal(activeSeeker(world)!.stories.tiferet!.delivered, true);
    assert.equal(world.seekers[0].stories.tiferet!.delivered, false);
    assert(!window.document.querySelector("#boarding-form"));
    assert.equal(
      window.document
        .querySelector('[data-world-detail="gate"]')!
        .getAttribute("data-variant"),
      "-1",
    );
    const ids = [...window.document.querySelectorAll("[id]")].map(
      (el) => el.id,
    );
    assert.equal(new Set(ids).size, ids.length);
  } finally {
    await window.happyDOM.close();
  }
});
