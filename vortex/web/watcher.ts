import type { Seeker, World } from "./session.ts";
import { status } from "./session.ts";
import { neighbors } from "./lattice.ts";

/** Silent referee. Never shown as speech. Guides must not quote it. */
export type WatcherDirective = "haste" | "tilt" | "thin" | "still";

export type WatcherSense = {
  directive: WatcherDirective;
  /** Water copy. Never "the Watcher". */
  water: string;
  /** Compass pressure. Empty string means leave the compass alone. */
  pressure: string;
  darkSoon: boolean;
};

/**
 * Deterministic authored referee. Same inputs → same directive.
 * A hosted model may later *choose among these four* after a player opt-in.
 * It must never invent a fifth, never return prose for the UI, and never run
 * on page load.
 */
export function authoredDirective(world: World, s: Seeker): WatcherDirective {
  const open = neighbors(s.current).filter(
    (n) => status(world, s, n) === "open",
  );
  if (s.walks >= 2 && open.length > 1) return "haste";
  const lean = Math.abs(s.pillars.mercy - s.pillars.severity);
  if (lean >= 0.35 && s.pillars.balance < 0.2) return "tilt";
  if (s.visited.length >= 3 && s.looked.length * 2 < s.visited.length)
    return "thin";
  return "still";
}

function copyFor(directive: WatcherDirective, s: Seeker) {
  if (directive === "haste")
    return {
      water: "The current is running ahead of you. One stream may still.",
      pressure: "Sit, or choose the next shore with care.",
    };
  if (directive === "tilt")
    return {
      water:
        s.pillars.mercy > s.pillars.severity
          ? "Mercy is loud. Severity has gone quiet."
          : "Severity is loud. Mercy has gone quiet.",
      pressure: "A rest at this office steadies all three pillars.",
    };
  if (directive === "thin")
    return {
      water: "You have passed shores without looking. They remain thin.",
      pressure: "Look at this shore before you leave it.",
    };
  return { water: "", pressure: "" };
}

export function senseWatcher(
  world: World,
  s: Seeker,
  override?: WatcherDirective | null,
): WatcherSense {
  const authored = authoredDirective(world, s);
  const directive =
    override === "haste" ||
    override === "tilt" ||
    override === "thin" ||
    override === "still"
      ? override
      : authored;
  const copy = copyFor(directive, s);
  return {
    directive,
    water: copy.water,
    pressure: copy.pressure,
    // Gameplay darkness stays authored. Hosted enum may only change water copy.
    darkSoon: authored === "haste",
  };
}
