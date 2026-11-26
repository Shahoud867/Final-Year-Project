// Injects native PowerPoint slide transitions into Granite_Proposal_Defense_v2.pptx.
//
// pptxgenjs cannot emit <p:transition> elements, so they are added here as a
// post-process on the generated package. Only plain ECMA-376 transition types are
// used (no p14/p159 extension namespaces), so the file stays standards-valid and
// opens in PowerPoint, Keynote and LibreOffice without a repair prompt.
//
// Deliberately restrained: a defense deck is judged on evidence, not motion.
// Fade only, slow on the title slide, medium everywhere else.
//
// Run:  node add_transitions_v2.js        (after generate_proposal_deck_v2.js)
const AdmZip = require("adm-zip");
const { XMLValidator } = require("fast-xml-parser");
const path = require("path");

const FILE = path.join(__dirname, "Granite_Proposal_Defense_v2.pptx");

const zip = new AdmZip(FILE);
const entries = zip.getEntries();

let injected = 0, skipped = 0;
for (const e of entries) {
  const m = /^ppt\/slides\/slide(\d+)\.xml$/.exec(e.entryName);
  if (!m) continue;
  const n = parseInt(m[1], 10);
  let xml = zip.readAsText(e);

  if (xml.includes("<p:transition")) { skipped++; continue; }

  // Title slide gets the slower fade; content slides the medium one.
  const speed = n === 1 ? "slow" : "med";
  const transition = `<p:transition spd="${speed}"><p:fade/></p:transition>`;

  // Schema order inside <p:sld> is cSld, clrMapOvr, transition, timing —
  // so appending immediately before </p:sld> is correct here.
  if (!xml.includes("</p:sld>")) {
    throw new Error(`unexpected slide XML shape in ${e.entryName}`);
  }
  xml = xml.replace("</p:sld>", `${transition}</p:sld>`);

  const check = XMLValidator.validate(xml);
  if (check !== true) {
    throw new Error(`injection produced invalid XML in ${e.entryName}: ${JSON.stringify(check.err)}`);
  }
  zip.updateFile(e.entryName, Buffer.from(xml, "utf8"));
  injected++;
}

zip.writeZip(FILE);

// Re-open and re-validate every XML part of the written file, not just the ones touched.
const after = new AdmZip(FILE);
let parts = 0, bad = [];
for (const e of after.getEntries()) {
  if (!e.entryName.endsWith(".xml") && !e.entryName.endsWith(".rels")) continue;
  parts++;
  const r = XMLValidator.validate(after.readAsText(e));
  if (r !== true) bad.push(e.entryName);
}
const withTransition = after.getEntries()
  .filter(e => /^ppt\/slides\/slide\d+\.xml$/.test(e.entryName))
  .filter(e => after.readAsText(e).includes("<p:transition")).length;

console.log(`transitions injected : ${injected} (skipped ${skipped} already present)`);
console.log(`slides with fade     : ${withTransition}`);
console.log(`xml parts revalidated: ${parts}`);
console.log(`malformed parts      : ${bad.length ? bad.join(", ") : "none"}`);
if (bad.length) process.exit(1);
