import { NODES, neighbors, place, isOffice, guideName } from "./lattice.ts";
import type { Pillar, Dialect, SefirahId, StreamStatus } from "./lattice.ts";
import { PATH_LETTERS, pathKey, pathBetween } from "./paths.ts";
import { CONTENT } from "./content.ts";
import { safeText } from "./safety.ts";

export type Entry = {
  turn: number;
  office: SefirahId;
  kind: "world" | "guide" | "discovery";
  text: string;
  speaker?: string;
};
export type Challenge = {
  address: string;
  message: string;
  nonce: string;
  issuedAt: number;
  expiresAt: number;
  seekerId: string;
};
export type Proof = Challenge & { signature: string; verifiedAt: number };
export type Seeker = {
  id: string;
  name: string;
  dialect: Dialect;
  current: SefirahId;
  pillars: Record<Pillar, number>;
  visited: SefirahId[];
  looked: SefirahId[];
  rested: SefirahId[];
  rites: Partial<Record<SefirahId, number>>;
  crossings: Record<string, number>;
  harmony: boolean;
  sigil: string;
  rooted: boolean;
  walks: number;
  turns: number;
  conversations: number;
  journal: Entry[];
  challenge: Challenge | null;
  proof: Proof | null;
  createdAt: number;
};
export type World = {
  version: 3;
  revision: number;
  clock: number;
  activeId: string | null;
  seekers: Seeker[];
  darkness: Record<string, number>;
};
export type Action =
  | { type: "walk"; to: SefirahId }
  | { type: "look" | "sit" | "root" }
  | { type: "rite"; choice: number }
  | { type: "sigil"; text: string }
  | { type: "talk"; text: string }
  | { type: "dialect"; dialect: Dialect };
export const emptyWorld = (): World => ({
  version: 3,
  revision: 0,
  clock: 0,
  activeId: null,
  seekers: [],
  darkness: {},
});
export const activeSeeker = (w: World) =>
  w.seekers.find((s) => s.id === w.activeId) ?? null;
export const riteCount = (s: Seeker) => Object.keys(s.rites).length;
export const readyToRoot = (s: Seeker) =>
  !!s.sigil && s.visited.length >= 6 && riteCount(s) >= 4;
export const isBound = (s: Seeker) => readyToRoot(s) && !!s.proof;
export function addSeeker(
  world: World,
  name: string,
  dialect: Dialect,
  pillars: Record<Pillar, number>,
  now = Date.now(),
  id: string = crypto.randomUUID(),
): World {
  if (world.seekers.length >= 12)
    throw new Error(
      "This tree holds 12 seekers. Export a journey before removing one.",
    );
  name = safeText(name, 32, 2);
  if (
    world.seekers.some(
      (s) =>
        s.name.toLocaleLowerCase() === name.toLocaleLowerCase() || s.id === id,
    )
  )
    throw new Error(
      "That seeker already has a place here. Choose them from Journeys.",
    );
  if (
    !["classical", "folk"].includes(dialect) ||
    !/^[A-Za-z0-9_-]{1,80}$/.test(id)
  )
    throw new Error("Invalid seeker identity.");
  if (
    ["mercy", "severity", "balance"].some((p) => {
      const n = pillars[p as Pillar];
      return !Number.isFinite(n) || n < 0 || n > 1;
    })
  )
    throw new Error("Invalid pillar scores.");
  const current = place(pillars, dialect === "folk").node.id;
  const s: Seeker = {
    id,
    name,
    dialect,
    current,
    pillars: { ...pillars },
    visited: [current],
    looked: [],
    rested: [],
    rites: {},
    crossings: {},
    harmony: false,
    sigil: "",
    rooted: false,
    walks: 0,
    turns: 0,
    conversations: 0,
    journal: [],
    challenge: null,
    proof: null,
    createdAt: now,
  };
  record(s, "world", CONTENT[current].scene);
  record(s, "guide", voice(s));
  return {
    ...world,
    revision: world.revision + 1,
    activeId: id,
    seekers: [...world.seekers, s],
  };
}
export function status(world: World, s: Seeker, to: SefirahId): StreamStatus {
  if (to === s.current || !neighbors(s.current).includes(to)) return "missing";
  if (to === "keter" && !s.harmony) return "veiled";
  if (
    pathBetween(s.current, to)?.letter === "Qoph" &&
    !s.looked.includes("netzach")
  )
    return "veiled";
  if ((world.darkness[pathKey(s.current, to)] ?? 0) > world.clock)
    return "dark";
  return "open";
}
export function record(s: Seeker, kind: Entry["kind"], text: string) {
  s.journal.push({
    turn: s.turns,
    office: s.current,
    kind,
    text,
    ...(kind === "guide"
      ? { speaker: guideName(NODES[s.current], s.dialect) }
      : {}),
  });
  s.journal = s.journal.slice(-80);
}
export function voice(s: Seeker) {
  const c = CONTENT[s.current];
  return s.dialect === "folk" && NODES[s.current].folkGuide
    ? c.folk
    : c.classical;
}
function harmony(s: Seeker) {
  if (
    s.current === "tiferet" &&
    s.pillars.mercy >= 0.25 &&
    s.pillars.severity >= 0.25 &&
    !s.harmony
  ) {
    s.harmony = true;
    record(
      s,
      "discovery",
      "Two currents meet without losing themselves. Above the heart, the Crown takes a name.",
    );
  }
}
function guideReply(s: Seeker, question: string) {
  const q = question.toLocaleLowerCase();
  const folk = s.dialect === "folk" && !!NODES[s.current].folkGuide;
  if (/key|seed|wallet|bitcoin|bound|signature/.test(q))
    return "An address may be a name on the door. Your wallet keeps its keys. Kingdom can wait; your journey is already yours.";
  if (/lost|where|help|next|stuck/.test(q)) {
    if (!s.looked.includes(s.current))
      return folk
        ? "Start small. Look at what’s actually here."
        : "Before choosing the next shore, attend to the one beneath your feet.";
    if (s.rites[s.current] === undefined)
      return (
        "There is a small piece of work here: " +
        CONTENT[s.current].rite.name.toLowerCase() +
        ". Give it your attention."
      );
    if (!s.sigil && neighbors(s.current).includes("hod"))
      return folk
        ? "You’ve got something worth saying. The ink is waiting next door."
        : "Carry a few words to the ink at Hod. Let them take a shape.";
    return "A return can teach what a first crossing cannot. Follow a stream you have walked once, or take a moment to Sit.";
  }
  if (/sad|tired|afraid|overwhelm|anxious|rest/.test(q))
    return folk
      ? "Nothing here needs you to push through. Sit. The tree will still be here."
      : "Set down what you can. You do not owe the water a performance.";
  if (/sigil|word|name|create/.test(q))
    return s.sigil
      ? "You chose “" +
          s.sigil +
          "”. What would those words look like as a small act tomorrow?"
      : "At Hod, a few words can become a mark. Choose a phrase that belongs to your life, not a secret.";
  if (/remember|journey|done|return/.test(q))
    return (
      "You have stood in " +
      s.visited.length +
      " offices and completed " +
      riteCount(s) +
      " rites. " +
      (s.harmony
        ? "The heart remembers your meeting of the pillars."
        : "There is still room for the two currents to meet.")
    );
  const refrains = [
    voice(s),
    "What would that thought ask of you in an ordinary day?",
    "Hold that beside " +
      CONTENT[s.current].rite.name.toLowerCase() +
      ". What becomes clearer?",
  ];
  return refrains[s.conversations % refrains.length];
}
export function transition(world: World, action: Action): World {
  if (
    ![
      "walk",
      "look",
      "sit",
      "root",
      "rite",
      "sigil",
      "talk",
      "dialect",
    ].includes(action.type)
  )
    throw new Error("Unknown action.");
  const next = structuredClone(world);
  const s = activeSeeker(next);
  if (!s) throw new Error("Choose a seeker first.");
  if (action.type === "walk") {
    const state = status(world, s, action.to);
    if (state !== "open")
      throw new Error(
        state === "dark"
          ? "That stream is dark. Sit, or take another."
          : state === "veiled"
            ? action.to === "keter"
              ? "Mercy and Severity must both stand in the heart before Crown opens."
              : "Look at Boundaries Pond to discover this stream."
            : "No stream leads there from this shore.",
      );
  }
  if (
    action.type === "rite" &&
    (!s.looked.includes(s.current) ||
      !Number.isInteger(action.choice) ||
      action.choice < 0 ||
      action.choice > 2 ||
      s.rites[s.current] !== undefined)
  )
    throw new Error("Look first. Each office offers one rite per journey.");
  if (
    action.type === "sigil" &&
    (s.current !== "hod" || s.rites.hod === undefined)
  )
    throw new Error("Complete the rite at Hod before making your sigil.");
  if (
    action.type === "root" &&
    (s.current !== "malkhut" || !readyToRoot(s) || s.rooted)
  )
    throw new Error(
      "Bring a sigil, six visited offices, and four completed rites to Kingdom.",
    );
  const text =
    action.type === "sigil"
      ? safeText(action.text, 80, 3)
      : action.type === "talk"
        ? safeText(action.text, 500)
        : "";
  if (
    action.type === "dialect" &&
    !["classical", "folk"].includes(action.dialect)
  )
    throw new Error("Unknown guide dialect.");
  if (action.type === "dialect") {
    s.dialect = action.dialect;
    record(s, "guide", voice(s));
    next.revision++;
    return next;
  }
  next.clock++;
  next.revision++;
  s.turns++;
  for (const [edge, until] of Object.entries(next.darkness))
    if (until <= next.clock) delete next.darkness[edge];
  if (action.type === "walk") {
    const path = pathBetween(s.current, action.to)!;
    s.current = action.to;
    s.walks = Math.min(3, s.walks + 1);
    if (!s.visited.includes(s.current)) s.visited.push(s.current);
    s.crossings[path.id] = (s.crossings[path.id] ?? 0) + 1;
    const n = s.crossings[path.id];
    record(
      s,
      n <= 2 ? "discovery" : "world",
      n === 1
        ? path.letter +
            " · " +
            path.title +
            ". A first crossing. Its meaning has not yet settled."
        : n === 2
          ? path.letter + " reveals its meaning: " + path.meaning
          : "You return by " + path.letter + ". The water remembers.",
    );
    record(s, "world", CONTENT[s.current].scene);
    record(s, "guide", voice(s));
    // Silent deterministic referee. A shared edge darkens only if another way remains.
    const choices = neighbors(s.current).filter(
      (n) => status(next, s, n) === "open",
    );
    if (s.walks >= 3 && choices.length > 1) {
      next.darkness[pathKey(s.current, choices[next.clock % choices.length])] =
        next.clock + 3;
      record(
        s,
        "world",
        "One of the streams dims. The water beside you becomes very still.",
      );
      s.walks = 0;
    }
  } else if (action.type === "look") {
    if (!s.looked.includes(s.current)) s.looked.push(s.current);
    s.walks = 0;
    record(s, "world", CONTENT[s.current].detail);
    if (s.current === "netzach")
      record(
        s,
        "discovery",
        "A descent at your back has become visible. Qoph waits below the reeds.",
      );
  } else if (action.type === "sit") {
    next.darkness = {};
    s.walks = 0;
    if (!s.rested.includes(s.current)) {
      s.rested.push(s.current);
      for (const p of ["mercy", "severity", "balance"] as Pillar[])
        s.pillars[p] = Math.min(1, s.pillars[p] + 0.08);
    }
    record(
      s,
      "world",
      "You let a breath arrive without reaching for it. Across the tree, the dark water clears.",
    );
  } else if (action.type === "rite") {
    s.rites[s.current] = action.choice;
    const p = NODES[s.current].pillar;
    s.pillars[p] = Math.min(1, s.pillars[p] + 0.14);
    record(
      s,
      "discovery",
      CONTENT[s.current].rite.name +
        " · " +
        CONTENT[s.current].rite.outcomes[action.choice],
    );
  } else if (action.type === "sigil") {
    if (s.sigil !== text) {
      s.proof = null;
      s.challenge = null;
      s.rooted = false;
    }
    s.sigil = text;
    record(s, "discovery", "Your sigil takes its shape: “" + text + "”.");
  } else if (action.type === "root") {
    s.rooted = true;
    record(
      s,
      "discovery",
      "ROOTED · Your mark has reached the floor of the world. The journey is complete, and the paths remain open. What comes next belongs to you.",
    );
  } else if (action.type === "talk") {
    // Only the authored response is retained. Raw personal questions are not saved.
    record(s, "guide", guideReply(s, text));
    s.conversations++;
  }
  harmony(s);
  return next;
}
export const discovered = (s: Seeker) =>
  PATH_LETTERS.filter((p) => (s.crossings[p.id] ?? 0) > 0).length;
export const revealed = (s: Seeker) =>
  PATH_LETTERS.filter((p) => (s.crossings[p.id] ?? 0) > 1).length;
export function objective(s: Seeker): string {
  if (s.rooted)
    return "The path remains open. Return to a stream and let its meaning deepen.";
  if (!s.looked.includes(s.current))
    return "Look closely. Every office holds something a passing glance will miss.";
  if (s.rites[s.current] === undefined)
    return "Complete " + CONTENT[s.current].rite.name.toLowerCase() + ".";
  if (!s.harmony)
    return "Let both pillars grow, then return to the heart at Vibe Temple.";
  if (!s.sigil)
    return "Find the ink at Meme Studio (Hod), and give your journey a sigil.";
  if (s.visited.length < 6 || riteCount(s) < 4)
    return "Carry your sigil through six offices and complete four rites.";
  if (s.current !== "malkhut")
    return "Take your mark to Kingdom. The floor of the world is waiting.";
  return "Root your journey here. A wallet signature is an optional second rite.";
}
