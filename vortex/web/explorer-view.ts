import { assetLink, explorerQuery } from "./explorer.ts";
import { escapeHtml as e } from "./safety.ts";

export function assetDestination(input: string): string {
  const asset = explorerQuery(input);
  return asset
    ? `<a class="secondary" href="${e(assetLink(asset))}" target="_blank" rel="noopener noreferrer">Inspect ${e(asset)} on xcp.io ↗</a><p class="small-note">The explorer will check this name. Preparing this link sends no request.</p>`
    : `<p class="small-note">${input.trim() ? "Use an asset name, numeric A… identifier, or a full PARENT.child name. Subasset spelling is case-sensitive." : "Type a name to prepare its explorer link. No address or ownership required."}</p>`;
}

export function assetAtlas(input: string): string {
  return `<section class="asset-atlas" aria-labelledby="asset-atlas-title"><div class="asset-atlas-intro"><div class="eyebrow">THE NILE HAS MANY TRIBUTARIES</div><h2 id="asset-atlas-title">Every Counterparty asset has a place</h2><p>Named tokens, numeric assets, subassets and Classic Bitcoin Stamps. A whole river of records, with Rare Pepe as our first storytellers.</p></div><div class="asset-atlas-search"><label for="asset-name">Find an asset on xcp.io</label><input id="asset-name" name="asset" value="${e(input)}" maxlength="250" spellcheck="false" autocapitalize="none" autocomplete="off" placeholder="Asset name · A… · PARENT.child" aria-describedby="asset-destination"><div id="asset-destination" aria-live="polite">${assetDestination(input)}</div></div><div class="actions"><a class="text-button" href="https://xcp.io/assets" target="_blank" rel="noopener noreferrer">Explore all Counterparty assets ↗</a><button class="text-button" data-modal="stamps">Read the Bitcoin Stamps teaching</button></div></section>`;
}
