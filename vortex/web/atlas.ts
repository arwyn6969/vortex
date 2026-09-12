import { RARES, OFFICE_RARE } from "./rares.ts";
import type { SefirahId } from "./lattice.ts";

export type Evidence =
  "Source account" | "VORTEX interpretation" | "Disputed account";
export type AtlasEntry = {
  id: string;
  name: string;
  aliases: string[];
  kind:
    | "Figure"
    | "Text"
    | "Object"
    | "Practice"
    | "Archetype"
    | "Tarot"
    | "Motif"
    | "Asset"
    | "Protocol";
  tradition: string;
  context: string;
  summary: string;
  distinction: string;
  evidence: Evidence;
  source: string;
  locator: string;
  office: SefirahId;
  groups: string[];
  image?: string;
  token?: string;
};
export const ATLAS_SOURCES: Record<string, { title: string; url: string }> = {
  egypt: {
    title: "The Met · Egyptian funerary imagery",
    url: "https://www.metmuseum.org/exhibitions/listings/2018/nedjemankh-gilded-coffin/exhibition-gallery",
  },
  tarot: {
    title: "Morgan Library · The history of tarot",
    url: "https://www.themorgan.org/collection/tarot-cards",
  },
  descent: {
    title: "Oxford ETCSL · Inana’s descent",
    url: "https://etcsl.orinst.ox.ac.uk/section1/tr141.htm",
  },
  nisaba: {
    title: "ORACC · Nidaba / Nisaba",
    url: "https://oracc.museum.upenn.edu/amgg/listofdeities/nidaba/",
  },
  maya: {
    title: "NMAI · Ball player, with Edgar Suyuc (Kaqchikel Maya)",
    url: "https://americanindian.si.edu/exhibitions/infinityofnations/meso-carib/240457.html",
  },
  popol: {
    title: "Allen J. Christenson · Popol Vuh translation",
    url: "https://www.mesoweb.org/publications/Christenson/PopolVuh.pdf",
  },
  dogon: {
    title: "The Met · Imina kanaga, object 1987.74i",
    url: "https://www.metmuseum.org/art/collection/search/315061",
  },
  restudy: {
    title: "Walter E. A. van Beek · Dogon Restudied (1991)",
    url: "https://pure.uvt.nl/ws/portalfiles/portal/1002365/dogonrestudied.pdf",
  },
  stamps: {
    title: "Bitcoin Stamps · Original specification",
    url: "https://github.com/mikeinspace/stamps/blob/main/BitcoinStamps.md",
  },
  kevin: {
    title: "KEVIN Stamp Saga · Community narrative",
    url: "https://kevinstamp.com/",
  },
  vortex: {
    title: "VORTEX · Editorial framework and source policy",
    url: "https://github.com/arwyn6969/vortex/blob/main/docs/LIVING_ATLAS.md",
  },
};
export const CLUSTERS = [
  {
    id: "memory",
    name: "Word, memory & witness",
    question: "What survives—and who gives it meaning?",
    office: "hod",
  },
  {
    id: "return",
    name: "Descent & return",
    question: "What changes when someone comes back?",
    office: "yesod",
  },
  {
    id: "threshold",
    name: "Thresholds & reversals",
    question: "What is the test really testing?",
    office: "netzach",
  },
] as const;
const rows: AtlasEntry[] = [];
function entry(
  id: string,
  name: string,
  kind: AtlasEntry["kind"],
  tradition: string,
  context: string,
  summary: string,
  distinction: string,
  source: string,
  locator: string,
  office: SefirahId,
  groups: string[],
  evidence: Evidence = "Source account",
  aliases: string[] = [],
) {
  rows.push({
    id,
    name,
    kind,
    tradition,
    context,
    summary,
    distinction,
    source,
    locator,
    office,
    groups,
    evidence,
    aliases,
  });
}
for (const c of CLUSTERS)
  entry(
    c.id,
    c.name,
    "Motif",
    "VORTEX",
    "Editorial exploration theme",
    c.question,
    "Membership is a way to explore a question, not evidence that traditions are identical.",
    "vortex",
    "Three exploration clusters",
    c.office,
    [c.id],
    "VORTEX interpretation",
  );
for (const [id, name, summary, group, office] of [
  [
    "scribe",
    "The Scribe",
    "Gives a thought a form that another person can read.",
    "memory",
    "hod",
  ],
  [
    "witness",
    "The Witness",
    "Keeps track of what was seen—and what remains unknown.",
    "memory",
    "malkhut",
  ],
  [
    "guardian",
    "The Guardian",
    "Asks what a boundary protects and whom it excludes.",
    "threshold",
    "gevurah",
  ],
  [
    "trickster",
    "The Trickster",
    "Finds the assumption hidden inside a rule.",
    "threshold",
    "netzach",
  ],
  [
    "caregiver",
    "The Caregiver",
    "Makes another person’s return possible through attention and practical help.",
    "return",
    "chesed",
  ],
  [
    "seeker",
    "The Seeker",
    "Crosses a threshold and accepts that an answer may change the question.",
    "return",
    "tiferet",
  ],
] as const)
  entry(
    id,
    name,
    "Archetype",
    "VORTEX",
    "A narrative role",
    summary,
    "A role can be shared, refused or changed. It does not define a whole deity or a player’s personality.",
    "vortex",
    "Narrative roles",
    office,
    [group],
    "VORTEX interpretation",
  );
for (const [id, name, summary, group, office] of [
  [
    "fool",
    "The Fool",
    "Try a first step without pretending to know the whole road.",
    "threshold",
    "tiferet",
  ],
  [
    "magician",
    "The Magician",
    "Notice what changes when intention becomes a made thing.",
    "memory",
    "hod",
  ],
  [
    "justice",
    "Justice",
    "Hear the evidence and make your terms visible.",
    "threshold",
    "gevurah",
  ],
  [
    "death",
    "Death",
    "Ask what must end for a return to become possible.",
    "return",
    "yesod",
  ],
  [
    "wheel",
    "The Wheel",
    "Watch a repeating pattern without assuming every cycle is the same.",
    "return",
    "netzach",
  ],
  [
    "world",
    "The World",
    "Carry a completed journey back into ordinary life.",
    "memory",
    "malkhut",
  ],
] as const)
  entry(
    "tarot-" + id,
    name,
    "Tarot",
    "Tarot · VORTEX lens",
    "Modern game interpretation of a tarot theme",
    summary,
    "These meanings are VORTEX’s lens. Tarot began as an Italian card game in the fifteenth century; occult readings came later. No ancient Egyptian origin or fixed stream assignment is claimed.",
    "tarot",
    "Collection introduction (history); meaning authored by VORTEX",
    office,
    [group],
    "VORTEX interpretation",
  );
for (const [id, name, summary, group, office] of [
  [
    "thoth",
    "Thoth",
    "In the cited coffin imagery, ibis-headed Thoth is associated with wisdom and writing.",
    "memory",
    "chokhmah",
  ],
  [
    "anubis",
    "Anubis",
    "Anubis performs embalming rituals in the cited Egyptian funerary imagery.",
    "threshold",
    "gevurah",
  ],
  [
    "isis",
    "Isis",
    "Isis mourns and protects Osiris in the cited funerary scenes.",
    "return",
    "chesed",
  ],
  [
    "osiris",
    "Osiris",
    "The cited scenes place Osiris within the care and ritual surrounding the dead.",
    "return",
    "yesod",
  ],
] as const)
  entry(
    id,
    name,
    "Figure",
    "Egyptian",
    "Funerary imagery described by The Met",
    summary,
    "This is one attested context. The associated VORTEX temple and frog character are later fictional placements.",
    "egypt",
    "Gallery discussion of funerary imagery",
    office,
    [group],
  );
entry(
  "nisaba",
  "Nisaba / Nidaba",
  "Figure",
  "Sumerian",
  "Scribal and agricultural traditions",
  "Nisaba connects grain and writing; ORACC discusses changes in her role and uncertainties in her imagery.",
  "Writing does not exhaust this figure’s associations. Some proposed visual identifications remain uncertain.",
  "nisaba",
  "Functions; Name and Spellings",
  "hod",
  ["memory"],
  "Source account",
  ["Nidaba", "Nissaba"],
);
entry(
  "descent",
  "Inana’s descent",
  "Text",
  "Sumerian",
  "A composition with manuscript variants",
  "Inana enters the underworld; help and the terms of return shape what follows.",
  "This entry follows the cited Sumerian composition, not a merged account of every later descent story.",
  "descent",
  "ETCSL 1.4.1",
  "yesod",
  ["return", "threshold"],
);
for (const [id, name, summary, locator, group, office, aliases] of [
  [
    "inana",
    "Inana / Inanna",
    "Descends through seven gates and later returns under conditions.",
    "Lines 114–172, 282–289",
    "return",
    "yesod",
    ["Inanna"],
  ],
  [
    "ereshkigal",
    "Ereshkigal",
    "Rules the underworld court encountered by Inana.",
    "Lines 94–128",
    "threshold",
    "gevurah",
    ["Erec-ki-gala"],
  ],
  [
    "ninshubur",
    "Ninshubur",
    "Carries out Inana’s instructions and seeks help when she does not return.",
    "Lines 173–225",
    "return",
    "chesed",
    ["Nincubura"],
  ],
  [
    "enki",
    "Enki",
    "Sends helpers with life-giving substances in the descent composition.",
    "Lines 217–253",
    "return",
    "chokhmah",
    [],
  ],
  [
    "neti",
    "Neti",
    "The gatekeeper announces Inana and follows the underworld’s entry instructions.",
    "Lines 78–128",
    "threshold",
    "netzach",
    [],
  ],
  [
    "dumuzi",
    "Dumuzi",
    "Becomes entangled in the cost of Inana’s return.",
    "Lines 348–358",
    "return",
    "yesod",
    ["Dumuzid"],
  ],
] as const)
  entry(
    id,
    name,
    "Figure",
    "Sumerian",
    "Role in Inana’s descent",
    summary,
    "The role belongs to this named text. Similarities to other traditions do not establish identity.",
    "descent",
    locator,
    office,
    [group],
    "Source account",
    [...aliases],
  );
entry(
  "popol-vuh",
  "Popol Vuh",
  "Text",
  "K’iche’ Maya",
  "K’iche’ textual tradition; Christenson translation",
  "The work relates creation accounts and the adventures of the Hero Twins.",
  "K’iche’ is a specific Maya context. It must not be collapsed into Aztec material or every Maya community’s tradition.",
  "popol",
  "Introduction and Hero Twins narrative",
  "netzach",
  ["return", "threshold"],
);
entry(
  "hero-twins",
  "The Hero Twins",
  "Figure",
  "K’iche’ Maya",
  "Hunahpu and Xbalanque in the Popol Vuh",
  "The twins confront underworld challenges, including the ball game.",
  "The paired-action puzzle in VORTEX is new fiction; it is not a reenactment of a sacred practice.",
  "popol",
  "The summons of Hunahpu and Xbalanque to Xibalba",
  "netzach",
  ["threshold", "return"],
  "Source account",
  ["Hunahpu", "Xbalanque", "Hunahpú", "Xbalanqué"],
);
entry(
  "ball-player",
  "The ball player at La Corona",
  "Object",
  "Classic Maya",
  "La Corona, Guatemala · AD 600–750",
  "A limestone panel depicts a ball player; the museum discusses sporting, ritual and cosmological contexts.",
  "This Classic-period object and the K’iche’ text have distinct contexts, even where comparison is useful.",
  "maya",
  "NMAI 24/457; Edgar Suyuc and object discussion",
  "netzach",
  ["threshold"],
);
entry(
  "kanaga",
  "Imina kanaga",
  "Object",
  "Dogon",
  "Sanga-region mask tradition; 20th-century museum object",
  "The Met records different interpretations of kanaga and acknowledges gaps in understanding.",
  "A public object description is not permission to imitate a restricted ritual or assume one universal interpretation.",
  "dogon",
  "Object 1987.74i; interpretation discussion",
  "binah",
  ["threshold"],
);
entry(
  "dama",
  "Dama",
  "Practice",
  "Dogon",
  "A ritual context described in the cited museum record",
  "The record situates kanaga within dama, a funerary context involving remembrance and hospitality.",
  "This is a reference note, not a playable ritual. Community context matters beyond an object label.",
  "dogon",
  "Opening description",
  "binah",
  ["memory", "return"],
);
entry(
  "dogon-restudy",
  "Reading the Dogon accounts",
  "Text",
  "Dogon · research history",
  "Griaule’s account and van Beek’s 1991 restudy",
  "Van Beek challenged important parts of Griaule’s account, including the significance attributed to Sirius.",
  "A disputed ethnographic claim is not established ancestral astronomy. Different accounts remain attributed rather than silently combined.",
  "restudy",
  "Dogon Restudied, Current Anthropology 32(2), 139–167",
  "binah",
  ["memory"],
  "Disputed account",
  ["Sirius", "Griaule", "van Beek"],
);
entry(
  "stamps",
  "Bitcoin Stamps",
  "Protocol",
  "Bitcoin",
  "Classic Stamps specification",
  "Classic Stamps carry image data through Bitcoin transaction outputs using Counterparty encoding.",
  "Preserving data does not establish its truth. Output design, chain history and interpretation still matter; SRC-20 is a separate record type.",
  "stamps",
  "What Makes a Bitcoin Stamp?",
  "hod",
  ["memory"],
);
entry(
  "kevin-saga",
  "The KEVIN Stamp Saga",
  "Text",
  "Bitcoin · community lore",
  "A contemporary meme narrative",
  "The Saga tells a story of repeated KEVIN images and a ghost in the machine.",
  "This is attributed community lore, not verified supernatural agency. Image Stamps and the SRC-20 token are distinct records.",
  "kevin",
  "Community narrative",
  "malkhut",
  ["memory"],
  "Source account",
  ["KEVIN"],
);
for (const [office, name] of Object.entries(OFFICE_RARE)) {
  const r = RARES.find((x) => x.name === name)!;
  const id = "asset-" + r.assetId;
  ATLAS_SOURCES[id] = {
    title: r.name + " · Counterparty record on xcp.io",
    url: r.explorer,
  };
  rows.push({
    id,
    name: r.name,
    aliases: [r.assetId],
    kind: "Asset",
    tradition: "Counterparty",
    context: "Bitcoin mainnet · recorded asset",
    summary:
      "An existing Counterparty asset, with its original art and a separate fictional role in VORTEX.",
    distinction:
      "Reading or discovering this record grants no token. Any Counterparty asset is eligible for the wider archive; these ten have authored encounters.",
    evidence: "Source account",
    source: id,
    locator: "Asset " + r.assetId + "; checked " + r.verifiedAt,
    office: office as SefirahId,
    groups: [
      office === "hod" || office === "malkhut" || office === "chokhmah"
        ? "memory"
        : office === "netzach" || office === "gevurah"
          ? "threshold"
          : "return",
    ],
    image: r.image,
    token: r.name,
  });
}
export const ATLAS = rows;
export const atlasEntry = (id: string) => ATLAS.find((e) => e.id === id);
export type AtlasRelation = {
  id: string;
  from: string;
  to: string;
  why: string;
  evidence: Evidence;
  source: string;
  locator: string;
};
export const RELATIONS: AtlasRelation[] = ATLAS.flatMap((e) =>
  e.groups
    .filter((g) => g !== e.id)
    .map((g) => ({
      id: e.id + ":" + g,
      from: e.id,
      to: g,
      why: `VORTEX places ${e.name} in this exploration theme. ${e.summary} This is a comparison prompt, not a claim of common origin.`,
      evidence: "VORTEX interpretation" as Evidence,
      source: "vortex",
      locator: "Editorial cluster membership",
    })),
);
for (const [from, to, why, source, locator] of [
  [
    "inana",
    "descent",
    "A participant in this composition.",
    "descent",
    "ETCSL 1.4.1",
  ],
  [
    "ninshubur",
    "inana",
    "Seeks help on Inana’s behalf.",
    "descent",
    "Lines 173–225",
  ],
  [
    "neti",
    "ereshkigal",
    "Follows the court’s gate instructions.",
    "descent",
    "Lines 114–128",
  ],
  [
    "hero-twins",
    "popol-vuh",
    "Appear in this K’iche’ narrative.",
    "popol",
    "Hero Twins narrative",
  ],
  [
    "kanaga",
    "dama",
    "The museum situates the mask in this ritual context.",
    "dogon",
    "Opening description",
  ],
] as const)
  RELATIONS.push({
    id: from + ":" + to,
    from,
    to,
    why,
    evidence: "Source account",
    source,
    locator,
  });
export function searchAtlas(query: string, tradition = "all", group = "all") {
  const normalize = (s: string) =>
    s.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
  const q = normalize(query.trim()).slice(0, 100);
  return ATLAS.filter(
    (e) =>
      (tradition === "all" || e.tradition === tradition) &&
      (group === "all" || e.groups.includes(group)) &&
      normalize(
        [e.name, ...e.aliases, e.tradition, e.summary, e.kind].join(" "),
      ).includes(q),
  );
}
