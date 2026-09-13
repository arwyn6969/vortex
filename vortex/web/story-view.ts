import type { Seeker } from "./session.ts";
import { revealed } from "./session.ts";
import { IDS, NODES } from "./lattice.ts";
import type { SefirahId } from "./lattice.ts";
import { rareAt } from "./rares.ts";
import { CONTENT } from "./content.ts";
import { PATH_LETTERS } from "./paths.ts";
import {
  STORIES,
  activeStories,
  completedStories,
  storyStage,
  readyForFestival,
  FESTIVAL_CHOICES,
  FESTIVAL_ENDINGS,
  festivalGuests,
} from "./stories.ts";
import { escapeHtml as e } from "./safety.ts";
import { boardingView } from "./boarding-view.ts";
import type { BoardingDraft } from "./boarding.ts";
export function storyPanel(
  s: Seeker,
  tracked?: SefirahId | null,
  aftermathInScene = false,
  boarding: BoardingDraft = {},
): string {
  const local = s.current,
    r = rareAt(local),
    p = s.stories[local],
    story = STORIES[local];
  const deliveries = activeStories(s).filter(
    (id) => STORIES[id].destination === local && !s.stories[id]!.delivered,
  );
  const incoming = deliveries
    .map((id) => {
      const from = rareAt(id),
        progress = s.stories[id]!;
      return `<section class="delivery-card" id="story-${id}" tabindex="-1"><div class="eyebrow">AN ERRAND FOR ${from.name}</div><h2>${e(STORIES[id].title)}</h2><p>You brought ${e(STORIES[id].cargo[progress.choice])}.</p><p>${s.rites[local] === undefined ? "Look around and complete this temple's rite, then make the delivery." : "The temple remembers your choice: “" + e(CONTENT[local].rite.choices[s.rites[local]!]) + "”. Bring that experience to this meeting."}</p>${id === "tiferet" && s.rites[local] !== undefined ? boardingView(s, boarding) : `<button class="primary" data-deliver="${id}" ${s.rites[local] === undefined ? "disabled" : ""}>Make the delivery</button>`}</section>`;
    })
    .join("");
  if (!s.looked.includes(local)) return incoming;
  const stage = storyStage(s, local);
  const path = PATH_LETTERS.find(
    (p) => (p.from === local || p.to === local) && (s.crossings[p.id] ?? 0) > 1,
  );
  let body = "";
  if (stage === "complete")
    body = `${aftermathInScene ? "" : `<p class="story-aftermath">${e(story.aftermath[p!.resolution!])}</p>`}<p class="small-note">Your choice: ${e(story.endings[p!.resolution!])}. This stays in Stories even after older journal entries fade.</p>`;
  else if (stage === "deliver")
    body = `<p>You are carrying ${e(story.cargo[p!.choice])}.</p><p>Next stop: <strong>${e(NODES[story.destination].pond)}</strong>. Complete its rite and make the delivery, then return here.</p><button class="secondary" data-track="${local}">Follow this story</button>`;
  else if (stage === "return")
    body = `<p>${e(story.returnPrompt)}</p>${path ? `<p class="stream-echo">On the return, ${path.letter} has taught you: ${e(path.meaning)}</p>` : ""}<div class="story-choices">${story.endings.map((choice, i) => `<button class="rite-choice" data-resolve="${local}" data-choice="${i}">${e(choice)}<span aria-hidden="true">↗</span></button>`).join("")}</div>`;
  else
    body = `<p>${e(story.request)}</p>${s.rites[local] === undefined ? '<p class="small-note">Complete the local rite to begin this story.</p>' : `<p class="story-memory">Last time, you chose “${e(CONTENT[local].rite.choices[s.rites[local]!])}”. ${e(CONTENT[local].rite.outcomes[s.rites[local]!])}</p><p class="small-note">Choose what to carry to ${e(NODES[story.destination].pond)}. Return here after the delivery.</p><div class="story-choices">${story.choices.map((choice, i) => `<button class="rite-choice" data-story-start="${local}" data-choice="${i}" ${activeStories(s).length >= 3 ? "disabled" : ""}>${e(choice)}<span aria-hidden="true">↗</span></button>`).join("")}</div>${activeStories(s).length >= 3 ? "<p>Three frogs are already counting on you. Bring one story home before accepting another.</p>" : ""}`}`;
  return (
    incoming +
    `<details class="story-card" id="story-${local}" ${stage === "return" || tracked === local ? "open" : ""}><summary><img src="${r.image}" width="64" height="88" alt=""><span><small>${r.name} · ${stage === "complete" ? "A STORY BROUGHT HOME" : stage === "return" ? "READY TO COME HOME" : "UNFINISHED BUSINESS"}</small><strong>${e(story.title)}</strong></span><span aria-hidden="true">＋</span></summary><div class="story-body">${body}<button class="text-button" data-rare="${r.name}">Inspect the original ${r.name} artwork ↗</button></div></details>`
  );
}
export function festivalPanel(s: Seeker): string {
  if (!s.rooted || s.current !== "malkhut") return "";
  const completed = completedStories(s).length;
  return `<section class="festival-card" id="festival" tabindex="-1"><div class="eyebrow">CHAPTER II · THE NILE REMEMBERS</div><h2>${s.festival === null ? "A festival made of small promises" : ["The long table", "The river of lanterns", "The unfinished chorus"][s.festival]}</h2>${
    s.festival !== null
      ? `<p>${e(FESTIVAL_ENDINGS[s.festival])}</p><p class="festival-mark">“${e(s.sigil)}”</p><details><summary>The guests remember your choices</summary>${festivalGuests(
          s,
        )
          .map((line) => `<p>${e(line)}</p>`)
          .join(
            "",
          )}</details><button class="secondary" data-view="stories">Keep exploring the stories</button>`
      : `<p>The frogs you helped have started arriving. The celebration grows from the promises you brought back, and the streams you came to understand.</p><div class="requirements"><span class="${completed >= 3 ? "done" : ""}">${Math.min(completed, 3)}/3 stories brought home</span><span class="${revealed(s) >= 4 ? "done" : ""}">${Math.min(revealed(s), 4)}/4 streams revealed</span></div>${readyForFestival(s) ? `<p>How will this Nile remember your journey?</p>${FESTIVAL_CHOICES.map((label, i) => `<button class="rite-choice" data-festival="${i}">${e(label)}<span aria-hidden="true">↗</span></button>`).join("")}` : '<button class="secondary" data-view="stories">Find your next story</button>'}`
  }</section>`;
}
export function storyBook(s: Seeker): string {
  const completed = completedStories(s),
    active = activeStories(s);
  const ordered = [
    ...active,
    ...IDS.filter((id) => !active.includes(id) && !completed.includes(id)),
    ...completed,
  ];
  return `<main id="main" class="collection story-book"><div class="collection-title"><div><div class="eyebrow">REAL RARES · FICTIONAL ADVENTURES · YOUR CONSEQUENCES</div><h1>The Nile remembers</h1><p>Carry a request to another temple, make the delivery, then return to decide what lasts. Up to three unfinished stories at once.</p></div><div class="big-stat">${completed.length}<span>/ 10 BROUGHT HOME</span></div></div><div class="chapter-strip"><strong>${s.festival !== null ? "The festival lives on" : s.rooted ? "Chapter II · Prepare the Nile festival" : "Chapter I · Carry your mark home"}</strong><span>${s.rooted ? `${Math.min(completed.length, 3)}/3 stories · ${Math.min(revealed(s), 4)}/4 streams revealed` : "Root your journey at Kingdom to open the next chapter. Stories can begin now."}</span></div><div class="story-grid">${ordered
    .map((id) => {
      const r = rareAt(id),
        story = STORIES[id],
        p = s.stories[id],
        stage = storyStage(s, id);
      const target = stage === "deliver" ? story.destination : id;
      const labels = {
        unmet: "COMPLETE THE TEMPLE RITE",
        available: "READY TO BEGIN",
        deliver: "CARRYING AN ERRAND",
        return: "READY TO RETURN",
        complete: "BROUGHT HOME",
      };
      return `<article class="story-ledger ${stage}"><div class="story-ledger-top"><button data-rare="${r.name}" class="story-token" aria-label="Inspect original ${r.name}"><img src="${r.image}" width="80" height="112" alt="Original ${r.name} artwork" loading="lazy"></button><div><small>${labels[stage]}</small><h2>${e(story.title)}</h2><span>${r.name}</span></div></div><p>${e(stage === "complete" ? story.aftermath[p!.resolution!] : stage === "deliver" ? "You are carrying " + story.cargo[p!.choice] + "." : stage === "return" ? story.returnPrompt : story.request)}</p><div class="story-route">${e(NODES[id].pond)} → ${e(NODES[story.destination].pond)} → home</div>${stage !== "complete" ? `<button class="secondary" data-track="${id}">${s.current === target ? "Continue here" : "Follow this story"} ↗</button>` : `<p class="small-note">Your lasting choice: ${e(story.endings[p!.resolution!])}</p>`}</article>`;
    })
    .join(
      "",
    )}</div><p class="archive-note">These adventures use the ten existing tokens in the Rare archive. Story props, deliveries, and festival outcomes belong to the game; no tokens change hands.</p></main>`;
}
