import type { Seeker } from "./session.ts";
import type { SefirahId } from "./lattice.ts";
import { atlasEntry, ATLAS } from "./atlas.ts";

export type InquiryProgress = {
  seen: string[];
  testimony: boolean;
  tablet: number | null;
  gate: number | null;
};
export const emptyInquiries = (): InquiryProgress => ({
  seen: [],
  testimony: false,
  tablet: null,
  gate: null,
});
export type InquiryAction =
  | { type: "study"; entry: string }
  | { type: "inquiry"; task: "testimony" | "tablet" | "gate"; choice: number };
export const TABLET_CHOICES = [
  "Keep both accounts, with their witnesses",
  "Publish the corroborated account",
  "Publish a provisional reading",
];
export const TABLET_MEMORIES = [
  "Two accounts now share the tablet. Each has a witness and room for a reply. The scribe has bought a second inkpot and is coping heroically.",
  "The waterline witness has a place beside the tablet. The archive records what was checked, and which questions are still open.",
  "A small clay tag reads PROVISIONAL. The scribe can correct the account without pretending the earlier reading never existed.",
];
export const GATE_CHOICES = [
  "Negotiate a crossing and accept a duty",
  "Solve it together: ask the guardian to hold one latch",
  "Call on a friend made earlier",
];
export const GATE_MEMORIES = [
  "The guardian opens a guest lane. Your duty is to leave its terms readable for the next traveller; a neatly lettered sign now stands in the reeds.",
  "The guardian takes one latch, you take the other. The gate opens. Its keeper admits that guarding a door is easier with company.",
  "A friend arrives with a stool for the waiting queue. The guardian recognizes a kindness carried forward and makes room.",
];
export function inquiryError(s: Seeker, a: InquiryAction): string | null {
  const p = s.inquiries;
  if (a.type === "study")
    return !atlasEntry(a.entry)
      ? "That entry is not in this atlas."
      : p.seen.includes(a.entry)
        ? "That connection is already in your notebook."
        : null;
  if (!Number.isInteger(a.choice) || a.choice < 0 || a.choice > 2)
    return "Choose one of the offered replies.";
  if (a.task === "testimony")
    return a.choice !== 0 ||
      s.current !== "yesod" ||
      !s.looked.includes("yesod") ||
      !p.seen.includes("stamps") ||
      p.testimony
      ? "Study Bitcoin Stamps, then Look at Yesod to consult the waterline witness."
      : null;
  if (a.task === "tablet") {
    if (s.current !== "hod" || s.rites.hod === undefined || p.tablet !== null)
      return "The scribe needs you at Hod after its rite, before this tablet is settled.";
    if (!p.seen.includes("stamps") || !p.seen.includes("nisaba"))
      return "Read and remember the Stamps and Nisaba entries before weighing the two accounts.";
    if (a.choice === 1 && !p.testimony)
      return "Consult the witness at Yesod before claiming corroboration.";
    return null;
  }
  if (a.task === "gate") {
    if (
      s.current !== "netzach" ||
      s.rites.netzach === undefined ||
      p.gate !== null
    )
      return "Meet the guardian at Netzach after its rite, before this gate is settled.";
    if (
      a.choice === 1 &&
      !p.seen.includes("hero-twins") &&
      !p.seen.includes("neti")
    )
      return "Read and remember the Hero Twins or Neti to reconsider how this test works.";
    if (
      a.choice === 2 &&
      p.tablet !== 0 &&
      s.stories.chesed?.resolution == null
    )
      return "A friendship grows from keeping both witnesses in the tablet, or bringing Mercy’s story home.";
    return null;
  }
  return "Unknown encounter.";
}
export function applyInquiry(s: Seeker, a: InquiryAction): string {
  const error = inquiryError(s, a);
  if (error) throw new Error(error);
  if (a.type === "study") {
    s.inquiries.seen.push(a.entry);
    return "Remembered in your atlas: " + atlasEntry(a.entry)!.name + ".";
  }
  if (a.task === "testimony") {
    s.inquiries.testimony = true;
    return "The waterline witness shows two flood marks: one account was written before the water rose, the other afterwards. A preserved record needs its context.";
  }
  s.inquiries[a.task] = a.choice;
  return (a.task === "tablet" ? TABLET_MEMORIES : GATE_MEMORIES)[a.choice];
}
export function inquiryMemory(s: Seeker, office: SefirahId): string | null {
  const p = s.inquiries;
  if (office === "hod" && p.tablet !== null) return TABLET_MEMORIES[p.tablet];
  if (office === "netzach" && p.gate !== null) return GATE_MEMORIES[p.gate];
  if (office === "yesod" && p.tablet !== null)
    return p.tablet === 1
      ? "The waterline witness has become the archive’s most reluctant celebrity. Visitors now ask when an account was made before asking whether it endured."
      : "The witness has brought a small correction to the archive. Because your account left room for context, it has somewhere to go.";
  if (office === "chesed" && p.gate === 2)
    return "The friend you called on has returned the stool. Three more travellers have borrowed it. Mercy appears to have started a furniture library.";
  if (office === "malkhut" && (p.tablet !== null || p.gate !== null))
    return [
      p.tablet === null
        ? ""
        : [
            "At dinner, two witnesses share the reading table. Disagreement has a chair.",
            "The festival archivist shows the dated flood marks beside the account.",
            "The feast’s programme has a correction flap. It is already being used.",
          ][p.tablet],
      p.gate === null
        ? ""
        : [
            "New guests arrive carrying the terms of their welcome.",
            "The guardian has invited a companion. They open the doors together.",
            "A spare stool waits at every threshold; someone remembered your friend.",
          ][p.gate],
    ]
      .filter(Boolean)
      .join(" ");
  return null;
}
export function validInquiries(
  p: InquiryProgress,
  s: Pick<Seeker, "rites" | "looked" | "stories">,
): boolean {
  return (
    Array.isArray(p.seen) &&
    p.seen.length <= ATLAS.length &&
    new Set(p.seen).size === p.seen.length &&
    p.seen.every((id) => typeof id === "string" && !!atlasEntry(id)) &&
    typeof p.testimony === "boolean" &&
    [p.tablet, p.gate].every(
      (n) => n === null || (Number.isInteger(n) && n! >= 0 && n! <= 2),
    ) &&
    (!p.testimony ||
      (s.looked.includes("yesod") && p.seen.includes("stamps"))) &&
    (p.tablet === null ||
      (s.rites.hod !== undefined &&
        p.seen.includes("stamps") &&
        p.seen.includes("nisaba") &&
        (p.tablet !== 1 || p.testimony))) &&
    (p.gate === null ||
      (s.rites.netzach !== undefined &&
        (p.gate !== 1 ||
          p.seen.includes("hero-twins") ||
          p.seen.includes("neti")) &&
        (p.gate !== 2 ||
          p.tablet === 0 ||
          s.stories.chesed?.resolution != null)))
  );
}
