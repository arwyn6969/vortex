import {
  ATLAS,
  ATLAS_SOURCES,
  CLUSTERS,
  RELATIONS,
  atlasEntry,
  searchAtlas,
} from "./atlas.ts";
import type { AtlasEntry } from "./atlas.ts";
import type { Seeker, World } from "./session.ts";
import { escapeHtml as e } from "./safety.ts";
import { NODES } from "./lattice.ts";
import type { SefirahId } from "./lattice.ts";
import {
  inquiryError,
  inquiryMemory,
  TABLET_CHOICES,
  GATE_CHOICES,
} from "./inquiries.ts";
import type { InquiryAction } from "./inquiries.ts";
import { route } from "./navigation.ts";
import { status } from "./session.ts";

export type AtlasView = {
  query: string;
  tradition: string;
  group: string;
  selected: string;
  compare: string[];
  notebook: boolean;
};
export const emptyAtlasView = (): AtlasView => ({
  query: "",
  tradition: "all",
  group: "all",
  selected: "memory",
  compare: [],
  notebook: false,
});
function source(entry: AtlasEntry) {
  const s = ATLAS_SOURCES[entry.source];
  return `<a href="${e(s.url)}" target="_blank" rel="noopener noreferrer">${e(s.title)} ↗</a><p class="small-note">${e(entry.locator)}</p>`;
}
function detail(entry: AtlasEntry, s: Seeker, compare: boolean) {
  return `<article class="atlas-detail" aria-labelledby="entry-${e(entry.id)}">
    <span class="eyebrow">${e(entry.kind)} · ${e(entry.evidence)}</span>
    <h2 id="entry-${e(entry.id)}" tabindex="-1">${e(entry.name)}</h2>
    ${entry.image ? `<button data-rare="${e(entry.token)}" class="atlas-original"><img src="${e(entry.image)}" width="400" height="560" alt="Original ${e(entry.name)} asset artwork"></button>` : ""}
    <p class="atlas-context">${e(entry.tradition)} · ${e(entry.context)}</p>
    <p>${e(entry.summary)}</p><p class="atlas-distinction">${e(entry.distinction)}</p>
    ${entry.aliases.length ? `<p class="small-note">Also indexed: ${e(entry.aliases.join(" · "))}</p>` : ""}
    <div class="actions"><button class="secondary" data-study="${e(entry.id)}" ${s.inquiries.seen.includes(entry.id) ? "disabled" : ""}>${s.inquiries.seen.includes(entry.id) ? "Remembered ✓" : "Remember this connection"}</button>
    <button class="text-button" data-compare="${e(entry.id)}" aria-pressed="${compare}">${compare ? "Remove from comparison" : "Compare"}</button></div>
    <details id="atlas-source-${e(entry.id)}"><summary>Source & context</summary>${source(entry)}<p class="small-note">Source notes reviewed 12 September 2026. Temple placements and cluster membership are VORTEX interpretations.${/Maya|Dogon/.test(entry.tradition) ? " These reading notes have not had a specialist cultural review." : ""}</p></details>
  </article>`;
}
export function atlasView(s: Seeker, state: AtlasView): string {
  const entries = searchAtlas(state.query, state.tradition, state.group).filter(
    (x) => !state.notebook || s.inquiries.seen.includes(x.id),
  );
  const selected = atlasEntry(state.selected) ?? ATLAS[0];
  const related = RELATIONS.filter(
    (r) => r.from === selected.id || r.to === selected.id,
  );
  const compare = state.compare
    .map(atlasEntry)
    .filter((x): x is AtlasEntry => !!x);
  const common =
    compare.length > 1
      ? CLUSTERS.filter((c) => compare.every((x) => x.groups.includes(c.id)))
      : [];
  return `<main id="main" class="atlas-page">
    <div class="atlas-heading"><div><span class="eyebrow">THE LIVING ATLAS · ${s.inquiries.seen.length} CONNECTIONS REMEMBERED</span><h1>Many stories. A shared river.</h1><p>Follow a question across myths, tarot and real assets. Keep the differences in view.</p></div><button class="secondary" data-view="tree">Return to the Nile</button></div>
    <div class="atlas-clusters">${CLUSTERS.map((c) => `<button data-cluster="${c.id}" aria-pressed="${state.group === c.id}"><strong>${e(c.name)}</strong><span>${e(c.question)}</span></button>`).join("")}</div>
    <form id="atlas-search" class="atlas-search"><label>Find a figure, token or idea<input id="atlas-query" name="query" maxlength="100" value="${e(state.query)}" placeholder="Nisaba, KEVIN, a guardian…"></label><label>Tradition<select name="tradition" id="atlas-tradition"><option value="all">All traditions</option>${[
      ...new Set(ATLAS.map((x) => x.tradition)),
    ]
      .sort()
      .map(
        (t) =>
          `<option ${t === state.tradition ? "selected" : ""} value="${e(t)}">${e(t)}</option>`,
      )
      .join(
        "",
      )}</select></label><button class="secondary" id="atlas-search-submit">Search</button><button type="button" class="text-button" data-atlas-clear>Clear filters</button></form>
    <div class="actions"><button class="text-button" data-notebook aria-pressed="${state.notebook}">${state.notebook ? "Show every entry" : "My remembered connections"}</button><span role="status">${entries.length} ${entries.length === 1 ? "entry" : "entries"}${state.group !== "all" ? " · " + e(CLUSTERS.find((c) => c.id === state.group)?.name) : ""}</span></div>
    ${compare.length ? `<section class="atlas-comparison" aria-label="Comparison"><div class="actions"><h2>Read them side by side</h2><button class="text-button" data-compare-clear>Clear comparison</button></div><p>${common.length ? "Shared exploration theme: " + common.map((c) => e(c.name)).join(" · ") + ". Membership is an editorial comparison, not common origin." : "These entries have different contexts. A useful comparison can reveal a difference."}</p><div class="atlas-compare-grid">${compare.map((x) => `<article><h3>${e(x.name)}</h3><p>${e(x.tradition)} · ${e(x.kind)}</p><p>${e(x.summary)}</p><p>${e(x.distinction)}</p>${source(x)}<button class="text-button" data-compare="${e(x.id)}">Remove ${e(x.name)}</button></article>`).join("")}</div></section>` : ""}
    <div class="atlas-layout"><nav class="atlas-index" aria-label="Atlas entries">${entries.length ? entries.map((x) => `<button data-atlas-entry="${e(x.id)}" aria-current="${selected.id === x.id ? "true" : "false"}"><span>${e(x.kind)}${s.inquiries.seen.includes(x.id) ? " · remembered" : ""}</span><strong>${e(x.name)}</strong><small>${e(x.tradition)}</small></button>`).join("") : "<p>No entries match. Try a different name or clear the filters.</p>"}</nav><div>
    ${detail(selected, s, state.compare.includes(selected.id))}
    <section class="atlas-connections"><h2>Why are these connected?</h2>${related
      .slice(0, 12)
      .map((r) => {
        const other = atlasEntry(r.from === selected.id ? r.to : r.from)!;
        return `<details id="atlas-relation-${e(r.id)}"><summary>${e(other.name)} · ${e(r.evidence)}</summary><p>${e(r.why)}</p><p class="small-note">${e(r.locator)}</p><a href="${e(ATLAS_SOURCES[r.source].url)}" target="_blank" rel="noopener noreferrer">Read this connection’s source ↗</a><br><button class="text-button" data-atlas-entry="${e(other.id)}">Explore ${e(other.name)}</button></details>`;
      })
      .join(
        "",
      )}${related.length > 12 ? "<p class='small-note'>More members appear in the cluster list. This view shows twelve connections at a time.</p>" : ""}</section>
    <aside class="atlas-callout"><h3>Bring an idea back to the water</h3><p>The scribe at Hod needs help with two accounts. The guardian at Netzach has a gate that one person cannot open.</p><button class="secondary" data-atlas-route="hod">Follow the tablet</button> <button class="secondary" data-atlas-route="netzach">Follow the gate</button></aside></div></div>
  </main>`;
}
const read = (id: string) =>
  `<button class="text-button" data-atlas-entry="${id}">Read ${e(atlasEntry(id)!.name)} ↗</button>`;
function choice(s: Seeker, task: "tablet" | "gate", label: string, i: number) {
  const error = inquiryError(s, { type: "inquiry", task, choice: i });
  const showReason =
    i === 0 || error !== inquiryError(s, { type: "inquiry", task, choice: 0 });
  return `<div><button class="rite-choice" data-inquiry="${task}" data-choice="${i}" ${error ? "disabled" : ""}>${e(label)}</button>${error && showReason ? `<p class="small-note">${e(error)}</p>` : ""}</div>`;
}
export function inquiryPanel(s: Seeker): string {
  const p = s.inquiries,
    here = s.current;
  if (here === "hod")
    return `<section class="inquiry-panel" id="inquiry-panel" tabindex="-1"><span class="eyebrow">AN ENCOUNTER · CLAY AND THE WORD</span><h2>The Disputed Tablet</h2>${p.tablet !== null ? `<p>${e(inquiryMemory(s, here))}</p><p class="small-note">Your decision is remembered at Yesod and Kingdom.</p>` : `<p>Two frogs insist the flood reached different steps. Both accounts have survived. The scribe asks whether a durable record is enough to settle the argument. Nisaba’s writing traditions and the Stamps chamber offer different ways into the question.</p><blockquote>“The tablet is permanent, fren. The argument has also applied for permanence.”</blockquote><div class="actions">${read("nisaba")}${read("stamps")}</div>${TABLET_CHOICES.map((x, i) => choice(s, "tablet", x, i)).join("")}<button class="text-button" data-atlas-route="yesod">Consult the waterline witness at Yesod</button>`}<p class="small-note">An authored VORTEX problem. Historical and protocol sources remain separate in the atlas.</p></section>`;
  if (here === "netzach")
    return `<section class="inquiry-panel" id="inquiry-panel" tabindex="-1"><span class="eyebrow">AN ENCOUNTER · THRESHOLDS AND REVERSALS</span><h2>The Gate That Remembers</h2>${p.gate !== null ? `<p>${e(inquiryMemory(s, here))}</p><p class="small-note">Kingdom will remember how you opened the gate.</p>` : `<p>The gate has two latches, too far apart for one frog. Its guardian is standing beside the other latch, firmly explaining that nobody can pass alone.</p><blockquote>${s.rites.netzach === 0 ? "“You wanted a firm boundary. Here it is. Very firm. Slightly lonely.”" : s.rites.netzach === 1 ? "“You made room at this threshold before. Show me what that means now.”" : "“A test can change without the doorway falling down. Probably.”"}</blockquote><div class="actions">${read("hero-twins")}${read("neti")}</div>${GATE_CHOICES.map((x, i) => choice(s, "gate", x, i)).join("")}`}<p class="small-note">This frog encounter is VORTEX fiction. It compares questions about cooperation and rules; it does not reenact the Popol Vuh.</p></section>`;
  if (here === "yesod" && p.testimony && p.tablet === null)
    return `<section class="inquiry-panel" id="inquiry-panel" tabindex="-1"><h2>The witness has been heard</h2><p>One account was made before the flood, the other after. You can now take this context to Hod before choosing what the tablet should say.</p><button class="secondary" data-atlas-route="hod">Return to the scribe</button></section>`;
  if (here === "yesod" && !p.testimony && p.tablet === null) {
    const error = inquiryError(s, {
      type: "inquiry",
      task: "testimony",
      choice: 0,
    });
    return `<section class="inquiry-panel" id="inquiry-panel" tabindex="-1"><h2>A witness at the waterline</h2><p>One mark before the flood. Another after. The frog here has been waiting for someone to ask when the accounts were made.</p>${read("stamps")}<button class="secondary" data-inquiry="testimony" data-choice="0" ${error ? "disabled" : ""}>Examine the two flood marks</button>${error ? `<p class="small-note">${e(error)}</p>` : ""}</section>`;
  }
  if (here === "binah")
    return `<aside class="atlas-callout"><h2>The room of several readings</h2><p>The librarian has left space between the accounts. A museum object, a community’s knowledge and a researcher’s interpretation are different kinds of evidence.</p>${read("kanaga")}${read("dogon-restudy")}</aside>`;
  return "";
}
export function atlasTravel(w: World, s: Seeker, to: SefirahId) {
  const steps = route(s, to);
  if (!steps) return null;
  if (steps.length < 2)
    return { label: "Read the encounter here", action: null };
  const next = steps[1];
  return status(w, s, next) === "dark"
    ? {
        label: "Sit to clear the next stream",
        action: { type: "sit" as const },
      }
    : {
        label: "Walk to " + NODES[next].pond,
        action: { type: "walk" as const, to: next },
      };
}
