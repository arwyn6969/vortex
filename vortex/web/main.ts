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
  objective,
  riteCount,
  discovered,
  revealed,
  readyToRoot,
  isBound,
} from "./session.ts";
import type { World, Action, Seeker } from "./session.ts";
import {
  loadWorld,
  saveWorld,
  importWorld,
  SAVE_KEY,
  MAX_SAVE_BYTES,
} from "./storage.ts";
import { issueChallenge, acceptSignature } from "./wallet.ts";
import { escapeHtml as e, safeText } from "./safety.ts";

const app = document.querySelector<HTMLDivElement>("#app")!;
let world = emptyWorld();
let loading = true,
  busy = false,
  damaged = false,
  newJourney = false;
let view: "tree" | "codex" | "journal" | "rares" = "tree";
let modal: "journeys" | "settings" | "help" | "wallet" | "rare" | null = null;
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
    world = next;
  };
  try {
    if (navigator.locks) await navigator.locks.request(SAVE_KEY, task);
    else await task();
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
async function act(action: Action) {
  await commit((w) => transition(w, action));
  if (!messageError && action.type === "walk")
    document.getElementById("location-title")?.focus({ preventScroll: true });
}
function map(s: Seeker | null) {
  const x = (id: SefirahId) => 74 + NODES[id].x * 4.52;
  const y = (id: SefirahId) => 16 + NODES[id].y * 6.05;
  const edge = PATH_LETTERS.map((p) => {
    const nearby = s && (p.from === s.current || p.to === s.current);
    const target = s && p.from === s.current ? p.to : p.from;
    const state = s && nearby ? status(world, s, target) : "distant";
    const visited = s && !!s.crossings[p.id];
    return (
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
      '"/>'
    );
  }).join("");
  const nodes = IDS.map((id, i) => {
    const node = NODES[id],
      current = s?.current === id,
      named = id !== "keter" || s?.harmony;
    const label = named ? shortPond(node.pond) : "Unnamed";
    const state = s ? status(world, s, id) : "distant";
    const align = node.x < 50 ? "end" : "start";
    const tx = node.x < 50 ? -29 : 29;
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
      '<text class="node-label" x="' +
      tx +
      '" y="3" text-anchor="' +
      align +
      '">' +
      e(label) +
      "</text>" +
      (current
        ? '<text class="here-label" x="' +
          tx +
          '" y="21" text-anchor="' +
          align +
          '">YOU ARE HERE</text>'
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
      ? (["tree", "codex", "rares", "journal"] as const)
          .map(
            (v) =>
              '<button data-view="' +
              v +
              '" aria-current="' +
              (view === v ? "page" : "false") +
              '">' +
              {
                tree: "The tree",
                codex: "Streams",
                rares: "Rare archive",
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
        '%"></span></div><h1>' +
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
  const moments = s.journal.filter(
    (j) =>
      j.turn === s.turns &&
      j.kind !== "guide" &&
      j.text !== c.scene &&
      j.text !== c.detail,
  );
  return (
    '<main id="main" class="play-layout"><aside class="map-panel"><div class="panel-kicker"><span>THE LATTICE</span><span>' +
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
    '<div class="location-art"><img src="/nile-world.jpg" alt="An illustrated Nile temple inspired by original Egyptian Rare Pepe tokens" width="1672" height="941"><div class="art-caption">' +
    e(c.subtitle.toUpperCase()) +
    "</div></div>" +
    '<p class="scene-text">' +
    e(s.looked.includes(s.current) ? c.detail : c.scene) +
    "</p>" +
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
        c.classical,
    ) +
    "</p></div></div>" +
    '<div class="actions"><button class="primary" data-act="look"><span aria-hidden="true">◉</span> Look</button><button class="secondary" data-act="sit"><span aria-hidden="true">◌</span> Sit</button><button class="secondary" data-show-rite ' +
    (!s.looked.includes(s.current) || s.rites[s.current] !== undefined
      ? "disabled"
      : "") +
    '><span aria-hidden="true">◇</span> ' +
    (s.rites[s.current] !== undefined ? "Rite complete" : "Perform a rite") +
    "</button></div>" +
    (moments.length
      ? '<section class="moment" role="status" aria-label="What changed">' +
        moments.map((j) => "<p>" + e(j.text) + "</p>").join("") +
        "</section>"
      : "") +
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
        s.visited.length +
        '/6 offices</span><span class="' +
        (rites >= 4 ? "done" : "") +
        '">' +
        rites +
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
    (s.looked.includes(s.current)
      ? '<button class="rare-encounter" data-rare="' +
        rareAt(s.current).name +
        '"><img src="' +
        rareAt(s.current).image +
        '" alt="" width="400" height="560"><span><small>FROM THE REAL RARE PEPE ARCHIVE</small><strong>' +
        rareAt(s.current).name +
        "</strong><span>Inspect the original artwork & token record ↗</span></span></button>"
      : "") +
    '<details class="ask-guide"><summary>Ask ' +
    e(guideName(n, s.dialect)) +
    '</summary><form id="talk-form"><label for="question">What’s on your mind?</label><div class="input-row"><input id="question" name="question" maxlength="500" placeholder="Ask about your journey…" value="' +
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
          (st === "veiled" ? "—" : p.letter) +
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
    '</div></section><div class="next-step"><span>YOUR NEXT THREAD</span><p>' +
    e(objective(s)) +
    "</p></div></section></main>"
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
    '<main id="main" class="collection rare-page"><div class="collection-title"><div><div class="eyebrow">THE FROGS EXIST. THE PILGRIMAGE IS YOURS.</div><h1>The Rare archive</h1><p>Ten existing Counterparty tokens, encountered along the Nile.<br>Look at a temple to find its connection. Inspect any original below.</p></div><div class="big-stat">' +
    found.length +
    '<span>/ 10 ENCOUNTERED</span></div></div><div class="rare-grid">' +
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
      '<div class="help-list"><p><strong>Walk.</strong> Choose an available stream. The tree is connected by twenty-two paths; there are no shortcuts between unconnected offices.</p><p><strong>Look.</strong> Notice the shore before performing its rite. Looking at Boundaries reveals a quiet descent.</p><p><strong>Sit.</strong> Slow down. Darkness clears for everyone on this local tree. Your first rest at each office gently strengthens all three pillars.</p><p><strong>Return.</strong> Walk the same stream a second time to reveal its meaning in your Codex.</p><p><strong>Meet.</strong> Bring Mercy and Severity to at least 25% each, then stand in Vibe Temple. Crown opens through that meeting.</p><p><strong>Make.</strong> Complete Hod’s rite and create a short sigil. Carry it through six offices and four rites, then root your journey at Kingdom.</p><p><strong>Continue.</strong> A wallet is optional. Your journey is complete without it. Nothing here requires a payment.</p></div>';
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
      '<div class="setting-row"><div><strong>Ambient sound</strong><p>A quiet chord. Always off until you choose.</p></div><button class="secondary" data-sound aria-pressed="' +
      sound +
      '">' +
      (sound ? "On" : "Off") +
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
      '<div class="privacy-note"><h2>Your journey stays here.</h2><p>The frog guides use authored, contextual dialogue. A silent Watcher keeps the rules of the tree. Questions are not saved or sent to a model. Saves live in this browser and are not encrypted. Export them before clearing browser data.</p><p>Optional wallet proof is verified on this device. No keys, transactions, accounts, or analytics are requested. Local progress is not an external credential.</p><p>These are fictional correspondences, not claims of authority over the living traditions that inspired them.</p></div>';
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
  const focused = document.activeElement?.id;
  const s = activeSeeker(world);
  document.documentElement.dataset.motion = reduced ? "reduced" : "full";
  app.innerHTML =
    header(s) +
    (loading
      ? '<main id="main" class="loading">Returning to the water…</main>'
      : damaged
        ? '<main id="main" class="recovery"><div class="eyebrow">YOUR ORIGINAL SAVE IS SAFE</div><h1>We couldn’t read this journey.</h1><p>' +
          e(message) +
          '</p><button class="secondary" data-export-raw>Download the original save</button><button class="text-button" data-reset-damaged>Start a new tree on this device</button></main>'
        : !s || newJourney
          ? gate()
          : view === "tree"
            ? tree(s)
            : view === "codex"
              ? codex(s)
              : view === "rares"
                ? rares(s)
                : journal(s)) +
    (s && !newJourney
      ? '<footer class="statusbar"><span>' +
        (isBound(s)
          ? "BOUND"
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
        " rites</span><span>Saved on this device</span></footer>"
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
    dialog(s);
  const d = document.querySelector("dialog");
  if (d) {
    d.showModal();
    d.addEventListener("cancel", () => {
      modal = null;
      message = "";
    });
  }
  if (focused) document.getElementById(focused)?.focus({ preventScroll: true });
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
    if (!audio) {
      audio = new AudioContext();
      const gain = audio.createGain();
      gain.gain.value = 0.015;
      gain.connect(audio.destination);
      [110, 164.81, 220].forEach((freq) => {
        const o = audio!.createOscillator();
        o.type = "sine";
        o.frequency.value = freq;
        o.connect(gain);
        o.start();
      });
    }
    if (sound) await audio.suspend();
    else await audio.resume();
    sound = !sound;
    render();
  } catch {
    sound = false;
    notice("Sound is unavailable in this browser. The tree is still open.");
  }
}
app.addEventListener("input", (event) => {
  const el = event.target as HTMLInputElement;
  if (el.id === "question" || el.id === "sigil") drafts[el.id] = el.value;
});
app.addEventListener("click", async (event) => {
  const el = (event.target as Element).closest<HTMLElement>(
    "button,a,[data-go]",
  );
  if (!el || busy) return;
  const d = el.dataset,
    s = activeSeeker(world);
  if (el.tagName === "A" && "home" in d) event.preventDefault();
  if ("rare" in d && RARES.some((r) => r.name === d.rare)) {
    selectedRare = d.rare!;
    modal = "rare";
    message = "";
    render();
  } else if ("close" in d) {
    modal = null;
    message = "";
    pendingDelete = "";
    render();
  } else if ("modal" in d) {
    modal = d.modal as typeof modal;
    message = "";
    render();
  } else if ("view" in d) {
    view = d.view as typeof view;
    render();
  } else if ("home" in d) {
    view = "tree";
    newJourney = false;
    render();
  } else if ("act" in d) await act({ type: d.act } as Action);
  else if ("go" in d) {
    drafts.rite = "";
    await act({ type: "walk", to: d.go as SefirahId });
  } else if ("showRite" in d && s) {
    drafts.rite = s.current;
    render();
    document
      .querySelector("#rite-area")
      ?.scrollIntoView({
        block: "nearest",
        behavior: reduced ? "instant" : "smooth",
      });
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
      notice(
        "Download the original first. Press “Start a new tree” again to replace this device’s unreadable save.",
        true,
      );
    } else {
      try {
        localStorage.removeItem(SAVE_KEY);
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
    }
    if (form.id === "sigil-form")
      await act({ type: "sigil", text: String(f.get("sigil")) });
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
    if (navigator.locks) await navigator.locks.request(SAVE_KEY, work);
    else await work();
    notice("Journeys imported. Existing progress was preserved.");
  } catch (error) {
    notice(errorText(error), true);
  }
});
window.addEventListener("storage", async (event) => {
  if (event.key !== SAVE_KEY || busy) return;
  try {
    world = await loadWorld(localStorage);
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
  loading = false;
  render();
}
render();
void start();
if (import.meta.env?.PROD && "serviceWorker" in navigator) {
  void navigator.serviceWorker.register("/sw.js").catch(() => {
    /* Online play and exports remain available. */
  });
}
