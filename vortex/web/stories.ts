import { IDS } from "./lattice.ts";
import type { SefirahId } from "./lattice.ts";
import type { Seeker } from "./session.ts";
import { PATH_LETTERS } from "./paths.ts";

export type StoryProgress = {
  choice: number;
  delivered: boolean;
  resolution: number | null;
};
type Three = [string, string, string];
export type Story = {
  title: string;
  destination: SefirahId;
  request: string;
  choices: Three;
  cargo: Three;
  delivery: Three;
  returnPrompt: string;
  endings: Three;
  aftermath: Three;
};
// These are authored VORTEX fiction starring the existing assets in OFFICE_RARE.
// The errands carry ideas and props, never blockchain tokens or ownership.
export const STORIES: Record<SefirahId, Story> = {
  keter: {
    title: "The crown's day off",
    destination: "malkhut",
    request:
      "LORDKEK has received forty-seven invitations to preside over things. His throne would like a day off. The bazaar needs a host, but perhaps it does not need another ruler.",
    choices: [
      "Invite the quietest stallholder",
      "Give every stall a turn",
      "Leave the host's chair empty",
    ],
    cargo: [
      "an invitation with room for a refusal",
      "a rota drawn on the back of a crown",
      "one gloriously empty chair",
    ],
    delivery: [
      "The quiet stallholder accepts, provided someone else does the announcing.",
      "The boatman claims the soup hour. Nobody is surprised.",
      "Without a throne to stare at, the bazaar starts noticing itself.",
    ],
    returnPrompt:
      "LORDKEK comes back in a linen apron. Apparently not being essential has opened up his whole afternoon. What should survive this royal experiment?",
    endings: [
      "Keep a seat for the overlooked",
      "Keep the rota visible",
      "Let the host join the crowd",
    ],
    aftermath: [
      "A small seat beside the throne is always reserved for a voice the room has missed.",
      "The throne has office hours. The scarab enforces them with alarming competence.",
      "The crown hangs on a kitchen hook. LORDKEK is surprisingly good at washing bowls.",
    ],
  },
  chokhmah: {
    title: "The prophecy with a correction",
    destination: "hod",
    request:
      "THOTHPEPE's bestselling prophecy predicts a flood of wisdom. A junior scribe points out that the original says a flood of biscuits. The correction must reach the posting station before the next sermon.",
    choices: [
      "Bring the original beside the correction",
      "Give the junior scribe the byline",
      "Ask readers to check the translation",
    ],
    cargo: [
      "two papyri that disagree politely",
      "a correction signed by the smallest scribe",
      "a translation with its uncertainty showing",
    ],
    delivery: [
      "KEKET prints both versions. The biscuit merchants withdraw their theological objection.",
      "The junior scribe's name fits at the top. The old prophecy becomes less lonely.",
      "Three readers catch a second error. The ibis calls this peer re-pepe-view.",
    ],
    returnPrompt:
      "THOTHPEPE's corrected scroll has fewer worshippers and better footnotes. He asks what the next edition should promise.",
    endings: [
      "A place for overlooked witnesses",
      "A visible correction history",
      "A question at the end of every scroll",
    ],
    aftermath: [
      "The scriptorium keeps a guest stool beside every grand claim.",
      "Corrections hang beside the scrolls. Nobody has to excavate the truth from a deleted post.",
      "Every prophecy now ends with a question. The biscuits remain excellent.",
    ],
  },
  binah: {
    title: "The monastery's loudest silence",
    destination: "yesod",
    request:
      "PEPEZENMSTR has achieved inner silence. Unfortunately the meditation bench squeaks in D minor. ZAZENPEPE might know how to give the bench a quieter foundation.",
    choices: [
      "Carry a cushion for the next novice",
      "Bring a careful sketch of the loose joint",
      "Record the rhythm of the squeak",
    ],
    cargo: [
      "a cushion with no enlightenment requirements",
      "a diagram of one extremely ordinary loose joint",
      "a surprisingly catchy bench rhythm",
    ],
    delivery: [
      "ZAZENPEPE puts the cushion on a sound bench. Comfort is permitted before wisdom.",
      "One peg fixes the joint. The builder looks almost disappointed by the lack of a grand theory.",
      "The builder taps along, then steadies the bench. The rhythm gets a farewell performance.",
    ],
    returnPrompt:
      "The bench is quiet. PEPEZENMSTR admits that he misses the D minor. What can the monastery learn from a problem that was partly a piece of furniture?",
    endings: [
      "Make the novices comfortable first",
      "Keep a small repair kit nearby",
      "Leave room to laugh during practice",
    ],
    aftermath: [
      "The monastery asks whether you need a cushion before it asks whether you need a teaching.",
      "Beside the sacred feather sits a screwdriver. Nobody confuses their purposes.",
      "One novice laughs. The master does too. The feather remains undisturbed.",
    ],
  },
  chesed: {
    title: "Soup for the sentinel",
    destination: "gevurah",
    request:
      "GODDESSISIS notices that GODANUBIS has guarded lunch through three consecutive lunches. She needs someone to bring a meal that does not become another obligation.",
    choices: [
      "Pack enough to share with the guest",
      "Include a note: your break is covered",
      "Bring ingredients for a pot at the gate",
    ],
    cargo: [
      "two warm bowls and no emotional invoice",
      "a lunch break with the word REQUIRED crossed out",
      "a tiny travelling soup kitchen",
    ],
    delivery: [
      "The sentinel and the candle-eating guest sit on the same step. The candles survive lunch.",
      "GODANUBIS puts down the tiny hammer. For once the boundary protects his own afternoon.",
      "The gate acquires a soup pot. Security has never smelled this reassuring.",
    ],
    returnPrompt:
      "GODDESSISIS receives a washed bowl and a thank-you written in exceptionally stern handwriting. How should the kitchen keep this going?",
    endings: [
      "Always count the cook and the guard",
      "Agree a break before the queue starts",
      "Let each temple take a cooking turn",
    ],
    aftermath: [
      "The soup ledger now counts the frogs doing the work, in ink rather than as an afterthought.",
      "The kitchen closes briefly for the cook's lunch. The sky declines to fall.",
      "Visiting temples take turns at the stove. GODANUBIS makes very precise dumplings.",
    ],
  },
  gevurah: {
    title: "The candle amnesty",
    destination: "chesed",
    request:
      "GODANUBIS has confiscated a sack of ceremonial candles from a repeat snacker. The guest says they looked like bread. The sentinel needs the kitchen's help with a consequence that repairs something.",
    choices: [
      "Ask for a proper meal for the guest",
      "Make signs that distinguish wax from bread",
      "Arrange a candle-replacement afternoon",
    ],
    cargo: [
      "a hungry guest's version of events",
      "a sign reading WAX IS NOT A FOOD GROUP",
      "a repair plan with a snack interval",
    ],
    delivery: [
      "GODDESSISIS feeds the guest. The account of the incident gets several important new details.",
      "The cook labels the bread too. The scarab requests its own DO NOT EAT sign.",
      "The kitchen supplies lunch for the repair crew. Four usable candles emerge from the afternoon.",
    ],
    returnPrompt:
      "GODANUBIS receives four candles, one apology, and a bread roll. The enormous hammer remains dusty. What belongs in the gate's new rule?",
    endings: [
      "Ask what happened before passing judgment",
      "State the boundary where everyone can see it",
      "Offer a route back after repair",
    ],
    aftermath: [
      "The gate keeps a stool for hearing the whole story before reaching for a hammer.",
      "The rules fit on one readable board. The sentinel is unreasonably proud of the spacing.",
      "A repaired mistake earns a welcome back. The guest now helps light the candles.",
    ],
  },
  tiferet: {
    title: "The solar boat's difficult encore",
    destination: "netzach",
    request:
      "PEPEPHARAON has promised a sunset procession. SPHINXPEPE's narrow channel can carry a boat, or the crocodile's ego, but probably not both at once. Someone must agree the passage.",
    choices: [
      "Ask who needs the quiet crossing",
      "Draw a safe boarding limit",
      "Propose two smaller processions",
    ],
    cargo: [
      "a guest list that begins with the least pushy frog",
      "a boarding plan with actual numbers",
      "a sunset timetable with a second chance",
    ],
    delivery: [
      "SPHINXPEPE opens a calm boarding space. The crocodile discovers that volume is not a ticket.",
      "The sphinx measures the channel. Even the clipboard admits that the boat has edges.",
      "Two sailings fit. The second group gets the better sunset and behaves with suspicious humility.",
    ],
    returnPrompt:
      "The boat returns with every passenger and most of the drum machine. PEPEPHARAON asks which part of the plan deserves to become a tradition.",
    endings: [
      "Hear the passenger at the back",
      "Let care and capacity set the course",
      "Make the second trip part of the celebration",
    ],
    aftermath: [
      "The solar boat's host listens to the back row before taking the microphone.",
      "Two oars and an honest passenger count carry the boat. The drum machine is optional.",
      "The second sailing has its own song. Nobody has to call it the consolation boat.",
    ],
  },
  netzach: {
    title: "The riddle's missing witness",
    destination: "chokhmah",
    request:
      "SPHINXPEPE has guarded the same riddle for centuries. A small frog points out that its answer assumes everyone owns shoes. The sphinx would like THOTHPEPE to check the question.",
    choices: [
      "Bring the barefoot frog's objection",
      "Mark the hidden assumption",
      "Ask for a riddle with several good answers",
    ],
    cargo: [
      "one inconvenient and entirely fair objection",
      "a riddle with its assumptions underlined",
      "a request for more than one right kind of frog",
    ],
    delivery: [
      "THOTHPEPE invites the witness into the margin. The margin proves too small; he starts a new page.",
      "The ibis finds three more assumptions. The sphinx's warranty does not cover this many centuries.",
      "The scribe writes three answers and leaves space for a fourth. No civilisation collapses.",
    ],
    returnPrompt:
      "SPHINXPEPE reads the revision and moves aside before you answer. Perhaps guarding a threshold can include changing the test.",
    endings: [
      "Let the next traveller question the riddle",
      "Explain what the gate actually protects",
      "Offer several ways through",
    ],
    aftermath: [
      "The sphinx asks whether its question makes sense before asking you to solve it.",
      "The crocodile's clipboard explains the boundary. His handwriting is almost a public service.",
      "The gate recognises more than one good answer. The reeds make room.",
    ],
  },
  hod: {
    title: "The post with no author",
    destination: "binah",
    request:
      "KEKET finds a beautiful papyrus circulating without its maker's name. Every repost says ancient wisdom. PEPEZENMSTR remembers the novice who wrote it yesterday, beside a squeaky bench.",
    choices: [
      "Carry the page back to its maker",
      "Ask permission before copying again",
      "Leave a blank credit instead of guessing",
    ],
    cargo: [
      "a famous page looking for its ordinary author",
      "a request that can be declined",
      "a credit line honestly marked UNKNOWN",
    ],
    delivery: [
      "The novice recognises a tea stain. Ancient wisdom turns out to be Tuesday's draft.",
      "The novice agrees to a reading, with their name attached. A request did what a thousand reposts could not.",
      "The master fills the gap with the novice's chosen name. Nobody has to invent an illustrious ancestor.",
    ],
    returnPrompt:
      "KEKET places the maker's name beside the papyrus. The page is no less beautiful for having been written yesterday. What should the posting station remember?",
    endings: [
      "Put the maker beside the work",
      "Keep permission with the copy",
      "Show uncertainty instead of inventing a source",
    ],
    aftermath: [
      "The posting station makes room for makers' names. The ink is the same size as the praise.",
      "A small permission note travels with each copied papyrus. It is much shorter than an argument.",
      "UNKNOWN is an acceptable entry in the archive. A guessed source is not.",
    ],
  },
  yesod: {
    title: "The pyramid that could open today",
    destination: "tiferet",
    request:
      "ZAZENPEPE's floating pyramid has a magnificent opening ceremony and no opening date. PEPEPHARAON could help turn its first sound platform into something frogs can actually use.",
    choices: [
      "Offer one safe place to rest",
      "Bring the smallest workable blueprint",
      "Invite a few frogs to try the first platform",
    ],
    cargo: [
      "a proposal for one good bench",
      "a blueprint with most of the pyramid crossed out",
      "three trial invitations and a pencil",
    ],
    delivery: [
      "The pharaoh moors the bench where tired passengers can reach it. It opens immediately.",
      "The solar boat can carry the modest platform. The grand opening becomes an ordinary useful afternoon.",
      "The visitors find a loose plank before a crowd does. Their feedback is mostly about the bench.",
    ],
    returnPrompt:
      "ZAZENPEPE sees frogs using the first platform. The unbuilt spire is briefly jealous. What earns the next stone?",
    endings: [
      "Whether it helps the frogs already here",
      "Whether the first piece still holds",
      "What the visitors discover by using it",
    ],
    aftermath: [
      "The builder adds a shaded bench before a decorative spire. Actual frogs approve.",
      "Every new stone gets a foundation check. The blueprint has stopped promising levitation.",
      "A pencil hangs by the platform. The building improves whenever someone uses it.",
    ],
  },
  malkhut: {
    title: "The portrait that declined a throne",
    destination: "keter",
    request:
      "The bazaar's RAREPEPE portrait has been offered an extremely important commemorative throne. The scribe suspects the portrait would rather remain a portrait. LORDKEK knows a thing or two about unnecessary crowns.",
    choices: [
      "Bring the original record, without a sales pitch",
      "Ask what the throne would actually change",
      "Suggest a place at the ordinary table",
    ],
    cargo: [
      "an honest record with no promised powers",
      "one practical question about a ceremonial chair",
      "an invitation to sit beside everyone else",
    ],
    delivery: [
      "LORDKEK checks the record and adds no prophecy. A real thing can stand without an invented promise.",
      "The throne would mainly block the doorway. The scarab quietly revises the floor plan.",
      "The winged frog brings an ordinary stool. It has excellent decentralisation properties: four legs.",
    ],
    returnPrompt:
      "The scribe displays the portrait beside its actual record. Nobody has become a monarch by looking at it. How should the bazaar welcome the next visitor?",
    endings: [
      "Tell the story without promising ownership",
      "Keep the record available to inspect",
      "Make room at the table without a purchase",
    ],
    aftermath: [
      "The scribe tells the portrait's story and keeps the fictional adventure separate from its token.",
      "The bazaar's records stay beside the art. Looking closer never requires a sales conversation.",
      "The table welcomes another frog. No receipt is required for a place to sit.",
    ],
  },
};

export const completedStories = (s: Seeker) =>
  IDS.filter((id) => s.stories[id]?.resolution != null);
export const activeStories = (s: Seeker) =>
  IDS.filter((id) => s.stories[id] && s.stories[id]!.resolution === null);
export function storyStage(
  s: Seeker,
  id: SefirahId,
): "unmet" | "available" | "deliver" | "return" | "complete" {
  const p = s.stories[id];
  if (!p) return s.rites[id] === undefined ? "unmet" : "available";
  return p.resolution !== null
    ? "complete"
    : p.delivered
      ? "return"
      : "deliver";
}
export const readyForFestival = (s: Seeker) =>
  s.rooted &&
  completedStories(s).length >= 3 &&
  PATH_LETTERS.filter((p) => (s.crossings[p.id] ?? 0) >= 2).length >= 4;
export const FESTIVAL_CHOICES: Three = [
  "Set a table with a place for every frog",
  "Light a procession along the safe channels",
  "Open a night of unfinished songs",
];
export const FESTIVAL_ENDINGS: Three = [
  "THE LONG TABLE · Bowls pass beneath the stars. The guard eats before his soup gets cold. Nobody has to earn their seat with a prophecy. Your mark becomes the first line of the guest book.",
  "THE RIVER OF LANTERNS · Each light marks a safe passage. The crocodile reads the rules aloud, briefly and correctly. The solar boat carries your mark downstream. There is room for a second sailing.",
  "THE UNFINISHED CHORUS · The drum machine loses a bar and the frogs sing through the gap. A novice offers a verse. Even the sphinx leaves its answer open. Your mark becomes a refrain someone else can change.",
];
export function festivalGuests(s: Seeker): string[] {
  return completedStories(s).map(
    (id) => STORIES[id].aftermath[s.stories[id]!.resolution!],
  );
}
export function returnMemory(s: Seeker, id: SefirahId): string | null {
  const p = s.stories[id];
  if (p?.resolution != null) return STORIES[id].aftermath[p.resolution];
  const incoming = IDS.filter(
    (source) =>
      STORIES[source].destination === id && s.stories[source]?.delivered,
  );
  if (incoming.length) {
    const source = incoming.at(-1)!;
    return STORIES[source].delivery[s.stories[source]!.choice];
  }
  return null;
}
