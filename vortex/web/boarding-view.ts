import { PASSENGERS, boardingSeats, boardingHelper } from "./boarding.ts";
import type { BoardingDraft } from "./boarding.ts";
import type { Seeker } from "./session.ts";
import { escapeHtml as e } from "./safety.ts";

export function boardingView(s: Seeker, draft: BoardingDraft = {}): string {
  const seats = boardingSeats(draft);
  return `<form id="boarding-form" class="boarding-puzzle" aria-labelledby="boarding-title">
    <span class="eyebrow">TRY THE CROSSING · AN OBSERVATION PUZZLE</span><h3 id="boarding-title">Six places. Two sailings. One very loud drum.</h3>
    <p>The crocodile counts volume. You can count passengers. Place each ticket on a sailing; the novices and their apprentice must travel together.</p>
    <ul class="boarding-rules"><li>Each sailing has three places. Everyone crosses once.</li><li>Keep each ticket together; the drum machine occupies a place.</li>${s.stories.tiferet?.choice === 0 ? "<li>Your promise: the quiet novices take the first crossing.</li>" : ""}</ul>
    <div class="boarding-boats" role="status" aria-label="Places on each sailing">${seats.map((n, trip) => `<div class="boarding-boat ${n > 3 ? "overfull" : ""}"><strong>${trip === 0 ? "First sailing" : "Second sailing"}</strong><span>${n}/3 places${n > 3 ? " · too full" : ""}</span><div class="boat-places" aria-hidden="true">${Array.from({ length: 3 }, (_, i) => `<i class="${i < n ? "occupied" : ""}"></i>`).join("")}</div></div>`).join("")}</div>
    <div class="boarding-tickets">${PASSENGERS.map((p) => `<fieldset class="boarding-ticket"><legend>${e(p.name)} <span>· ${p.seats} ${p.seats === 1 ? "place" : "places"}</span></legend><p>${e(p.clue)}</p><div>${[0, 1].map((trip) => `<label><input id="boarding-${p.id}-${trip}" type="radio" name="${p.id}" value="${trip}" data-passenger="${p.id}" ${draft[p.id] === trip ? "checked" : ""} required>${trip === 0 ? "First sailing" : "Second sailing"}</label>`).join("")}</div></fieldset>`).join("")}</div>
    ${boardingHelper(s) ? '<aside class="boarding-friend"><strong>A kindness comes back</strong><p>The cook you helped at Mercy recognizes you. “I can sit with the drummer. Give the novices someone they trust.”</p><button type="button" class="secondary" data-boarding-help>Ask the cook to lay out the tickets</button></aside>' : '<details id="boarding-hint"><summary>A nudge from the ferryman</summary><p>The two novices and their apprentice fill one sailing. Which tickets fill the other?</p></details>'}
    <div class="actions"><button class="primary" type="submit">Try this boarding plan</button><button class="text-button" type="button" data-boarding-reset>Start the plan again</button></div>
    <p class="small-note">You can rearrange the tickets freely. An unsuccessful plan uses no turn.</p>
  </form><button class="text-button" data-deliver="tiferet">Let the sphinx arrange the crossing</button><p class="small-note">Either way, everyone gets across and the story continues.</p>`;
}
