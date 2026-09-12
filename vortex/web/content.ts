import type { Pillar, SefirahId } from "./lattice.ts";
export type Rite = {
  name: string;
  prompt: string;
  choices: [string, string, string];
  outcomes: [string, string, string];
};
export type OfficeContent = {
  subtitle: string;
  scene: string;
  detail: string;
  classical: string;
  folk: string;
  rite: Rite;
};
export const CONTENT: Record<SefirahId, OfficeContent> = {
  keter: {
    subtitle: "The crown has logged off",
    scene:
      "Above the last stair, a winged frog sits on a throne that casts no shadow. A very small scarab is polishing an invisible crown.",
    detail:
      "The scarab hands you a receipt for absolutely nothing. It is the first honest receipt you have seen all day. The throne is empty the moment you stop expecting an emperor.",
    classical:
      "You brought Mercy and Severity into one heart. Now see whether you can wear a crown without turning everyone else into a subject.",
    folk: "You made it, fren. The final boss was the need to have a final boss. Extremely expensive hat, though.",
    rite: {
      name: "The invisible crown",
      prompt:
        "The scarab offers an invisible crown. What do you leave on the throne?",
      choices: [
        "My need to be right",
        "My need for applause",
        "My need to finish first",
      ],
      outcomes: [
        "The scarab issues a receipt for one surrendered certainty. The paper weighs less than before.",
        "Nobody claps. The sun rises anyway. A very promising development.",
        "Another frog arrives ahead of you. You discover that you are still here.",
      ],
    },
  },
  chokhmah: {
    subtitle: "The scriptorium of questionable certainty",
    scene:
      "An ibis-beaked frog is arguing with his own footnote. Papyrus scrolls tower over a blue-tiled well; one has escaped and is learning to fly.",
    detail:
      "A margin note reads: SOURCE? The note has its own margin note. Thoth looks delighted. Beyond his desk, a carved THOTHPEPE gazes back from the archive.",
    classical:
      "The ibis has two jobs: keeping the record and admitting when the record needs a correction. You may find the second more demanding.",
    folk: "Another ancient prophecy with no source. Classic. Bring a question, fren. We have enough confident frogs.",
    rite: {
      name: "The disputed footnote",
      prompt:
        "The ibis offers you a dangerously confident scroll. What goes in its margin?",
      choices: [
        "What have we not noticed?",
        "Who is missing from this story?",
        "What would change our minds?",
      ],
      outcomes: [
        "The scroll develops a window. Fresh air causes three ancient errors to fall off.",
        "A frog from outside the frame pulls up a chair. The record gets better.",
        "The ibis draws an arrow in both directions. He respects the edit.",
      ],
    },
  },
  binah: {
    subtitle: "The temple of fewer open tabs",
    scene:
      "A frog in linen tends a pair of scales. One pan holds a feather. The other holds seventeen opinions nobody asked for.",
    detail:
      "The feather is winning. A novice quietly removes an eighteenth opinion from his sleeve. The monk pretends not to notice.",
    classical:
      "Give the thought a vessel. A thought without an edge spills into every room and calls itself wisdom.",
    folk: "Seventeen tabs open. One is playing the temple flute. Let us locate it before enlightenment.",
    rite: {
      name: "The weighing of the bags",
      prompt:
        "The scales cannot balance while you hold all seventeen opinions. Put one thing down.",
      choices: [
        "An answer I borrowed",
        "A promise I cannot keep",
        "An argument I have already won",
      ],
      outcomes: [
        "The feather rises. You are no less yourself without the borrowed answer.",
        "The promise becomes small enough to carry. The monk gives one approving blink.",
        "The argument tries to crawl back into your bag. You gently close the zip.",
      ],
    },
  },
  chesed: {
    subtitle: "Soup before prophecy",
    scene:
      "Under the wings of a lotus-crowned frog, a temple kitchen is in glorious disorder. Everyone is being fed, including the crocodile who said he was just browsing.",
    detail:
      "An enormous soup pot bears three instructions: FEED THE GUEST. FEED THE COOK. DO NOT PUT THE SCARAB IN THE SOUP. The scarab underlines the last one.",
    classical:
      "A wing can shelter without owning the creature beneath it. Offer what leaves both giver and guest able to breathe.",
    folk: "Welcome, fren. Soup is free. The emotional invoice has been abolished. Yes, you also get bread.",
    rite: {
      name: "The sacred soup ledger",
      prompt:
        "The last bowl of soup is ready. The cook has not eaten. What happens next?",
      choices: [
        "Split it with the cook",
        "Ask everyone to add a little",
        "Make a second pot together",
      ],
      outcomes: [
        "Two frogs eat. The ledger fails to find a loser.",
        "A small feast emerges from several very ordinary cupboards.",
        "Someone chops. Someone stirs. Even the crocodile does the washing up.",
      ],
    },
  },
  gevurah: {
    subtitle: "The hall of proportionate consequences",
    scene:
      "A jackal-faced sentinel examines a tiny banhammer beside an unnecessarily enormous one. Somewhere, a frog is attempting to appeal a law of physics.",
    detail:
      "The enormous hammer is dusty. The little one has a beautifully worn handle. Someone has scratched JUST ENOUGH into the bench.",
    classical:
      "Power is most exact when it knows where to stop. Cut the knot. Leave the cloth, the hand, and the possibility of tomorrow.",
    folk: "We can set a boundary without summoning the apocalypse. Tiny hammer first. The big one is mostly for the decor.",
    rite: {
      name: "The tiny banhammer",
      prompt:
        "A guest keeps eating the temple’s ceremonial candles. Choose the smallest useful boundary.",
      choices: [
        "Move the candles and offer lunch",
        "Say clearly: the candles stay",
        "Ask the guest to help replace them",
      ],
      outcomes: [
        "The guest wanted a snack, not a conflict. An astonishingly cheap investigation.",
        "The boundary holds. No dynasty needs to fall for this.",
        "Two new candles appear. The guest now has a sensible respect for wax.",
      ],
    },
  },
  tiferet: {
    subtitle: "The solar boat has aux",
    scene:
      "A solar boat is stuck between two banks. One frog insists on mercy. Another insists on limits. A third has brought a drum machine and no useful advice.",
    detail:
      "Two oars rest across the deck. One alone makes the boat spin. Together they carry it straight toward a sun wearing a deeply unimpressed expression.",
    classical:
      "The heart is not a compromise in which both currents weaken. It is a vessel in which both can work.",
    folk: "Soft heart. Firm oar. Both hands, fren. We are not doing another century of ceremonial doughnuts.",
    rite: {
      name: "Tune the solar boat",
      prompt:
        "Mercy wants to invite everyone. Severity wants the boat to stay afloat. Give them a shared plan.",
      choices: [
        "Hear both before sailing",
        "Name the care behind both concerns",
        "Make two safe trips",
      ],
      outcomes: [
        "Both frogs finish their sentences. The drum-machine frog calls it a remix.",
        "One protects the guests. One protects the boat. The disagreement finds its shape.",
        "Everyone crosses. The sun grudgingly awards full marks for logistics.",
      ],
    },
  },
  netzach: {
    subtitle: "The crocodile’s guest list",
    scene:
      "Papyrus reeds surround a gate attended by a crocodile with a clipboard. Every frog on the list has written PLUS ONE in suspiciously similar handwriting.",
    detail:
      "Behind the gate, you find a narrow channel toward Kingdom. The crocodile has been sitting on the sign. He calls this information management.",
    classical:
      "A living boundary bends without abandoning its roots. Decide what belongs here and what needs a different shore.",
    folk: "The croc says you are not on the list. The list is a napkin. Look around before accepting his administrative authority.",
    rite: {
      name: "The crocodile’s guest list",
      prompt:
        "The crocodile blocks a safe channel. Negotiate a boundary that can stay alive.",
      choices: [
        "Keep the roots, open the water",
        "Make a resting place beside the gate",
        "Write a guest rule everyone can read",
      ],
      outcomes: [
        "The reeds bend. The bank holds. The crocodile calls it his idea.",
        "The waiting frogs sit down. Urgency loses its ceremonial hat.",
        "The napkin becomes legible. The crocodile loses a little mystery and gains a lunch break.",
      ],
    },
  },
  hod: {
    subtitle: "The papyrus posting station",
    scene:
      "Brushes rattle in a ceramic jar. An ink-stained frog is carving a sentence into a stamp, then laughing so hard the table moves.",
    detail:
      "The desk is littered with magnificent failed drafts. A THOTHPEPE likeness presides over them. On the wall: THE FIRST DRAFT IS ALLOWED TO BE A FROG.",
    classical:
      "A mark becomes yours when you can stand beside it after the applause has gone elsewhere. Choose language that survives an ordinary morning.",
    folk: "Welcome to the posting temple. We turn thoughts into marks and typos into ancient mysteries. What are we making?",
    rite: {
      name: "The unborrowed post",
      prompt:
        "Your papyrus is blank. Before the ink lands, decide what it should do.",
      choices: [
        "Make room for another frog",
        "Say one thing clearly",
        "Carry a little light",
      ],
      outcomes: [
        "The margins widen. There is room for a reader to bring themselves.",
        "The sentence drops three impressive words and starts saying something.",
        "A tiny sun appears in the ink. It does not ask you to subscribe.",
      ],
    },
  },
  yesod: {
    subtitle: "The staircase beneath the lily pad",
    scene:
      "A builder frog presents an ambitious blueprint for a floating pyramid. Its entire foundation is labelled TOMORROW, PROBABLY.",
    detail:
      "Below the blueprint lies one plain stone. The builder has finally written TODAY on it. You can almost hear the whole pyramid exhale.",
    classical:
      "A dream does not need less imagination. It needs one small agreement with the ground.",
    folk: "Vision: immaculate. Foundation: vibes. Let us introduce a brick to this situation.",
    rite: {
      name: "One actual brick",
      prompt:
        "The floating pyramid needs something that can happen today. Choose its first stone.",
      choices: [
        "Finish one small kindness",
        "Practice one useful boundary",
        "Make something without posting it",
      ],
      outcomes: [
        "A modest kindness holds up an immodest amount of architecture.",
        "The stone fits. No other stone has to apologise for existing.",
        "The thing exists before anyone likes it. A radical building material.",
      ],
    },
  },
  malkhut: {
    subtitle: "The floor. The record. The frog.",
    scene:
      "The temple opens onto a noisy riverside bazaar. A scribe keeps a ledger beside real Rare Pepe portraits. A boatman refuses to accept enlightenment as exact change.",
    detail:
      "The old RAREPEPE portrait has outlived countless grand announcements. Beside it, the ledger records names and marks. The scribe leaves your wallet firmly on your side of the desk.",
    classical:
      "A story carried into matter acquires consequences. Keep the record honest, and your keys where they belong.",
    folk: "You reached the actual floor, fren. The receipt exists. The frog exists. Your keys still belong to you. A surprisingly solid ending.",
    rite: {
      name: "The honest receipt",
      prompt:
        "The scribe asks what you will actually carry out of the temple. Choose something you can return to.",
      choices: [
        "A kindness I can sustain",
        "A truth I can speak gently",
        "A practice small enough for tomorrow",
      ],
      outcomes: [
        "The receipt reads: ONE REPEATABLE KINDNESS. The scribe puts away the unnecessary flourish.",
        "Your truth survives contact with another frog. This counts.",
        "The grand pyramid has become a small step. You can walk that far.",
      ],
    },
  },
};
export const QUESTIONS = [
  {
    text: "A stranger is lost beside the water. Your first instinct?",
    answers: [
      "Walk beside them for a while",
      "Help them read the map",
      "Ask where they hoped to go",
    ],
  },
  {
    text: "A door has been left open. What draws your attention?",
    answers: [
      "Who might need shelter",
      "What the threshold protects",
      "The meeting of inside and outside",
    ],
  },
  {
    text: "You find an unfinished song. What would you add?",
    answers: ["A new voice", "A steady rhythm", "A space to listen"],
  },
  {
    text: "Two friends ask more than you can give. You choose to…",
    answers: [
      "Offer what care I can sustain",
      "Make my limits clear",
      "Find a smaller promise we can share",
    ],
  },
  {
    text: "In a garden after a storm, you first notice…",
    answers: [
      "The new shoots",
      "The roots that held",
      "What bent and survived",
    ],
  },
  {
    text: "You can carry one thing into the tree.",
    answers: ["An open hand", "An honest question", "A little stillness"],
  },
];
export function quizPillars(answers: number[]): Record<Pillar, number> {
  const scores = { mercy: 0.18, severity: 0.18, balance: 0.18 };
  const keys: Pillar[] = ["mercy", "severity", "balance"];
  answers.forEach((i) => {
    if (Number.isInteger(i) && i >= 0 && i < 3) scores[keys[i]] += 0.1;
  });
  return scores;
}
