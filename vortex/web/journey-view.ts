import type { Seeker } from "./session.ts";
import { revealed, riteCount } from "./session.ts";
import { CONTENT } from "./content.ts";
import { rareAt } from "./rares.ts";
import { completedStories, STORIES } from "./stories.ts";
import { TABLET_CHOICES, GATE_CHOICES } from "./inquiries.ts";
import type { SefirahId } from "./lattice.ts";
import { escapeHtml as e } from "./safety.ts";

// Reframe the existing illustration; original token artwork remains intact.
const SHORES: Record<SefirahId, { position: string; accent: string }> = {
  keter: { position: "100% 15%", accent: "#ebd59b" },
  chokhmah: { position: "0% 35%", accent: "#9dcbd5" },
  binah: { position: "30% 15%", accent: "#c1bfdb" },
  chesed: { position: "20% 45%", accent: "#b8dcaa" },
  gevurah: { position: "78% 35%", accent: "#dcab90" },
  tiferet: { position: "62% 50%", accent: "#e6ce87" },
  netzach: { position: "42% 75%", accent: "#a9d4b3" },
  hod: { position: "8% 70%", accent: "#d9b596" },
  yesod: { position: "55% 85%", accent: "#a7cadb" },
  malkhut: { position: "95% 75%", accent: "#d5ceaa" },
};

export function chapterProgress(s: Seeker): string {
  const items: { label: string; count: number; goal: number }[] =
    s.festival !== null
      ? [
          { label: "Rites", count: riteCount(s), goal: 10 },
          {
            label: "Stories home",
            count: completedStories(s).length,
            goal: 10,
          },
          { label: "Streams revealed", count: revealed(s), goal: 22 },
        ]
      : s.rooted
        ? [
            {
              label: "Stories home",
              count: completedStories(s).length,
              goal: 3,
            },
            { label: "Streams revealed", count: revealed(s), goal: 4 },
          ]
        : [
            { label: "Sigil made", count: Number(!!s.sigil), goal: 1 },
            { label: "Temples visited", count: s.visited.length, goal: 6 },
            { label: "Rites", count: riteCount(s), goal: 4 },
          ];
  return `<ul class="chapter-progress" aria-label="${s.festival !== null ? "Further exploration" : "Chapter progress"}">${items
    .map(
      ({ label, count, goal }) =>
        `<li class="${count >= goal ? "done" : ""}"><span class="progress-check" aria-hidden="true">${count >= goal ? "✓" : "○"}</span><span>${e(label)}</span><strong>${Math.min(count, goal)}/${goal}</strong></li>`,
    )
    .join("")}</ul>`;
}

export function templeScene(s: Seeker): string {
  const c = CONTENT[s.current],
    r = rareAt(s.current),
    shore = SHORES[s.current];
  const choice =
    s.current === "hod" && s.inquiries.tablet !== null
      ? TABLET_CHOICES[s.inquiries.tablet]
      : s.current === "netzach" && s.inquiries.gate !== null
        ? GATE_CHOICES[s.inquiries.gate]
        : s.stories[s.current]?.resolution != null
          ? STORIES[s.current].endings[s.stories[s.current]!.resolution!]
          : s.rites[s.current] !== undefined
            ? c.rite.choices[s.rites[s.current]!]
            : null;
  return `<div class="temple-scene" style="--shore-position:${shore.position};--shore-accent:${shore.accent}">
    <img class="scene-panorama" src="/nile-world.jpg" width="1672" height="941" alt="A detail of the illustrated Nile temple, a VORTEX interpretation">
    <div class="scene-inscription"><span>${choice ? "YOUR CHOICE LIVES HERE" : "A SMALL PROBLEM AT THIS SHORE"}</span><strong>${e(choice ?? c.rite.name)}</strong>${choice ? "<small>The temple remembers.</small>" : "<small>Look around, then choose a rite.</small>"}</div>
    ${s.looked.includes(s.current) ? `<button class="scene-token" data-rare="${r.name}" aria-label="Inspect original ${r.name} artwork and token record"><img src="${r.image}" width="400" height="560" alt="Original ${r.name} artwork"><span>${r.name} ↗</span><small>ORIGINAL RARE PEPE</small></button>` : ""}
  </div>`;
}
