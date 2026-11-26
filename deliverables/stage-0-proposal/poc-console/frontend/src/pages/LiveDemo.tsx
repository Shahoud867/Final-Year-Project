import { STATIC } from "../api";
// Raw-text import so the static-export build can inline the whole demo page
// into one file (as a data: URI) instead of relying on a sibling file next
// to index.html. Normal dev/build ignores this string entirely and keeps
// loading the live file from public/ -- ?raw has no runtime cost there
// beyond the string sitting unused in the bundle.
import onclickDemoHtml from "../../public/onclick-demo/index.html?raw";

const IFRAME_SRC = STATIC
  ? "data:text/html;charset=utf-8," + encodeURIComponent(onclickDemoHtml)
  : "/onclick-demo/index.html";

export function LiveDemo() {
  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <iframe
        src={IFRAME_SRC}
        title="Granite — live one-click diagnosis demo"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}
