import test from "node:test";
import assert from "node:assert/strict";
import { assetLink, addressLink, explorerQuery } from "../explorer.ts";
import { assetDestination } from "../explorer-view.ts";
import { stampBody, stampInvitation } from "../stamps-view.ts";
import { STAMP_OFFICES, stampReply } from "../stamps.ts";
import { NODES } from "../lattice.ts";
import { activeSeeker, transition } from "../session.ts";
import { finish, travel } from "./helpers.ts";

test("explorer routes support named, numeric and case-sensitive subassets without external URL injection", () => {
  assert.equal(explorerQuery(" xcp "), "XCP");
  assert.equal(explorerQuery("pepecash"), "PEPECASH");
  assert.equal(explorerQuery("A95428956661682277"), "A95428956661682277");
  assert.equal(
    explorerQuery("PARENT.Mixed_Case-@!.child"),
    "PARENT.Mixed_Case-@!.child",
  );
  assert.equal(
    new URL(assetLink("A95428956661682277", "PARENT.Mixed_Case-@!.child"))
      .pathname,
    "/asset/PARENT.Mixed_Case-%40!.child",
  );
  for (const input of [
    "",
    "https://evil.example",
    '<img src=x onerror="alert(1)">',
    "a ".repeat(12),
    "../escape",
    "NAME\nOTHER",
    "a".repeat(251),
  ]) {
    assert.equal(explorerQuery(input), null);
    assert(!assetDestination(input).includes("<a"));
  }
  assert.equal(new URL(assetLink('NAME\"/><script>')).origin, "https://xcp.io");
  assert.equal(
    new URL(addressLink("1/address?next=evil")).origin,
    "https://xcp.io",
  );
});

test("Stamps teaching lives in the making-to-ledger descent and distinguishes lore, data and protocols", () => {
  assert.equal(stampInvitation("keter"), "");
  for (const id of STAMP_OFFICES) {
    assert.match(stampInvitation(id), /data-modal="stamps"/);
    const body = stampBody(id, "folk");
    assert.match(
      body,
      new RegExp(`data-stamp-office="${id}" aria-pressed="true"`),
    );
    assert.match(body, /VORTEX fiction/);
    assert.match(body, /not SRC-20 holdings/);
    assert(!body.includes("data-act="));
    assert.notEqual(stampBody(id, "classical"), body);
  }
  assert.match(stampBody("malkhut", "folk"), /https:\/\/kevinstamp.com\//);
  assert.match(stampBody("malkhut", "folk"), /community legend/);
  assert.match(stampBody("yesod", "folk"), /If a data-bearing output is spent/);
});

test("asking about Bitcoin Stamps reaches contextual teaching without minting or changing achievements", () => {
  const finished = finish();
  for (const id of STAMP_OFFICES) {
    const before = travel(finished, id);
    const after = transition(before, {
      type: "talk",
      text: "Tell me about Bitcoin Stamps and immutable data",
    });
    const original = activeSeeker(before)!,
      s = activeSeeker(after)!;
    assert.equal(
      s.journal.at(-1)!.text,
      stampReply(
        id,
        s.dialect === "folk" && NODES[id].folkGuide ? "folk" : "classical",
      ),
    );
    for (const field of [
      "sigil",
      "rooted",
      "festival",
      "stories",
      "proof",
      "rites",
    ] as const)
      assert.deepEqual(s[field], original[field]);
    assert(
      !JSON.stringify(after).includes(
        "Tell me about Bitcoin Stamps and immutable data",
      ),
    );
  }
});
