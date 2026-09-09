import type { SefirahId } from "./lattice";

export type PathLetter = {
  from: SefirahId;
  to: SefirahId;
  letter: string;
  title: string;
  meaning: string;
};

/** The 22 streams. Keys are unordered; lookup uses pathBetween. */
export const PATH_LETTERS: PathLetter[] = [
  { from: "keter", to: "chokhmah", letter: "Aleph", title: "Ox / Air", meaning: "Breath before a name. The ox pulls what has no words yet." },
  { from: "keter", to: "binah", letter: "Beth", title: "House", meaning: "A house is a boundary you live in. Form begins as a roof." },
  { from: "keter", to: "tiferet", letter: "Gimel", title: "Camel / Moon", meaning: "The camel crosses the empty stretch. Crown and heart do not touch without a journey." },
  { from: "chokhmah", to: "binah", letter: "Daleth", title: "Door", meaning: "Flash meets form. A door that only opens one way at a time." },
  { from: "chokhmah", to: "tiferet", letter: "Heh", title: "Window", meaning: "Insight looking at beauty. Do not climb through. Look." },
  { from: "chokhmah", to: "chesed", letter: "Vav", title: "Nail", meaning: "A nail joins. Wisdom that cannot hold is only weather." },
  { from: "binah", to: "tiferet", letter: "Zain", title: "Sword", meaning: "Understanding cuts. Beauty survives the honest blade." },
  { from: "binah", to: "gevurah", letter: "Cheth", title: "Fence", meaning: "Discipline is a fence, not a wall. Severity lives inside it." },
  { from: "chesed", to: "gevurah", letter: "Teth", title: "Serpent", meaning: "Mercy and severity coil. Neither eats the other if the spine is true." },
  { from: "chesed", to: "tiferet", letter: "Yod", title: "Hand", meaning: "Kindness offered as a hand, not a flood." },
  { from: "chesed", to: "netzach", letter: "Kaph", title: "Palm", meaning: "The open palm that can still close. Endurance begins as a gift." },
  { from: "gevurah", to: "tiferet", letter: "Lamed", title: "Ox-goad", meaning: "A goad teaches the heart to walk straight." },
  { from: "gevurah", to: "hod", letter: "Mem", title: "Water", meaning: "Severity poured into language. Water takes the shape of the vessel." },
  { from: "tiferet", to: "netzach", letter: "Nun", title: "Fish", meaning: "Beauty that swims. Victory is not a pose." },
  { from: "tiferet", to: "hod", letter: "Samekh", title: "Prop", meaning: "The heart props the mouth. Speech that cannot stand falls." },
  { from: "tiferet", to: "yesod", letter: "Ayin", title: "Eye", meaning: "The eye of the tree. Foundation is what the heart is willing to see." },
  { from: "netzach", to: "hod", letter: "Peh", title: "Mouth", meaning: "Endurance speaking. A mouth without a fence is a flood." },
  { from: "netzach", to: "yesod", letter: "Tzaddi", title: "Fish-hook", meaning: "Victory hooks the foundation. Do not land every fish." },
  { from: "netzach", to: "malkhut", letter: "Qoph", title: "Back of head", meaning: "The unconscious descent. Kingdom can be reached without looking forward." },
  { from: "hod", to: "yesod", letter: "Resh", title: "Head / Sun", meaning: "Language becoming ground. The sun of the mouth sets into the moon." },
  { from: "hod", to: "malkhut", letter: "Shin", title: "Tooth / Fire", meaning: "A word that can burn into the floor of the world." },
  { from: "yesod", to: "malkhut", letter: "Tav", title: "Mark / Saturn", meaning: "The mark. Foundation writes itself into form." },
];

export function pathKey(a: SefirahId, b: SefirahId) {
  return [a, b].sort().join(":");
}

export function pathBetween(a: SefirahId, b: SefirahId): PathLetter | null {
  return (
    PATH_LETTERS.find(
      (p) => (p.from === a && p.to === b) || (p.from === b && p.to === a),
    ) ?? null
  );
}
