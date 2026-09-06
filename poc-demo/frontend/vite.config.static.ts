// Static, shareable-single-file build config -- separate from vite.config.ts
// so the normal `npm run dev` / `npm run build` experience is untouched.
// Produces one self-contained dist/index.html (JS/CSS inlined) that serves
// all data from src/staticData.json instead of the live backend.
//
// Usage:
//   npm run build:static
// Output: dist/index.html -- open it directly, no server needed.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  define: {
    "import.meta.env.VITE_STATIC_EXPORT": JSON.stringify("true"),
  },
  // Everything (including the Live demo page) is now inlined into index.html
  // via ?raw + a data: URI (see src/pages/LiveDemo.tsx) -- skip copying
  // public/ so the shareable output really is one file.
  publicDir: false,
  build: {
    outDir: "dist-static",
    cssCodeSplit: false,
    assetsInlineLimit: 100_000_000,
  },
});
