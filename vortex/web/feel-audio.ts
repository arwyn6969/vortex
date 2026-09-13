type Mixer = {
  ctx: AudioContext;
  master: GainNode;
  music: GainNode;
  sfx: GainNode;
  drones: OscillatorNode[];
};

let mixer: Mixer | null = null;
let enabled = false;
let intent = 0;
let pending: Promise<boolean> = Promise.resolve(true);

function bus(ctx: AudioContext) {
  const master = ctx.createGain();
  // Stay silent until an explicit enable finishes successfully.
  master.gain.value = 0;
  master.connect(ctx.destination);
  const music = ctx.createGain();
  music.gain.value = 0.45;
  music.connect(master);
  const sfx = ctx.createGain();
  sfx.gain.value = 0.7;
  sfx.connect(master);
  return { master, music, sfx };
}

function ensure(): Mixer | null {
  if (typeof window === "undefined") return null;
  if (mixer) return mixer;
  try {
    const AudioCtx =
      window.AudioContext ||
      (window as typeof window & { webkitAudioContext?: typeof AudioContext })
        .webkitAudioContext;
    if (!AudioCtx) return null;
    const ctx = new AudioCtx({ latencyHint: "interactive" });
    const { master, music, sfx } = bus(ctx);
    mixer = { ctx, master, music, sfx, drones: [] };
    return mixer;
  } catch {
    return null;
  }
}

function beep(
  freq: number,
  dur: number,
  type: OscillatorType,
  gain: number,
  when = 0,
) {
  const m = mixer;
  if (!m || !enabled) return;
  try {
    const t = m.ctx.currentTime + when;
    const o = m.ctx.createOscillator();
    const g = m.ctx.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(gain, t + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g);
    g.connect(m.sfx);
    o.start(t);
    o.stop(t + dur + 0.02);
    o.onended = () => {
      o.disconnect();
      g.disconnect();
    };
  } catch {
    failSilent(m);
  }
}

function failSilent(m: Mixer) {
  enabled = false;
  intent++;
  try {
    m.master.gain.value = 0;
  } catch {
    /* Device may already be gone. */
  }
  void m.ctx.suspend().catch(() => {});
}

export function feelEnabled() {
  return enabled;
}

export function unlockFeel() {
  // Game actions must never construct or resume a context, especially after Off.
  return enabled && mixer?.ctx.state === "running";
}

export function setFeelEnabled(on: boolean): Promise<boolean> {
  const request = ++intent;
  enabled = on;
  // Mute immediately; a pending resume must not undo a newer Off request.
  if (mixer) mixer.master.gain.value = 0;
  const change = async (): Promise<boolean> => {
    if (request !== intent) return false;
    if (!on) {
      try {
        await mixer?.ctx.suspend();
      } catch {
        /* Already muted. */
      }
      return request === intent;
    }
    const m = ensure();
    if (!m) {
      enabled = false;
      return false;
    }
    try {
      await m.ctx.resume();
      if (request !== intent || !enabled || mixer !== m) return false;
      if (m.ctx.state !== "running") throw new Error("Audio is unavailable");
      if (!m.drones.length) {
        const specs: [number, OscillatorType, number][] = [
          [92, "sine", 0.18],
          [138, "triangle", 0.1],
          [184, "sine", 0.06],
        ];
        for (const [freq, type, vol] of specs) {
          const o = m.ctx.createOscillator();
          const g = m.ctx.createGain();
          o.type = type;
          o.frequency.value = freq;
          g.gain.value = vol;
          o.connect(g);
          g.connect(m.music);
          o.start();
          m.drones.push(o);
        }
      }
      m.master.gain.value = 0.22;
      return true;
    } catch {
      m.master.gain.value = 0;
      if (request === intent) enabled = false;
      return false;
    }
  };
  // Browsers can settle resume/suspend out of order. Serialize those operations.
  const result = pending.then(change, change);
  pending = result;
  return result;
}

export async function disposeFeel() {
  enabled = false;
  intent++;
  const m = mixer;
  mixer = null;
  if (!m) return;
  m.master.gain.value = 0;
  for (const oscillator of m.drones) {
    try {
      oscillator.stop();
      oscillator.disconnect();
    } catch {
      /* Already stopped. */
    }
  }
  try {
    await m.ctx.close();
  } catch {
    /* Unloading is still safe. */
  }
}

export function leanDrone(pillars: {
  mercy: number;
  severity: number;
  balance: number;
}) {
  const m = mixer;
  if (!m || !enabled || m.drones.length < 3) return;
  try {
    const t = m.ctx.currentTime;
    m.drones[0].frequency.setTargetAtTime(82 + pillars.mercy * 40, t, 0.4);
    m.drones[1].frequency.setTargetAtTime(130 + pillars.severity * 50, t, 0.4);
    m.drones[2].frequency.setTargetAtTime(170 + pillars.balance * 60, t, 0.4);
  } catch {
    failSilent(m);
  }
}

export function playWalk(firstCrossing: boolean) {
  if (!unlockFeel() || !enabled) return;
  beep(196, 0.11, "sine", 0.07);
  beep(247, 0.14, "triangle", 0.045, 0.04);
  if (firstCrossing) beep(330, 0.22, "sine", 0.05, 0.08);
}

export function playLook() {
  if (!unlockFeel() || !enabled) return;
  beep(392, 0.18, "sine", 0.055);
  beep(494, 0.28, "triangle", 0.03, 0.06);
}

export function playSit() {
  if (!unlockFeel() || !enabled) return;
  beep(110, 0.4, "sine", 0.06);
  beep(147, 0.5, "triangle", 0.035, 0.05);
}

export function playReveal() {
  if (!unlockFeel() || !enabled) return;
  beep(262, 0.2, "sine", 0.05);
  beep(392, 0.28, "sine", 0.04, 0.08);
  beep(523, 0.35, "triangle", 0.03, 0.16);
}
