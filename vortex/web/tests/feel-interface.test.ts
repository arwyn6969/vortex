import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { pathBetween } from "../paths.ts";
import { newGame } from "./helpers.ts";

test("travel feedback appears in the same turn, animates once and never leaks into another seeker", async () => {
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<div id="app"></div><div id="journey-announcement"></div>';
  const w = newGame(),
    second = structuredClone(w.seekers[0]);
  second.id = "quiet-frog";
  second.name = "Quiet Frog";
  w.seekers.push(second);
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(w));
  Object.defineProperty(window.navigator, "locks", {
    value: { request: async (_: string, work: () => unknown) => work() },
  });
  let audioContexts = 0;
  Object.defineProperty(window, "AudioContext", {
    value: class {
      constructor() {
        audioContexts++;
        throw new Error("unexpected audio");
      }
    },
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
    for (let i = 0; i < 8; i++)
      await new Promise((resolve) => setImmediate(resolve));
  };
  const click = async (selector: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    assert(!el.disabled, selector);
    el.dispatchEvent(
      new window.MouseEvent("click", { bubbles: true, cancelable: true }),
    );
    await settle();
  };
  try {
    await import("../bootstrap.ts");
    await settle();
    assert.equal(window.document.querySelectorAll(".stream-letter").length, 0);
    await click('[data-act="look"]');
    assert(window.document.querySelector(".felt-look"));
    await click('[data-go="hod"]');
    assert.equal(
      window.document.querySelector(".stream-letter")?.textContent,
      pathBetween("tiferet", "hod")!.letter,
    );
    assert.equal(
      window.document.querySelectorAll(".stream.just-crossed").length,
      1,
    );
    assert(window.document.querySelector(".felt-reveal"));
    assert.equal(window.document.activeElement?.id, "location-title");
    await click('[data-modal="help"]');
    assert(
      !window.document.querySelector(".felt-reveal"),
      "dialogs do not replay feedback",
    );
    await click("[data-close]");
    await click('[data-go="yesod"]');
    assert.equal(
      window.document.querySelector(".stream-letter")?.textContent,
      pathBetween("hod", "yesod")!.letter,
    );
    await click('[data-act="sit"]');
    assert(window.document.querySelector(".felt-sit"));
    await click('[data-modal="journeys"]');
    await click('[data-switch="quiet-frog"]');
    assert.equal(
      window.document.querySelectorAll(".stream-letter,.just-crossed").length,
      0,
    );
    assert.equal(
      window.document.querySelectorAll('[class*="felt-"]').length,
      0,
    );
    const saved = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
    assert.deepEqual(saved.seekers[1].crossings, {});
    assert(saved.seekers[0].crossings[pathBetween("hod", "yesod")!.id]);
    assert.equal(
      audioContexts,
      0,
      "ordinary play is silent until explicitly enabled",
    );
  } finally {
    await window.happyDOM.close();
  }
});
