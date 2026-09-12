import { assetLink, addressLink } from "./explorer.ts";
import { formatHolding } from "./counterparty.ts";
import type { CollectionState, Holding } from "./counterparty.ts";
import { RARES, rareAt } from "./rares.ts";
import { IDS, NODES } from "./lattice.ts";
import type { Seeker } from "./session.ts";
import { escapeHtml as e } from "./safety.ts";

export function collectionInvitation(): string {
  return '<section class="collection-invitation"><div><div class="eyebrow">THE SCRIBE’S OTHER LEDGER</div><h2>A ledger for every kind of mark</h2><p>Look up every reported Counterparty asset at an address: named tokens, numeric assets, subassets and Classic Stamps. Our Rare Pepe characters are one part of that wider river. No wallet connection or signature needed.</p></div><button class="secondary" data-modal="collection">Open the address ledger</button></section>';
}
function holdingRow(h: Holding, s: Seeker): string {
  const rare = RARES.find((r) => r.name === h.asset),
    office = rare ? IDS.find((id) => rareAt(id).name === h.asset)! : null;
  return `<article class="holding-row"><div class="holding-identity">${rare ? `<img src="${rare.image}" alt="Original ${rare.name} artwork" width="54" height="76" loading="lazy">` : ""}<div><h3>${e(h.longname ?? h.asset)}</h3><span>${e(h.asset)}</span>${office ? `<small>${e(NODES[office].pond)} · ${s.looked.includes(office) ? "Encountered in this journey" : "Awaiting your visit"}</small>` : ""}</div></div><div class="holding-quantity"><strong>${formatHolding(h.raw, h.divisible)}</strong>${h.divisible === null ? "<small>Divisibility unavailable; amount is unscaled.</small>" : ""}${h.outputs ? `<small>${formatHolding(h.addressRaw, h.divisible)} at address<br>${formatHolding(h.attachedRaw, h.divisible)} attached to ${h.outputs} Bitcoin output${h.outputs === 1 ? "" : "s"}</small>` : ""}</div><div class="holding-links">${office ? `<button class="text-button" data-track="${office}">Visit this character</button>` : ""}<a class="text-button" href="${e(assetLink(h.asset, h.longname))}" target="_blank" rel="noopener noreferrer">Asset record on xcp.io ↗</a></div></article>`;
}
export function collectionBody(
  state: CollectionState,
  s: Seeker,
  filter: "world" | "all",
  visible: number,
  query = "",
): string {
  const snapshot = state.snapshot;
  const matches =
    snapshot?.holdings.filter((h) => RARES.some((r) => r.name === h.asset)) ??
    [];
  const scoped = filter === "world" ? matches : (snapshot?.holdings ?? []);
  const term = query.trim().toLowerCase();
  const rows = scoped.filter(
    (h) =>
      !term ||
      h.asset.toLowerCase().includes(term) ||
      h.longname?.toLowerCase().includes(term),
  );
  return `<p>Enter a public Bitcoin mainnet address. This sends that address to <strong>api.counterparty.io</strong> when you press Look up. Results and the address stay in memory until you close this ledger; they are never added to your saved journey.</p><form id="collection-form"><label for="collection-address">Public address</label><div class="input-row"><input id="collection-address" name="address" value="${e(state.input)}" maxlength="90" spellcheck="false" autocapitalize="none" autocomplete="off" placeholder="1… · 3… · bc1…" aria-describedby="collection-privacy" required><button class="primary" type="submit" ${state.status === "loading" ? "disabled" : ""}>${state.status === "loading" ? "Looking up…" : "Look up"}</button></div><small id="collection-privacy">An address only. Never enter a private key or recovery phrase. No signing, spending, or token transfers.</small></form><div id="collection-result" aria-live="polite" aria-atomic="false">${state.status === "loading" ? `<div class="collection-progress"><p>Reading Counterparty’s ledger${state.rows ? " · " + state.rows + " balance entries received" : "…"}</p><button class="text-button" data-collection-cancel>Cancel lookup</button></div>` : state.status === "error" ? `<div class="collection-error" role="alert"><p>${e(state.error)}</p><button class="secondary" data-collection-retry>Try again</button></div>` : ""}${
    snapshot
      ? `<section class="collection-snapshot"><div class="collection-snapshot-heading"><div><span class="eyebrow">REPORTED AT THIS ADDRESS</span><p class="address">${e(snapshot.address)}</p><p class="small-note">Checked ${e(new Date(snapshot.checkedAt).toLocaleString())}. Node reported block ${snapshot.nodeHeight.toLocaleString("en-US")}.</p></div><button class="text-button" data-collection-retry>Refresh</button></div><p class="collection-scope">Address balances and attached Bitcoin outputs. Excludes BTC, escrow, SRC-20 holdings and unconfirmed changes. The public API may cache replies; this is a report from a service, not a proof of ownership or a guaranteed block snapshot.</p><div class="collection-filters" role="group" aria-label="Token view"><button class="secondary" data-collection-filter="all" aria-pressed="${filter === "all"}">All Counterparty assets (${snapshot.holdings.length})</button><button class="secondary" data-collection-filter="world" aria-pressed="${filter === "world"}">Rare Pepe characters (${matches.length})</button></div><label for="collection-search">Find an asset in these results</label><input id="collection-search" value="${e(query)}" maxlength="250" placeholder="Name, numeric identifier or subasset" autocomplete="off" spellcheck="false"><p class="small-note">${rows.length} of ${scoped.length} assets in this view · filtering stays on this device.</p>${
          rows.length
            ? `<div class="holdings-list">${rows
                .slice(0, visible)
                .map((h) => holdingRow(h, s))
                .join(
                  "",
                )}</div>${rows.length > visible ? `<button class="secondary" data-collection-more>Show more · ${visible} of ${rows.length}</button>` : ""}`
            : `<p class="collection-empty">${term && scoped.length ? "No assets in this view match your search. Clear the search or choose All Counterparty assets." : filter === "world" && snapshot.holdings.length ? "None of the ten tokens in this game appeared in the reported balances. You can still meet every character, or view all Counterparty assets above." : "The API reported no positive Counterparty balances for this address. Both game chapters remain open to you."}</p>`
        }<div class="actions"><a class="text-button" href="${e(addressLink(snapshot.address))}" target="_blank" rel="noopener noreferrer">Inspect this address on xcp.io ↗</a><button class="text-button" data-collection-clear>Clear address & results</button></div></section>`
      : ""
  }</div><p class="small-note">Discoveries in the Rare archive belong to your game journey. Balances belong to the address you chose to inspect. Neither unlocks or blocks a story or ending.</p>`;
}
