import { IDS, isOffice } from "./lattice.ts";
import type { Pillar, SefirahId } from "./lattice.ts";
import { PATH_LETTERS } from "./paths.ts";
import { emptyWorld } from "./session.ts";
import type { World, Seeker, Challenge, Proof, Entry } from "./session.ts";
import { safeText } from "./safety.ts";
import { verifyProof } from "./wallet.ts";
export const SAVE_KEY = "vortex-world-v3";
export const MAX_SAVE_BYTES = 1_000_000;
export interface StoragePort {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}
const fail = (): never => {
  throw new Error(
    "This save is damaged or uses an unsupported format. The original has been preserved.",
  );
};
const object = (x: unknown): Record<string, unknown> =>
  x && typeof x === "object" && !Array.isArray(x)
    ? (x as Record<string, unknown>)
    : fail();
const integer = (x: unknown, max = 1_000_000) =>
  typeof x === "number" && Number.isSafeInteger(x) && x >= 0 && x <= max
    ? x
    : fail();
const bool = (x: unknown) => (typeof x === "boolean" ? x : fail());
const str = (x: unknown, max: number) =>
  typeof x === "string" && x.length <= max ? x : fail();
const officeList = (x: unknown): SefirahId[] =>
  Array.isArray(x) &&
  x.length <= 10 &&
  x.every(isOffice) &&
  new Set(x).size === x.length
    ? x
    : fail();
const timestamp = (x: unknown) => integer(x, 8_640_000_000_000_000);
function parseChallenge(raw: unknown): Challenge | null {
  if (raw === null) return null;
  const c = object(raw);
  return {
    address: str(c.address, 90),
    nonce: str(c.nonce, 80),
    message: str(c.message, 2048),
    issuedAt: timestamp(c.issuedAt),
    expiresAt: timestamp(c.expiresAt),
    seekerId: str(c.seekerId, 80),
  };
}
function parseSeeker(raw: unknown): Seeker {
  const s = object(raw);
  if (
    !isOffice(s.current) ||
    !["classical", "folk"].includes(String(s.dialect))
  )
    return fail();
  const pillars = object(s.pillars);
  for (const p of ["mercy", "severity", "balance"])
    if (
      typeof pillars[p] !== "number" ||
      !Number.isFinite(pillars[p]) ||
      Number(pillars[p]) < 0 ||
      Number(pillars[p]) > 1
    )
      return fail();
  const rites: Seeker["rites"] = {},
    crossings: Seeker["crossings"] = {};
  for (const [key, value] of Object.entries(object(s.rites))) {
    if (!isOffice(key)) return fail();
    rites[key] = integer(value, 2);
  }
  for (const [key, value] of Object.entries(object(s.crossings))) {
    if (!PATH_LETTERS.some((p) => p.id === key)) return fail();
    crossings[key] = integer(value);
  }
  if (!Array.isArray(s.journal) || s.journal.length > 80) return fail();
  const journal = s.journal.map((rawEntry) => {
    const e = object(rawEntry);
    if (
      !isOffice(e.office) ||
      !["world", "guide", "discovery"].includes(String(e.kind))
    )
      return fail();
    return {
      office: e.office,
      kind: e.kind as Entry["kind"],
      turn: integer(e.turn),
      text: safeText(e.text, 1200),
      ...(e.speaker === undefined ? {} : { speaker: safeText(e.speaker, 80) }),
    };
  });
  const proofData = s.proof === null ? null : object(s.proof);
  const proof = proofData
    ? ({
        ...parseChallenge(proofData)!,
        signature: str(proofData.signature, 2048),
        verifiedAt: timestamp(proofData.verifiedAt),
      } as Proof)
    : null;
  const player: Seeker = {
    id: str(s.id, 80),
    name: safeText(s.name, 32, 2),
    dialect: s.dialect as Seeker["dialect"],
    current: s.current,
    pillars: {
      mercy: Number(pillars.mercy),
      severity: Number(pillars.severity),
      balance: Number(pillars.balance),
    },
    visited: officeList(s.visited),
    looked: officeList(s.looked),
    rested: officeList(s.rested),
    rites,
    crossings,
    harmony: bool(s.harmony),
    sigil: s.sigil === "" ? "" : safeText(s.sigil, 80, 3),
    rooted: bool(s.rooted),
    walks: integer(s.walks, 3),
    turns: integer(s.turns),
    conversations: integer(s.conversations),
    journal,
    createdAt: timestamp(s.createdAt),
    challenge: parseChallenge(s.challenge),
    proof,
  };
  if (
    !/^[A-Za-z0-9_-]{1,80}$/.test(player.id) ||
    !player.visited.includes(player.current) ||
    player.looked.some((p) => !player.visited.includes(p)) ||
    player.rested.some((p) => !player.visited.includes(p)) ||
    Object.keys(rites).some((p) => !player.looked.includes(p as SefirahId))
  )
    return fail();
  if (
    player.harmony &&
    (player.pillars.mercy < 0.25 ||
      player.pillars.severity < 0.25 ||
      !player.visited.includes("tiferet"))
  )
    return fail();
  if (player.sigil && rites.hod === undefined) return fail();
  if (
    player.rooted &&
    (!player.sigil ||
      player.visited.length < 6 ||
      Object.keys(rites).length < 4)
  )
    return fail();
  return player;
}
export function parseWorld(text: string): World {
  if (text.length > MAX_SAVE_BYTES)
    throw new Error("This save is too large. Nothing was changed.");
  const w = object(JSON.parse(text));
  if (w.version !== 3)
    throw new Error(
      "This edition reads version 3 journey files. Other versions are preserved, never guessed or overwritten.",
    );
  if (!Array.isArray(w.seekers) || w.seekers.length > 12) return fail();
  const seekers = w.seekers.map(parseSeeker);
  if (
    new Set(seekers.map((s) => s.id)).size !== seekers.length ||
    new Set(seekers.map((s) => s.name.toLowerCase())).size !== seekers.length
  )
    return fail();
  if (w.activeId !== null && !seekers.some((s) => s.id === w.activeId))
    return fail();
  const darkness: World["darkness"] = {};
  for (const [key, value] of Object.entries(object(w.darkness))) {
    if (!PATH_LETTERS.some((p) => p.id === key)) return fail();
    darkness[key] = integer(value);
  }
  return {
    version: 3,
    revision: integer(w.revision),
    clock: integer(w.clock),
    activeId: w.activeId as string | null,
    seekers,
    darkness,
  };
}
export async function validateProofs(world: World): Promise<World> {
  for (const s of world.seekers)
    if (s.proof && !(await verifyProof(s, s.proof)))
      throw new Error(
        "A saved wallet proof cannot be verified. The original file has been preserved.",
      );
  return world;
}
export async function loadWorld(storage: StoragePort): Promise<World> {
  const raw = storage.getItem(SAVE_KEY);
  return raw ? validateProofs(parseWorld(raw)) : emptyWorld();
}
export function saveWorld(
  storage: StoragePort,
  world: World,
  expectedRevision: number,
): void {
  const raw = storage.getItem(SAVE_KEY);
  const existing = raw ? parseWorld(raw) : emptyWorld();
  if (existing.revision !== expectedRevision)
    throw new Error(
      "Another tab has changed this tree. The latest journey has been loaded; please try your action again.",
    );
  if (world.revision <= expectedRevision)
    throw new Error("The save must advance its revision.");
  const serialized = JSON.stringify(world);
  if (serialized.length > MAX_SAVE_BYTES)
    throw new Error(
      "This tree is full. Export your journeys before continuing.",
    );
  storage.setItem(SAVE_KEY, serialized);
}
export async function importWorld(
  storage: StoragePort,
  text: string,
): Promise<World> {
  const incoming = await validateProofs(parseWorld(text));
  const existing = await loadWorld(storage);
  const byId = new Map(existing.seekers.map((s) => [s.id, s]));
  for (const s of incoming.seekers) {
    const current = byId.get(s.id);
    if (current) {
      // Do not silently rewind or merge contradictory histories under one identity.
      if (JSON.stringify(current) !== JSON.stringify(s))
        throw new Error(
          "This file has a different version of an existing journey. Export the current tree and remove that seeker before restoring it.",
        );
    } else {
      if (
        existing.seekers.some(
          (p) => p.name.toLowerCase() === s.name.toLowerCase(),
        )
      )
        throw new Error(
          "A different seeker already uses that name. Rename the existing seeker before importing.",
        );
      byId.set(s.id, s);
    }
  }
  if (byId.size > 12) throw new Error("This import would exceed 12 seekers.");
  const next: World = {
    ...existing,
    seekers: [...byId.values()],
    activeId: existing.activeId ?? incoming.activeId,
    revision: existing.revision + 1,
  };
  // A merge retains the current world's clock/darkness; a first restore recovers both.
  if (!existing.seekers.length) {
    next.clock = incoming.clock;
    next.darkness = incoming.darkness;
  }
  saveWorld(storage, next, existing.revision);
  return next;
}
