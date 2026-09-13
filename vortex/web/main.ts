import { atlasView, emptyAtlasView, inquiryPanel } from "./atlas-view.ts";
import { atlasEntry, searchAtlas } from "./atlas.ts";
import { inquiryMemory } from "./inquiries.ts";
import { withJourneyLock } from "./journey-lock.ts";
import "./style.css";
import { NODES, IDS, neighbors, guideName, shortPond } from "./lattice.ts";
import type { Dialect, SefirahId } from "./lattice.ts";
import { PATH_LETTERS, pathBetween } from "./paths.ts";
import { CONTENT, QUESTIONS, quizPillars } from "./content.ts";
import {
  RARES,
  rareAt,
  portraitStyle,
  PORTRAITS,
  PORTRAIT_TOKENS,
  supply,
} from "./rares.ts";
import {
  emptyWorld,
  activeSeeker,
  addSeeker,
  transition,
  status,
  riteCount,
  discovered,
  revealed,
  readyToRoot,
  isBound,
  voice,
} from "./session.ts";
import type { World, Action, Seeker } from "./session.ts";
import {
  loadWorld,
  saveWorld,
  importWorld,
  SAVE_KEY,
  MAX_SAVE_BYTES,
  BACKUP_KEY,
  RECOVERY_KEY,
  recoveryWorld,
  restoreBackup,
} from "./storage.ts";
import { issueChallenge, acceptSignature } from "./wallet.ts";
import { escapeHtml as e, safeText } from "./safety.ts";
import { nextStep } from "./navigation.ts";
import { registerJourneyTools } from "./webmcp.ts";
import type { JourneyContext } from "./webmcp.ts";
import { storyPanel, storyBook, festivalPanel } from "./story-view.ts";
import { completedStories, returnMemory } from "./stories.ts";
import { stampInvitation, stampBody } from "./stamps-view.ts";
import { isStampOffice } from "./stamps.ts";
import type { StampOffice } from "./stamps.ts";
import { assetAtlas, assetDestination } from "./explorer-view.ts";
import { CollectionLookup } from "./counterparty.ts";
import { collectionBody, collectionInvitation } from "./collection-view.ts";
import { chapterProgress, templeScene } from "./journey-view.ts";
import { worldVignette } from "./world-view.ts";
import { suggestedBoarding, boardingHelper, PASSENGERS } from "./boarding.ts";
import type { BoardingDraft, BoardingPlan, PassengerId } from "./boarding.ts";
import { senseWatcher } from "./watcher.ts";
import {
  feelEnabled,
  setFeelEnabled,
  unlockFeel,
  playWalk,
  playLook,
  playSit,
  playReveal,
  leanDrone,
} from "./feel-audio.ts";

const app = document.querySelector<HTMLDivElement>("#app")!;
let world = emptyWorld();
let loading = true,
  busy = false,
  damaged = false,
  newJourney = false;
let atlasState = emptyAtlasView();
let renderedSeekerId: string | null = null;
let boardingDraft: BoardingDraft = {};
let boardingScope = "";
let atlasTarget: SefirahId | null = null;
let backup: World | null = null;
let pendingRestore = false;
let restoreSnapshot: { raw: string | null; backup: string | null } | null =
  null;
let preservedAvailable = false;
let damagedOriginal: string | null = null;
let waitingWorker: ServiceWorker | null = null;
let updating = false;
let tracked: { seeker: string; story: SefirahId } | null = null;
let lastCrossed: { id: string; letter: string } | null = null;
let lastFeel: "walk" | "look" | "sit" | "reveal" | null = null;
let view: "tree" | "codex" | "journal" | "rares" | "stories" | "atlas" = "tree";
let renderedPageKey = "";
const readingPlaces = new Map<string, { scrollY: number; details: string[] }>();
function measureNavigation() {
  const height =
    document.querySelector(".topbar")?.getBoundingClientRect().height ?? 0;
  document.documentElement.style.setProperty(
    "--navigation-height",
    `${Math.ceil(height)}px`,
  );
}
const navigationObserver =
  typeof window.ResizeObserver === "function"
    ? new window.ResizeObserver(measureNavigation)
    : null;
let modal:
  | "journeys"
  | "settings"
  | "help"
  | "wallet"
  | "rare"
  | "collection"
  | "stamps"
  | null = null;
let modalTrigger: [string, string] | null = null;
let stampOffice: StampOffice = "hod";
let collectionSearch = "";
let collectionFilter: "world" | "all" = "all",
  collectionVisible = 50;
let collectionSeeker: string | null = null;
const collection = new CollectionLookup(() => {
  if (modal === "collection") render();
});
let selectedRare = "THOTHPEPE";
let message = "",
  messageError = false,
  pendingDelete = "";
let name = "",
  dialect: Dialect = "folk",
  answers: number[] = [],
  asking = false;
let audio: AudioContext | null = null,
  sound = false;
let reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const drafts: Record<string, string> = {};
const roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];
const mark =
  '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M20 3 6 13 20 21 34 13 20 3V37L6 28V13L34 28V13M6 28 20 37 34 28 20 21" fill="none" stroke="currentColor" stroke-width="1.3"/><circle cx="20" cy="21" r="3" fill="currentColor"/></svg>';
function notice(text: string, error = false) {
  message = text;
  messageError = error;
  render();
}
function errorText(error: unknown) {
  return error instanceof Error
    ? error.message
    : "Something interrupted that action. Your previous save is safe.";
}
async function commit(change: (w: World) => World | Promise<World>) {
  if (busy || damaged) return;
  busy = true;
  const expected = world.revision;
  const task = async () => {
    const current = await loadWorld(localStorage);
    if (current.revision !== expected) {
      world = current;
      throw new Error(
        "Another tab has changed this tree. The latest journey is loaded. Please try again.",
      );
    }
    const next = await change(current);
    saveWorld(localStorage, next, expected);
    backup = current;
    world = next;
  };
  try {
    await withJourneyLock(task);
    message = "";
    messageError = false;
  } catch (error) {
    message = errorText(error);
    messageError = true;
  } finally {
    busy = false;
    render();
  }
}
function focusPanel(id: string) {
  const el = document.getElementById(id);
  if (!el) return;
  if (el.tagName === "DETAILS") (el as HTMLDetailsElement).open = true;
  el.setAttribute("tabindex", "-1");
  el.focus({ preventScroll: true });
  el.scrollIntoView?.({
    block: "nearest",
    behavior: reduced ? "instant" : "smooth",
  });
}
function focusView() {
  const place = readingPlaces.get(renderedPageKey);
  if (!place) return focusPanel("main");
  const main = document.getElementById("main");
  main?.setAttribute("tabindex", "-1");
  main?.focus({ preventScroll: true });
  window.scrollTo({ top: place.scrollY, behavior: "instant" });
}
async function act(action: Action) {
  const from = activeSeeker(world)?.current;
  await commit((w) => transition(w, action));
  if (messageError) return;
  const s = activeSeeker(world);
  if (s && action.type === "walk" && from) {
    const path = pathBetween(from, action.to);
    if (path) {
      lastCrossed = { id: path.id, letter: path.letter };
      lastFeel = (s.crossings[path.id] ?? 0) === 1 ? "reveal" : "walk";
      if (lastFeel === "reveal") playReveal();
      else playWalk(false);
    }
    focusPanel("location-title");
  }
  if (s && action.type === "look") {
    lastFeel = "look";
    playLook();
    document
      .querySelector<HTMLButtonElement>("[data-show-rite]:not(:disabled)")
      ?.focus({ preventScroll: true });
  }
  if (s && action.type === "sit") {
    lastFeel = "sit";
    playSit();
  }
  if (s) leanDrone(s.pillars);
  const announcement = document.getElementById("journey-announcement");
  if (s && announcement)
    announcement.textContent = s.journal
      .filter((j) => j.turn === s.turns)
      .map((j) => j.text)
      .join(" ");
}
function closeDialog() {
  pendingRestore = false;
  restoreSnapshot = null;
  if (modal === "collection") collection.edit("");
  modal = null;
  message = "";
  pendingDelete = "";
  render();
  if (modalTrigger) {
    const [key, value] = modalTrigger;
    [...document.querySelectorAll<HTMLButtonElement>("button")]
      .find((el) => el.getAttribute(key) === value)
      ?.focus({ preventScroll: true });
  }
  modalTrigger = null;
}
function map(s: Seeker | null) {
  const x = (id: SefirahId) => 74 + NODES[id].x * 4.52;
  const y = (id: SefirahId) => 16 + NODES[id].y * 6.05;
  const edge = PATH_LETTERS.map((p) => {
    const nearby = s && (p.from === s.current || p.to === s.current);
    const target = s && p.from === s.current ? p.to : p.from;
    const state = s && nearby ? status(world, s, target) : "distant";
    const visited = s && !!s.crossings[p.id];
    const just = lastCrossed?.id === p.id;
    const mx = (x(p.from) + x(p.to)) / 2;
    const my = (y(p.from) + y(p.to)) / 2;
    return (
      '<g class="stream-group">' +
      '<line x1="' +
      x(p.from) +
      '" y1="' +
      y(p.from) +
      '" x2="' +
      x(p.to) +
      '" y2="' +
      y(p.to) +
      '" class="stream ' +
      state +
      (visited ? " walked" : "") +
      (just ? " just-crossed" : "") +
      '"/>' +
      (just
        ? '<text class="stream-letter" x="' +
          mx +
          '" y="' +
          (my - 6) +
          '" text-anchor="middle">' +
          e(p.letter) +
          "</text>"
        : "") +
      "</g>"
    );
  }).join("");
  const nodes = IDS.map((id, i) => {
    const node = NODES[id],
      current = s?.current === id,
      named = id !== "keter" || s?.harmony;
    const label = named ? shortPond(node.pond) : "Unnamed";
    const state = s ? status(world, s, id) : "distant";
    const showLabel = !s || current || state === "open";
    const align = node.x < 50 ? "end" : "start";
    const tx = node.x < 50 ? -26 : 26;
    return (
      '<g transform="translate(' +
      x(id) +
      "," +
      y(id) +
      ')" class="office ' +
      node.pillar +
      (current ? " current" : "") +
      (s?.visited.includes(id) ? " visited" : "") +
      '" ' +
      (s && !current
        ? 'role="button" tabindex="0" data-go="' +
          id +
          '" aria-label="' +
          e(
            label +
              ", " +
              (state === "open"
                ? "walk here"
                : state === "missing"
                  ? "not connected to your current office"
                  : state),
          ) +
          '" aria-disabled="' +
          (state !== "open") +
          '"'
        : 'aria-label="' +
          e(current ? label + ", you are here" : label) +
          '"') +
      ">" +
      (current ? '<circle class="current-halo" r="24"/>' : "") +
      '<circle class="node" r="' +
      (current ? 13 : 9) +
      '"/>' +
      '<text class="node-number" text-anchor="middle" y="4">' +
      (named ? roman[i] : "·") +
      "</text>" +
      (showLabel
        ? '<text class="node-label" x="' +
          tx +
          '" y="3" text-anchor="' +
          align +
          '">' +
          e(label) +
          "</text>"
        : "") +
      "</g>"
    );
  }).join("");
  return (
    '<svg class="tree-svg" viewBox="0 0 600 640" aria-label="The ten offices and twenty-two streams of the tree">' +
    edge +
    nodes +
    "</svg>"
  );
}
function header(s: Seeker | null) {
  return (
    '<header class="topbar"><a class="brand" href="#" data-home>' +
    mark +
    "<span>VORTEX<small>THE NILE OF RARE FROGS</small></span></a>" +
    '<nav aria-label="Game views">' +
    (s && !newJourney
      ? (["tree", "stories", "atlas", "codex", "rares", "journal"] as const)
          .map(
            (v) =>
              '<button data-view="' +
              v +
              '" aria-current="' +
              (view === v ? "page" : "false") +
              '">' +
              {
                tree: "The tree",
                stories: "Stories",
                atlas: "Living Atlas",
                codex: "Streams",
                rares: "Asset archive",
                journal: "Journal",
              }[v] +
              "</button>",
          )
          .join("")
      : '<span class="edition">ANCIENT EGYPT · INTERNET FROGS · REAL RARES</span>') +
    '</nav><div class="header-tools"><button class="icon-button" data-modal="help" aria-label="How to play">?</button><button class="quiet" data-modal="journeys">' +
    (s ? e(s.name) : "Journeys") +
    '<span aria-hidden="true"> ▾</span></button><button class="icon-button" data-modal="settings" aria-label="Settings">☷</button></div></header>'
  );
}
function gate() {
  return (
    '<main id="main" class="gate"><section class="gate-copy"><div class="eyebrow">THE TEMPLE IS OPEN, FREN</div>' +
    (asking && answers.length < QUESTIONS.length
      ? '<div class="question-count">WHO ARRIVED <span>' +
        (answers.length + 1) +
        ' / 6</span></div><div class="quiz-progress"><span style="width:' +
        (answers.length / 6) * 100 +
        '%"></span></div><h1 id="quiz-question" tabindex="-1">' +
        e(QUESTIONS[answers.length].text) +
        '</h1><div class="quiz-options">' +
        QUESTIONS[answers.length].answers
          .map(
            (a, i) =>
              '<button data-answer="' +
              i +
              '"><span class="option-index">0' +
              (i + 1) +
              "</span>" +
              e(a) +
              '<span class="option-arrow" aria-hidden="true">↗</span></button>',
          )
          .join("") +
        '</div><button class="text-button" data-back-question>← ' +
        (answers.length ? "Previous question" : "Back to your name") +
        "</button>"
      : '<h1>The Nile is deep.<br>The frogs are rare.</h1><p class="gate-description">Enter a strange Egyptian afterlife built from real Rare Pepe lore. Outsmart a crocodile. Consult a questionable ibis. Find your way through ten temples and twenty-two streams.</p>' +
        '<form id="gate-form"><label for="seeker-name">What shall we call you?</label><input id="seeker-name" name="name" autocomplete="nickname" minlength="2" maxlength="32" placeholder="Your chosen name" value="' +
        e(name) +
        '" required><fieldset><legend>Choose the voices you’ll meet</legend><div class="dialect-choice"><label><input type="radio" name="dialect" value="classical" ' +
        (dialect === "classical" ? "checked" : "") +
        '><span><strong>Classical</strong><small>Myth, mischief, and ancient voices</small></span></label><label><input type="radio" name="dialect" value="folk" ' +
        (dialect === "folk" ? "checked" : "") +
        '><span><strong>Folk</strong><small>More frog. Less ceremony.</small></span></label></div></fieldset><button class="primary" type="submit">Enter the Nile <span aria-hidden="true">↗</span></button></form><p class="hospitality">Six choices. One strange pilgrimage. No account or wallet needed. Original Rare Pepe tokens inspire this fictional world.</p>') +
    (activeSeeker(world)
      ? '<button class="text-button" data-cancel-new>Return to ' +
        e(activeSeeker(world)!.name) +
        "</button>"
      : "") +
    '</section><section class="gate-tree" aria-label="The Egyptian Rare Pepe universe"><div class="threshold-scene"><img src="/nile-world.jpg" alt="An Egyptian temple populated by characters inspired by existing Rare Pepe tokens" width="1672" height="941"></div><div class="original-trio">' +
    ["THOTHPEPE", "LORDKEK", "SPHINXPEPE"]
      .map((name) => {
        const r = RARES.find((r) => r.name === name)!;
        return (
          '<button data-rare="' +
          r.name +
          '" aria-label="See original ' +
          r.name +
          ' artwork and Counterparty record"><img src="' +
          r.image +
          '" alt="Original ' +
          r.name +
          ' Rare Pepe card" width="400" height="560"><span>' +
          r.name +
          "</span></button>"
        );
      })
      .join("") +
    "</div><p>REAL COUNTERPARTY TOKENS. A NEW WAY INTO THEIR WORLD.</p></section></main>"
  );
}
function tree(s: Seeker) {
  const c = CONTENT[s.current],
    n = NODES[s.current],
    rites = riteCount(s);
  const following = tracked?.seeker === s.id ? tracked.story : null;
  const hint = nextStep(world, s, following, atlasTarget);
  const felt = senseWatcher(world, s);
  const memories = [
    returnMemory(s, s.current),
    inquiryMemory(s, s.current),
  ].filter((text): text is string => !!text);
  const memory = memories.join(" ");
  const moments = s.journal.filter(
    (j) =>
      j.turn === s.turns &&
      j.kind !== "guide" &&
      j.text !== c.scene &&
      j.text !== c.detail &&
      !memories.some((text) => j.text.includes(text)),
  );
  return (
    '<main id="main" class="play-layout' +
    (lastFeel ? " felt-" + lastFeel : "") +
    (felt.darkSoon ? " water-haste" : "") +
    '"><aside class="map-panel"><div class="panel-kicker"><span>THE LATTICE</span><span>' +
    String(s.turns).padStart(3, "0") +
    " TURNS</span></div>" +
    map(s) +
    '<div class="map-legend"><span><i class="legend-line"></i>Available</span><span><i class="legend-line dim"></i>Unwalked</span><span><i class="legend-line veil"></i>Veiled</span></div><div class="pillars" aria-label="Your pillar balance">' +
    (["mercy", "balance", "severity"] as const)
      .map(
        (p) =>
          '<div><div class="pillar-label"><span>' +
          p +
          "</span><span>" +
          Math.round(s.pillars[p] * 100) +
          '%</span></div><div class="pillar-track"><span class="' +
          p +
          '" style="width:' +
          s.pillars[p] * 100 +
          '%"></span></div></div>',
      )
      .join("") +
    '</div><p class="map-note">Movement follows the streams.<br>Stillness changes what is possible.</p></aside><section class="story-panel">' +
    '<section class="journey-compass' +
    (atlasTarget ? " atlas-route" : "") +
    '" id="journey-compass" tabindex="-1" aria-label="Suggested next step"><div><span>' +
    (s.festival !== null
      ? "THE FESTIVAL LIVES ON"
      : s.rooted
        ? "CHAPTER II · THE NILE REMEMBERS"
        : "CHAPTER I · A MARK CARRIED HOME") +
    "</span><p>" +
    (atlasTarget
      ? "<strong>Following " + e(NODES[atlasTarget].pond) + "</strong><br>"
      : following && s.stories[following]?.resolution == null
        ? "<strong>Following " + e(rareAt(following).name) + "</strong><br>"
        : "") +
    e(hint.text) +
    "</p>" +
    (felt.water ? '<p class="water-note">' + e(felt.water) + "</p>" : "") +
    '</div><button class="secondary" data-next' +
    (atlasTarget ? " data-atlas-step" : "") +
    ">" +
    e(hint.label) +
    "</button>" +
    (atlasTarget || following
      ? '<button class="text-button" data-atlas-stop>Stop following</button>'
      : "") +
    chapterProgress(s) +
    "</section>" +
    '<div class="location-header"><div><div class="eyebrow">' +
    roman[IDS.indexOf(s.current)] +
    " · " +
    s.current.toUpperCase() +
    " · " +
    n.pillar.toUpperCase() +
    '</div><h1 tabindex="-1" id="location-title">' +
    e(n.pond) +
    "</h1><p>" +
    e(c.subtitle) +
    '</p></div><span class="location-seal" aria-hidden="true">' +
    roman[IDS.indexOf(s.current)] +
    "</span></div>" +
    templeScene(s) +
    worldVignette(s) +
    '<p class="scene-text">' +
    e(s.looked.includes(s.current) ? c.detail : c.scene) +
    "</p>" +
    (memory
      ? '<aside class="return-memory"><span>THE NILE REMEMBERS</span><p>' +
        e(memory) +
        "</p></aside>"
      : "") +
    '<div class="guide-quote"><div class="guide-portrait" style="' +
    portraitStyle(s.current) +
    '" role="img" aria-label="VORTEX interpretation of ' +
    PORTRAIT_TOKENS[PORTRAITS[s.current]] +
    '"></div><div><div class="guide-name">' +
    e(guideName(n, s.dialect)) +
    "<span>" +
    s.dialect +
    " voice</span></div><p>" +
    e(
      [...s.journal]
        .reverse()
        .find((j) => j.kind === "guide" && j.office === s.current)?.text ??
        voice(s),
    ) +
    "</p></div></div>" +
    '<div class="actions"><button class="primary" data-act="look"><span aria-hidden="true">◉</span> Look</button><button class="secondary" data-act="sit"><span aria-hidden="true">◌</span> Sit</button><button class="secondary" data-show-rite ' +
    (!s.looked.includes(s.current) || s.rites[s.current] !== undefined
      ? "disabled"
      : "") +
    '><span aria-hidden="true">◇</span> ' +
    (s.rites[s.current] !== undefined ? "Rite complete" : "Perform a rite") +
    "</button></div>" +
    '<div id="rite-area">' +
    (drafts.rite === s.current &&
    s.rites[s.current] === undefined &&
    s.looked.includes(s.current)
      ? '<section class="rite-card"><div class="eyebrow">THE RITE · ' +
        e(c.rite.name.toUpperCase()) +
        "</div><h2>" +
        e(c.rite.prompt) +
        "</h2>" +
        c.rite.choices
          .map(
            (choice, i) =>
              '<button class="rite-choice" data-rite="' +
              i +
              '">' +
              e(choice) +
              '<span aria-hidden="true">↗</span></button>',
          )
          .join("") +
        "</section>"
      : "") +
    "</div>" +
    (moments.length
      ? '<section class="moment" aria-label="What changed">' +
        moments.map((j) => "<p>" + e(j.text) + "</p>").join("") +
        "</section>"
      : "") +
    (s.current === "hod" && s.rites.hod !== undefined
      ? '<form id="sigil-form" class="sigil-form"><label for="sigil">Give your journey a mark</label><p>A short phrase you want to carry. Changing it renews your work and any wallet proof.</p><div class="input-row"><input id="sigil" name="sigil" maxlength="80" minlength="3" placeholder="e.g. Make room for the light" value="' +
        e(drafts.sigil ?? s.sigil) +
        '" required><button class="secondary" type="submit">' +
        (s.sigil ? "Reshape" : "Make sigil") +
        "</button></div></form>"
      : "") +
    (s.current === "malkhut"
      ? '<section class="kingdom-card"><div class="eyebrow">THE FLOOR OF THE WORLD</div><h2>' +
        (isBound(s)
          ? "Your mark is Bound."
          : s.rooted
            ? "Your journey has taken root."
            : "Bring the journey into form.") +
        "</h2><p>" +
        (s.rooted
          ? "You can keep walking. A return is a beginning, too."
          : "A sigil, six offices, and four rites. This is enough to carry something home.") +
        '</p><div class="requirements"><span class="' +
        (s.sigil ? "done" : "") +
        '">' +
        (s.sigil ? "✓" : "○") +
        ' Sigil</span><span class="' +
        (s.visited.length >= 6 ? "done" : "") +
        '">' +
        Math.min(s.visited.length, 6) +
        '/6 offices</span><span class="' +
        (rites >= 4 ? "done" : "") +
        '">' +
        Math.min(rites, 4) +
        '/4 rites</span></div><div class="actions">' +
        (!s.rooted
          ? '<button class="primary" data-act="root" ' +
            (!readyToRoot(s) ? "disabled" : "") +
            ">Root the journey</button>"
          : '<button class="secondary" data-export-sigil>Keep your mark ↗</button>') +
        '<button class="text-button" data-modal="wallet" ' +
        (!readyToRoot(s) ? "disabled" : "") +
        ">" +
        (isBound(s) ? "View wallet witness" : "Optional: bind an address") +
        "</button></div></section>"
      : "") +
    storyPanel(s, following, true, boardingDraft) +
    inquiryPanel(s) +
    (s.looked.includes(s.current) ? stampInvitation(s.current) : "") +
    festivalPanel(s) +
    (s.current === "malkhut" ? collectionInvitation() : "") +
    '<details class="ask-guide"><summary>Ask ' +
    e(guideName(n, s.dialect)) +
    '</summary><div class="conversation-topics"><button class="text-button" data-topic="What changed here?">What changed here?</button><button class="text-button" data-topic="Tell me about the stories">Stories & the festival</button><button class="text-button" data-topic="Help me find my next step">I’m a little lost</button></div><form id="talk-form"><label for="question">What’s on your mind?</label><div class="input-row"><input id="question" name="question" maxlength="500" placeholder="Ask about your journey…" value="' +
    e(drafts.question ?? "") +
    '" required><button class="secondary">Ask</button></div><small>Your question is not saved. Never enter wallet secrets.</small></form></details>' +
    '<section class="exits"><div class="section-label">STREAMS FROM HERE</div><div class="exit-grid">' +
    neighbors(s.current)
      .map((id) => {
        const st = status(world, s, id),
          p = pathBetween(s.current, id)!;
        return (
          '<button data-go="' +
          id +
          '" class="exit ' +
          st +
          '"><span class="exit-letter">' +
          (st === "veiled" || !s.crossings[p.id] ? "—" : p.letter) +
          "</span><strong>" +
          e(
            id === "keter" && !s.harmony ? "The unnamed shore" : NODES[id].pond,
          ) +
          "</strong><small>" +
          (st === "open"
            ? "Walk this stream ↗"
            : st === "dark"
              ? "Dark · Sit to reopen"
              : "Veiled · not yet revealed") +
          "</small></button>"
        );
      })
      .join("") +
    "</div></section></section></main>"
  );
}
function codex(s: Seeker) {
  return (
    '<main id="main" class="collection"><div class="collection-title"><div><div class="eyebrow">WHAT THE WALK HAS TAUGHT YOU</div><h1>The twenty-two streams</h1><p>A first crossing gives a name. A second gives a meaning.</p></div><div class="big-stat">' +
    revealed(s) +
    '<span>/ 22 REVEALED</span></div></div><div class="codex-grid">' +
    PATH_LETTERS.map((p, i) => {
      const count = s.crossings[p.id] ?? 0;
      return (
        '<article class="codex-card ' +
        (count > 1 ? "revealed" : count ? "named" : "unread") +
        '"><div class="codex-top"><span>' +
        String(i + 1).padStart(2, "0") +
        "</span><span>" +
        (count > 1 ? "REVEALED" : count ? "NAMED" : "UNWALKED") +
        "</span></div><h2>" +
        (count ? p.letter : "—") +
        "</h2><h3>" +
        (count ? e(p.title) : "A stream you have yet to meet") +
        "</h3><p>" +
        (count > 1
          ? e(p.meaning)
          : count
            ? "Return by this stream. Its meaning has not yet settled."
            : "The water keeps its own counsel.") +
        "</p>" +
        (count
          ? "<footer>" +
            e(shortPond(NODES[p.from].pond)) +
            " ↔ " +
            e(shortPond(NODES[p.to].pond)) +
            "</footer>"
          : "") +
        "</article>"
      );
    }).join("") +
    "</div></main>"
  );
}
function rares(s: Seeker) {
  const found = IDS.filter((id) => s.looked.includes(id));
  return (
    '<main id="main" class="collection rare-page"><div class="collection-title"><div><div class="eyebrow">THE FROGS EXIST. THE PILGRIMAGE IS YOURS.</div><h1>The Counterparty archive</h1><p>An open river of assets, with a Rare Pepe heart.<br>Meet the temple frogs, or follow any Counterparty name into the ledger.</p></div><div class="big-stat">' +
    found.length +
    "<span>/ 10 ENCOUNTERED</span></div></div>" +
    assetAtlas(drafts.asset ?? "") +
    '<h2 class="archive-section-title">The Rare Pepe temple court</h2><div class="rare-grid">' +
    IDS.map((id) => {
      const r = rareAt(id),
        seen = s.looked.includes(id);
      return (
        '<button class="rare-display ' +
        (seen ? "encountered" : "unseen") +
        '" data-rare="' +
        r.name +
        '"><div class="rare-image"><img src="' +
        r.image +
        '" alt="Original ' +
        r.name +
        ' artwork" loading="lazy" width="400" height="560"></div><div class="rare-caption"><span>' +
        (seen ? "✓ ENCOUNTERED" : "AWAITING YOUR VISIT") +
        "</span><h2>" +
        r.name +
        "</h2><p>" +
        e(NODES[id].pond) +
        "</p><small>COUNTERPARTY · VIEW RECORD ↗</small></div></button>"
      );
    }).join("") +
    '</div><p class="archive-note">Original Rare Pepe artwork and verified asset names. The temple associations are VORTEX fiction. Encountering an artwork does not mean owning its token.</p></main>'
  );
}
function journal(s: Seeker) {
  return (
    '<main id="main" class="collection journal-page"><div class="collection-title"><div><div class="eyebrow">A RECORD OF RETURNING</div><h1>' +
    e(s.name) +
    '’s journal</h1><p>The last eighty moments. Your own questions remain yours.</p></div><button class="secondary" data-export>Export journeys ↗</button></div>' +
    (s.sigil
      ? '<div class="journal-sigil"><span>YOUR MARK</span><blockquote>“' +
        e(s.sigil) +
        '”</blockquote><button class="text-button" data-export-sigil>Keep your mark ↗</button></div>'
      : "") +
    '<ol class="journal-list">' +
    [...s.journal]
      .reverse()
      .map(
        (j) =>
          '<li class="' +
          j.kind +
          '"><div class="journal-time">' +
          String(j.turn).padStart(3, "0") +
          "<span>" +
          e(shortPond(NODES[j.office].pond)) +
          '</span></div><div><span class="entry-kind">' +
          (j.kind === "guide"
            ? e(j.speaker ?? guideName(NODES[j.office], s.dialect))
            : j.kind === "discovery"
              ? "DISCOVERY"
              : "THE WORLD") +
          "</span><p>" +
          e(j.text) +
          "</p></div></li>",
      )
      .join("") +
    "</ol></main>"
  );
}
function dialog(s: Seeker | null) {
  if (!modal) return "";
  let title = "",
    body = "";
  if (modal === "help") {
    title = "Before consulting the crocodile";
    body =
      '<div class="help-list"><p><strong>Walk, Look, Sit.</strong> Walk a connected stream. Look before a rite. Sit to clear shared darkness and steady the pillars.</p><p><strong>Return.</strong> A second crossing of the same stream reveals its meaning.</p><p><strong>Meet and make.</strong> Both pillars ≥ 25% at Vibe Temple names Crown. A sigil at Hod, six temples, four rites, then Root at Kingdom. A wallet is optional.</p><p><strong>Stories and Atlas.</strong> After a rite, a Rare Pepe may send you. The Living Atlas is a notebook, not a second map. At Kingdom you may look up a public address; that lookup is not saved.</p></div>';
  } else if (modal === "journeys") {
    title = "Many seekers. One tree.";
    body =
      '<p>Journeys are kept on this device. Darkness is shared; your rites, discoveries, and Harmony are your own.</p><div class="seeker-list">' +
      world.seekers
        .map(
          (p) =>
            '<div class="seeker-row"><button data-switch="' +
            p.id +
            '"><strong>' +
            e(p.name) +
            (p.id === world.activeId ? " · here" : "") +
            "</strong><span>" +
            e(NODES[p.current].pond) +
            " · " +
            p.visited.length +
            " offices · " +
            (isBound(p)
              ? "Bound"
              : p.rooted
                ? "Rooted"
                : riteCount(p) + " rites") +
            '</span></button><button class="text-button remove" data-remove="' +
            p.id +
            '" aria-label="Remove ' +
            e(p.name) +
            '">×</button></div>',
        )
        .join("") +
      "</div>" +
      (pendingDelete
        ? '<div class="delete-confirm"><p>Remove this seeker from this device? Export first if you want to keep the journey.</p><button class="danger" data-confirm-remove="' +
          e(pendingDelete) +
          '">Remove seeker</button><button class="text-button" data-cancel-remove>Keep them</button></div>'
        : "") +
      (preservedAvailable
        ? '<button class="text-button" data-export-preserved>Download preserved original</button>'
        : "") +
      (backup
        ? '<section class="recovery-option"><h2>Last recovery copy</h2><p>' +
          backup.seekers.length +
          " seekers · revision " +
          backup.revision +
          '. Restoring replaces the current tree. Download the current tree first; its original is also preserved locally.</p><button class="secondary" data-restore-backup>' +
          (pendingRestore
            ? "Confirm: restore recovery copy"
            : "Restore recovery copy") +
          '</button><button class="text-button" data-export-backup>Download recovery copy</button></section>'
        : "") +
      '<button class="primary" data-new>Welcome another seeker ↗</button><div class="actions"><button class="secondary" data-export>Export all</button><label class="secondary file-button">Import journeys<input type="file" id="import-file" accept=".json,application/json"></label></div>' +
      (s
        ? '<form id="rename-form"><label for="rename">Rename ' +
          e(s.name) +
          '</label><div class="input-row"><input id="rename" name="name" minlength="2" maxlength="32" value="' +
          e(s.name) +
          '" required><button class="secondary">Rename</button></div></form>'
        : "");
  } else if (modal === "settings") {
    title = "Make room for your own pace";
    body =
      '<div class="setting-row"><div><strong>Ambient sound</strong><p>A low chord that leans with your pillars, and small tones for Walk, Look and Sit. Always off until you choose.</p></div><button class="secondary" data-sound aria-pressed="' +
      feelEnabled() +
      '">' +
      (feelEnabled() ? "On" : "Off") +
      '</button></div><div class="setting-row"><div><strong>Reduce motion</strong><p>Keep the water still.</p></div><button class="secondary" data-motion aria-pressed="' +
      reduced +
      '">' +
      (reduced ? "On" : "Off") +
      "</button></div>" +
      (s
        ? '<div class="setting-row"><div><strong>Guide dialect</strong><p>Different voices, the same offices.</p></div><button class="secondary" data-dialect>' +
          s.dialect +
          "</button></div>"
        : "") +
      '<div class="privacy-note"><h2>Your journey stays here.</h2><p>The frog guides use authored, contextual dialogue. A silent Watcher keeps the rules of the tree. Questions are not saved or sent to a model. Saves live in this browser and are not encrypted. Export them before clearing browser data.</p><p>Optional wallet proof is verified on this device. The address ledger sends only the public address you submit to Counterparty; that lookup is not saved with your journey. No keys, transactions, accounts, or analytics are requested. Local progress is not an external credential.</p><p>These are fictional correspondences, not claims of authority over the living traditions that inspired them.</p></div>';
  } else if (modal === "collection" && s && s.current === "malkhut") {
    title = "The address ledger";
    body = collectionBody(
      collection.state,
      s,
      collectionFilter,
      collectionVisible,
      collectionSearch,
    );
  } else if (modal === "stamps" && s) {
    title = "The chamber of the enduring mark";
    body = stampBody(stampOffice, s.dialect);
  } else if (modal === "rare") {
    const r = RARES.find((r) => r.name === selectedRare)!;
    title = r.name;
    body =
      '<div class="original-art"><img src="' +
      r.image +
      '" alt="Original ' +
      r.name +
      ' token artwork" width="400" height="560"></div><div class="token-record"><span>ORIGINAL RARE PEPE · COUNTERPARTY / BITCOIN</span><dl><div><dt>Asset ID</dt><dd>' +
      r.assetId +
      "</dd></div><div><dt>First issued at block</dt><dd>" +
      r.firstIssuanceBlock.toLocaleString() +
      "</dd></div><div><dt>Supply at verification</dt><dd>" +
      supply(r) +
      "</dd></div><div><dt>Issuance</dt><dd>" +
      (r.locked ? "Locked" : "Unlocked") +
      " · " +
      (r.divisible ? "Divisible" : "Indivisible") +
      "</dd></div></dl><p>Asset record checked " +
      r.verifiedAt +
      " at Counterparty block " +
      r.ledgerHeight +
      '. These are original token images. VORTEX’s characters and stories are new interpretations.</p><a class="secondary" href="' +
      r.explorer +
      '" target="_blank" rel="noopener noreferrer">View the token record ↗</a><a class="text-button" href="' +
      r.originalImage +
      '" target="_blank" rel="noopener noreferrer">Original artwork ↗</a><p class="small-note">Finding a card in the game does not transfer or mint a token. Your journey discoveries and your wallet holdings are separate.</p></div>';
  } else if (modal === "wallet" && s) {
    title = isBound(s)
      ? "Your wallet has witnessed the mark"
      : "Bind a name at Kingdom";
    body =
      "<p>This optional rite proves control of a Bitcoin mainnet address. Sign a message in your own wallet, then bring back only its signature. Nothing is spent or written to the blockchain.</p>";
    if (s.proof)
      body +=
        '<div class="verified-proof"><span>✓ VERIFIED WITNESS</span><p class="address">' +
        e(s.proof.address) +
        "</p><p>Your key never entered this game.</p></div>";
    else if (s.challenge)
      body +=
        '<p class="address">' +
        e(s.challenge.address) +
        '</p><label for="challenge-message">Sign this exact message in your wallet</label><textarea id="challenge-message" readonly rows="8">' +
        e(s.challenge.message) +
        '</textarea><button class="secondary" data-copy-challenge>Copy message</button><p class="small-note">Expires ' +
        e(new Date(s.challenge.expiresAt).toLocaleTimeString()) +
        '. BIP-322 simple and supported legacy message signatures.</p><form id="proof-form"><label for="signature">Wallet signature</label><textarea id="signature" name="signature" rows="3" maxlength="2048" placeholder="Base64 signature only" required></textarea><button class="primary">Verify and bind ↗</button></form><button class="text-button" data-new-challenge>Use another address or renew challenge</button>';
    else
      body +=
        '<form id="address-form"><label for="address">Bitcoin mainnet address</label><input id="address" name="address" maxlength="90" autocomplete="off" placeholder="bc1…" required><button class="primary">Create a ten-minute challenge ↗</button></form><p class="small-note">If your wallet does not support message signing for this address, you can leave this rite unfinished. Your Rooted journey remains complete.</p>';
  }
  return (
    '<dialog aria-labelledby="dialog-title"><div class="dialog-header"><h2 id="dialog-title">' +
    title +
    '</h2><button class="icon-button" data-close aria-label="Close dialog">×</button></div>' +
    (message
      ? '<div class="dialog-message ' +
        (messageError ? "error" : "") +
        '" role="status">' +
        e(message) +
        "</div>"
      : "") +
    body +
    "</dialog>"
  );
}
function render() {
  const s = activeSeeker(world);
  const nextBoardingScope = `${s?.id}/${s?.current}/${s?.stories.tiferet?.choice}/${s?.stories.tiferet?.delivered}`;
  if (boardingScope !== nextBoardingScope) {
    boardingDraft = {};
    boardingScope = nextBoardingScope;
  }
  const seekerChanged = renderedSeekerId !== (s?.id ?? null);
  if (seekerChanged) {
    for (const key of Object.keys(drafts)) delete drafts[key];
    boardingDraft = {};
    atlasState = emptyAtlasView();
    atlasTarget = null;
    tracked = null;
    readingPlaces.clear();
    renderedPageKey = "";
    renderedSeekerId = s?.id ?? null;
  }
  const previous = document.activeElement;
  const focused = previous?.id;
  const focusData = previous
    ? [...previous.attributes]
        .filter((a) => a.name.startsWith("data-"))
        .map((a) => [a.name, a.value])
    : [];
  const openDetails = seekerChanged
    ? []
    : [...document.querySelectorAll<HTMLDetailsElement>("details[open]")].map(
        (el) =>
          el.id || (el.classList.contains("ask-guide") ? "ask-guide" : ""),
      );
  const pageKey =
    s && !newJourney && !loading && !damaged
      ? `${s.id}:${view}${view === "tree" ? ":" + s.current : ""}`
      : "";
  const pageChanged = pageKey !== renderedPageKey;
  if (pageChanged && renderedPageKey)
    readingPlaces.set(renderedPageKey, {
      scrollY: window.scrollY,
      details: openDetails,
    });
  const rememberedDetails = pageChanged
    ? (readingPlaces.get(pageKey)?.details ?? [])
    : openDetails;
  renderedPageKey = pageKey;
  if (
    modal !== "collection" &&
    (collection.state.status !== "idle" || collection.state.input)
  )
    collection.edit("");
  if (
    modal === "collection" &&
    (!s || s.id !== collectionSeeker || s.current !== "malkhut")
  ) {
    collection.edit("");
    modal = null;
  }
  document.documentElement.dataset.motion = reduced ? "reduced" : "full";
  app.innerHTML =
    header(s) +
    (!loading && !navigator.locks
      ? '<aside class="update-notice" role="status">This browser can read and export journeys, but cannot save them safely. Use a current browser to continue playing.</aside>'
      : "") +
    (loading
      ? '<main id="main" class="loading">Returning to the water…</main>'
      : damaged
        ? '<main id="main" class="recovery"><div class="eyebrow">YOUR ORIGINAL SAVE IS SAFE</div><h1>We couldn’t read this journey.</h1><p>' +
          e(message) +
          '</p><button class="secondary" data-export-raw>Download the original save</button>' +
          (backup
            ? '<button class="secondary" data-restore-backup>' +
              (pendingRestore
                ? "Confirm: restore recovery copy"
                : "Restore last recovery copy") +
              '</button><button class="text-button" data-export-backup>Download recovery copy</button>'
            : "") +
          '<button class="text-button" data-reset-damaged>Start a new tree on this device</button></main>'
        : !s || newJourney
          ? gate()
          : view === "tree"
            ? tree(s)
            : view === "atlas"
              ? atlasView(s, atlasState)
              : view === "codex"
                ? codex(s)
                : view === "rares"
                  ? rares(s)
                  : view === "stories"
                    ? storyBook(s)
                    : journal(s)) +
    (s && !newJourney
      ? '<footer class="statusbar"><span>' +
        (isBound(s)
          ? "BOUND"
          : s.festival !== null
            ? "FESTIVAL"
            : s.rooted
              ? "ROOTED"
              : s.harmony
                ? "THE CROWN IS OPEN"
                : "THE WALK CONTINUES") +
        "</span><span>" +
        s.visited.length +
        "/10 offices · " +
        discovered(s) +
        "/22 streams · " +
        riteCount(s) +
        " rites · " +
        completedStories(s).length +
        " stories</span><span>Saved on this device</span></footer>"
      : "") +
    (message && !damaged && !modal
      ? '<div class="toast ' +
        (messageError ? "error" : "") +
        '" role="' +
        (messageError ? "alert" : "status") +
        '">' +
        e(message) +
        '<button data-dismiss aria-label="Dismiss">×</button></div>'
      : "") +
    (waitingWorker
      ? '<aside class="update-notice" role="status"><span>A fresh edition is ready. Your journey is saved on this device.</span><button class="secondary" data-update>Update and return</button></aside>'
      : "") +
    dialog(s);
  measureNavigation();
  navigationObserver?.disconnect();
  const topbar = document.querySelector(".topbar");
  if (topbar) navigationObserver?.observe(topbar);
  const d = document.querySelector("dialog");
  if (d) {
    d.showModal();
    d.addEventListener("cancel", (event) => {
      event.preventDefault();
      closeDialog();
    });
  }
  for (const id of rememberedDetails) {
    const el =
      id === "ask-guide"
        ? document.querySelector<HTMLDetailsElement>(".ask-guide")
        : (document.getElementById(id) as HTMLDetailsElement | null);
    if (el?.tagName === "DETAILS") el.open = true;
  }
  const restore = focused
    ? document.getElementById(focused)
    : focusData.length
      ? [...document.querySelectorAll<HTMLElement>("button,a,[data-go]")].find(
          (el) =>
            focusData.every(([key, value]) => el.getAttribute(key) === value),
        )
      : null;
  if (restore && !restore.matches(":disabled") && (!d || d.contains(restore)))
    restore.focus({ preventScroll: true });
}
function download(name: string, text: string, type = "application/json") {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
async function toggleSound() {
  try {
    unlockFeel();
    const on = !feelEnabled();
    if (!setFeelEnabled(on)) throw new Error("unavailable");
    sound = on;
    const s = activeSeeker(world);
    if (on && s) leanDrone(s.pillars);
    render();
  } catch {
    sound = false;
    notice("Sound is unavailable in this browser. The tree is still open.");
  }
}
app.addEventListener("input", (event) => {
  const el = event.target as HTMLInputElement;
  if (el.id === "seeker-name") name = el.value;
  if (el.id === "question" || el.id === "sigil") drafts[el.id] = el.value;
  if (el.id === "asset-name") {
    drafts.asset = el.value;
    document.getElementById("asset-destination")!.innerHTML = assetDestination(
      el.value,
    );
  }
  if (el.id === "collection-search") {
    const start = el.selectionStart,
      end = el.selectionEnd;
    collectionSearch = el.value;
    collectionVisible = 50;
    render();
    document
      .querySelector<HTMLInputElement>("#collection-search")
      ?.setSelectionRange(start, end);
  }
  if (el.id === "collection-address") {
    collectionSearch = "";
    const start = el.selectionStart,
      end = el.selectionEnd;
    collection.edit(el.value);
    render();
    document
      .querySelector<HTMLInputElement>("#collection-address")
      ?.setSelectionRange(start, end);
  }
});
app.addEventListener("click", async (event) => {
  const el = (event.target as Element).closest<HTMLElement>(
    "button,a,[data-go]",
  );
  if (!el || busy) return;
  const d = el.dataset,
    s = activeSeeker(world);
  if (el.tagName === "A" && "home" in d) event.preventDefault();
  if ("atlasEntry" in d && s && atlasEntry(d.atlasEntry!)) {
    // A link from an encounter or another entry must remain readable even if
    // an earlier search or notebook filter excluded its destination.
    if (
      !searchAtlas(
        atlasState.query,
        atlasState.tradition,
        atlasState.group,
      ).some(
        (x) =>
          x.id === d.atlasEntry &&
          (!atlasState.notebook || s.inquiries.seen.includes(x.id)),
      )
    ) {
      atlasState.query = "";
      atlasState.tradition = "all";
      atlasState.group = "all";
      atlasState.notebook = false;
    }
    atlasState.selected = d.atlasEntry!;
    view = "atlas";
    render();
    focusPanel("entry-" + d.atlasEntry);
  } else if ("cluster" in d) {
    atlasState.query = "";
    atlasState.tradition = "all";
    atlasState.notebook = false;
    atlasState.group = d.cluster!;
    atlasState.selected = d.cluster!;
    view = "atlas";
    render();
    focusPanel("entry-" + d.cluster);
  } else if ("atlasClear" in d) {
    atlasState.query = "";
    atlasState.tradition = "all";
    atlasState.group = "all";
    atlasState.notebook = false;
    render();
  } else if ("notebook" in d) {
    atlasState.notebook = !atlasState.notebook;
    render();
  } else if ("atlasConnections" in d) {
    atlasState.expandedConnections =
      atlasState.expandedConnections === d.atlasConnections
        ? undefined
        : d.atlasConnections;
    render();
  } else if ("compare" in d && atlasEntry(d.compare!)) {
    if (atlasState.compare.includes(d.compare!))
      atlasState.compare = atlasState.compare.filter((id) => id !== d.compare);
    else if (atlasState.compare.length < 3) atlasState.compare.push(d.compare!);
    else {
      notice("Compare up to three entries. Remove one before adding another.");
      return;
    }
    render();
  } else if ("compareClear" in d) {
    atlasState.compare = [];
    render();
  } else if ("study" in d) {
    await act({ type: "study", entry: d.study! });
    if (!messageError) focusPanel("entry-" + d.study);
  } else if ("inquiry" in d) {
    await act({
      type: "inquiry",
      task: d.inquiry as "tablet" | "gate" | "testimony",
      choice: Number(d.choice),
    });
    focusPanel("inquiry-panel");
  } else if ("atlasRoute" in d && IDS.includes(d.atlasRoute as SefirahId)) {
    atlasTarget = d.atlasRoute as SefirahId;
    tracked = null;
    view = "tree";
    render();
    focusPanel("main");
  } else if ("atlasStop" in d) {
    atlasTarget = null;
    tracked = null;
    render();
  } else if ("restoreBackup" in d) {
    if (!pendingRestore) {
      try {
        const snapshot = {
          raw: localStorage.getItem(SAVE_KEY),
          backup: localStorage.getItem(BACKUP_KEY),
        };
        const recovered = await recoveryWorld(localStorage);
        if (
          !recovered ||
          snapshot.raw !== localStorage.getItem(SAVE_KEY) ||
          snapshot.backup !== localStorage.getItem(BACKUP_KEY)
        )
          throw new Error(
            "The recovery copy changed. Open Journeys again before restoring.",
          );
        backup = recovered;
        restoreSnapshot = snapshot;
        pendingRestore = true;
        notice(
          "Restoring returns to the previous recovery copy. The current original is preserved locally. Press Confirm to continue.",
        );
      } catch (err) {
        notice(errorText(err), true);
      }
      return;
    }
    if (!restoreSnapshot) return;
    const expected = restoreSnapshot;
    try {
      await withJourneyLock(async () => {
        world = await restoreBackup(
          localStorage,
          expected.raw,
          expected.backup,
        );
      });
      preservedAvailable = expected.raw !== null;
      renderedSeekerId = null;
      restoreSnapshot = null;
      damaged = false;
      pendingRestore = false;
      modal = null;
      newJourney = false;
      view = "tree";
      notice(
        "Recovery copy restored. The replaced original can be downloaded from Journeys.",
      );
    } catch (err) {
      pendingRestore = false;
      restoreSnapshot = null;
      notice(errorText(err), true);
    }
  } else if ("exportBackup" in d)
    download(
      "vortex-recovery-copy.json",
      localStorage.getItem(BACKUP_KEY) ?? "",
    );
  else if ("exportPreserved" in d)
    download(
      "vortex-preserved-original.json",
      localStorage.getItem(RECOVERY_KEY) ?? "",
    );
  else if ("update" in d && waitingWorker) {
    // Completed actions are already saved. Updating must remain possible when
    // this client cannot parse a save written by a newer edition.
    try {
      const worker = waitingWorker;
      updating = true;
      // An initially uncontrolled page may not receive controllerchange.
      // Observe activation itself so its next navigation uses the new worker.
      const returnToGame = () => {
        if (updating && worker.state === "activated") location.reload();
      };
      worker.addEventListener("statechange", returnToGame);
      returnToGame();
      worker.postMessage({ type: "ACTIVATE_UPDATE" });
    } catch (err) {
      notice(errorText(err), true);
    }
  } else if ("rare" in d && RARES.some((r) => r.name === d.rare)) {
    modalTrigger = ["data-rare", d.rare!];
    selectedRare = d.rare!;
    modal = "rare";
    message = "";
    render();
  } else if ("close" in d) {
    closeDialog();
  } else if ("modal" in d) {
    if (d.modal === "collection" && (!s || s.current !== "malkhut")) return;
    if (d.modal === "collection") {
      collectionSeeker = s!.id;
      collection.edit("");
      collectionFilter = "all";
      collectionSearch = "";
      collectionVisible = 50;
    }
    if (d.modal === "stamps") {
      if (!s) return;
      stampOffice = isStampOffice(s.current) ? s.current : "hod";
    }
    modalTrigger = ["data-modal", d.modal!];
    modal = d.modal as typeof modal;
    message = "";
    render();
  } else if ("stampOffice" in d && modal === "stamps") {
    const id = d.stampOffice as SefirahId;
    if (isStampOffice(id)) {
      stampOffice = id;
      render();
    }
  } else if ("view" in d) {
    view = d.view as typeof view;
    render();
    focusView();
  } else if ("home" in d) {
    view = "tree";
    newJourney = false;
    render();
  } else if ("collectionCancel" in d) collection.cancel();
  else if ("collectionClear" in d) collection.clear();
  else if ("collectionRetry" in d && modal === "collection") {
    collectionVisible = 50;
    void collection.run();
  } else if (
    "collectionFilter" in d &&
    (d.collectionFilter === "world" || d.collectionFilter === "all")
  ) {
    collectionFilter = d.collectionFilter;
    collectionVisible = 50;
    render();
  } else if ("collectionMore" in d) {
    collectionVisible += 50;
    render();
  } else if ("topic" in d) {
    await act({ type: "talk", text: d.topic! });
  } else if ("next" in d && s) {
    const hint = nextStep(
      world,
      s,
      tracked?.seeker === s.id ? tracked.story : null,
      atlasTarget,
    );
    if (hint.action) await act(hint.action);
    else if (hint.panel === "rite") {
      drafts.rite = s.current;
      render();
      focusPanel("rite-area");
    } else if (hint.panel === "sigil")
      document.getElementById("sigil")?.focus();
    else
      focusPanel(
        hint.panel === "inquiry"
          ? "inquiry-panel"
          : hint.panel === "festival"
            ? "festival"
            : "story-" + (hint.target ?? s.current),
      );
  } else if ("track" in d && s && IDS.includes(d.track as SefirahId)) {
    if (modal === "collection") {
      collection.edit("");
      modal = null;
      modalTrigger = null;
    }
    tracked = { seeker: s.id, story: d.track as SefirahId };
    atlasTarget = null;
    view = "tree";
    render();
    const target = document.getElementById("story-" + d.track);
    if (target) focusPanel(target.id);
    else focusPanel("main");
  } else if ("storyStart" in d) {
    await act({
      type: "story-start",
      story: d.storyStart as SefirahId,
      choice: Number(d.choice),
    });
    if (!messageError && s) {
      tracked = { seeker: s.id, story: d.storyStart as SefirahId };
      atlasTarget = null;
    }
    render();
    focusPanel("story-" + d.storyStart);
  } else if ("boardingHelp" in d && s && boardingHelper(s)) {
    boardingDraft = suggestedBoarding();
    render();
    focusPanel("boarding-title");
  } else if ("boardingReset" in d) {
    boardingDraft = {};
    render();
    focusPanel("boarding-title");
  } else if ("deliver" in d) {
    await act({ type: "story-deliver", story: d.deliver as SefirahId });
    focusPanel("journey-compass");
  } else if ("resolve" in d) {
    await act({
      type: "story-resolve",
      story: d.resolve as SefirahId,
      choice: Number(d.choice),
    });
    focusPanel("story-" + d.resolve);
  } else if ("festival" in d) {
    await act({ type: "festival", choice: Number(d.festival) });
    focusPanel("festival");
  } else if ("act" in d) await act({ type: d.act } as Action);
  else if ("go" in d) {
    drafts.rite = "";
    await act({ type: "walk", to: d.go as SefirahId });
  } else if ("showRite" in d && s) {
    drafts.rite = s.current;
    render();
    focusPanel("rite-area");
  } else if ("rite" in d) {
    await act({ type: "rite", choice: Number(d.rite) });
    drafts.rite = "";
  } else if ("answer" in d) {
    answers.push(Number(d.answer));
    if (answers.length === 6) {
      await commit((w) => addSeeker(w, name, dialect, quizPillars(answers)));
      if (!messageError) {
        newJourney = false;
        asking = false;
        answers = [];
        view = "tree";
        render();
      } else {
        answers.pop();
        render();
      }
    } else render();
    focusPanel(asking ? "quiz-question" : "location-title");
  } else if ("backQuestion" in d) {
    if (answers.length) answers.pop();
    else asking = false;
    render();
  } else if ("new" in d) {
    newJourney = true;
    asking = false;
    answers = [];
    name = "";
    modal = null;
    render();
  } else if ("cancelNew" in d) {
    newJourney = false;
    asking = false;
    render();
  } else if ("switch" in d) {
    await commit((w) => ({
      ...w,
      activeId: d.switch!,
      revision: w.revision + 1,
    }));
    modal = null;
    newJourney = false;
    view = "tree";
    render();
  } else if ("remove" in d) {
    pendingDelete = d.remove!;
    render();
  } else if ("cancelRemove" in d) {
    pendingDelete = "";
    render();
  } else if ("confirmRemove" in d) {
    await commit((w) => {
      const seekers = w.seekers.filter((p) => p.id !== d.confirmRemove);
      return {
        ...w,
        seekers,
        activeId:
          w.activeId === d.confirmRemove
            ? (seekers[0]?.id ?? null)
            : w.activeId,
        revision: w.revision + 1,
      };
    });
    pendingDelete = "";
    atlasTarget = null;
    render();
  } else if ("export" in d)
    download(
      "vortex-journeys-" + new Date().toISOString().slice(0, 10) + ".json",
      JSON.stringify(world, null, 2),
    );
  else if ("exportRaw" in d) {
    try {
      download(
        "vortex-original-save.json",
        localStorage.getItem(SAVE_KEY) ?? "",
      );
    } catch {
      notice(
        "Browser storage is unavailable. Allow site storage to return to this tree.",
        true,
      );
    }
  } else if ("resetDamaged" in d) {
    if (!pendingDelete) {
      pendingDelete = "damaged";
      damagedOriginal = localStorage.getItem(SAVE_KEY);
      notice(
        "Download the original first. Press “Start a new tree” again to replace this device’s unreadable save.",
        true,
      );
    } else {
      try {
        await withJourneyLock(async () => {
          const original = localStorage.getItem(SAVE_KEY);
          if (original !== damagedOriginal)
            throw new Error(
              "The journey changed. Reload before starting a new tree.",
            );
          if (original) localStorage.setItem(RECOVERY_KEY, original);
          localStorage.removeItem(SAVE_KEY);
          preservedAvailable = original !== null;
        });
        world = emptyWorld();
        damaged = false;
        message = "";
        pendingDelete = "";
        render();
      } catch {
        notice(
          "Browser storage is unavailable. Allow site storage before starting a new tree.",
          true,
        );
      }
    }
  } else if ("exportSigil" in d && s?.sigil) {
    const certificate = [
      "VORTEX — A mark carried through the tree",
      "",
      s.sigil,
      "",
      "Seeker: " + s.name,
      "Offices visited: " + s.visited.map((id) => NODES[id].pond).join(", "),
      "Rites completed: " + riteCount(s),
      "Streams revealed: " + revealed(s),
      "Stories brought home: " + completedStories(s).length,
      "Festival: " +
        (s.festival === null
          ? "Not yet celebrated"
          : [
              "The long table",
              "The river of lanterns",
              "The unfinished chorus",
            ][s.festival]),
      "Journey: " +
        (isBound(s) ? "Bound" : s.rooted ? "Rooted" : "In progress"),
      "",
      "A fictional journey. A local record. No monetary or external rights are conferred.",
    ].join("\n");
    download("vortex-mark-" + s.id + ".txt", certificate, "text/plain");
  } else if ("sound" in d) await toggleSound();
  else if ("motion" in d) {
    reduced = !reduced;
    render();
  } else if ("dialect" in d && s)
    await act({
      type: "dialect",
      dialect: s.dialect === "classical" ? "folk" : "classical",
    });
  else if ("copyChallenge" in d && s?.challenge) {
    try {
      await navigator.clipboard.writeText(s.challenge.message);
      notice("Message copied. Sign it in your wallet.");
    } catch {
      notice("Copy is unavailable. Select and copy the message above.");
    }
  } else if ("newChallenge" in d)
    await commit((w) => {
      const n = structuredClone(w);
      activeSeeker(n)!.challenge = null;
      n.revision++;
      return n;
    });
  else if ("dismiss" in d) {
    message = "";
    render();
  }
});
app.addEventListener("keydown", (event) => {
  if (
    (event.key === "Enter" || event.key === " ") &&
    (event.target as Element).matches("g[data-go]")
  ) {
    event.preventDefault();
    (event.target as Element).dispatchEvent(
      new MouseEvent("click", { bubbles: true }),
    );
  }
});
app.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (busy) return;
  const form = event.target as HTMLFormElement,
    f = new FormData(form);
  try {
    if (form.id === "collection-form" && modal === "collection") {
      collection.edit(String(f.get("address")));
      collectionVisible = 50;
      void collection.run();
    }
    if (form.id === "gate-form") {
      name = safeText(f.get("name"), 32, 2);
      if (
        world.seekers.some((s) => s.name.toLowerCase() === name.toLowerCase())
      )
        throw new Error(
          "That seeker is already here. Open Journeys to return to them.",
        );
      dialect = f.get("dialect") as Dialect;
      asking = true;
      render();
      focusPanel("quiz-question");
    }
    if (form.id === "sigil-form") {
      await act({ type: "sigil", text: String(f.get("sigil")) });
      if (!messageError) delete drafts.sigil;
    }
    if (form.id === "boarding-form") {
      const boarding = Object.fromEntries(
        PASSENGERS.map(({ id }) => [id, Number(f.get(id) ?? -1)]),
      ) as BoardingPlan;
      await act({ type: "story-deliver", story: "tiferet", boarding });
      if (!messageError) focusPanel("journey-compass");
    }
    if (form.id === "talk-form") {
      await act({ type: "talk", text: String(f.get("question")) });
      if (!messageError) {
        drafts.question = "";
        render();
      }
    }
    if (form.id === "rename-form")
      await commit((w) => {
        const n = structuredClone(w),
          s = activeSeeker(n)!;
        const name = safeText(f.get("name"), 32, 2);
        if (
          n.seekers.some(
            (p) => p.id !== s.id && p.name.toLowerCase() === name.toLowerCase(),
          )
        )
          throw new Error("That name is already in use.");
        s.name = name;
        n.revision++;
        return n;
      });
    if (form.id === "atlas-search") {
      atlasState.query = String(f.get("query") ?? "").slice(0, 100);
      atlasState.tradition = String(f.get("tradition") ?? "all");
      const matches = searchAtlas(
        atlasState.query,
        atlasState.tradition,
        atlasState.group,
      ).filter(
        (x) =>
          !atlasState.notebook ||
          activeSeeker(world)?.inquiries.seen.includes(x.id),
      );
      if (matches.length && !matches.some((x) => x.id === atlasState.selected))
        atlasState.selected = matches[0].id;
      render();
    }
    if (form.id === "address-form")
      await commit((w) => issueChallenge(w, String(f.get("address"))));
    if (form.id === "proof-form") {
      const nonce = activeSeeker(world)?.challenge?.nonce ?? "";
      await commit((w) =>
        acceptSignature(w, String(f.get("signature")), nonce),
      );
    }
  } catch (error) {
    notice(errorText(error), true);
  }
});
app.addEventListener("change", async (event) => {
  const input = event.target as HTMLInputElement;
  if (
    input.dataset.passenger &&
    PASSENGERS.some((p) => p.id === input.dataset.passenger) &&
    (input.value === "0" || input.value === "1")
  ) {
    boardingDraft[input.dataset.passenger as PassengerId] = Number(
      input.value,
    ) as 0 | 1;
    render();
  }
  if (input.name === "dialect" && input.closest("#gate-form"))
    dialect = input.value as Dialect;
  if (input.id !== "import-file" || !input.files?.[0]) return;
  const file = input.files[0];
  if (file.size > MAX_SAVE_BYTES) {
    notice("That file is too large. Nothing was changed.", true);
    return;
  }
  try {
    const text = await file.text();
    const work = async () => {
      world = await importWorld(localStorage, text);
    };
    await withJourneyLock(work);
    backup = await recoveryWorld(localStorage);
    notice("Journeys imported. Existing progress was preserved.");
  } catch (error) {
    notice(errorText(error), true);
  }
});
window.addEventListener("storage", async (event) => {
  if (event.key !== SAVE_KEY || busy) return;
  try {
    world = await loadWorld(localStorage);
    try {
      backup = await recoveryWorld(localStorage);
    } catch {
      backup = null;
    }
    pendingRestore = false;
    restoreSnapshot = null;
    notice(
      "This tree changed in another tab. You are seeing its latest state.",
    );
  } catch (error) {
    notice(errorText(error), true);
  }
});
async function start() {
  try {
    world = await loadWorld(localStorage);
  } catch (error) {
    damaged = true;
    message = errorText(error);
  }
  try {
    backup = await recoveryWorld(localStorage);
  } catch {
    backup = null;
  }
  try {
    preservedAvailable = localStorage.getItem(RECOVERY_KEY) !== null;
  } catch {
    preservedAvailable = false;
  }
  loading = false;
  render();
}
render();
void start();
if (import.meta.env?.PROD && "serviceWorker" in navigator) {
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (updating) location.reload();
  });
  void navigator.serviceWorker
    .register("/sw.js")
    .then((registration) => {
      const check = () => {
        waitingWorker = registration.waiting;
        render();
      };
      check();
      registration.addEventListener("updatefound", () =>
        registration.installing?.addEventListener("statechange", check),
      );
    })
    .catch(() => {
      /* Online play and exports remain available. */
    });
}

const disposeJourneyTools = registerJourneyTools(
  (document as Document & { modelContext?: JourneyContext }).modelContext,
  () => {
    if (loading || damaged)
      throw new Error(
        "The journey is not ready. Finish loading or recover the original save first.",
      );
    return world;
  },
  async (action, expected) => {
    if (loading || busy || damaged || newJourney)
      throw new Error("Finish the current interaction first.");
    if (
      world.activeId !== expected.seekerId ||
      world.revision !== expected.revision
    )
      throw new Error(
        "The journey changed. Read the latest state before acting.",
      );
    await act(action);
    if (messageError) throw new Error(message);
    view = "tree";
    modal = null;
    render();
  },
  undefined,
  (w, s) =>
    nextStep(
      w,
      s,
      tracked?.seeker === s.id ? tracked.story : null,
      atlasTarget,
    ),
);
import.meta.hot?.dispose(() => {
  disposeJourneyTools();
  collection.edit("");
});
window.addEventListener("pagehide", () => collection.clear());
