import { BookOpen, ChevronRight, FileCode2, FlaskConical, GitBranch, GitCommitHorizontal, Inbox, Moon, PlugZap, Plus, ShieldCheck, Sigma, Sun, Workflow } from "lucide-react";
import { useEffect, useState } from "react";
import { api, getToken, setToken } from "./api";
import { BrandMark, Card, ModeBadge } from "./components/ui";
import type { Icon } from "./components/ui";
import { BUILD, commitUrl, repoUrl } from "./delivery";
import { useLoad, useRoute, useTheme } from "./hooks";
import { Connections } from "./pages/Connections";
import { Evaluation } from "./pages/Evaluation";
import { Evidence } from "./pages/Evidence";
import { Lab } from "./pages/Lab";
import { FindingDetail } from "./pages/FindingDetail";
import { Guide } from "./pages/Guide";
import { Home } from "./pages/Home";
import { NewRun } from "./pages/NewRun";
import { RunDetail } from "./pages/RunDetail";
import { Runs } from "./pages/Runs";
import { StyleGuide } from "./pages/StyleGuide";
import type { Health } from "./types";

type NavItem = { route: string; href: string; label: string; icon: Icon };
/** Working pages first; explanation last, in its own group (roadmap section 4). The case file is reached from the Inbox. */
const NAV: NavItem[] = [
  { route: "", href: "#/", label: "Inbox", icon: Inbox },
  { route: "runs", href: "#/runs", label: "Runs", icon: Workflow },
  { route: "lab", href: "#/lab", label: "Fault Lab", icon: FlaskConical },
  { route: "evaluation", href: "#/evaluation", label: "Evaluation", icon: Sigma },
  { route: "connections", href: "#/connections", label: "Connections", icon: PlugZap },
];
const HELP: NavItem[] = [
  { route: "guide", href: "#/guide", label: "How it works", icon: BookOpen },
  { route: "evidence", href: "#/evidence", label: "Why Granite", icon: ShieldCheck },
];
const SECTION: Record<string, string> = {
  "": "Inbox", findings: "Inbox", runs: "Runs", new: "New run", lab: "Fault Lab", evaluation: "Evaluation",
  connections: "Connections", guide: "How it works", evidence: "Why Granite", styleguide: "Style guide",
};
/** The style guide renders every component in every state; it ships only in development or when the build asks for it. */
const STYLEGUIDE = import.meta.env.DEV || import.meta.env.VITE_STYLEGUIDE === "1";

function Brand() {
  return (
    <a className="brand" href="#/">
      <BrandMark />
      <span className="brand-text"><span className="brand-name">Granite</span><span className="brand-tag">find · prove · fix</span></span>
    </a>
  );
}

/** This server, as it reports itself: reachability, model mode, version and the commit the bundle was built from. */
function Instance({ health, error }: { health: Health | null; error: string }) {
  return (
    <div className="instance">
      <div className="instance-row">
        <span className={`dot tone-${error ? "bad" : health ? "ok" : "neutral"}`} aria-hidden="true" />
        <span>{error ? "Server unreachable" : health ? "Server online" : "Checking server…"}</span>
      </div>
      {health ? <div className="instance-row"><ModeBadge mode={health.llm_mode} /></div> : null}
      <div className="instance-row mono">
        <GitCommitHorizontal size={13} aria-hidden="true" />
        <span>{health ? `v${health.version}` : "version n/a"}</span>
        {BUILD.sha ? <a href={commitUrl(BUILD.sha)} target="_blank" rel="noreferrer" title="The commit this interface was built from">{BUILD.sha}</a> : <span className="dim" title="The build did not record a commit">no build stamp</span>}
      </div>
    </div>
  );
}

function ServerTools({ health, error }: { health: Health | null; error: string }) {
  const [msg, setMsg] = useState("");
  const [token, setTok] = useState(getToken());
  return (
    <>
      {msg && <span role="status" className="muted small hide-phone">{msg}</span>}
      {error ? <span className="badge tone-bad" role="status">server unreachable</span> : null}
      {health ? (
        <span className="row tight" role="status" aria-label={`Server online, ${health.llm_mode} mode${health.live_model_reachable ? ", live model reachable" : ""}`}>
          <span className="dot tone-ok" aria-hidden="true" />
          <ModeBadge mode={health.llm_mode} />
          {health.live_model_reachable ? <span className="chip tone-replay hide-phone">model online</span> : null}
        </span>
      ) : null}
      {health?.auth_required && (
        <input aria-label="Access token" type="password" placeholder="Access token" value={token} style={{ width: 140 }}
               onChange={(e) => { setTok(e.target.value); setToken(e.target.value); }} />
      )}
      <button type="button" className="btn sm hide-phone" title="Send one tiny request to the configured model"
              onClick={async () => { try { setMsg((await api.testLlm()).message); } catch { setMsg("Could not reach the server."); } }}>
        Test model
      </button>
    </>
  );
}

export default function App() {
  const [page = "", id = ""] = useRoute();
  const [theme, toggleTheme] = useTheme();
  const health = useLoad(() => api.health(), []);
  useEffect(() => { document.documentElement.scrollTop = 0; }, [page, id]);

  let view = <Home />;
  if (page === "new") view = <NewRun />;
  else if (page === "lab") view = <Lab />;
  else if (page === "evaluation") view = <Evaluation />;
  else if (page === "connections") view = <Connections />;
  else if (page === "guide") view = <Guide />;
  else if (page === "evidence") view = <Evidence />;
  else if (page === "runs" && id) view = <RunDetail id={id} key={id} />;
  else if (page === "runs") view = <Runs />;
  else if (page === "findings" && id) view = <FindingDetail id={id} key={id} />;
  else if (page === "styleguide" && STYLEGUIDE) view = <StyleGuide />;
  else if (page) view = <Card><h1>Page not found</h1><p className="muted"><a href="#/">Back to the inbox</a></p></Card>;

  const section = page === "styleguide" && !STYLEGUIDE ? "Not found" : SECTION[page] ?? "Not found";
  const exact = (route: string) => (page === route && !id ? "page" : undefined);
  // a case file belongs to the Inbox and a run page to Runs, so their section stays highlighted
  const within = (route: string) => (route === "" && page === "findings") || (route === "runs" && page === "runs" && !!id);
  const link = (n: NavItem) => (
    <a key={n.route} href={n.href} aria-current={exact(n.route)} data-active={within(n.route) || undefined}>
      <n.icon size={16} aria-hidden="true" /><span>{n.label}</span>
    </a>
  );
  return (
    <div className="shell">
      <a className="skip" href="#main">Skip to content</a>
      <aside className="sidebar">
        <Brand />
        <nav className="nav" aria-label="Main">
          {NAV.map(link)}
          <div className="nav-help" role="group" aria-labelledby="nav-help-h">
            <div className="nav-group" id="nav-help-h">Help</div>
            {HELP.map(link)}
          </div>
        </nav>
        <div className="sidebar-foot">
          <Instance health={health.data} error={health.error} />
          <div className="side-links">
            <a href="/docs" target="_blank" rel="noreferrer" title="Generated API reference (OpenAPI)"><FileCode2 size={13} aria-hidden="true" /><span>API reference</span></a>
            <a href={repoUrl()} target="_blank" rel="noreferrer" title="Source repository"><GitBranch size={13} aria-hidden="true" /><span>Repository</span></a>
          </div>
        </div>
      </aside>
      <div className="main-col">
        <header className="topbar">
          <Brand />
          <div className="crumbs" aria-hidden="true">
            <span>Granite</span><ChevronRight size={13} /><strong>{section}</strong>
            {id ? <><ChevronRight size={13} /><span className="mono truncate">{id}</span></> : null}
          </div>
          <div className="topbar-actions">
            <ServerTools health={health.data} error={health.error} />
            <button type="button" className="btn ghost icon sm" onClick={toggleTheme} aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} theme`} title="Light theme suits projectors">
              {theme === "dark" ? <Sun size={15} aria-hidden="true" /> : <Moon size={15} aria-hidden="true" />}
            </button>
            {page !== "new" ? <a className="btn primary sm" href="#/new" aria-label="New run"><Plus size={14} aria-hidden="true" /><span className="hide-phone">New run</span></a> : null}
          </div>
        </header>
        <main id="main">{view}</main>
      </div>
    </div>
  );
}
