import { IDS, NODES, neighbors } from "./lattice.ts";
import type { SefirahId } from "./lattice.ts";
import type { World, Seeker, Action } from "./session.ts";
import { readyToRoot, status, revealed } from "./session.ts";
import { pathBetween, PATH_LETTERS } from "./paths.ts";
import {
  activeStories,
  completedStories,
  readyForFestival,
  STORIES,
} from "./stories.ts";
import { rareAt } from "./rares.ts";

export type NextStep = {
  text: string;
  label: string;
  action?: Action;
  panel?: "rite" | "story" | "sigil" | "festival" | "inquiry";
  target?: SefirahId;
};
// Route suggestions respect permanent veils. A temporary dark stream offers Sit,
// never a teleport, and every actual crossing still goes through the reducer.
export function route(s: Seeker, to: SefirahId): SefirahId[] | null {
  const queue: SefirahId[][] = [[s.current]],
    seen = new Set([s.current]);
  while (queue.length) {
    const path = queue.shift()!,
      here = path.at(-1)!;
    if (here === to) return path;
    for (const next of neighbors(here)) {
      if (
        seen.has(next) ||
        (next === "keter" && !s.harmony) ||
        (pathBetween(here, next)?.letter === "Qoph" &&
          !s.looked.includes("netzach"))
      )
        continue;
      seen.add(next);
      queue.push([...path, next]);
    }
  }
  return null;
}
function nearest(s: Seeker, ids: SefirahId[]): SefirahId | undefined {
  return ids
    .map((id) => ({ id, distance: route(s, id)?.length ?? Infinity }))
    .filter((p) => Number.isFinite(p.distance))
    .sort((a, b) => a.distance - b.distance)[0]?.id;
}
function toward(
  w: World,
  s: Seeker,
  target: SefirahId,
  reason: string,
): NextStep {
  const steps = route(s, target);
  if (!steps) return harmonyStep(w, s);
  const next = steps[1];
  if (!next)
    return {
      text: reason,
      label: "Look here",
      action: { type: "look" },
      target,
    };
  if (status(w, s, next) === "dark")
    return {
      text:
        "The stream toward " +
        NODES[target].pond +
        " has darkened. One pause will clear it.",
      label: "Sit to clear the water",
      action: { type: "sit" },
      target,
    };
  return {
    text:
      reason +
      " · " +
      (steps.length - 1) +
      (steps.length - 1 === 1 ? " crossing away" : " crossings away"),
    label: "Walk to " + NODES[next].pond,
    action: { type: "walk", to: next },
    target,
  };
}
function harmonyStep(w: World, s: Seeker): NextStep {
  if (s.pillars.mercy >= 0.25 && s.pillars.severity >= 0.25)
    return toward(
      w,
      s,
      "tiferet",
      "Meet the two pillars at Vibe Temple to open Crown",
    );
  if (!s.rested.includes(s.current))
    return {
      text: "A first rest here strengthens both pillars and helps open Crown.",
      label: "Sit with both currents",
      action: { type: "sit" },
    };
  const to = nearest(
    s,
    IDS.filter((id) => !s.rested.includes(id)),
  )!;
  return toward(
    w,
    s,
    to,
    "Find a fresh shore to rest and strengthen both pillars",
  );
}
export function nextStep(
  w: World,
  s: Seeker,
  tracked?: SefirahId | null,
  encounter?: SefirahId | null,
): NextStep {
  if (encounter) {
    if (s.current !== encounter)
      return toward(
        w,
        s,
        encounter,
        "Follow the encounter at " + NODES[encounter].pond,
      );
    if (!s.looked.includes(encounter))
      return {
        text: "You have reached the encounter. Look at the shore before speaking to its keeper.",
        label: "Look around",
        action: { type: "look" },
        target: encounter,
      };
    if (
      (encounter === "hod" || encounter === "netzach") &&
      s.rites[encounter] === undefined
    )
      return {
        text: "The encounter begins with this temple’s rite. Your route has brought you to the right place.",
        label: "Choose your rite",
        panel: "rite",
        target: encounter,
      };
    return {
      text: "You have arrived. Open the encounter to follow its clues or revisit your decision.",
      label: "Read the encounter here",
      panel: "inquiry",
      target: encounter,
    };
  }
  if (!s.looked.includes(s.current))
    return {
      text: "Start with the shore beneath your feet. Looking reveals its rite and its Rare Pepe.",
      label: "Look around",
      action: { type: "look" },
    };
  if (s.rites[s.current] === undefined)
    return {
      text: "This temple has a small problem only a visiting frog can help with.",
      label: "Choose your rite",
      panel: "rite",
    };
  const delivery = activeStories(s).find(
    (id) => !s.stories[id]!.delivered && STORIES[id].destination === s.current,
  );
  if (delivery)
    return {
      text:
        "You brought " +
        STORIES[delivery].cargo[s.stories[delivery]!.choice] +
        ".",
      label: "Make the delivery",
      panel: "story",
      target: delivery,
    };
  if (
    s.stories[s.current]?.delivered &&
    s.stories[s.current]!.resolution === null
  )
    return {
      text: rareAt(s.current).name + " is ready to hear what happened.",
      label: "Bring this story home",
      panel: "story",
      target: s.current,
    };
  if (!s.sigil && s.current === "hod")
    return {
      text: "The ink is ready. Give your journey a short phrase to carry.",
      label: "Make your sigil",
      panel: "sigil",
    };
  if (!s.rooted && readyToRoot(s) && s.current === "malkhut")
    return {
      text: "Your mark, six offices, and four rites are enough. The first ending is yours.",
      label: "Root the journey",
      action: { type: "root" },
    };
  if (s.festival === null && readyForFestival(s) && s.current === "malkhut")
    return {
      text: "Your guests are here. Choose the festival they will remember.",
      label: "Open the festival",
      panel: "festival",
    };
  const active = activeStories(s);
  const follow =
    tracked && s.stories[tracked]?.resolution == null
      ? tracked
      : s.rooted
        ? active[0]
        : undefined;
  if (follow) {
    const progress = s.stories[follow];
    const target =
      !progress || progress.delivered ? follow : STORIES[follow].destination;
    if (!progress && target === s.current) {
      if (active.length >= 3)
        return toward(
          w,
          s,
          s.stories[active[0]]!.delivered
            ? active[0]
            : STORIES[active[0]].destination,
          "Bring an unfinished story home to make room for another",
        );
      return {
        text: rareAt(follow).name + " has a story to tell.",
        label: "Hear their story",
        panel: "story",
        target: follow,
      };
    }
    return toward(
      w,
      s,
      target,
      (!progress
        ? "Meet "
        : progress.delivered
          ? "Return to "
          : "Carry the errand for ") + rareAt(follow).name,
    );
  }
  if (!s.rooted) {
    if (readyToRoot(s))
      return toward(w, s, "malkhut", "Carry your mark to Kingdom");
    if (!s.sigil) return toward(w, s, "hod", "Find the ink at Meme Studio");
    const unfinished = nearest(
      s,
      IDS.filter((id) => s.rites[id] === undefined),
    );
    if (unfinished)
      return toward(
        w,
        s,
        unfinished,
        "Carry your mark to another temple and its rite",
      );
  }
  if (readyForFestival(s) && s.festival === null)
    return toward(w, s, "malkhut", "The festival is ready at Kingdom");
  if (completedStories(s).length < 3 || s.festival !== null) {
    if (!s.stories[s.current])
      return {
        text:
          rareAt(s.current).name +
          " has unfinished business. Your earlier rite is where the story begins.",
        label: "Hear their story",
        panel: "story",
        target: s.current,
      };
    const fresh = nearest(
      s,
      IDS.filter((id) => !s.stories[id]),
    );
    if (fresh)
      return toward(w, s, fresh, "Meet another frog with a story to tell");
  }
  if (!s.harmony && completedStories(s).length === 10) return harmonyStep(w, s);
  const streams = PATH_LETTERS.filter((p) => (s.crossings[p.id] ?? 0) < 2)
    .map((p) => ({
      p,
      count: s.crossings[p.id] ?? 0,
      target: nearest(s, [p.from, p.to]),
    }))
    .filter((p) => p.target !== undefined)
    .sort(
      (a, b) =>
        b.count - a.count ||
        route(s, a.target!)!.length - route(s, b.target!)!.length,
    );
  const stream = streams[0];
  if (stream) {
    if (s.current === stream.p.from || s.current === stream.p.to)
      return toward(
        w,
        s,
        s.current === stream.p.from ? stream.p.to : stream.p.from,
        stream.count
          ? "Return by " + stream.p.letter + " to reveal its meaning"
          : "Give an unwalked stream its first crossing",
      );
    return toward(
      w,
      s,
      stream.target!,
      "Find " + stream.p.letter + " and let a return reveal its meaning",
    );
  }
  return {
    text:
      "Ten stories brought home. " +
      revealed(s) +
      " streams understood. The Nile remembers the shape you gave it.",
    label: "Rest beside the water",
    action: { type: "sit" },
  };
}
