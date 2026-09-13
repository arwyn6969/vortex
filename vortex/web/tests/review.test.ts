import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { ATLAS, RELATIONS } from "../atlas.ts";
import { atlasView, emptyAtlasView } from "../atlas-view.ts";
import { chapterProgress, templeScene } from "../journey-view.ts";
import { activeSeeker, transition } from "../session.ts";
import { finish, newGame, travel } from "./helpers.ts";

test("atlas detail belongs to the result set and empty searches/notebooks have no unrelated entry", () => {
  const s = activeSeeker(newGame())!;
  const state = emptyAtlasView();
  for (const filters of [{ query: "no-such-frog-xyz" }, { notebook: true }]) {
    const html = atlasView(s, { ...state, ...filters });
    assert(!html.includes('class="atlas-detail"'));
    assert(!html.includes('class="atlas-connections"'));
    assert(html.includes("No matching entries"));
  }
  const html = atlasView(s, { ...state, query: "Nidaba" });
  assert(html.includes('id="entry-nisaba"'));
  assert(!html.includes('id="entry-memory"'));
});

test("every published atlas relationship has an accessible explanation, including the overflow", () => {
  const s = activeSeeker(newGame())!;
  for (const entry of ATLAS) {
    const links = RELATIONS.filter(
      (r) => r.from === entry.id || r.to === entry.id,
    );
    const state = { ...emptyAtlasView(), selected: entry.id };
    const collapsed = atlasView(s, state);
    if (links.length > 12)
      assert(collapsed.includes(`Show all ${links.length} connections`));
    const full = atlasView(s, { ...state, expandedConnections: entry.id });
    for (const link of links)
      assert(full.includes(`id="atlas-relation-${link.id}"`), link.id);
  }
  const pairs = RELATIONS.map((r) => [r.from, r.to].sort().join("/"));
  assert.equal(
    new Set(pairs).size,
    pairs.length,
    "duplicate relationship pairs",
  );
});

test("scene choices and chapter requirements reflect actual progress without awarding it", () => {
  let w = newGame();
  const before = JSON.stringify(w);
  assert(chapterProgress(activeSeeker(w)!).includes("Sigil made"));
  assert(!templeScene(activeSeeker(w)!).includes('class="scene-token"'));
  assert.equal(JSON.stringify(w), before);
  w = transition(w, { type: "look" });
  assert(templeScene(activeSeeker(w)!).includes('class="scene-token"'));
  w = transition(w, { type: "rite", choice: 2 });
  assert(templeScene(activeSeeker(w)!).includes("Make two safe trips"));
  const rooted = activeSeeker(finish())!;
  assert(chapterProgress(rooted).includes("Stories home"));
  assert(!chapterProgress(rooted).includes("Sigil made"));
});

test("interface isolates seekers, preserves onboarding drafts, focuses choices and avoids repeated aftermath", async () => {
  const { SAVE_KEY, parseWorld } = await import("../storage.ts");
  const { voice } = await import("../session.ts");
  const { TABLET_MEMORIES } = await import("../inquiries.ts");
  const window = new Window({ url: "http://localhost:5173" });
  window.document.body.innerHTML =
    '<div id="app"></div><div id="journey-announcement"></div>';
  let w = travel(finish(), "hod");
  for (let i = 0; i < 90; i++) w = transition(w, { type: "sit" });
  const first = activeSeeker(w)!;
  first.name = "First reviewer";
  const second = structuredClone(first);
  second.id = "second-reviewer";
  second.name = "Second reviewer";
  second.sigil = "A mark belonging to the second frog";
  second.inquiries.seen = ["nisaba", "stamps"];
  w.seekers.push(second);
  window.localStorage.setItem(SAVE_KEY, JSON.stringify(w));
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
  const fill = (selector: string, value: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    el.value = value;
    el.dispatchEvent(new window.Event("input", { bubbles: true }));
  };
  const submit = async (selector: string) => {
    window.document
      .querySelector(selector)!
      .dispatchEvent(
        new window.Event("submit", { bubbles: true, cancelable: true }),
      );
    await settle();
  };
  try {
    await import("../main.ts");
    await settle();
    assert.equal(
      window.document.querySelector(".guide-quote p")!.textContent,
      voice(first),
    );
    fill("#sigil", "Unsubmitted words from the first frog");
    fill("#question", "A question belonging to the first frog");
    await click('[data-view="atlas"]');
    await click('[data-atlas-route="netzach"]');
    assert(window.document.querySelector(".atlas-route"));
    await click('[data-modal="journeys"]');
    await click(`[data-switch="${second.id}"]`);
    assert.equal(
      (window.document.querySelector("#sigil") as any).value,
      second.sigil,
    );
    assert.equal((window.document.querySelector("#question") as any).value, "");
    assert(!window.document.querySelector(".atlas-route"));
    assert(
      activeSeeker(parseWorld(window.localStorage.getItem(SAVE_KEY)!))!.rooted,
    );
    (window.document.querySelector("#inquiry-panel") as any).open = true;
    await click('[data-inquiry="tablet"][data-choice="0"]');
    assert.equal(
      window.document.querySelector(".return-memory p")!.textContent,
      TABLET_MEMORIES[0],
    );
    assert(
      !window.document
        .querySelector(".moment")
        ?.textContent.includes(TABLET_MEMORIES[0]),
    );
    assert(
      !window.document
        .querySelector("#inquiry-panel")!
        .textContent.includes(TABLET_MEMORIES[0]),
    );
    await click('[data-view="atlas"]');
    await click('[data-cluster="return"]');
    await click('[data-atlas-connections="return"]');
    assert.equal(
      window.document.querySelectorAll(".atlas-connections details").length,
      19,
    );
    fill("#atlas-query", "no-such-frog-xyz");
    await submit("#atlas-search");
    assert(!window.document.querySelector(".atlas-detail"));
    await click('[data-view="tree"]');
    await click('[data-modal="journeys"]');
    await click("[data-new]");
    fill("#seeker-name", "Third reviewer");
    const radio = window.document.querySelector(
      '[name="dialect"][value="classical"]',
    ) as any;
    radio.checked = true;
    radio.dispatchEvent(new window.Event("change", { bubbles: true }));
    await click('[data-modal="help"]');
    await click("[data-close]");
    assert.equal(
      (window.document.querySelector("#seeker-name") as any).value,
      "Third reviewer",
    );
    assert(
      (
        window.document.querySelector(
          '[name="dialect"][value="classical"]',
        ) as any
      ).checked,
    );
    await submit("#gate-form");
    assert.equal(window.document.activeElement?.id, "quiz-question");
    for (let i = 0; i < 6; i++) await click('[data-answer="2"]');
    assert(
      [...window.document.querySelectorAll(".exit-letter")].every(
        (el) => el.textContent === "—",
      ),
    );
    await click('[data-act="look"]');
    await click("[data-show-rite]");
    assert.equal(window.document.activeElement?.id, "rite-area");
    assert(
      window.document
        .querySelector("#rite-area")!
        .compareDocumentPosition(
          window.document.querySelector(".story-card")!,
        ) & 4,
    );
    await click('[data-rite="2"]');
    assert(
      window.document
        .querySelector(".scene-inscription")!
        .textContent.includes("Make two safe trips"),
    );
  } finally {
    await window.happyDOM.close();
  }
});
