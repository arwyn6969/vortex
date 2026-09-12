import test from "node:test";
import assert from "node:assert/strict";
import vectors from "./fixtures/bip322.json" with { type: "json" };
import {
  verifyMessage,
  verifyProof,
  issueChallenge,
  acceptSignature,
} from "../wallet.ts";
import { Signer } from "bip322-js";
import { activeSeeker } from "../session.ts";
import { loadWorld, SAVE_KEY } from "../storage.ts";
import { finish, newGame, MemoryStorage } from "./helpers.ts";

test("published BIP-322 examples verify, including finalized smp prefix and old Taproot format", async () => {
  for (const v of vectors.simple.filter((v) =>
    ["p2wpkh", "p2tr"].includes(v.type),
  )) {
    for (const signature of v.bip322_signatures) {
      assert.equal(
        await verifyMessage(v.address, v.message, signature),
        true,
        v.type,
      );
      assert.equal(
        await verifyMessage(v.address, v.message + "tampered", signature),
        false,
      );
    }
  }
});
test("published invalid proofs and unsupported multisig are rejected", async () => {
  for (const v of vectors.error)
    assert.equal(
      await verifyMessage(v.address, v.message, v.signature),
      false,
      v.description,
    );
  const v = vectors.simple.find((v) => v.type.includes("multisig"))!;
  assert.equal(
    await verifyMessage(v.address, v.message, v.bip322_signatures[0]),
    false,
  );
});
test("wallet binding checks readiness, checksum and supported script before asking for a signature", async () => {
  const address = vectors.simple[0].address;
  await assert.rejects(issueChallenge(newGame(), address), /Kingdom/);
  await assert.rejects(
    issueChallenge(finish(), address.slice(0, -1) + "x"),
    /checksum/,
  );
  await assert.rejects(
    issueChallenge(finish(), vectors.simple[2].address),
    /not supported/,
  );
});
test("a signed challenge binds only its own seeker, sigil, nonce, address and time window", async () => {
  // Public, deliberately compromised BIP-322 fixture key; never use for funds.
  // Source is the CC0 Bitcoin BIPs vector file linked in fixtures/bip322.json.
  const fixtureWif = "L3VFeEujGtevx9w18HD1fhRbCH67Az2dpCymeRE1SoPK6XQtaN2k";
  const now = 1_700_000_000_000,
    address = vectors.simple[0].address;
  const w = await issueChallenge(finish(), address, now, "public-test-nonce");
  const s = activeSeeker(w)!,
    c = s.challenge!;
  const signature = Signer.sign(fixtureWif, address, c.message);
  const bound = await acceptSignature(w, signature, c.nonce, now + 1);
  const p = activeSeeker(bound)!.proof!;
  assert(activeSeeker(bound)!.rooted);
  assert(await verifyProof(s, p));
  for (const patch of [
    { seekerId: "someone-else" },
    { nonce: "wrong" },
    { address: "1BoatSLRHtKNngkdXEeobR76b53LETtpyT" },
    { verifiedAt: now - 1 },
    { verifiedAt: c.expiresAt + 1 },
    { expiresAt: c.expiresAt + 1 },
    { message: c.message + "!" },
  ])
    assert.equal(await verifyProof(s, { ...p, ...patch }), false);
  assert.equal(await verifyProof({ ...s, sigil: "Changed" }, p), false);
  await assert.rejects(acceptSignature(w, signature, "wrong", now), /replaced/);
  await assert.rejects(
    acceptSignature(w, signature, c.nonce, c.expiresAt + 1),
    /expired/,
  );
  await assert.rejects(
    acceptSignature(bound, signature, c.nonce, now),
    /replaced/,
  );
  const store = new MemoryStorage();
  store.setItem(SAVE_KEY, JSON.stringify(bound));
  assert.deepEqual(await loadWorld(store), bound);
  activeSeeker(bound)!.proof!.signature = "AAAA";
  store.setItem(SAVE_KEY, JSON.stringify(bound));
  await assert.rejects(loadWorld(store), /cannot be verified/);
});
