export function looksLikeSecret(value: string): boolean {
  const text = value.trim();
  return (
    /(?:^|\s)(?:[5KLc9][1-9A-HJ-NP-Za-km-z]{49,52}|(?:0x)?[a-fA-F0-9]{64})(?:$|\s)/.test(
      text,
    ) ||
    /\b(?:sk-[A-Za-z0-9_-]{16,}|-----BEGIN .*PRIVATE KEY-----)/.test(text) ||
    ([12, 15, 18, 21, 24].includes(text.split(/\s+/).length) &&
      /^[a-z]+(?:\s+[a-z]+)+$/i.test(text))
  );
}
export function safeText(value: unknown, max: number, min = 1): string {
  if (typeof value !== "string") throw new Error("Please enter text.");
  const text = value.trim().normalize("NFC");
  if (
    text.length < min ||
    text.length > max ||
    /[\u0000-\u001f\u007f]/.test(text)
  )
    throw new Error("Use " + min + "–" + max + " characters on one line.");
  if (looksLikeSecret(text))
    throw new Error(
      "That may contain a private key or recovery phrase. It was not saved. Keep wallet secrets in your wallet.",
    );
  return text;
}
export const escapeHtml = (s: unknown) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ]!,
  );
