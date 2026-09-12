import { isOffice, NODES, neighbors } from "./lattice.ts";
import { activeSeeker, status, readyToRoot } from "./session.ts";
import type { World, Action } from "./session.ts";
import { nextStep } from "./navigation.ts";
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
] as const;
export function journeySnapshot(w: World) {
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
    festival: s.festival,
    next: nextStep(w, s),
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
    ...(p.action === "walk"
      ? ["office"]
      : p.action?.toString().startsWith("story-")
        ? ["story"]
        : []),
    ...(["rite", "story-start", "story-resolve", "festival"].includes(
      String(p.action),
    )
      ? ["choice"]
      : []),
  ]);
  if (Object.keys(p).some((key) => !allowed.has(key)))
    throw new Error("Unexpected action fields.");
  const choice = ["rite", "story-start", "story-resolve", "festival"].includes(
    String(p.action),
  );
  if (
    choice &&
    (!Number.isInteger(p.choice) ||
      Number(p.choice) < 0 ||
      Number(p.choice) > 2)
  )
    throw new Error("Choice must be 0, 1, or 2.");
  let action: Action;
  if (p.action === "walk") {
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
        ? { type: p.action, story: p.story }
        : { type: p.action, story: p.story, choice: Number(p.choice) };
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
) {
  const lifecycle = new AbortController();
  if (!context?.registerTool) return () => lifecycle.abort();
  const tools: JourneyTool[] = [
    {
      name: "get_journey_state",
      description:
        "Read the active VORTEX journey, legal exits, story stages, choices and next step. Does not expose wallet details or the journal.",
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
        return journeySnapshot(getWorld());
      },
    },
    {
      name: "take_journey_action",
      description:
        "Perform one visible game action and save it: walk, look, sit, rite, root, start/deliver/resolve a story, or celebrate the festival. Read the current state first. Choice indexes are 0–2. Sigils, identity changes and wallet operations stay in the interface.",
      inputSchema: {
        type: "object",
        properties: {
          seekerId: { type: "string" },
          revision: { type: "integer", minimum: 0 },
          action: { type: "string", enum: actions },
          office: { type: "string", enum: IDS },
          story: { type: "string", enum: IDS },
          choice: { type: "integer", minimum: 0, maximum: 2 },
        },
        required: ["seekerId", "revision", "action"],
        additionalProperties: false,
      },
      annotations: { readOnlyHint: false, untrustedContentHint: true },
      async execute(input) {
        const p = parseAction(input);
        await apply(p.action, { seekerId: p.seekerId, revision: p.revision });
        return journeySnapshot(getWorld());
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
