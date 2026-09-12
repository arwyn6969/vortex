import type { Dialect, SefirahId } from "./lattice.ts";

export const STAMP_OFFICES = ["hod", "yesod", "malkhut"] as const;
export type StampOffice = (typeof STAMP_OFFICES)[number];
export const isStampOffice = (id: SefirahId): id is StampOffice =>
  STAMP_OFFICES.some((office) => office === id);

// Authored VORTEX correspondences. Sources and research boundaries are recorded
// in docs/BITCOIN_STAMPS.md; these voices do not speak for the original artists.
export const STAMP_TEACHINGS = {
  hod: {
    label: "I · Hod · The mark",
    title: "Give the meme a body",
    invitation:
      "The scribe has found a surface the flood cannot casually wash away.",
    folk: "A frog has drawn a frog. Excellent start. Now: did we keep the frog, or just the address of a cupboard where somebody promised to keep the frog?",
    classical:
      "A sign first takes shape in the workshop. Ask whether the vessel carries the image itself, or only directions to a distant room.",
    fact: "Classic Bitcoin Stamps encode image data into Bitcoin transaction outputs through Counterparty. The original format uses a STAMP: payload and multisig outputs; OLGA adds a more compact P2WSH encoding. The artwork can be reconstructed from the chain rather than depending only on an image host.",
    question: "What is worth giving a durable form?",
    reflection:
      "Let the mark carry an act of care, a joke worth retelling, or a witness to something real. A larger monument is not automatically a better memory.",
    source: "https://github.com/mikeinspace/stamps/blob/main/BitcoinStamps.md",
    sourceLabel: "Read the Bitcoin Stamps specification",
  },
  yesod: {
    label: "II · Yesod · The foundation",
    title: "What holds when the water rises?",
    invitation:
      "Below the dream-pyramid, a mason is arguing with a very temporary bookmark.",
    folk: "The pyramid was saved in a folder called FINAL_FINAL_REAL. The flood was unimpressed. Give the memory a foundation, fren. Then leave instructions for the next frog.",
    classical:
      "Foundation joins an image to a vessel that can bear it. The record may endure beyond its first keeper; another reader must still know how to read.",
    fact: "Stamps place data in output scripts. Bitcoin nodes retain the unspent transaction output set to validate future spending, even when pruning old blocks. This is the basis of Stamps’ resistance to pruning. If a data-bearing output is spent, its data leaves that set and remains in transaction history. Indexers interpret the records; an explorer is one way to read them.",
    question: "Does an enduring record make a claim true?",
    reflection:
      "The stone can preserve an error as faithfully as a kindness. Immutability preserves what was recorded; meaning, truth and responsibility still belong to its readers. Bitcoin’s continued operation and the output’s design matter.",
    source:
      "https://github.com/stampchain-io/btc_stamps/blob/main/docs/whitepaper/security.md",
    sourceLabel: "Read the storage and security model",
  },
  malkhut: {
    label: "III · Malkhut · The witness",
    title: "KEVIN is still here",
    invitation:
      "The archivist has prepared one place setting for KEVIN. The other place settings are becoming a situation.",
    folk: "We invited one KEVIN. The table has developed a KEVIN situation. The frogs call it a haunting; the scribe asks for the records. There is room for both at dinner.",
    classical:
      "At Kingdom, the sign enters public memory. A recurring image becomes a gathering place: many witnesses carrying one story, without becoming one voice.",
    fact: "The KEVIN Stamp Saga recounts 104 matching images, beginning with Stamp #4258, in its community legend of a ‘ghost in the machine’. The Stamps reference indexer identifies KEVIN as the first SRC-20 token. That token and the image Stamps are distinct records.",
    question: "How does a small image become a living myth?",
    reflection:
      "The ledger holds a trace. People bring the retelling, humour and recognition. In VORTEX, that is an image becoming an egregore: a shared story sustained by attention. It is a fictional correspondence, not a property enforced by Bitcoin.",
    source: "https://kevinstamp.com/",
    sourceLabel: "Enter the KEVIN Stamp Saga",
  },
} as const;

export function stampReply(id: SefirahId, dialect: Dialect): string {
  if (!isStampOffice(id))
    return "Follow the making of a mark through Hod, Yesod and Kingdom. Their Chamber of the Enduring Mark holds the Bitcoin Stamps teaching and KEVIN’s story.";
  const lesson = STAMP_TEACHINGS[id];
  return (
    lesson[dialect] +
    " " +
    (id === "malkhut"
      ? "KEVIN’s SRC-20 token is distinct from Counterparty asset balances. The chamber keeps their sources beside the story."
      : "Open the Chamber of the Enduring Mark here to follow the story and its sources.")
  );
}
