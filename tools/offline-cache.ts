import { createHash } from "node:crypto";

/** Every cached file participates, including HTML whose filename never changes. */
export function offlineCacheName(
  files: Record<string, string | Uint8Array>,
): string {
  const fingerprint = createHash("sha256");
  for (const name of Object.keys(files).sort()) {
    const content = files[name];
    // Separate names and content hashes so different file boundaries cannot collide.
    fingerprint.update(
      JSON.stringify([
        name,
        createHash("sha256").update(content).digest("hex"),
      ]),
    );
  }
  return "vortex-" + fingerprint.digest("hex").slice(0, 16);
}
