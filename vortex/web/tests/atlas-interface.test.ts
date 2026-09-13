import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { finish, travel } from "./helpers.ts";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { activeSeeker } from "../session.ts";

test("atlas search, comparison, remembered sources and tablet resolution use the actual interface", async () => {
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<div id="app"></div><div id="journey-announcement" role="status"></div>';
  window.localStorage.setItem(
    SAVE_KEY,
    JSON.stringify(travel(finish(), "hod")),
  );
  Object.defineProperty(window.navigator, "locks", {
    value: { request: async (_name: string, work: () => unknown) => work() },
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
  await import("../bootstrap.ts");
  const settle = async () => {
    for (let i = 0; i < 8; i++) await new Promise((r) => setImmediate(r));
  };
  const click = async (selector: string) => {
    const button = window.document.querySelector(selector) as any;
    assert(button, selector);
    assert(!button.disabled, selector);
    button.click();
    await settle();
  };
  await settle();
  for (const id of ["nisaba", "stamps"]) {
    await click(`[data-atlas-entry="${id}"]`);
    await click(`[data-study="${id}"]`);
    assert.equal(window.document.activeElement?.id, "entry-" + id);
    await click(`[data-compare="${id}"]`);
    await click('[data-view="tree"]');
  }
  await click('[data-inquiry="tablet"][data-choice="0"]');
  const saved = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
  assert.equal(activeSeeker(saved)!.inquiries.tablet, 0);
  await click('[data-view="atlas"]');
  assert.match(
    window.document.querySelector(".atlas-comparison")!.textContent,
    /Shared exploration theme/,
  );
  (window.document.getElementById("atlas-query") as any).value = "Nidaba";
  window.document
    .getElementById("atlas-search")!
    .dispatchEvent(
      new window.Event("submit", { bubbles: true, cancelable: true }),
    );
  await settle();
  assert.equal(
    window.document.querySelectorAll(".atlas-index button").length,
    1,
  );
  assert.match(
    window.document.querySelector(".atlas-detail h2")!.textContent,
    /Nisaba/,
  );
  await click('[data-modal="journeys"]');
  assert(window.document.querySelector("[data-restore-backup]"));
  await window.happyDOM.close();
});
