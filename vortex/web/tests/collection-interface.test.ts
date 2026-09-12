import test from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { SAVE_KEY } from "../storage.ts";
import { finish } from "./helpers.ts";
const ADDRESS = "1GQhaWqejcGJ4GhQar7SjcCfadxvf5DNBD";
test("Kingdom lookup is opt-in, never changes the save, links to real characters, and clears on close", async () => {
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
  ])
    Object.defineProperty(globalThis, key, {
      configurable: true,
      writable: true,
      value: key === "window" ? window : (window as any)[key],
    });
  const original = JSON.stringify(finish());
  window.localStorage.setItem(SAVE_KEY, original);
  let requests = 0,
    offline = false;
  const oldFetch = globalThis.fetch;
  globalThis.fetch = (async (url: unknown) => {
    requests++;
    if (offline) throw new Error("offline");
    const body = String(url).includes("/balances?")
      ? {
          result: [
            {
              address: ADDRESS,
              utxo: null,
              utxo_address: null,
              asset: "THOTHPEPE",
              quantity: 1,
              asset_info: { divisible: false },
            },
            {
              address: ADDRESS,
              utxo: null,
              utxo_address: null,
              asset: "A95428956661682277",
              quantity: 700,
              asset_info: {
                divisible: false,
                asset_longname: "PARENT.MixedCase",
              },
            },
          ],
          next_cursor: null,
          result_count: 2,
        }
      : {
          result: {
            server_ready: true,
            network: "mainnet",
            ledger_state: "Following",
            counterparty_height: 900000,
            backend_height: 900000,
          },
        };
    return new Response(JSON.stringify(body), {
      headers: { "content-type": "application/json" },
    });
  }) as typeof fetch;
  const settle = async () => {
    for (let i = 0; i < 12; i++)
      await new Promise((resolve) => setImmediate(resolve));
  };
  const click = async (selector: string) => {
    const el = window.document.querySelector(selector) as any;
    assert(el, selector);
    el.focus();
    el.click();
    await settle();
  };
  const address = () =>
    window.document.querySelector("#collection-address") as any;
  const submit = async () => {
    window.document
      .querySelector("#collection-form")!
      .dispatchEvent(
        new window.Event("submit", { bubbles: true, cancelable: true }),
      );
    await settle();
  };
  try {
    await import("../main.ts");
    await settle();
    await click('[data-modal="collection"]');
    assert.equal(requests, 0);
    address().value = ADDRESS;
    address().dispatchEvent(new window.Event("input", { bubbles: true }));
    assert.equal(requests, 0);
    await submit();
    for (
      let i = 0;
      i < 100 && !window.document.querySelector(".collection-snapshot");
      i++
    )
      await settle();
    assert.equal(requests, 3);
    assert(window.document.querySelector(".collection-snapshot"));
    assert.equal(window.document.querySelectorAll(".holding-row").length, 2);
    assert(
      window.document.querySelector(
        'a[href="https://xcp.io/asset/PARENT.MixedCase"]',
      ),
    );
    const search = window.document.querySelector("#collection-search") as any;
    search.focus();
    search.value = "mixedcase";
    search.dispatchEvent(new window.Event("input", { bubbles: true }));
    assert.equal(window.document.querySelectorAll(".holding-row").length, 1);
    assert.equal(window.document.activeElement?.id, "collection-search");
    assert.match(
      window.document.querySelector(".holding-row")!.textContent,
      /PARENT.MixedCase/,
    );
    await click('[data-collection-filter="world"]');
    assert.match(
      window.document.querySelector(".collection-empty")!.textContent,
      /No assets in this view match/,
    );
    const resetSearch = window.document.querySelector(
      "#collection-search",
    ) as any;
    resetSearch.value = "";
    resetSearch.dispatchEvent(new window.Event("input", { bubbles: true }));
    assert.equal(window.document.querySelectorAll(".holding-row").length, 1);
    assert.equal(requests, 3);
    assert.equal(window.localStorage.getItem(SAVE_KEY), original);
    await click('[data-track="chokhmah"]');
    assert(!window.document.querySelector("dialog"));
    assert.match(
      window.document.querySelector(".journey-compass")!.textContent,
      /THOTHPEPE/,
    );
    assert.equal(window.localStorage.getItem(SAVE_KEY), original);
    await click('[data-modal="collection"]');
    assert.equal(address().value, "");
    assert(!window.document.querySelector(".collection-snapshot"));
    address().value = "abandon ".repeat(11) + "about";
    await submit();
    assert.equal(requests, 3);
    assert.match(
      window.document.querySelector(".collection-error")!.textContent,
      /public Bitcoin address/,
    );
    address().value = ADDRESS;
    offline = true;
    await submit();
    for (
      let i = 0;
      i < 200 && !window.document.querySelector(".collection-error");
      i++
    )
      await new Promise((resolve) => setTimeout(resolve, 1));
    assert.match(
      window.document.querySelector(".collection-error")!.textContent,
      /connection|Counterparty/,
    );
    assert(!window.document.querySelector(".collection-empty"));
    await click("[data-close]");
    await click('[data-modal="collection"]');
    assert.equal(address().value, "");
    await click("[data-close]");
    await click('[data-modal="stamps"]');
    assert.match(
      window.document.querySelector(".stamp-teaching")!.textContent,
      /KEVIN is still here/,
    );
    await click('[data-stamp-office="yesod"]');
    assert.match(
      window.document.querySelector(".stamp-teaching")!.textContent,
      /data-bearing output is spent/,
    );
    assert.equal(
      (window.document.activeElement as any)?.dataset.stampOffice,
      "yesod",
    );
    await click("[data-close]");
    await click('[data-view="rares"]');
    assert.match(
      window.document.querySelector("h1")!.textContent,
      /Counterparty archive/,
    );
    const assetName = window.document.querySelector("#asset-name") as any;
    assetName.value = "PARENT.MixedCase";
    assetName.dispatchEvent(new window.Event("input", { bubbles: true }));
    assert(
      window.document.querySelector(
        '#asset-destination a[href="https://xcp.io/asset/PARENT.MixedCase"]',
      ),
    );
    assetName.value = "https://evil.example";
    assetName.dispatchEvent(new window.Event("input", { bubbles: true }));
    assert(!window.document.querySelector("#asset-destination a"));
    assert.equal(requests, 4);
    assert.equal(window.localStorage.getItem(SAVE_KEY), original);
  } finally {
    globalThis.fetch = oldFetch;
    await window.happyDOM.close();
  }
});
