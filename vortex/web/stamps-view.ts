import { STAMP_OFFICES, STAMP_TEACHINGS, isStampOffice } from "./stamps.ts";
import type { StampOffice } from "./stamps.ts";
import type { Dialect, SefirahId } from "./lattice.ts";
import { escapeHtml as e } from "./safety.ts";

export function stampInvitation(id: SefirahId): string {
  if (!isStampOffice(id)) return "";
  return `<section class="stamp-invitation"><span class="eyebrow">BITCOIN STAMPS · ${e(id.toUpperCase())}</span><h2>The chamber of the enduring mark</h2><p>${e(STAMP_TEACHINGS[id].invitation)}</p><button class="secondary" data-modal="stamps">Enter the chamber</button></section>`;
}

export function stampBody(office: StampOffice, dialect: Dialect): string {
  const lesson = STAMP_TEACHINGS[office];
  return `<p class="stamp-intro">From the scribe’s ink to the foundation beneath the temple, then down to the public ledger. Three readings of one enduring mark.</p><div class="stamp-path" role="group" aria-label="Readings of the enduring mark">${STAMP_OFFICES.map((id) => `<button class="secondary" data-stamp-office="${id}" aria-pressed="${id === office}">${e(STAMP_TEACHINGS[id].label)}</button>`).join("")}</div><article class="stamp-teaching" aria-live="polite" aria-atomic="true"><span class="eyebrow">${e(lesson.label)}</span><h2>${e(lesson.title)}</h2><blockquote>${e(lesson[dialect])}</blockquote><div class="stamp-record"><h3>At the ledger</h3><p>${e(lesson.fact)}</p><a class="text-button" href="${lesson.source}" target="_blank" rel="noopener noreferrer">${e(lesson.sourceLabel)} ↗</a>${office === "malkhut" ? '<a class="text-button" href="https://github.com/stampchain-io/btc_stamps" target="_blank" rel="noopener noreferrer">Read KEVIN’s protocol history ↗</a>' : ""}</div><details class="stamp-reflection"><summary>${e(lesson.question)}</summary><p>${e(lesson.reflection)}</p></details></article><p class="small-note stamp-boundary">These temple correspondences are VORTEX fiction. Classic Stamps use Counterparty assets; modern SRC-20 uses its own protocol and indexer. The address ledger here reports Counterparty balances, not SRC-20 holdings. Your journey’s sigil remains local: reading this chamber does not stamp or publish it.</p>`;
}
