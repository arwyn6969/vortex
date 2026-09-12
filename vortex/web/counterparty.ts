import { validateLookupAddress } from "./wallet.ts";

export const COUNTERPARTY_API = "https://api.counterparty.io:4000/v2/";
export const COLLECTION_LIMITS = {
  pageSize: 100,
  pages: 20,
  bytesPerPage: 1_000_000,
  timeoutMs: 30_000,
} as const;
export type Holding = {
  asset: string;
  longname: string | null;
  raw: string;
  divisible: boolean | null;
  addressRaw: string;
  attachedRaw: string;
  outputs: number;
};
export type CollectionSnapshot = {
  address: string;
  holdings: Holding[];
  checkedAt: number;
  nodeHeight: number;
  rows: number;
  pages: number;
};
export class CollectionError extends Error {
  code:
    | "network"
    | "timeout"
    | "unready"
    | "changed"
    | "invalid"
    | "limit"
    | "rate"
    | "cancelled";
  constructor(code: CollectionError["code"], message: string) {
    super(message);
    this.name = "CollectionError";
    this.code = code;
  }
}
const invalid = () =>
  new CollectionError(
    "invalid",
    "The service returned incomplete or inconsistent balance data. Try again later or inspect the address on xcp.io.",
  );
function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw invalid();
  return value as Record<string, unknown>;
}
function unsigned(value: unknown): string {
  const text =
    typeof value === "number" && Number.isSafeInteger(value)
      ? String(value)
      : typeof value === "string"
        ? value
        : "";
  if (
    !/^(0|[1-9]\d{0,19})$/.test(text) ||
    BigInt(text) > 18_446_744_073_709_551_615n
  )
    throw invalid();
  return text;
}
function integer(value: unknown): number {
  const n = Number(unsigned(value));
  if (!Number.isSafeInteger(n)) throw invalid();
  return n;
}
// A regular JSON.parse would round raw token amounts above 2^53. Match complete
// JSON string/number tokens, protecting quoted content, and preserve only unsafe
// integer literals as decimal strings before handing syntax validation to JSON.
export function parseExactJson(text: string): unknown {
  try {
    JSON.parse(text);
  } catch {
    throw invalid();
  }
  const exact = text.replace(
    /"(?:[^"\\]|\\.)*"|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/g,
    (token) => {
      if (
        token[0] === '"' ||
        /[.eE]/.test(token) ||
        Number.isSafeInteger(Number(token))
      )
        return token;
      return '"' + token + '"';
    },
  );
  try {
    return JSON.parse(exact);
  } catch {
    throw invalid();
  }
}
export function formatHolding(raw: string, divisible: boolean | null): string {
  const value = BigInt(raw);
  if (divisible === null) return value.toLocaleString("en-US") + " raw units";
  if (!divisible) return value.toLocaleString("en-US");
  const fraction = (value % 100_000_000n)
    .toString()
    .padStart(8, "0")
    .replace(/0+$/, "");
  return (
    (value / 100_000_000n).toLocaleString("en-US") +
    (fraction ? "." + fraction : "")
  );
}
function label(value: unknown): string | null {
  return typeof value === "string" &&
    value.length > 0 &&
    value.length <= 250 &&
    !/[\x00-\x1f\x7f]/.test(value)
    ? value
    : null;
}
async function readResponse(response: Response): Promise<unknown> {
  if (response.status === 503)
    throw new CollectionError(
      "unready",
      "The Counterparty node is catching up. Your game is still available; try the address again later.",
    );
  if (response.status === 429)
    throw new CollectionError(
      "rate",
      "The public service is busy. Wait a little before trying again.",
    );
  if (!response.ok)
    throw new CollectionError(
      "network",
      "The Counterparty service could not complete this lookup. Try again later.",
    );
  if (response.headers.get("x-counterparty-ready")?.toLowerCase() === "false")
    throw new CollectionError(
      "unready",
      "The Counterparty node is not ready to report balances.",
    );
  if (!response.headers.get("content-type")?.includes("application/json"))
    throw invalid();
  if (
    Number(response.headers.get("content-length")) >
      COLLECTION_LIMITS.bytesPerPage ||
    !response.body
  )
    throw new CollectionError(
      "limit",
      "This response is too large to load safely here. Inspect the address on xcp.io.",
    );
  const reader = response.body.getReader(),
    decoder = new TextDecoder("utf-8", { fatal: true });
  let bytes = 0,
    text = "";
  try {
    while (true) {
      const part = await reader.read();
      if (part.done) break;
      bytes += part.value.byteLength;
      if (bytes > COLLECTION_LIMITS.bytesPerPage)
        throw new CollectionError(
          "limit",
          "This response is too large to load here. Inspect the address on xcp.io.",
        );
      text += decoder.decode(part.value, { stream: true });
    }
    text += decoder.decode();
    return parseExactJson(text);
  } finally {
    await reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}
function readiness(raw: unknown): number {
  const r = object(object(raw).result);
  if (
    r.server_ready !== true ||
    r.network !== "mainnet" ||
    r.ledger_state !== "Following"
  )
    throw new CollectionError(
      "unready",
      "The Counterparty node is not ready to report mainnet balances. Try again later.",
    );
  const height = integer(r.counterparty_height),
    backend = integer(r.backend_height);
  if (height < backend - 1)
    throw new CollectionError(
      "unready",
      "The Counterparty node is still catching up with Bitcoin.",
    );
  return height;
}
function balanceRow(
  raw: unknown,
  address: string,
): { holding: Holding; key: string } {
  const r = object(raw);
  if (
    typeof r.asset !== "string" ||
    !/^(?:[A-Z]{4,12}|A[0-9]{1,20}|XCP|BTC)$/.test(r.asset)
  )
    throw invalid();
  const quantity = unsigned(r.quantity);
  const utxo = r.utxo;
  if (
    utxo !== null &&
    (typeof utxo !== "string" || !/^[0-9a-f]{64}:(0|[1-9]\d{0,9})$/.test(utxo))
  )
    throw invalid();
  if (utxo === null ? r.address !== address : r.utxo_address !== address)
    throw invalid();
  const info = r.asset_info == null ? {} : object(r.asset_info);
  const divisible = typeof info.divisible === "boolean" ? info.divisible : null;
  return {
    key: r.asset + "|" + (utxo ?? "address"),
    holding: {
      asset: r.asset,
      longname: label(info.asset_longname) ?? label(r.asset_longname),
      raw: quantity,
      divisible,
      addressRaw: utxo === null ? quantity : "0",
      attachedRaw: utxo === null ? "0" : quantity,
      outputs: utxo === null ? 0 : 1,
    },
  };
}
export async function fetchCollection(
  input: string,
  options: {
    signal?: AbortSignal;
    fetcher?: typeof fetch;
    now?: () => number;
    onProgress?: (rows: number) => void;
    timeoutMs?: number;
  } = {},
): Promise<CollectionSnapshot> {
  const address = await validateLookupAddress(input);
  if (options.signal?.aborted)
    throw new CollectionError("cancelled", "Lookup cancelled.");
  const controller = new AbortController();
  const abort = () => controller.abort();
  options.signal?.addEventListener("abort", abort, { once: true });
  let timedOut = false;
  const timer = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, options.timeoutMs ?? COLLECTION_LIMITS.timeoutMs);
  const request = async (path: string) => {
    const response = await (options.fetcher ?? fetch)(COUNTERPARTY_API + path, {
      method: "GET",
      mode: "cors",
      credentials: "omit",
      referrerPolicy: "no-referrer",
      cache: "no-store",
      redirect: "error",
      signal: controller.signal,
    });
    return readResponse(response);
  };
  try {
    // Readiness headers are not exposed by every CORS deployment. The root's
    // JSON body is readable everywhere; check it before and after all pages.
    const startHeight = readiness(await request(""));
    let cursor: string | null = null,
      count: number | null = null,
      rows = 0,
      pages = 0;
    const cursors = new Set<string>(),
      seen = new Set<string>(),
      holdings = new Map<string, Holding>();
    do {
      if (pages >= COLLECTION_LIMITS.pages)
        throw new CollectionError(
          "limit",
          "This address has more than 2,000 balance entries. No partial total is shown. Inspect the full address on xcp.io.",
        );
      const query = new URLSearchParams({
        limit: String(COLLECTION_LIMITS.pageSize),
        verbose: "true",
        type: "all",
        ...(cursor === null ? {} : { cursor }),
      });
      const page = object(
        await request(
          "addresses/" + encodeURIComponent(address) + "/balances?" + query,
        ),
      );
      if (
        !Array.isArray(page.result) ||
        page.result.length > COLLECTION_LIMITS.pageSize ||
        !("next_cursor" in page)
      )
        throw invalid();
      const total = integer(page.result_count);
      if (count !== null && total !== count)
        throw new CollectionError(
          "changed",
          "The balances changed during this lookup. Refresh to collect a new result.",
        );
      count = total;
      for (const row of page.result) {
        const { holding, key } = balanceRow(row, address);
        if (seen.has(key))
          throw new CollectionError(
            "changed",
            "A balance repeated while the pages were loading. Refresh to avoid a misleading total.",
          );
        seen.add(key);
        rows++;
        if (holding.raw === "0") continue;
        const previous = holdings.get(holding.asset);
        if (previous) {
          if (
            previous.divisible !== holding.divisible ||
            previous.longname !== holding.longname
          )
            throw invalid();
          previous.raw = (
            BigInt(previous.raw) + BigInt(holding.raw)
          ).toString();
          previous.addressRaw = (
            BigInt(previous.addressRaw) + BigInt(holding.addressRaw)
          ).toString();
          previous.attachedRaw = (
            BigInt(previous.attachedRaw) + BigInt(holding.attachedRaw)
          ).toString();
          previous.outputs += holding.outputs;
        } else holdings.set(holding.asset, holding);
      }
      cursor = page.next_cursor === null ? null : unsigned(page.next_cursor);
      if (cursor !== null && (!page.result.length || cursors.has(cursor)))
        throw invalid();
      if (cursor !== null) cursors.add(cursor);
      pages++;
      options.onProgress?.(rows);
    } while (cursor !== null);
    if (rows !== count)
      throw new CollectionError(
        "changed",
        "The response did not contain every reported balance. Refresh or check xcp.io; no partial total is shown.",
      );
    const nodeHeight = readiness(await request(""));
    if (nodeHeight !== startHeight)
      throw new CollectionError(
        "changed",
        "A new block arrived during the lookup. Refresh to collect the balances again.",
      );
    if (controller.signal.aborted)
      throw new CollectionError(
        timedOut ? "timeout" : "cancelled",
        timedOut
          ? "The lookup took too long. Try again later."
          : "Lookup cancelled.",
      );
    return {
      address,
      holdings: [...holdings.values()].sort((a, b) =>
        a.asset.localeCompare(b.asset),
      ),
      checkedAt: (options.now ?? Date.now)(),
      nodeHeight,
      rows,
      pages,
    };
  } catch (error) {
    if (controller.signal.aborted)
      throw new CollectionError(
        timedOut ? "timeout" : "cancelled",
        timedOut
          ? "The public service took too long. Your game is still available; try again later."
          : "Lookup cancelled.",
      );
    if (error instanceof CollectionError) throw error;
    throw new CollectionError(
      "network",
      "The lookup could not reach Counterparty. Check your connection or try again later. Offline play still works.",
    );
  } finally {
    clearTimeout(timer);
    options.signal?.removeEventListener("abort", abort);
  }
}

export type CollectionState = {
  status: "idle" | "loading" | "ready" | "error";
  input: string;
  snapshot: CollectionSnapshot | null;
  error: string;
  rows: number;
};
// Ephemeral controller: never writes a World, storage, journal, URL or wallet proof.
export class CollectionLookup {
  state: CollectionState = {
    status: "idle",
    input: "",
    snapshot: null,
    error: "",
    rows: 0,
  };
  private serial = 0;
  private pending: AbortController | null = null;
  private changed: () => void;
  private loader: typeof fetchCollection;
  constructor(
    changed: () => void,
    loader: typeof fetchCollection = fetchCollection,
  ) {
    this.changed = changed;
    this.loader = loader;
  }
  edit(input: string) {
    this.serial++;
    this.pending?.abort();
    this.pending = null;
    this.state = { status: "idle", input, snapshot: null, error: "", rows: 0 };
  }
  clear() {
    this.edit("");
    this.changed();
  }
  cancel() {
    this.edit(this.state.input);
    this.changed();
  }
  async run() {
    this.pending?.abort();
    const pending = new AbortController(),
      serial = ++this.serial;
    this.pending = pending;
    this.state = {
      ...this.state,
      status: "loading",
      snapshot: null,
      error: "",
      rows: 0,
    };
    this.changed();
    try {
      const result = await this.loader(this.state.input, {
        signal: pending.signal,
        onProgress: (rows) => {
          if (this.serial === serial) {
            this.state.rows = rows;
            this.changed();
          }
        },
      });
      if (this.serial !== serial) return;
      this.state = {
        status: "ready",
        input: result.address,
        snapshot: result,
        error: "",
        rows: result.rows,
      };
    } catch (error) {
      if (this.serial !== serial) return;
      this.state = {
        ...this.state,
        status: "error",
        snapshot: null,
        error:
          error instanceof Error
            ? error.message
            : "The address lookup could not complete.",
      };
    } finally {
      if (this.serial === serial) {
        this.pending = null;
        this.changed();
      }
    }
  }
}
