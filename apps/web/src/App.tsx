import { BookOpen, ChevronRight, FileCode2, FlaskConical, GitBranch, GitCommitHorizontal, Moon, Mountain, Plus, Radar, ShieldCheck, Sun } from "lucide-react";
import { useEffect, useState } from "react";
import { api, getToken, setToken } from "./api";
import { Card, ModeBadge } from "./components/ui";
import type { Icon } from "./components/ui";
import { BUILD, commitUrl, repoUrl } from "./delivery";
import { useLoad, useRoute, useTheme } from "./hooks";
import { Evidence } from "./pages/Evidence";
import { FindingDetail } from "./pages/FindingDetail";
import { Guide } from "./pages/Guide";
import { Home } from "./pages/Home";
import { NewRun } from "./pages/NewRun";
import { RunDetail } from "./pages/RunDetail";
import type { Health } from "./types";

const NAV: { route: string; href: string; label: string; icon: Icon }[] = [
  { route: "", href: "#/", label: "Investigations", icon: Radar },
  { route: "new", href: "#/new", label: "Task Studio", icon: FlaskConical },
  { route: "guide", href: "#/guide", label: "How it works", icon: BookOpen },
  { route: "evidence", href: "#/evidence", label: "Evidence", icon: ShieldCheck },
];
const SECTION: Record<string, string> = { "": "Investigations", new: "Task Studio", guide: "How it works", evidence: "Evidence", runs: "Investigations", findings: "Investigations" };

function Brand() {
  return (
    <a className="brand" href="#/">
      <span className="brand-mark"><Mountain size={16} aria-hidden="true" /></span>
      <span className="brand-text"><span className="brand-name">Granite</span><span className="brand-tag">find · prove · verify</span></span>
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
  else if (page === "guide") view = <Guide />;
  else if (page === "evidence") view = <Evidence />;
  else if (page === "runs" && id) view = <RunDetail id={id} key={id} />;
  else if (page === "findings" && id) view = <FindingDetail id={id} key={id} />;
  else if (page) view = <Card><h1>Page not found</h1><p className="muted"><a href="#/">Back to investigations</a></p></Card>;

  const section = SECTION[page] ?? "Not found";
  const exact = (route: string) => (page === route && !id ? "page" : undefined);
  const within = (route: string) => route === "" && (page === "runs" || page === "findings");
  return (
    <div className="shell">
      <a className="skip" href="#main">Skip to content</a>
      <aside className="sidebar">
        <Brand />
        <nav className="nav" aria-label="Main">
          {NAV.map((n) => (
            <a key={n.route} href={n.href} aria-current={exact(n.route)} data-active={within(n.route) || undefined}>
              <n.icon size={16} aria-hidden="true" /><span>{n.label}</span>
            </a>
          ))}
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
