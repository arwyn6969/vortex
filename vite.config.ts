import { defineConfig } from "vite";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
function publicFiles(directory: string, prefix = ""): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) =>
    entry.isDirectory()
      ? publicFiles(join(directory, entry.name), prefix + entry.name + "/")
      : [prefix + entry.name],
  );
}
export default defineConfig({
  root: "vortex/web",
  build: { outDir: "../../dist", emptyOutDir: true, target: "es2022" },
  server: { strictPort: true, port: 5173 },
  plugins: [
    {
      name: "vortex-offline",
      generateBundle(_options, bundle) {
        const assets = publicFiles("vortex/web/public");
        const fingerprint = createHash("sha256").update(
          JSON.stringify(Object.keys(bundle).sort()),
        );
        for (const name of assets)
          fingerprint.update(readFileSync(join("vortex/web/public", name)));
        const cache = "vortex-" + fingerprint.digest("hex").slice(0, 16);
        const urls = [
          ...new Set([
            "/",
            "/index.html",
            ...Object.keys(bundle).map((p) => "/" + p),
            ...assets.map((p) => "/" + p),
          ]),
        ];
        this.emitFile({
          type: "asset",
          fileName: "sw.js",
          source: `
const CACHE=${JSON.stringify(cache)};
const FILES=${JSON.stringify(urls)};
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('vortex-') && key !== CACHE).map(key => caches.delete(key)))));
});
self.addEventListener('fetch', event => {
  const url=new URL(event.request.url);
  if(event.request.method !== 'GET' || url.origin !== self.location.origin || !FILES.includes(url.pathname)) return;
  event.respondWith(caches.open(CACHE).then(async cache => (await cache.match(url.pathname)) || fetch(event.request)));
});
`,
        });
      },
    },
  ],
});
