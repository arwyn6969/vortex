import type { Seeker } from "./session.ts";
import { completedStories } from "./stories.ts";
import { escapeHtml as e } from "./safety.ts";

type WorldDetail = {
  kind: "desk" | "gate" | "gathering" | "boat";
  variant: number;
  title: string;
  caption: string;
};
export function worldDetail(s: Seeker): WorldDetail | null {
  if (!s.looked.includes(s.current)) return null;
  if (s.current === "hod") {
    const variant = s.inquiries.tablet ?? -1;
    return {
      kind: "desk",
      variant,
      title:
        variant === -1
          ? "The scribe has left a space"
          : [
              "Two witnesses. Two inkpots.",
              "A record with its context",
              "Room for the next correction",
            ][variant],
      caption:
        variant === -1
          ? "Two accounts wait beside an empty writing board."
          : [
              "Both accounts have a place at the desk; neither witness has been erased.",
              "The dated flood marks sit beside the tablet you chose to corroborate.",
              "A loose clay tag keeps the provisional reading open to correction.",
            ][variant],
    };
  }
  if (s.current === "netzach") {
    const variant = s.inquiries.gate ?? -1;
    return {
      kind: "gate",
      variant,
      title:
        variant === -1
          ? "Two latches, one stubborn guardian"
          : [
              "The guest lane is open",
              "The keeper has company",
              "Someone brought a spare stool",
            ][variant],
      caption:
        variant === -1
          ? "The courtyard gate waits for an arrangement its keeper can live with."
          : [
              "Your agreed duty is posted beside the courtyard entrance.",
              "Two frogs work the courtyard latches together.",
              "A friend from your earlier kindness has made room for the waiting guests.",
            ][variant],
    };
  }
  if (s.current === "malkhut") {
    const variant = s.festival ?? -1;
    return {
      kind: "gathering",
      variant,
      title:
        variant === -1
          ? completedStories(s).length
            ? "Promises are becoming guests"
            : "A table waiting for a story"
          : [
              "The long table is set",
              "Lanterns follow the safe water",
              "There is room in the chorus",
            ][variant],
      caption: [
        s.inquiries.tablet === 0
          ? "Two witnesses share a reading place."
          : s.inquiries.tablet === 1
            ? "The flood marks have a place beside the programme."
            : s.inquiries.tablet === 2
              ? "A correction flap hangs from the programme."
              : "Every story brought home makes a little more room.",
        s.inquiries.gate === 2
          ? "Spare stools wait for the next arrival."
          : s.inquiries.gate === 1
            ? "The guardian arrives with a companion."
            : s.inquiries.gate === 0
              ? "The welcome has its terms written clearly."
              : "",
      ]
        .filter(Boolean)
        .join(" "),
    };
  }
  if (s.current === "tiferet" && s.stories.tiferet?.delivered)
    return {
      kind: "boat",
      variant: s.stories.tiferet.choice,
      title: "The river has room for a second sailing",
      caption:
        "The agreed crossing is now part of the shore. The apprentice, novices and very loud drum all came home.",
    };
  return null;
}

// Small original vector props, drawn from local choices. These are fictional
// scene illustrations, not token artwork or historical/cultural diagrams.
const frog = (x: number, y: number, color = "#95b781") =>
  `<g transform="translate(${x} ${y})"><ellipse cy="5" rx="16" ry="13" fill="${color}"/><circle cx="-9" cy="-6" r="7" fill="${color}"/><circle cx="9" cy="-6" r="7" fill="${color}"/><circle cx="-9" cy="-7" r="2" fill="#16352e"/><circle cx="9" cy="-7" r="2" fill="#16352e"/><path d="M-6 7 Q0 12 6 7" fill="none" stroke="#16352e" stroke-width="2"/></g>`;
const stool = (x: number, y: number) =>
  `<g transform="translate(${x} ${y})" stroke="#c3986a" stroke-width="5" fill="#d6b17c"><path d="M-12 0 -16 23 M12 0 16 23"/><ellipse rx="21" ry="6"/></g>`;
const tablet = (x: number, y: number, width = 65) =>
  `<g transform="translate(${x} ${y})"><rect width="${width}" height="68" rx="8" fill="#bc8661" stroke="#e0b18a" stroke-width="2"/><path d="M12 18h${width - 24}m-${width - 24} 12h${width - 30}m-${width - 30} 12h${width - 24}m-${width - 24} 12h${width - 33}" stroke="#654d3b" stroke-width="3" fill="none"/></g>`;
const water = `<path d="M0 153Q90 136 180 153T360 153T540 153T720 153M-60 168Q30 151 120 168T300 168T480 168T660 168" stroke="#407d80" stroke-width="2" fill="none" opacity=".7"/>`;
const boat = (x: number, y: number, people = 3) =>
  `<g transform="translate(${x} ${y})"><path d="M-74 5Q-53 48 61 16L80 0Q12 22-74 5Z" fill="#b68a55" stroke="#e6c38a" stroke-width="2"/>${Array.from({ length: people }, (_, i) => frog(-35 + i * 32, -4, i === 2 ? "#c8b475" : "#9cbe8a")).join("")}<path d="M15-51V12M15-47 56-6H15" fill="#dfd0a7" stroke="#dfd0a7" stroke-width="3"/></g>`;
function drawing(s: Seeker, model: WorldDetail): string {
  const v = model.variant;
  if (model.kind === "desk")
    return `<path d="M80 151H566M150 128v37m340-37v37" stroke="#735d46" stroke-width="8"/><rect x="102" y="106" width="438" height="24" rx="8" fill="#ad855b"/>${frog(142, 80)}${v === 0 ? frog(500, 80, "#c2ae7c") : ""}${tablet(v === 0 ? 236 : 278, 31)}${v === 0 ? tablet(330, 31) : v === -1 ? tablet(370, 39, 54) : ""}<path d="M182 101h25l-4-18h-17z" fill="#90acaa"/>${v === 0 ? '<path d="M432 101h25l-4-18h-17z" fill="#c29b7b"/>' : ""}${v === 1 ? '<path d="M374 38v61M364 57h40M364 79h40" stroke="#8ec3bd" stroke-width="4"/><circle cx="398" cy="57" r="4" fill="#e7d39b"/>' : ""}${v === 2 ? '<path d="M330 50l31 32" stroke="#eed5a6" stroke-width="2"/><path d="m351 69 53 7-6 32-53-7Z" fill="#e2c480"/><path d="m360 82 26 4m-28 7 19 3" stroke="#7c6845" stroke-width="3"/>' : ""}`;
  if (model.kind === "gate")
    return `<path d="M70 150H570" stroke="#8b8760" stroke-width="5"/><path d="M219 142V31h205v111" stroke="#c3af7b" stroke-width="15" fill="none"/><g stroke="#bc9363" stroke-width="6"><path d="${v === -1 ? "M236 44V140M267 44V140M298 44V140M329 44V140M360 44V140M391 44V140M236 88H402" : "M236 44 184 67V145L236 140M408 44 458 67V145L408 140"}" fill="none"/></g>${frog(480, 118)}${v === 1 ? frog(166, 118, "#b5c9a4") : ""}${v === 2 ? `${stool(154, 128)}${frog(155, 108, "#c5b787")}${stool(535, 128)}` : ""}${v === 0 ? '<path d="M150 70v74" stroke="#bb9160" stroke-width="5"/><rect x="117" y="57" width="68" height="46" rx="3" fill="#dcc99c"/><path d="M128 70h45m-45 11h37m-37 11h42" stroke="#756745" stroke-width="3"/>' : ""}${s.stories.tiferet?.delivered ? `<g transform="translate(0 32) scale(.5)">${boat(615, 202)}</g>` : ""}`;
  if (model.kind === "boat") return water + boat(210, 119) + boat(448, 119);
  const guests = Math.min(completedStories(s).length, 5);
  const people = Array.from({ length: guests }, (_, i) =>
    frog(181 + i * 63, 105, i % 2 ? "#bdad77" : "#91b28a"),
  ).join("");
  const witnesses =
    s.inquiries.tablet === 0
      ? `${tablet(84, 86, 44)}${tablet(132, 86, 44)}`
      : s.inquiries.tablet === 1
        ? tablet(100, 83, 52) +
          '<path d="M164 92v61m-7-44h25m-25 23h25" stroke="#8ec3bd" stroke-width="3"/>'
        : s.inquiries.tablet === 2
          ? tablet(100, 83, 52) +
            '<path d="m133 112 45 7-5 28-45-7Z" fill="#e2c480"/><path d="m139 123 25 4m-26 5 18 3" stroke="#7c6845" stroke-width="2"/>'
          : "";
  const chairs = s.inquiries.gate === 2 ? stool(82, 128) + stool(552, 128) : "";
  const display =
    v === 1
      ? water +
        Array.from(
          { length: 7 },
          (_, i) =>
            `<g class="river-lantern" transform="translate(${96 + i * 73} ${113 + (i % 2) * 25})"><ellipse rx="17" ry="5" fill="#b18958"/><path d="M-9-3V-22H9V-3Z" fill="#f3d18a"/><path d="M0-16v8" stroke="#ac683f" stroke-width="2"/></g>`,
        ).join("")
      : `<path d="M146 147H493M172 147v18m292-18v18" stroke="#ad855b" stroke-width="9"/>${v === 2 ? '<path d="M300 82v47m0-38 37-9v36" stroke="#d9c17e" stroke-width="4" fill="none"/><ellipse cx="290" cy="130" rx="10" ry="6" fill="#d9c17e"/><ellipse cx="327" cy="119" rx="10" ry="6" fill="#d9c17e"/>' : ""}`;
  const welcome =
    s.inquiries.gate === 0
      ? '<path d="M554 104v55" stroke="#bb9160" stroke-width="4"/><rect x="529" y="95" width="50" height="36" rx="3" fill="#dcc99c"/><path d="M537 104h34m-34 9h27m-27 9h31" stroke="#756745" stroke-width="2"/>'
      : "";
  return `${people}${display}${witnesses}${chairs}${welcome}${s.inquiries.gate === 1 ? frog(549, 108, "#bbbc91") : ""}`;
}
export function worldVignette(s: Seeker): string {
  const model = worldDetail(s);
  if (!model) return "";
  return `<figure class="world-vignette" data-world-detail="${model.kind}" data-variant="${model.variant}"><svg viewBox="0 0 640 190" role="img" aria-label="${e(model.title + ". " + model.caption)}"><path d="M40 167H600" stroke="#345247" stroke-width="2"/>${drawing(s, model)}</svg><figcaption><strong>${e(model.title)}</strong><span>${e(model.caption)}</span></figcaption></figure>`;
}
