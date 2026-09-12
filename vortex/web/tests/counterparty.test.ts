import test from "node:test";
import assert from "node:assert/strict";
import {
  fetchCollection,
  formatHolding,
  parseExactJson,
  CollectionError,
  CollectionLookup,
  COUNTERPARTY_API,
  COLLECTION_LIMITS,
} from "../counterparty.ts";
import type { CollectionSnapshot } from "../counterparty.ts";
import { validateLookupAddress } from "../wallet.ts";
import { collectionBody } from "../collection-view.ts";
import { activeSeeker } from "../session.ts";
import { finish } from "./helpers.ts";
const ADDRESS = "1GQhaWqejcGJ4GhQar7SjcCfadxvf5DNBD",
  SECOND = "1DevGw4eJWtGZWNjQXagEVnP3XGXH4o6dT";
const health = (height = 900000, ready = true) => ({
  result: {
    server_ready: ready,
    network: "mainnet",
    ledger_state: "Following",
    counterparty_height: height,
    backend_height: height,
  },
});
const row = (
  asset = "THOTHPEPE",
  quantity: unknown = 1,
  divisible: unknown = false,
  utxo: string | null = null,
) => ({
  address: utxo ? null : ADDRESS,
  utxo,
  utxo_address: utxo ? ADDRESS : null,
  asset,
  asset_longname: null,
  quantity,
  asset_info: { divisible, asset_longname: null },
});
const page = (
  result: unknown[],
  next_cursor: unknown = null,
  result_count = result.length,
) => ({ result, next_cursor, result_count });
const response = (body: unknown, status = 200) =>
  new Response(typeof body === "string" ? body : JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
function scripted(...bodies: unknown[]): typeof fetch {
  return (async () => {
    assert(bodies.length, "unexpected request");
    return response(bodies.shift());
  }) as typeof fetch;
}
test("collection reads all cursor pages, adds attached outputs once, and preserves exact quantities above Number precision", async () => {
  const requests: { url: string; options: RequestInit }[] = [];
  const huge = "9007199254740993";
  const bodies = [
    health(),
    page([row("THOTHPEPE", 1)], 7, 3),
    JSON.stringify(
      page(
        [
          row("THOTHPEPE", 2, false, "a".repeat(64) + ":0"),
          row("LORDKEK", "UNSAFE", true),
        ],
        null,
        3,
      ),
    ).replace('"UNSAFE"', huge),
    health(),
  ];
  const fetcher = (async (url: unknown, options: RequestInit) => {
    requests.push({ url: String(url), options });
    return response(bodies.shift());
  }) as typeof fetch;
  const result = await fetchCollection(ADDRESS, { fetcher, now: () => 12345 });
  assert.equal(result.pages, 2);
  assert.equal(result.rows, 3);
  assert.equal(result.checkedAt, 12345);
  assert.deepEqual(
    result.holdings.find((h) => h.asset === "THOTHPEPE"),
    {
      asset: "THOTHPEPE",
      longname: null,
      raw: "3",
      divisible: false,
      addressRaw: "1",
      attachedRaw: "2",
      outputs: 1,
    },
  );
  assert.equal(
    formatHolding(result.holdings[0].raw, true),
    "90,071,992.54740993",
  );
  assert(requests[2].url.includes("cursor=7"));
  assert(requests[1].url.includes("type=all"));
  for (const request of requests) {
    assert(request.url.startsWith(COUNTERPARTY_API));
    assert.equal(request.options.credentials, "omit");
    assert.equal(request.options.referrerPolicy, "no-referrer");
    assert.equal(request.options.cache, "no-store");
    assert.equal(request.options.redirect, "error");
    assert.equal(request.options.method, "GET");
  }
  assert.equal(formatHolding("1", true), "0.00000001");
  assert.equal(formatHolding("100000000", true), "1");
  assert.equal(formatHolding("300", null), "300 raw units");
  assert.deepEqual(
    parseExactJson(
      '{"number":9007199254740993,"text":"9007199254740993 \\\"quoted\\\""}',
    ),
    { number: huge, text: '9007199254740993 "quoted"' },
  );
  assert.throws(() => parseExactJson("{9007199254740993:1}"));
});
test("missing metadata stays unscaled and untrusted labels are escaped without loading external art", async () => {
  const missing = {
    ...row("MISSING", 123),
    asset_info: null,
    asset_longname: "<img src=x onerror=alert(1)>",
  };
  const snapshot = await fetchCollection(ADDRESS, {
    fetcher: scripted(health(), page([missing]), health()),
  });
  assert.equal(snapshot.holdings[0].divisible, null);
  const markup = collectionBody(
    { status: "ready", snapshot, input: ADDRESS, error: "", rows: 1 },
    activeSeeker(finish())!,
    "all",
    50,
  );
  assert(markup.includes("123 raw units"));
  assert(markup.includes("&lt;img"));
  assert(!markup.includes("<img src=x"));
  assert(!markup.includes('href="javascript:'));
});
test("unready nodes, mixed pages, duplicates, foreign rows, invalid quantities and incomplete cursors never yield totals", async () => {
  const cases: unknown[][] = [
    [health(900000, false)],
    [health(), page([row()]), health(900001)],
    [health(), page([row()], 3, 2), page([row("KEKET")], null, 3)],
    [health(), page([row()], 3, 2), page([row()], null, 2)],
    [health(), page([{ ...row(), address: SECOND }])],
    [
      health(),
      page([{ ...row(), utxo: "a".repeat(64) + ":0", utxo_address: SECOND }]),
    ],
    [health(), page([row("THOTHPEPE", -1)])],
    [health(), page([row("THOTHPEPE", 1.5)])],
    [health(), page([row("THOTHPEPE", "1e30")])],
    [health(), { result: [row()], result_count: 1 }],
    [health(), page([], 1, 0)],
    [health(), page([row()], null, 2)],
    [health(), page([row()], 2, 3), page([row("KEKET")], 2, 3)],
  ];
  for (const bodies of cases)
    await assert.rejects(
      fetchCollection(ADDRESS, { fetcher: scripted(...bodies) }),
      CollectionError,
    );
  for (const code of [429, 503, 500])
    await assert.rejects(
      fetchCollection(ADDRESS, {
        fetcher: (async () => response({}, code)) as typeof fetch,
      }),
      CollectionError,
    );
  await assert.rejects(
    fetchCollection(ADDRESS, {
      fetcher: (async () =>
        new Response("offline proxy", {
          headers: { "content-type": "text/html" },
        })) as typeof fetch,
    }),
    CollectionError,
  );
});
test("requests are bounded in time, response size and page count, and can be cancelled", async () => {
  const never = (async (_url: unknown, options: RequestInit) =>
    new Promise((_resolve, reject) =>
      options.signal!.addEventListener(
        "abort",
        () => reject(new Error("aborted")),
        { once: true },
      ),
    )) as typeof fetch;
  await assert.rejects(
    fetchCollection(ADDRESS, { fetcher: never, timeoutMs: 5 }),
    (err: unknown) => err instanceof CollectionError && err.code === "timeout",
  );
  const abort = new AbortController();
  abort.abort();
  await assert.rejects(
    fetchCollection(ADDRESS, { signal: abort.signal, fetcher: never }),
    (err: unknown) =>
      err instanceof CollectionError && err.code === "cancelled",
  );
  await assert.rejects(
    fetchCollection(ADDRESS, {
      fetcher: scripted(" ".repeat(COLLECTION_LIMITS.bytesPerPage + 1)),
    }),
    (err: unknown) => err instanceof CollectionError && err.code === "limit",
  );
  let n = 0;
  const endless = (async () =>
    n++ === 0
      ? response(health())
      : response(page([row("A" + n)], n, 21))) as typeof fetch;
  await assert.rejects(
    fetchCollection(ADDRESS, { fetcher: endless }),
    (err: unknown) => err instanceof CollectionError && err.code === "limit",
  );
  assert.equal(n, 21);
});
test("only checksum-valid mainnet addresses reach the service; lookup accepts P2SH without changing signing rules", async () => {
  let calls = 0;
  for (const input of [
    "not-an-address",
    ADDRESS.slice(0, -1) + "A",
    "abandon ".repeat(11) + "about",
    "a".repeat(64),
    "https://example.com/",
    "tb1qtest",
  ])
    await assert.rejects(
      fetchCollection(input, {
        fetcher: (async () => {
          calls++;
          return response({});
        }) as typeof fetch,
      }),
    );
  assert.equal(calls, 0);
  assert.equal(
    await validateLookupAddress("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"),
    "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
  );
  const empty = await fetchCollection(ADDRESS, {
    fetcher: scripted(health(), page([]), health()),
  });
  assert.deepEqual(empty.holdings, []);
});
test("cancelled, closed and superseded requests cannot restore old addresses or overwrite newer results", async () => {
  const pending: ((value: CollectionSnapshot) => void)[] = [];
  const loader = (async () =>
    new Promise<CollectionSnapshot>((resolve) =>
      pending.push(resolve),
    )) as typeof fetchCollection;
  const state = new CollectionLookup(() => {}, loader);
  const snapshot = (address: string): CollectionSnapshot => ({
    address,
    holdings: [],
    checkedAt: 1,
    nodeHeight: 1,
    pages: 1,
    rows: 0,
  });
  state.edit(ADDRESS);
  const first = state.run();
  state.edit(SECOND);
  const second = state.run();
  pending[1](snapshot(SECOND));
  await second;
  pending[0](snapshot(ADDRESS));
  await first;
  assert.equal(state.state.snapshot?.address, SECOND);
  const third = state.run();
  state.clear();
  pending[2](snapshot(SECOND));
  await third;
  assert.deepEqual(state.state, {
    status: "idle",
    input: "",
    snapshot: null,
    error: "",
    rows: 0,
  });
});
