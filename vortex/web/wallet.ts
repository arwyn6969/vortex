import type { Challenge, Proof, Seeker, World } from "./session.ts";
import { activeSeeker, readyToRoot, record } from "./session.ts";
import { looksLikeSecret } from "./safety.ts";

async function verifier() {
  const { Buffer } = await import("buffer");
  (globalThis as unknown as { Buffer: typeof Buffer }).Buffer ??= Buffer;
  return import("bip322-js");
}
// bip322-js verifies the witness. Handle the finalized BIP's human-readable
// prefix here; full transactions, PSBTs, multisig and script paths are excluded.
export async function verifyMessage(
  address: string,
  message: string,
  signature: string,
): Promise<boolean> {
  try {
    if (
      !/^(1|bc1)[a-zA-Z0-9]+$/.test(address) ||
      signature.length > 2048 ||
      /^(ful|pof)/.test(signature)
    )
      return false;
    const { Address, Verifier } = await verifier();
    const simple = signature.startsWith("smp");
    const raw = simple ? signature.slice(3) : signature;
    if (!/^[A-Za-z0-9+/]+={0,2}$/.test(raw)) return false;
    const bytes = Buffer.from(raw, "base64");
    if (bytes.toString("base64").replace(/=+$/, "") !== raw.replace(/=+$/, ""))
      return false;
    if (Address.isP2PKH(address)) {
      if (simple || bytes.length !== 65) return false;
    } else if (Address.isP2WPKH(address) || Address.isP2TR(address)) {
      // Never interpret a recoverable legacy ECDSA signature as a simple proof.
      if (bytes.length === 65) return false;
    } else return false;
    return Verifier.verifySignature(address, message, raw, true);
  } catch {
    return false;
  }
}
export function challengeMessage(
  s: Pick<Seeker, "id" | "sigil">,
  c: Pick<Challenge, "address" | "nonce" | "issuedAt" | "expiresAt">,
) {
  return [
    "VORTEX — bind a journey, never authorize a payment.",
    "Network: bitcoin-mainnet",
    "Seeker: " + s.id,
    "Sigil: " + s.sigil,
    "Address: " + c.address,
    "Nonce: " + c.nonce,
    "Issued: " + new Date(c.issuedAt).toISOString(),
    "Expires: " + new Date(c.expiresAt).toISOString(),
    "This signature records control of an address for this local game only.",
  ].join("\n");
}
export async function issueChallenge(
  world: World,
  address: string,
  now = Date.now(),
  nonce: string = crypto.randomUUID(),
): Promise<World> {
  const s = activeSeeker(world);
  if (!s || s.current !== "malkhut" || !readyToRoot(s))
    throw new Error(
      "Bring a sigil, six offices, and four rites to Kingdom before binding.",
    );
  address = address.trim();
  if (looksLikeSecret(address))
    throw new Error("Use an address, never a private key or recovery phrase.");
  if (address.length > 90 || !/^(1|3|bc1)[a-zA-Z0-9]+$/.test(address))
    throw new Error("Use a Bitcoin mainnet address.");
  const { Address } = await verifier();
  if (!Address.isValidBitcoinAddress(address))
    throw new Error("That address has an invalid format or checksum.");
  if (!(
    Address.isP2PKH(address) ||
    Address.isP2WPKH(address) ||
    Address.isP2TR(address)
  ))
    throw new Error(
      "Use a single-key native SegWit, Taproot, or legacy address. Multisig and nested addresses are not supported in this edition.",
    );
  const next = structuredClone(world),
    player = activeSeeker(next)!;
  const challenge: Challenge = {
    address,
    nonce,
    issuedAt: now,
    expiresAt: now + 10 * 60_000,
    seekerId: s.id,
    message: "",
  };
  challenge.message = challengeMessage(s, challenge);
  player.challenge = challenge;
  player.proof = null;
  next.revision++;
  return next;
}
export async function verifyProof(
  s: Pick<Seeker, "id" | "sigil">,
  p: Proof,
): Promise<boolean> {
  try {
    if (
      p.seekerId !== s.id ||
      p.verifiedAt < p.issuedAt ||
      p.verifiedAt > p.expiresAt ||
      p.expiresAt - p.issuedAt !== 600_000 ||
      p.message !== challengeMessage(s, p) ||
      !/^(1|3|bc1)[a-zA-Z0-9]+$/.test(p.address) ||
      p.signature.length > 2048
    )
      return false;
    return verifyMessage(p.address, p.message, p.signature);
  } catch {
    return false;
  }
}
export async function acceptSignature(
  world: World,
  signature: string,
  expectedNonce: string,
  now = Date.now(),
): Promise<World> {
  const s = activeSeeker(world);
  if (!s || s.current !== "malkhut" || !readyToRoot(s))
    throw new Error("Return to Kingdom with your completed work.");
  const c = s.challenge;
  if (!c || c.nonce !== expectedNonce || now < c.issuedAt || now > c.expiresAt)
    throw new Error(
      "That challenge has expired or was replaced. Ask for a new one.",
    );
  signature = signature.trim();
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(signature) || signature.length > 2048)
    throw new Error(
      "Paste only the Base64 message signature supplied by your wallet.",
    );
  const proof: Proof = { ...c, signature, verifiedAt: now };
  if (!(await verifyProof(s, proof)))
    throw new Error(
      "The signature does not match this address and exact message. Use BIP-322 simple or a supported legacy message signature.",
    );
  const next = structuredClone(world),
    player = activeSeeker(next)!;
  player.proof = proof;
  player.challenge = null;
  player.rooted = true;
  next.revision++;
  record(
    player,
    "discovery",
    "BOUND · Your wallet has witnessed the mark. The key remains with you. Nothing was spent or sent to the chain.",
  );
  return next;
}
