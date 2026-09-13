import test from "node:test";
import assert from "node:assert/strict";
import {
  disposeFeel,
  feelEnabled,
  setFeelEnabled,
  unlockFeel,
  playWalk,
  playLook,
  playSit,
  playReveal,
} from "../feel-audio.ts";

class Param {
  value = 0;
  setValueAtTime(value: number) {
    this.value = value;
  }
  exponentialRampToValueAtTime(value: number) {
    this.value = value;
  }
  setTargetAtTime(value: number) {
    this.value = value;
  }
}
class AudioNode {
  gain = new Param();
  frequency = new Param();
  started = false;
  stopped = false;
  connect() {}
  disconnect() {}
  start() {
    this.started = true;
  }
  stop() {
    this.stopped = true;
  }
}
class Context {
  static instances: Context[] = [];
  static rejectResume = false;
  static deferResume = false;
  state = "suspended";
  currentTime = 0;
  destination = {};
  gains: AudioNode[] = [];
  oscillators: AudioNode[] = [];
  resumes = 0;
  rejectSuspend = false;
  releaseResume: (() => void) | undefined;
  constructor() {
    Context.instances.push(this);
  }
  createGain() {
    const node = new AudioNode();
    this.gains.push(node);
    return node;
  }
  createOscillator() {
    const node = new AudioNode();
    this.oscillators.push(node);
    return node;
  }
  async resume() {
    this.resumes++;
    if (Context.rejectResume) throw new Error("Audio denied");
    if (Context.deferResume)
      await new Promise<void>((resolve) => {
        this.releaseResume = resolve;
      });
    this.state = "running";
  }
  async suspend() {
    if (this.rejectSuspend) throw new Error("Audio suspend denied");
    this.state = "suspended";
  }
  async close() {
    this.state = "closed";
  }
}
const gestures = () => {
  playWalk(true);
  playLook();
  playSit();
  playReveal();
};
test.beforeEach(async () => {
  await disposeFeel();
  Context.instances = [];
  Context.rejectResume = false;
  Context.deferResume = false;
  Object.defineProperty(globalThis, "window", {
    configurable: true,
    value: { AudioContext: Context },
  });
});
test.afterEach(async () => {
  await disposeFeel();
});

test("a silent journey never constructs an audio context, including an explicit Off", async () => {
  gestures();
  assert.equal(unlockFeel(), false);
  assert.equal(await setFeelEnabled(false), true);
  assert.equal(Context.instances.length, 0);
});

test("Off stays silent through later game actions and enabling again reuses the same drone", async () => {
  assert.equal(await setFeelEnabled(true), true);
  const ctx = Context.instances[0];
  assert.equal(ctx.oscillators.length, 3);
  playLook();
  const sounded = ctx.oscillators.length;
  assert(sounded > 3);
  await setFeelEnabled(false);
  assert.equal(ctx.gains[0].gain.value, 0);
  gestures();
  assert.equal(ctx.resumes, 1, "muted actions must not resume the drone");
  assert.equal(ctx.oscillators.length, sounded);
  assert.equal(feelEnabled(), false);
  await setFeelEnabled(true);
  assert.equal(ctx.oscillators.length, sounded, "three drones are reused");
  assert.equal(Context.instances.length, 1);
  await disposeFeel();
  assert.equal(ctx.state, "closed");
  assert.equal(feelEnabled(), false);
});

test("a rejected audio resume reports unavailable and never leaks an unhandled rejection", async () => {
  Context.rejectResume = true;
  assert.equal(await setFeelEnabled(true), false);
  assert.equal(feelEnabled(), false);
  gestures();
  assert.equal(Context.instances[0].oscillators.length, 0);
  assert.equal(Context.instances[0].gains[0].gain.value, 0);
});

test("turning Off during a pending resume wins and leaves no audible drone", async () => {
  Context.deferResume = true;
  const enabling = setFeelEnabled(true);
  await new Promise((resolve) => setImmediate(resolve));
  const ctx = Context.instances[0];
  const disabling = setFeelEnabled(false);
  assert.equal(ctx.gains[0].gain.value, 0);
  assert.equal(feelEnabled(), false);
  ctx.releaseResume!();
  assert.equal(await enabling, false);
  assert.equal(await disabling, true);
  assert.equal(ctx.state, "suspended");
  gestures();
  assert.equal(ctx.oscillators.length, 0);
  assert.equal(ctx.resumes, 1);
});

test("Off still mutes the master when the browser refuses to suspend", async () => {
  await setFeelEnabled(true);
  const ctx = Context.instances[0];
  ctx.rejectSuspend = true;
  assert.equal(await setFeelEnabled(false), true);
  assert.equal(ctx.gains[0].gain.value, 0);
  gestures();
  assert.equal(ctx.oscillators.length, 3);
  assert.equal(feelEnabled(), false);
});

test("an effect device error falls back to silence instead of interrupting a game action", async () => {
  await setFeelEnabled(true);
  const ctx = Context.instances[0];
  ctx.createOscillator = () => {
    throw new Error("Device disconnected");
  };
  assert.doesNotThrow(gestures);
  assert.equal(feelEnabled(), false);
  assert.equal(ctx.gains[0].gain.value, 0);
});
