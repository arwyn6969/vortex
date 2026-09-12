import data from "./lattice-data.json" with { type: "json" };
import type { SefirahId } from "./lattice.ts";
export type PathLetter = {
  id: string;
  from: SefirahId;
  to: SefirahId;
  letter: string;
  title: string;
  meaning: string;
};
export const PATH_LETTERS = data.paths as PathLetter[];
export const pathKey = (a: SefirahId, b: SefirahId) => [a, b].sort().join(":");
export const pathBetween = (a: SefirahId, b: SefirahId): PathLetter | null =>
  PATH_LETTERS.find((p) => p.id === pathKey(a, b)) ?? null;
