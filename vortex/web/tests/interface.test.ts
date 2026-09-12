import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { SAVE_KEY, parseWorld } from "../storage.ts";
import { activeSeeker } from "../session.ts";

test("interface supports first and second seekers, rites, journal, switching and reloadable saves", async () => {
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML = '<div id="app"></div>';
  for (const key of [
    "window",
    "document",
    "navigator",
    "localStorage",
    "FormData",
    "MouseEvent",
    "HTMLElement",
    "HTMLInputElement",
  ]) {
    Object.defineProperty(globalThis, key, {
      configurable: true,
      writable: true,
      value: key === "window" ? window : (window as any)[key],
    });
  }
  await import("../main.ts");
  const settle = async () => {
    for (let i = 0; i < 8; i++)
      await new Promise((resolve) => setImmediate(resolve));
  };
  const click = async (selector: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    el.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
    await settle();
  };
  const submit = async (selector: string) => {
    const form = window.document.querySelector(selector)!;
    assert(form, selector);
    form.dispatchEvent(
      new window.Event("submit", { bubbles: true, cancelable: true }),
    );
    await settle();
  };
  const enter = async (name: string) => {
    (window.document.querySelector("#seeker-name") as any).value = name;
    await submit("#gate-form");
    for (let n = 0; n < 6; n++) await click('[data-answer="2"]');
    assert(window.document.querySelector("#location-title"));
  };
  await settle();
  await enter("First Frog");
  await click('[data-act="look"]');
  await click("[data-show-rite]");
  await click('[data-rite="1"]');
  assert(window.document.querySelector(".moment"));
  await click('[data-view="journal"]');
  assert.match(window.document.body.textContent, /First Frog/);
  await click('[data-modal="journeys"]');
  await click("[data-new]");
  await enter("Second Frog");
  let saved = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
  assert.equal(saved.seekers.length, 2);
  assert.equal(activeSeeker(saved)!.name, "Second Frog");
  assert.equal(Object.keys(activeSeeker(saved)!.rites).length, 0);
  await click('[data-modal="journeys"]');
  await click('[data-switch="' + saved.seekers[0].id + '"]');
  saved = parseWorld(window.localStorage.getItem(SAVE_KEY)!);
  assert.equal(activeSeeker(saved)!.name, "First Frog");
  assert.equal(Object.keys(activeSeeker(saved)!.rites).length, 1);
  await click('[data-go="hod"]');
  assert.match(
    window.document.querySelector("#location-title")!.textContent,
    /Meme/,
  );
  await window.happyDOM.close();
});
