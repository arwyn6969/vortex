import test from "node:test";
import assert from "node:assert/strict";
import { registerJourneyTools } from "../webmcp.ts";
import type { JourneyTool } from "../webmcp.ts";
import { transition } from "../session.ts";
import { newGame } from "./helpers.ts";

test("native-tool contract exposes sourced atlas content, validates mutations and excludes private fields", async () => {
  let w = newGame();
  const registered = new Map<string, JourneyTool>();
  let signal: AbortSignal | undefined;
  const dispose = registerJourneyTools(
    {
      registerTool: (t, options) => {
        registered.set(t.name, t);
        signal = options.signal;
      },
    },
    () => w,
    async (action, expected) => {
      if (expected.revision !== w.revision || expected.seekerId !== w.activeId)
        throw new Error("stale");
      w = transition(w, action);
    },
  );
  const read = registered.get("read_atlas_entry")!,
    state = registered.get("get_journey_state")!,
    action = registered.get("take_journey_action")!;
  const before = JSON.stringify(w);
  const entry: any = read.execute({ entry: "nisaba" });
  assert.match(entry.sourceRecord.url, /oracc/);
  assert.equal(JSON.stringify(w), before);
  assert.throws(() => read.execute({ entry: "invented" }));
  assert.throws(() =>
    read.execute({ entry: "nisaba", question: "private question" }),
  );
  const revision = w.revision;
  await action.execute({
    seekerId: w.activeId,
    revision,
    action: "study",
    entry: "nisaba",
  });
  const saved = JSON.stringify(w);
  await assert.rejects(
    Promise.resolve().then(() =>
      action.execute({ seekerId: w.activeId, revision, action: "sit" }),
    ),
    /stale/,
  );
  assert.equal(JSON.stringify(w), saved);
  for (const input of [
    { action: "sigil", text: "private" },
    { action: "study", entry: "__proto__" },
    { action: "inquiry", task: "tablet", choice: 9 },
    { action: "sit", address: "private" },
  ])
    await assert.rejects(
      Promise.resolve().then(() =>
        action.execute({
          seekerId: w.activeId,
          revision: w.revision,
          ...input,
        }),
      ),
    );
  const snapshot = JSON.stringify(state.execute({}));
  for (const field of [
    '"journal"',
    '"proof"',
    '"challenge"',
    '"address"',
    '"sigil"',
  ])
    assert(!snapshot.includes(field));
  dispose();
  assert(signal?.aborted);
});
