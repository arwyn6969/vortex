import { neighbors, IDS } from "../lattice.ts";
import type { SefirahId } from "../lattice.ts";
import { activeSeeker, addSeeker, emptyWorld, transition } from "../session.ts";
import type { World } from "../session.ts";
import { quizPillars } from "../content.ts";
import type { StoragePort } from "../storage.ts";

export class MemoryStorage implements StoragePort {
  data = new Map<string, string>();
  getItem(key: string) {
    return this.data.get(key) ?? null;
  }
  setItem(key: string, value: string) {
    this.data.set(key, value);
  }
  removeItem(key: string) {
    this.data.delete(key);
  }
}
export const newGame = (answers = [2, 2, 2, 2, 2, 2]) =>
  addSeeker(
    emptyWorld(),
    "River Frog",
    "folk",
    quizPillars(answers),
    1_700_000_000_000,
    "test-seeker",
  );
export function travel(w: World, to: SefirahId): World {
  const start = activeSeeker(w)!.current;
  const paths: SefirahId[][] = [[start]],
    seen = new Set([start]);
  while (paths.length) {
    const path = paths.shift()!,
      last = path.at(-1)!;
    if (last === to) {
      for (const step of path.slice(1)) {
        w = transition(w, { type: "look" });
        w = transition(w, { type: "sit" });
        w = transition(w, { type: "walk", to: step });
      }
      return w;
    }
    for (const n of neighbors(last))
      if (!seen.has(n)) {
        seen.add(n);
        paths.push([...path, n]);
      }
  }
  throw new Error("Unreachable office");
}
export function finish(answers?: number[]): World {
  let w = travel(newGame(answers), "tiferet");
  w = transition(w, { type: "sit" });
  for (const id of IDS) {
    w = travel(w, id);
    w = transition(w, { type: "look" });
    w = transition(w, { type: "rite", choice: 1 });
    if (id === "hod")
      w = transition(w, { type: "sigil", text: "Make room for strange frogs" });
  }
  return transition(w, { type: "root" });
}
