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
  look: string;
  x: number;
  y: number;
  art: string;
};

export const NODES: Record<SefirahId, SefirahNode> = {
  keter: {
    id: "keter",
    pond: "Crown Pond",
    pillar: "balance",
    classicalGuide: "Thoth",
    folkGuide: null,
    ledgerFloor: false,
    creationUnlock: false,
    look: "A still crown of light above the tree. Nothing asks for a key here. The beginning is hidden on purpose.",
    x: 50,
    y: 8,
    art: "/art/tiferet.jpg",
  },
  chokhmah: {
    id: "chokhmah",
    pond: "Wisdom Pond",
    pillar: "mercy",
    classicalGuide: "Thoth",
    folkGuide: "Wise Pepe",
    ledgerFloor: false,
    creationUnlock: false,
    look: "A well of water ringed by unread scrolls. Insight arrives faster than language.",
    x: 78,
    y: 20,
    art: "/art/wisdom.jpg",
  },
  binah: {
    id: "binah",
    pond: "Zen Zone",
    pillar: "severity",
    classicalGuide: "Maat",
    folkGuide: "Monk Pepe",
    ledgerFloor: false,
    creationUnlock: false,
    look: "Stone, breath, and the weight of form. Understanding is a slow architecture.",
    x: 22,
    y: 20,
    art: "/art/severity.jpg",
  },
  chesed: {
    id: "chesed",
    pond: "Mercy Pond",
    pillar: "mercy",
    classicalGuide: "Isis",
    folkGuide: "Cozy Pepe",
    ledgerFloor: false,
    creationUnlock: false,
    look: "Warm water. A cabin of kindness. Comfort can be a teacher or a trap.",
    x: 78,
    y: 38,
    art: "/art/mercy.jpg",
  },
  gevurah: {
    id: "gevurah",
    pond: "Severity Pond",
    pillar: "severity",
    classicalGuide: "Set",
    folkGuide: "Giga Pepe",
    ledgerFloor: false,
    creationUnlock: false,
    look: "Iron and ember. Discipline without cruelty is the work. Gains of the mind, not the jaw.",
    x: 22,
    y: 38,
    art: "/art/severity.jpg",
  },
  tiferet: {
    id: "tiferet",
    pond: "Vibe Temple",
    pillar: "balance",
    classicalGuide: "Horus",
    folkGuide: "Vibe Pepe",
    ledgerFloor: false,
    creationUnlock: false,
    look: "The heart of the tree. Geometry sings. Beauty that does not perform.",
    x: 50,
    y: 48,
    art: "/art/tiferet.jpg",
  },
  netzach: {
    id: "netzach",
    pond: "Boundaries Pond",
    pillar: "mercy",
    classicalGuide: "Wadjet",
    folkGuide: null,
    ledgerFloor: false,
    creationUnlock: false,
    look: "Edges that keep a thing itself. Victory is endurance, not volume.",
    x: 78,
    y: 64,
    art: "/art/mercy.jpg",
  },
  hod: {
    id: "hod",
    pond: "Meme Studio",
    pillar: "severity",
    classicalGuide: "Thoth",
    folkGuide: "Artist Pepe",
    ledgerFloor: false,
    creationUnlock: true,
    look: "Language as living material. A stamp is a thought that agrees to stay.",
    x: 22,
    y: 64,
    art: "/art/hod.jpg",
  },
  yesod: {
    id: "yesod",
    pond: "Harmony Pond",
    pillar: "balance",
    classicalGuide: "Isis",
    folkGuide: null,
    ledgerFloor: false,
    creationUnlock: true,
    look: "Foundation. Dream-logic is in bounds. What you build here holds the kingdom.",
    x: 50,
    y: 76,
    art: "/art/tiferet.jpg",
  },
  malkhut: {
    id: "malkhut",
    pond: "Kingdom Pond",
    pillar: "balance",
    classicalGuide: "Spider Woman",
    folkGuide: null,
    ledgerFloor: true,
    creationUnlock: true,
    look: "The world of form. A public ledger. Names become records. Keys stay in your own wallet.",
    x: 50,
    y: 92,
    art: "/art/malkhut.jpg",
  },
};

/** Traditional Tree of Life edges (undirected). */
export const PATHS: Array<[SefirahId, SefirahId]> = [
  ["keter", "chokhmah"],
  ["keter", "binah"],
  ["keter", "tiferet"],
  ["chokhmah", "binah"],
  ["chokhmah", "chesed"],
  ["chokhmah", "tiferet"],
  ["binah", "gevurah"],
  ["binah", "tiferet"],
  ["chesed", "gevurah"],
  ["chesed", "tiferet"],
  ["chesed", "netzach"],
  ["gevurah", "tiferet"],
  ["gevurah", "hod"],
  ["tiferet", "netzach"],
  ["tiferet", "hod"],
  ["tiferet", "yesod"],
  ["netzach", "hod"],
  ["netzach", "yesod"],
  ["netzach", "malkhut"],
  ["hod", "yesod"],
  ["hod", "malkhut"],
  ["yesod", "malkhut"],
];

export type StreamStatus = "open" | "dark" | "veiled" | "missing";

export type VeilState = {
  harmony: boolean;
  lookedNetzach: boolean;
  closedStream: SefirahId | null;
  closedLeft: number;
};

export function neighbors(id: SefirahId): SefirahId[] {
  const out: SefirahId[] = [];
  for (const [a, b] of PATHS) {
    if (a === id) out.push(b);
    if (b === id) out.push(a);
  }
  return out;
}

export function canTravel(from: SefirahId, to: SefirahId): boolean {
  if (from === to) return true;
  return neighbors(from).includes(to);
}

/** Session overlay on the 22-letter graph. Topology stays; the Watcher and the veils decide who may walk. */
export function streamStatus(from: SefirahId, to: SefirahId, v: VeilState): StreamStatus {
  if (from === to) return "open";
  if (!canTravel(from, to)) return "missing";
  if (to === "keter" && !v.harmony) return "veiled";
  const qoph = (from === "netzach" && to === "malkhut") || (from === "malkhut" && to === "netzach");
  if (qoph && !v.lookedNetzach) return "veiled";
  if (v.closedStream === to && v.closedLeft > 0) return "dark";
  return "open";
}

export function veilError(status: StreamStatus, to: SefirahId): string | null {
  if (status === "missing") return "There is no stream from here to that pond. Paths follow the tree.";
  if (status === "dark") return "That stream is dark. Sit, or take another.";
  if (status === "veiled" && to === "keter") {
    return "The crown is still unnamed. Mercy and Severity must both stand in the heart first.";
  }
  if (status === "veiled") {
    return "That stream is unlooked. Look here first. The back of the head is not a shortcut you invent.";
  }
  return null;
}

export function place(pillars: Record<Pillar, number>, folk: boolean) {
  const entries = Object.entries(pillars) as [Pillar, number][];
  const dominant = entries.sort((a, b) => b[1] - a[1])[0][0];
  const max = Math.max(...entries.map(([, v]) => v));
  const id: SefirahId =
    max < 0.15
      ? "tiferet"
      : dominant === "mercy"
        ? "chokhmah"
        : dominant === "severity"
          ? "binah"
          : "tiferet";
  const node = NODES[id];
  const dialect: Dialect = folk && node.folkGuide ? "folk" : "classical";
  return { node, dialect, dominant };
}

export function guideName(node: SefirahNode, dialect: Dialect): string {
  if (dialect === "folk" && node.folkGuide) return node.folkGuide;
  return node.classicalGuide;
}

export function shortPond(name: string) {
  return name.replace(/ Pond$/, "").replace(/ Zone$/, "").replace(/ Temple$/, "").replace(/ Studio$/, "");
}
