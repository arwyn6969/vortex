import test from "node:test";
import assert from "node:assert/strict";
import { offlineCacheName } from "../../../tools/offline-cache.ts";

test("offline updates detect HTML-only edits, public-file renames and changed artwork", () => {
  const files = {
    "index.html": "<title>Old edition</title>",
    "assets/game.js": "game()",
    "art.jpg": new Uint8Array([1, 2]),
  };
  const original = offlineCacheName(files);
  assert.equal(
    original,
    offlineCacheName(Object.fromEntries(Object.entries(files).reverse())),
  );
  assert.notEqual(
    original,
    offlineCacheName({ ...files, "index.html": "<title>New edition</title>" }),
  );
  assert.notEqual(
    original,
    offlineCacheName({ ...files, "art.jpg": new Uint8Array([1, 3]) }),
  );
  const renamed = { ...files, "new-art.jpg": files["art.jpg"] };
  delete (renamed as Partial<typeof files>)["art.jpg"];
  assert.notEqual(original, offlineCacheName(renamed));
});
