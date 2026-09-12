import data from "./lattice-data.json" with { type: "json" };
export type Pillar = "mercy" | "severity" | "balance";
export type Dialect = "classical" | "folk";
export type SefirahId =
  | "keter"
  | "chokhmah"
  | "binah"
  | "chesed"
  | "gevurah"
  | "tiferet"
  | "netzach"
  | "hod"
  | "yesod"
  | "malkhut";
export type SefirahNode = {
  id: SefirahId;
  pond: string;
  pillar: Pillar;
  classicalGuide: string;
  folkGuide: string | null;
  ledgerFloor: boolean;
  creationUnlock: boolean;
  x: number;
  y: number;
};
export const NODES = data.nodes as Record<SefirahId, SefirahNode>;
export const IDS = Object.keys(NODES) as SefirahId[];
export const PATHS = data.paths.map((p) => [p.from, p.to]) as [
  SefirahId,
  SefirahId,
][];
export const isOffice = (value: unknown): value is SefirahId =>
  typeof value === "string" && Object.hasOwn(NODES, value);
export function neighbors(id: SefirahId): SefirahId[] {
  return PATHS.flatMap(([a, b]) => (a === id ? [b] : b === id ? [a] : []));
}
export const canTravel = (a: SefirahId, b: SefirahId) =>
  a === b || neighbors(a).includes(b);
export function place(pillars: Record<Pillar, number>, folk: boolean) {
  const normalized = Object.fromEntries(
    (["mercy", "severity", "balance"] as Pillar[]).map((k) => [
      k,
      Number.isFinite(pillars[k]) ? Math.max(0, Math.min(1, pillars[k])) : 0,
    ]),
  ) as Record<Pillar, number>;
  const max = Math.max(...Object.values(normalized));
  const tied = (Object.keys(normalized) as Pillar[]).filter(
    (k) => normalized[k] === max,
  );
  const dominant: Pillar =
    tied.length !== 1 || max < 0.15 ? "balance" : tied[0];
  const id = { mercy: "chokhmah", severity: "binah", balance: "tiferet" }[
    dominant
  ] as SefirahId;
  const node = NODES[id];
  return {
    node,
    dominant,
    dialect: (folk && node.folkGuide ? "folk" : "classical") as Dialect,
  };
}
export const guideName = (node: SefirahNode, dialect: Dialect) =>
  dialect === "folk" && node.folkGuide ? node.folkGuide : node.classicalGuide;
export const shortPond = (name: string) =>
  name.replace(/ (Pond|Zone|Temple|Studio)$/, "");
export type StreamStatus = "open" | "dark" | "veiled" | "missing";
export type VeilState = {
  harmony: boolean;
  lookedNetzach: boolean;
  closedStream: SefirahId | null;
  closedLeft: number;
};
export function streamStatus(
  from: SefirahId,
  to: SefirahId,
  v: VeilState,
): StreamStatus {
  if (from === to) return "open";
  if (!canTravel(from, to)) return "missing";
  if (to === "keter" && !v.harmony) return "veiled";
  if (
    [from, to].includes("netzach") &&
    [from, to].includes("malkhut") &&
    !v.lookedNetzach
  )
    return "veiled";
  if (v.closedStream === to && v.closedLeft > 0) return "dark";
  return "open";
}
export function veilError(status: StreamStatus, to: SefirahId): string | null {
  if (status === "missing") return "There is no stream between these offices.";
  if (status === "dark") return "The stream is dark. Sit to let it reopen.";
  if (status === "veiled")
    return to === "keter"
      ? "Bring Mercy and Severity together in the heart."
      : "Look at Boundaries Pond before taking this descent.";
  return null;
}
