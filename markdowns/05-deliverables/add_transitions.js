// Injects native PowerPoint slide transitions into every slide of a pptx
// produced by pptxgenjs (which has no transition/animation API of its own).
// Per-element build/entrance animations are deliberately NOT injected here —
// hand-authored <p:timing> trees are high-risk to get byte-perfect and a
// corrupt file is the worst possible failure mode for a live defense.
// Slide-level <p:transition> is a single, well-documented element and safe.
const AdmZip = require("adm-zip");

const IN = process.argv[2];
const OUT = process.argv[3];
if (!IN || !OUT) { console.error("usage: node add_transitions.js in.pptx out.pptx"); process.exit(1); }

const zip = new AdmZip(IN);
const entries = zip.getEntries().filter(e => /^ppt\/slides\/slide\d+\.xml$/.test(e.entryName));
let changed = 0;

entries.forEach((entry) => {
  let xml = entry.getData().toString("utf8");
  if (xml.includes("<p:transition")) return; // idempotent
  const marker = "</p:cSld>";
  const idx = xml.indexOf(marker);
  if (idx === -1) { console.error("no </p:cSld> in " + entry.entryName); return; }
  const insertAt = idx + marker.length;
  const transitionXml = '<p:transition spd="med"><p:fade/></p:transition>';
  xml = xml.slice(0, insertAt) + transitionXml + xml.slice(insertAt);
  zip.updateFile(entry, Buffer.from(xml, "utf8"));
  changed++;
});

zip.writeZip(OUT);
console.log(`Injected transitions into ${changed} slide(s). Wrote ${OUT}`);
