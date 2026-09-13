import { ATLAS, ATLAS_SOURCES, atlasEntry, RELATIONS } from "./atlas.ts";
import { inquiryError, TABLET_CHOICES, GATE_CHOICES } from "./inquiries.ts";
import { isOffice, NODES, neighbors } from "./lattice.ts";
import { activeSeeker, status, readyToRoot } from "./session.ts";
import type { World, Action, Seeker } from "./session.ts";
import { nextStep } from "./navigation.ts";
import type { NextStep } from "./navigation.ts";
import { PASSENGERS, boardingError, boardingHelper } from "./boarding.ts";
import type { BoardingPlan } from "./boarding.ts";
import {
  STORIES,
  storyStage,
  readyForFestival,
  FESTIVAL_CHOICES,
} from "./stories.ts";
import { CONTENT } from "./content.ts";
import { IDS } from "./lattice.ts";

export interface JourneyTool {
  name: string;
  description: string;
  inputSchema: object;
  annotations: { readOnlyHint: boolean; untrustedContentHint: boolean };
  execute(input: unknown): unknown | Promise<unknown>;
}
export interface JourneyContext {
  registerTool(
    tool: JourneyTool,
    options: { signal: AbortSignal },
  ): void | Promise<void>;
}
const actions = [
  "walk",
  "look",
  "sit",
  "rite",
  "root",
  "story-start",
  "story-deliver",
  "story-resolve",
  "festival",
  "study",
  "inquiry",
] as const;
type GuidanceReader = (w: World, s: Seeker) => NextStep;
export function journeySnapshot(w: World, guidance: GuidanceReader = nextStep) {
  const s = activeSeeker(w);
  if (!s)
    return {
      revision: w.revision,
      seeker: null,
      message: "Start a journey using the name and six questions in the game.",
    };
  return {
    revision: w.revision,
    seeker: { id: s.id, name: s.name },
    location: { id: s.current, name: NODES[s.current].pond },
    rooted: s.rooted,
    inquiries: { ...s.inquiries, seen: [...s.inquiries.seen] },
    encounters: (["tablet", "gate"] as const).map((task) => ({
      task,
      choices: (task === "tablet" ? TABLET_CHOICES : GATE_CHOICES).map(
        (label, choice) => ({
          label,
          choice,
          unavailable: inquiryError(s, { type: "inquiry", task, choice }),
        }),
      ),
    })),
    festival: s.festival,
    next: guidance(w, s),
    boarding:
      s.current === "netzach" &&
      s.rites.netzach !== undefined &&
      s.stories.tiferet &&
      !s.stories.tiferet.delivered
        ? {
            passengers: PASSENGERS,
            placesPerSailing: 3,
            novicesTravelWithApprentice: true,
            novicesFirst: s.stories.tiferet.choice === 0,
            cookOffersHelp: boardingHelper(s),
            canDelegate: true,
          }
        : null,
    exits: neighbors(s.current).map((id) => ({
      id,
      name: NODES[id].pond,
      status: status(w, s, id),
    })),
    rite:
      s.looked.includes(s.current) && s.rites[s.current] === undefined
        ? CONTENT[s.current].rite
        : null,
    canRoot: s.current === "malkhut" && readyToRoot(s) && !s.rooted,
    festivalChoices:
      s.current === "malkhut" && readyForFestival(s) && s.festival === null
        ? FESTIVAL_CHOICES
        : null,
    stories: IDS.map((id) => ({
      id,
      title: STORIES[id].title,
      stage: storyStage(s, id),
      destination: STORIES[id].destination,
      choices:
        storyStage(s, id) === "return"
          ? STORIES[id].endings
          : storyStage(s, id) === "available"
            ? STORIES[id].choices
            : null,
    })),
  };
}
function parseAction(raw: unknown): {
  revision: number;
  seekerId: string;
  action: Action;
} {
  if (!raw || typeof raw !== "object" || Array.isArray(raw))
    throw new Error("Provide one journey action.");
  const p = raw as Record<string, unknown>;
  if (
    typeof p.seekerId !== "string" ||
    !Number.isSafeInteger(p.revision) ||
    Number(p.revision) < 0 ||
    !actions.includes(p.action as (typeof actions)[number])
  )
    throw new Error(
      "Read the journey first and supply its seekerId, revision, and an available action.",
    );
  const allowed = new Set([
    "seekerId",
    "revision",
    "action",
    ...(p.action === "story-deliver" ? ["boarding"] : []),
    ...(p.action === "study"
      ? ["entry"]
      : p.action === "inquiry"
        ? ["task"]
        : []),
    ...(p.action === "walk"
      ? ["office"]
      : p.action?.toString().startsWith("story-")
        ? ["story"]
        : []),
    ...([
      "rite",
      "story-start",
      "story-resolve",
      "festival",
      "inquiry",
    ].includes(String(p.action))
      ? ["choice"]
      : []),
  ]);
  if (Object.keys(p).some((key) => !allowed.has(key)))
    throw new Error("Unexpected action fields.");
  const choice = [
    "rite",
    "story-start",
    "story-resolve",
    "festival",
    "inquiry",
  ].includes(String(p.action));
  if (
    choice &&
    (!Number.isInteger(p.choice) ||
      Number(p.choice) < 0 ||
      Number(p.choice) > 2)
  )
    throw new Error("Choice must be 0, 1, or 2.");
  let action: Action;
  if (p.action === "study") {
    if (typeof p.entry !== "string" || !atlasEntry(p.entry))
      throw new Error("Unknown atlas entry.");
    action = { type: "study", entry: p.entry };
  } else if (p.action === "inquiry") {
    if (!["testimony", "tablet", "gate"].includes(String(p.task)))
      throw new Error("Unknown encounter.");
    action = {
      type: "inquiry",
      task: p.task as "testimony" | "tablet" | "gate",
      choice: Number(p.choice),
    };
  } else if (p.action === "walk") {
    if (!isOffice(p.office)) throw new Error("Unknown office.");
    action = { type: "walk", to: p.office };
  } else if (
    p.action === "story-start" ||
    p.action === "story-resolve" ||
    p.action === "story-deliver"
  ) {
    if (!isOffice(p.story)) throw new Error("Unknown story.");
    action =
      p.action === "story-deliver"
        ? {
            type: p.action,
            story: p.story,
            ...(Object.hasOwn(p, "boarding")
              ? { boarding: p.boarding as BoardingPlan }
              : {}),
          }
        : { type: p.action, story: p.story, choice: Number(p.choice) };
    if (Object.hasOwn(p, "boarding")) {
      const error = boardingError(p.boarding, 1);
      if (error) throw new Error(error);
    }
  } else if (p.action === "rite" || p.action === "festival")
    action = { type: p.action, choice: Number(p.choice) };
  else action = { type: p.action as "look" | "sit" | "root" };
  return { seekerId: p.seekerId, revision: Number(p.revision), action };
}
export function registerJourneyTools(
  context: JourneyContext | undefined,
  getWorld: () => World,
  apply: (
    action: Action,
    expected: { seekerId: string; revision: number },
  ) => Promise<void>,
  report: (error: unknown) => void = () => {},
  guidance?: GuidanceReader,
) {
  const lifecycle = new AbortController();
  if (!context?.registerTool) return () => lifecycle.abort();
  const tools: JourneyTool[] = [
    {
      name: "read_atlas_entry",
      description:
        "Read a published atlas entry and its sourced or interpretive connections. This does not mark it remembered or change a journey.",
      inputSchema: {
        type: "object",
        properties: { entry: { type: "string", enum: ATLAS.map((x) => x.id) } },
        required: ["entry"],
        additionalProperties: false,
      },
      annotations: { readOnlyHint: true, untrustedContentHint: true },
      execute(input) {
        if (
          !input ||
          typeof input !== "object" ||
          Array.isArray(input) ||
          Object.keys(input).some((k) => k !== "entry")
        )
          throw new Error("Provide only an atlas entry identifier.");
        const entry = atlasEntry(String((input as { entry: unknown }).entry));
        if (!entry) throw new Error("Unknown atlas entry.");
        return {
          ...entry,
          sourceRecord: ATLAS_SOURCES[entry.source],
          connections: RELATIONS.filter(
            (r) => r.from === entry.id || r.to === entry.id,
          ).map((r) => ({ ...r, sourceRecord: ATLAS_SOURCES[r.source] })),
        };
      },
    },
    {
      name: "get_journey_state",
      description:
        "Read the active VORTEX journey, legal exits, story stages, remembered atlas entries, encounter choices and next step. Does not expose wallet details or the journal.",
      inputSchema: {
        type: "object",
        properties: {},
        additionalProperties: false,
      },
      annotations: { readOnlyHint: true, untrustedContentHint: true },
      execute(input) {
        if (
          !input ||
          typeof input !== "object" ||
          Array.isArray(input) ||
          Object.keys(input).length
        )
          throw new Error("No input fields are accepted.");
        return journeySnapshot(getWorld(), guidance);
      },
    },
    {
      name: "take_journey_action",
      description:
        "Perform one visible game action and save it: walk, look, sit, rite, root, start/deliver/resolve a story, celebrate the festival, remember an atlas entry, or resolve an inquiry. For the solar boat delivery, optionally supply a boarding object assigning every passenger ticket to sailing 0 or 1; omitting it delegates boarding to the sphinx. Read atlas entries before studying them. Testimony is at Yesod and uses choice 0. Read the current state first. Choice indexes are 0–2. Sigils, identity changes and wallet operations stay in the interface.",
      inputSchema: {
        type: "object",
        properties: {
          seekerId: { type: "string" },
          revision: { type: "integer", minimum: 0 },
          action: { type: "string", enum: actions },
          office: { type: "string", enum: IDS },
          story: { type: "string", enum: IDS },
          entry: { type: "string", enum: ATLAS.map((x) => x.id) },
          task: { type: "string", enum: ["testimony", "tablet", "gate"] },
          choice: { type: "integer", minimum: 0, maximum: 2 },
          boarding: {
            type: "object",
            properties: Object.fromEntries(
              PASSENGERS.map((p) => [p.id, { type: "integer", enum: [0, 1] }]),
            ),
            required: PASSENGERS.map((p) => p.id),
            additionalProperties: false,
          },
        },
        required: ["seekerId", "revision", "action"],
        additionalProperties: false,
      },
      annotations: { readOnlyHint: false, untrustedContentHint: true },
      async execute(input) {
        const p = parseAction(input);
        await apply(p.action, { seekerId: p.seekerId, revision: p.revision });
        return journeySnapshot(getWorld(), guidance);
      },
    },
  ];
  for (const tool of tools)
    try {
      void Promise.resolve(
        context.registerTool(tool, { signal: lifecycle.signal }),
      ).catch(report);
    } catch (error) {
      report(error);
    }
  return () => lifecycle.abort();
}
