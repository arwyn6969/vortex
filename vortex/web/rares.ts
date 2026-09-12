import data from "./rarepepe-data.json" with { type: "json" };
import type { SefirahId } from "./lattice.ts";
export const RARES = data;
export type Rare = (typeof RARES)[number];
// VORTEX's fictional associations, not claims about utility of the original assets.
export const OFFICE_RARE: Record<SefirahId, string> = {
  keter: "LORDKEK",
  chokhmah: "THOTHPEPE",
  binah: "PEPEZENMSTR",
  chesed: "GODDESSISIS",
  gevurah: "GODANUBIS",
  tiferet: "PEPEPHARAON",
  netzach: "SPHINXPEPE",
  hod: "KEKET",
  yesod: "ZAZENPEPE",
  malkhut: "RAREPEPE",
};
export const rareAt = (id: SefirahId) =>
  RARES.find((r) => r.name === OFFICE_RARE[id])!;
export const PORTRAITS: Record<SefirahId, number> = {
  keter: 5,
  chokhmah: 0,
  binah: 3,
  chesed: 1,
  gevurah: 2,
  tiferet: 4,
  netzach: 3,
  hod: 0,
  yesod: 1,
  malkhut: 5,
};
export const PORTRAIT_TOKENS = [
  "THOTHPEPE",
  "GODDESSISIS",
  "GODANUBIS",
  "SPHINXPEPE",
  "PEPEPHARAON",
  "LORDKEK",
];
export function portraitStyle(id: SefirahId) {
  const n = PORTRAITS[id];
  return (
    "background-position:" + (n % 3) * 50 + "% " + Math.floor(n / 3) * 100 + "%"
  );
}
export function supply(r: Rare): string {
  const raw = BigInt(r.supplyRaw);
  if (!r.divisible) return raw.toLocaleString("en-US");
  const whole = (raw / 100000000n).toLocaleString("en-US");
  const fraction = (raw % 100000000n)
    .toString()
    .padStart(8, "0")
    .replace(/0+$/, "");
  return whole + (fraction ? "." + fraction : "");
}
