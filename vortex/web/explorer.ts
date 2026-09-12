// Verified against XCP/explorer's asset-link helper and app routes, 2026-09-12.
// Keep subasset longnames byte-exact: their suffix is case-sensitive.
export const assetLink = (asset: string, longname?: string | null) =>
  "https://xcp.io/asset/" + encodeURIComponent(longname || asset);
export const addressLink = (address: string) =>
  "https://xcp.io/address/" + encodeURIComponent(address);

export function explorerQuery(input: string): string | null {
  const value = input.trim();
  if (!value || value.length > 250) return null;
  if (value.includes(".")) {
    // A routing aid, not issuance validation or a claim that an asset exists.
    return /^[A-Z]{4,12}\.[A-Za-z0-9._@!\-]+$/.test(value) ? value : null;
  }
  const upper = value.toUpperCase();
  return /^(?:[A-Z]{4,12}|A[0-9]{1,20}|XCP)$/.test(upper) ? upper : null;
}
