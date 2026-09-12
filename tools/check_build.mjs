import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import vm from "node:vm";

// Exercise the generated offline worker without an agent browser.
const source = readFileSync("dist/sw.js", "utf8");
const handlers = {},
  cachesByName = new Map();
let networkCalls = 0;
const caches = {
  keys: async () => [...cachesByName.keys()],
  delete: async (key) => cachesByName.delete(key),
  open: async (key) => {
    if (!cachesByName.has(key)) cachesByName.set(key, new Map());
    const cache = cachesByName.get(key);
    return {
      addAll: async (urls) => {
        assert.equal(new Set(urls).size, urls.length, "Duplicate offline URLs");
        for (const url of urls) {
          assert(existsSync("dist" + (url === "/" ? "/index.html" : url)), url);
          cache.set(url, { cached: url });
        }
      },
      match: async (url) => cache.get(url),
    };
  },
};
vm.runInNewContext(source, {
  URL,
  Promise,
  caches,
  self: {
    location: { origin: "https://game.example" },
    addEventListener: (type, fn) => (handlers[type] = fn),
  },
  fetch: async () => {
    networkCalls++;
    throw new Error("offline");
  },
});
let pending;
handlers.install({ waitUntil: (promise) => (pending = promise) });
await pending;
assert(cachesByName.size === 1);
const cache = [...cachesByName.values()][0];
for (const path of [
  "/",
  "/index.html",
  "/nile-world.jpg",
  "/nile-guides.jpg",
  "/rarepepe/THOTHPEPE.jpg",
]) {
  let result;
  handlers.fetch({
    request: { method: "GET", url: "https://game.example" + path },
    respondWith: (promise) => (result = promise),
  });
  assert.deepEqual(await result, { cached: path });
}
for (const request of [
  { method: "POST", url: "https://game.example/" },
  { method: "GET", url: "https://api.counterparty.io:4000/v2/" },
  { method: "GET", url: "https://game.example/unknown" },
])
  handlers.fetch({
    request,
    respondWith: () => assert.fail("Unexpected interception"),
  });
cachesByName.set("unrelated-cache", new Map());
cachesByName.set("vortex-obsolete", new Map());
handlers.activate({ waitUntil: (promise) => (pending = promise) });
await pending;
assert(cachesByName.has("unrelated-cache"));
assert(!cachesByName.has("vortex-obsolete"));
assert.equal(networkCalls, 0);
console.log(
  "Offline worker checked: " +
    cache.size +
    " existing files, cached navigation/art, safe request boundary, old-cache cleanup.",
);
