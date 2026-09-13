import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { mount } from "../main.ts";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { newGame } from "./helpers.ts";
import type { JourneyTool } from "../webmcp.ts";

test("the mount module can be imported without a browser during server rendering", () => {
  assert.equal(typeof globalThis.document, "undefined");
  assert.equal(typeof globalThis.window, "undefined");
  assert.equal(typeof mount, "function");
});

test("mount, immediate unmount and remount leave one game, one set of listeners and no stale tools", async () => {
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<dialog id="host-dialog">Host controls</dialog><div id="app"></div>';
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(newGame()));
  let holdLock = false;
  let releaseLock = () => {};
  Object.defineProperty(window.navigator, "locks", {
    value: {
      request: async (_: string, work: () => unknown) => {
        if (!holdLock) return work();
        return new Promise((resolve, reject) => {
          releaseLock = () =>
            Promise.resolve().then(work).then(resolve, reject);
        });
      },
    },
  });
  const tools: Array<{ tool: JourneyTool; signal: AbortSignal }> = [];
  Object.defineProperty(window.document, "modelContext", {
    value: {
      registerTool: (
        tool: JourneyTool,
        { signal }: { signal: AbortSignal },
      ) => {
        tools.push({ tool, signal });
      },
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
  const root = window.document.querySelector("#app")!;
  let close = () => {};
  try {
    const first = mount(root as any);
    const firstTools = tools.slice();
    first(); // Simulates a strict development host disposing before async load settles.
    await settle();
    assert.equal(root.childElementCount, 0);
    assert.equal(window.document.querySelector("#journey-announcement"), null);
    assert(firstTools.every((t) => t.signal.aborted));
    assert.throws(
      () =>
        firstTools
          .find((t) => t.tool.name === "get_journey_state")!
          .tool.execute({}),
      /not ready/,
    );
    close = mount(root as any);
    await settle();
    assert.equal(root.querySelectorAll("#main").length, 1);
    assert.equal(
      window.document.querySelectorAll("#journey-announcement").length,
      1,
    );
    assert(
      !(window.document.querySelector("#host-dialog") as any).open,
      "the game does not control its host's dialog",
    );
    const before = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
    (root.querySelector('[data-act="look"]') as any).click();
    await settle();
    const after = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
    assert.equal(after.revision, before.revision + 1);
    assert.equal(after.seekers[0].turns, before.seekers[0].turns + 1);
    const saved = window.localStorage.getItem(SAVE_KEY);
    const oldButton = root.querySelector('[data-act="sit"]')!;
    close();
    (oldButton as any).click();
    await settle();
    assert.equal(window.localStorage.getItem(SAVE_KEY), saved);
    assert.equal(root.childElementCount, 0);
    assert(tools.every((t) => t.signal.aborted));
    assert(window.document.querySelector("#host-dialog"));
    close = mount(root as any);
    await settle();
    holdLock = true;
    (root.querySelector('[data-act="look"]') as any).click();
    await settle();
    close();
    releaseLock();
    await settle();
    assert.equal(
      window.localStorage.getItem(SAVE_KEY),
      saved,
      "an action queued behind another tab's lock is cancelled on unmount",
    );
  } finally {
    close();
    await window.happyDOM.close();
  }
});
