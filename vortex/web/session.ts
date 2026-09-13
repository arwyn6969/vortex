import {
  emptyInquiries,
  applyInquiry,
  inquiryError,
  inquiryMemory,
} from "./inquiries.ts";
import type { InquiryProgress, InquiryAction } from "./inquiries.ts";
import { NODES, neighbors, place, isOffice, guideName } from "./lattice.ts";
import type { Pillar, Dialect, SefirahId, StreamStatus } from "./lattice.ts";
import { PATH_LETTERS, pathKey, pathBetween } from "./paths.ts";
import { stampReply } from "./stamps.ts";
import { CONTENT } from "./content.ts";
import { safeText } from "./safety.ts";
import {
  STORIES,
  activeStories,
  completedStories,
  returnMemory,
  readyForFestival,
  FESTIVAL_ENDINGS,
  festivalGuests,
} from "./stories.ts";
import type { StoryProgress } from "./stories.ts";
import { rareAt } from "./rares.ts";
import { boardingError } from "./boarding.ts";
import type { BoardingPlan } from "./boarding.ts";

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
  stories: Partial<Record<SefirahId, StoryProgress>>;
  festival: number | null;
  inquiries: InquiryProgress;
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
  version: 5;
  revision: number;
  clock: number;
  activeId: string | null;
  seekers: Seeker[];
  darkness: Record<string, number>;
};
export type Action =
  | InquiryAction
  | { type: "walk"; to: SefirahId }
  | { type: "look" | "sit" | "root" }
  | { type: "rite"; choice: number }
  | { type: "story-start" | "story-resolve"; story: SefirahId; choice: number }
  | { type: "story-deliver"; story: SefirahId; boarding?: BoardingPlan }
  | { type: "festival"; choice: number }
  | { type: "sigil"; text: string }
  | { type: "talk"; text: string }
  | { type: "dialect"; dialect: Dialect };
export const emptyWorld = (): World => ({
  version: 5,
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
    stories: {},
    festival: null,
    inquiries: emptyInquiries(),
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
  if (/key|seed|wallet|bound|signature/.test(q))
    return "An address may be a name on the door. Your wallet keeps its keys. Kingdom can wait; your journey is already yours.";
  if (/stamp|kevin|immutable|immutability|egregore|bitcoin/.test(q))
    return stampReply(s.current, folk ? "folk" : "classical");
  if (/atlas|myth|tarot|sumer|maya|dogon|archetype/.test(q))
    return "Open the Living Atlas to compare stories, figures and real assets. Each connection explains its sources. At Hod the scribe has two accounts to weigh; at Netzach a guardian needs a different way of thinking.";
  if (/tablet|guardian|witness|changed|remember here|last time/.test(q))
    return (
      inquiryMemory(s, s.current) ??
      returnMemory(s, s.current) ??
      (s.rites[s.current] !== undefined
        ? "You chose “" +
          CONTENT[s.current].rite.choices[s.rites[s.current]!] +
          "”. " +
          CONTENT[s.current].rite.outcomes[s.rites[s.current]!]
        : "Look at this shore, then try its rite. A place begins to change when you give it your attention.")
    );
  if (/story|errand|festival|frog|pepe/.test(q)) {
    const id = activeStories(s)[0];
    if (id) {
      const p = s.stories[id]!;
      return p.delivered
        ? rareAt(id).name +
            " is waiting at " +
            NODES[id].pond +
            ". The errand is done; the important part is what you make of it together."
        : "You are carrying " +
            STORIES[id].cargo[p.choice] +
            " to " +
            NODES[STORIES[id].destination].pond +
            ". Look and complete the local rite, then make the delivery.";
    }
    return s.rooted
      ? "The Nile has another chapter: bring three stories home and reveal four streams, then return to Kingdom for the festival. The guests will remember your decisions."
      : "After a temple's rite, its Rare Pepe has a piece of unfinished business. Start a story here, or see who is waiting in Stories.";
  }
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
      "story-start",
      "story-deliver",
      "story-resolve",
      "festival",
      "study",
      "inquiry",
    ].includes(action.type)
  )
    throw new Error("Unknown action.");
  const next = structuredClone(world);
  const s = activeSeeker(next);
  if (!s) throw new Error("Choose a seeker first.");
  if (action.type === "study" || action.type === "inquiry") {
    const error = inquiryError(s, action);
    if (error) throw new Error(error);
    next.revision++;
    if (action.type === "inquiry") {
      next.clock++;
      s.turns++;
      s.walks = 0;
    }
    record(s, "discovery", applyInquiry(s, action));
    return next;
  }
  if (
    action.type === "story-start" ||
    action.type === "story-deliver" ||
    action.type === "story-resolve"
  ) {
    if (!isOffice(action.story))
      throw new Error("That story does not belong to this tree.");
    const id = action.story,
      story = STORIES[id],
      progress = s.stories[id];
    if (
      action.type !== "story-deliver" &&
      (!Number.isInteger(action.choice) ||
        action.choice < 0 ||
        action.choice > 2)
    )
      throw new Error("Choose one of the three replies.");
    if (
      action.type === "story-start" &&
      (s.current !== id ||
        s.rites[id] === undefined ||
        progress ||
        activeStories(s).length >= 3)
    )
      throw new Error(
        "Complete this temple's rite first. Carry at most three unfinished stories at a time.",
      );
    if (
      action.type === "story-deliver" &&
      (!progress ||
        progress.delivered ||
        s.current !== story.destination ||
        s.rites[s.current] === undefined)
    )
      throw new Error(
        "Bring the errand to its destination and complete the local rite before delivering it.",
      );
    if (
      action.type === "story-resolve" &&
      (!progress?.delivered || progress.resolution !== null || s.current !== id)
    )
      throw new Error(
        "Make the delivery, then return to the frog who asked for your help.",
      );
    if (action.type === "story-deliver" && Object.hasOwn(action, "boarding")) {
      if (id !== "tiferet")
        throw new Error(
          "The boarding plan belongs to the solar boat’s errand.",
        );
      const error = boardingError(action.boarding, progress!.choice);
      if (error) throw new Error(error);
    }
  }
  if (
    action.type === "festival" &&
    (s.current !== "malkhut" ||
      !readyForFestival(s) ||
      s.festival !== null ||
      !Number.isInteger(action.choice) ||
      action.choice < 0 ||
      action.choice > 2)
  )
    throw new Error(
      "Root your journey, bring three stories home, and reveal four streams before opening the festival at Kingdom.",
    );
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
    const memory = returnMemory(s, s.current);
    if (memory) record(s, "world", memory);
    const inquiry = inquiryMemory(s, s.current);
    if (inquiry) record(s, "world", inquiry);
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
  } else if (action.type === "story-start") {
    s.stories[action.story] = {
      choice: action.choice,
      delivered: false,
      resolution: null,
    };
    s.walks = 0;
    record(
      s,
      "discovery",
      rareAt(action.story).name +
        " · " +
        STORIES[action.story].title +
        ". You take " +
        STORIES[action.story].cargo[action.choice] +
        " to " +
        NODES[STORIES[action.story].destination].pond +
        ".",
    );
  } else if (action.type === "story-deliver") {
    const p = s.stories[action.story]!;
    p.delivered = true;
    s.walks = 0;
    record(s, "discovery", STORIES[action.story].delivery[p.choice]);
    if (action.boarding)
      record(
        s,
        "discovery",
        "Your boarding plan gives each sailing three places. The novices cross beside their apprentice. The crocodile checks the arithmetic twice and reluctantly waves you through.",
      );
    record(
      s,
      "world",
      "Your earlier choice here still stands: " +
        CONTENT[s.current].rite.outcomes[s.rites[s.current]!],
    );
  } else if (action.type === "story-resolve") {
    s.stories[action.story]!.resolution = action.choice;
    s.walks = 0;
    record(
      s,
      "discovery",
      STORIES[action.story].title +
        " · " +
        STORIES[action.story].aftermath[action.choice],
    );
  } else if (action.type === "festival") {
    s.festival = action.choice;
    record(s, "discovery", FESTIVAL_ENDINGS[action.choice]);
    for (const memory of festivalGuests(s)) record(s, "world", memory);
    const inquiry = inquiryMemory(s, "malkhut");
    if (inquiry) record(s, "world", inquiry);
  } else if (action.type === "sigil") {
    if (s.sigil !== text) {
      s.proof = null;
      s.challenge = null;
      s.rooted = false;
      s.festival = null;
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
  if (s.festival !== null)
    return "The festival lives on. There are more frogs to help and streams to understand.";
  if (s.rooted)
    return readyForFestival(s)
      ? "Bring the celebration to Kingdom. Your guests have stories to tell."
      : "Prepare the Nile festival: bring three stories home (" +
          completedStories(s).length +
          "/3) and reveal four streams (" +
          revealed(s) +
          "/4).";
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
