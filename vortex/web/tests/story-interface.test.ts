import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import type { HTMLButtonElement as HappyButton } from "happy-dom";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { activeSeeker } from "../session.ts";
import { STORIES, completedStories } from "../stories.ts";
import type { JourneyTool } from "../webmcp.ts";
import { finish } from "./helpers.ts";

test("the interface follows a selected story, delivers it, remembers its outcome, and completes the festival", async () => {
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<div id="app"></div><div id="journey-announcement" role="status"></div>';
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
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(finish()));
  const registered = new Map<string, JourneyTool>();
  Object.defineProperty(window.document, "modelContext", {
    value: {
      registerTool: (tool: JourneyTool) => registered.set(tool.name, tool),
    },
  });
  // Happy DOM has no Web Locks; emulate the supported browser contract here.
  Object.defineProperty(window.navigator, "locks", {
    configurable: true,
    value: { request: async (_name: string, work: () => unknown) => work() },
  });
  await import("../bootstrap.ts");
  const settle = async () => {
    for (let i = 0; i < 8; i++)
      await new Promise((resolve) => setImmediate(resolve));
  };
  const click = async (selector: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    assert(!el.disabled, selector + " is disabled");
    el.focus();
    el.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
    await settle();
  };
  const seeker = () =>
    activeSeeker(parseWorld(window.localStorage.getItem(SAVE_KEY)!))!;
  await settle();
  assert(window.document.querySelector(".festival-card"));
  await click('[data-modal="help"]');
  await click("[data-close]");
  assert.equal((window.document.activeElement as any)?.dataset.modal, "help");
  await click('[data-view="stories"]');
  assert.equal(window.document.querySelectorAll(".story-ledger").length, 10);
  await click('[data-track="chokhmah"]');
  for (let i = 0; i < 10 && seeker().current !== "chokhmah"; i++)
    await click("[data-next]");
  assert.equal(seeker().current, "chokhmah");
  await click("[data-next]");
  assert((window.document.querySelector("#story-chokhmah") as any).open);
  await click('[data-story-start="chokhmah"][data-choice="2"]');
  for (let i = 0; i < 10 && seeker().current !== "hod"; i++)
    await click("[data-next]");
  await click('[data-deliver="chokhmah"]');
  assert.equal(seeker().stories.chokhmah?.delivered, true);
  assert.equal(window.document.activeElement?.id, "journey-compass");
  for (let i = 0; i < 10 && seeker().current !== "chokhmah"; i++)
    await click("[data-next]");
  await click('[data-resolve="chokhmah"][data-choice="1"]');
  assert.equal(seeker().stories.chokhmah?.resolution, 1);
  assert(
    window.document
      .getElementById("journey-announcement")!
      .textContent.includes(STORIES.chokhmah.aftermath[1]),
  );
  assert(
    window.document
      .querySelector(".return-memory")
      ?.textContent.includes(STORIES.chokhmah.aftermath[1]),
  );
  await click('[data-topic="What changed here?"]');
  assert(
    window.document
      .querySelector(".guide-quote")
      ?.textContent.includes(STORIES.chokhmah.aftermath[1]),
  );
  await click('[data-view="stories"]');
  await click('[data-track="chesed"]'); // replace the completed tracked story
  for (let i = 0; i < 140 && seeker().festival === null; i++) {
    const s = seeker();
    const localStart = window.document.querySelector<HappyButton>(
      `#story-${s.current}[open] [data-story-start]`,
    );
    const deliver = window.document.querySelector<HappyButton>(
      "[data-deliver]:not(:disabled)",
    );
    const resolve =
      window.document.querySelector<HappyButton>("[data-resolve]");
    const festival =
      window.document.querySelector<HappyButton>("[data-festival]");
    if (deliver)
      await click('[data-deliver="' + deliver.dataset.deliver + '"]');
    else if (resolve)
      await click(
        '[data-resolve="' + resolve.dataset.resolve + '"][data-choice="0"]',
      );
    else if (localStart)
      await click('[data-story-start="' + s.current + '"][data-choice="0"]');
    else if (festival && completedStories(s).length >= 3)
      await click('[data-festival="1"]');
    else await click("[data-next]");
  }
  assert.equal(seeker().festival, 1);
  assert.match(
    window.document.querySelector(".festival-card")!.textContent!,
    /river of lanterns/,
  );
  assert.equal(window.document.activeElement?.id, "festival");
  // This exercises the WebMCP integration contract in an emulated context;
  // it does not claim support in a real browser's implementation.
  assert.deepEqual(
    [...registered.keys()],
    ["read_atlas_entry", "get_journey_state", "take_journey_action"],
  );
  const read = registered.get("get_journey_state")!,
    action = registered.get("take_journey_action")!;
  assert.equal(read.annotations.readOnlyHint, true);
  assert.equal(action.annotations.readOnlyHint, false);
  const state = read.execute({}) as any;
  assert(!("journal" in state));
  assert(!("proof" in state));
  await action.execute({
    seekerId: state.seeker.id,
    revision: state.revision,
    action: "sit",
  });
  assert.equal((read.execute({}) as any).revision, state.revision + 1);
  const before = window.localStorage.getItem(SAVE_KEY);
  await assert.rejects(
    () =>
      action.execute({
        seekerId: state.seeker.id,
        revision: state.revision,
        action: "sit",
      }) as Promise<unknown>,
  );
  await assert.rejects(
    () =>
      action.execute({
        seekerId: state.seeker.id,
        revision: state.revision + 1,
        action: "wallet",
      }) as Promise<unknown>,
  );
  await assert.rejects(
    () =>
      action.execute({
        seekerId: state.seeker.id,
        revision: state.revision + 1,
        action: "rite",
        choice: -1,
      }) as Promise<unknown>,
  );
  assert.equal(window.localStorage.getItem(SAVE_KEY), before);
  await window.happyDOM.close();
});
