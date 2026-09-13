import type { Seeker } from "./session.ts";

export const PASSENGERS = [
  {
    id: "novices",
    name: "Two quiet novices",
    seats: 2,
    clue: "They will board only with the apprentice who knows the channel.",
  },
  {
    id: "apprentice",
    name: "The ferryman’s apprentice",
    seats: 1,
    clue: "Promises to stay beside the novices for their first crossing.",
  },
  {
    id: "cook",
    name: "The temple cook",
    seats: 1,
    clue: "Can take either sailing. Has packed enough soup for both.",
  },
  {
    id: "drummer",
    name: "The drummer and the drum machine",
    seats: 2,
    clue: "Together they take two places. The machine will not fit on anyone’s lap.",
  },
] as const;
export type PassengerId = (typeof PASSENGERS)[number]["id"];
export type BoardingPlan = Record<PassengerId, 0 | 1>;
export type BoardingDraft = Partial<BoardingPlan>;
export const boardingHelper = (s: Seeker) =>
  s.stories.chesed?.resolution != null;
export const suggestedBoarding = (): BoardingPlan => ({
  novices: 0,
  apprentice: 0,
  cook: 1,
  drummer: 1,
});
export function boardingSeats(plan: BoardingDraft): [number, number] {
  const counts: [number, number] = [0, 0];
  for (const p of PASSENGERS) {
    const trip = plan[p.id];
    if (trip === 0 || trip === 1) counts[trip] += p.seats;
  }
  return counts;
}
/** Validate the full manifest before the existing delivery can consume a turn. */
export function boardingError(plan: unknown, approach: number): string | null {
  if (!plan || typeof plan !== "object" || Array.isArray(plan))
    return "Choose a sailing for all four passenger tickets.";
  const p = plan as BoardingDraft;
  if (
    Object.keys(p).length !== PASSENGERS.length ||
    PASSENGERS.some(
      ({ id }) => !Object.hasOwn(p, id) || (p[id] !== 0 && p[id] !== 1),
    )
  )
    return "Choose each passenger ticket exactly once, on the first or second sailing.";
  const [first, second] = boardingSeats(p);
  if (first > 3 || second > 3)
    return `The ${first > 3 ? "first" : "second"} sailing has ${first > 3 ? first : second} passengers’ places filled, but the boat holds three. Move a ticket to the other sailing.`;
  if (p.novices !== p.apprentice)
    return "The novices need the apprentice beside them. Put their tickets on the same sailing.";
  if (approach === 0 && p.novices !== 0)
    return "Your guest list promised the quiet novices the first crossing. Keep that promise in the plan.";
  return null;
}
