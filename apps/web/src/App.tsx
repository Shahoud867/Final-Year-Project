import { useState } from "react";
import { api, getToken, setToken } from "./api";
import { Badge } from "./components/ui";
import { useLoad, useRoute } from "./hooks";
import { FindingDetail } from "./pages/FindingDetail";
import { Guide } from "./pages/Guide";
import { Home } from "./pages/Home";
import { NewRun } from "./pages/NewRun";
import { RunDetail } from "./pages/RunDetail";

function Status() {
  const health = useLoad(() => api.health(), []);
  const [msg, setMsg] = useState("");
  const [token, setTok] = useState(getToken());
  const h = health.data;
  return (
    <div className="row small">
      {health.error && <Badge value="error" text="server unreachable" />}
      {h && <Badge value="completed" text={`server ok · ${h.llm_mode}${h.live_model_reachable ? " · model online" : ""}`} />}
      {h?.auth_required && (
        <input aria-label="Access token" type="password" placeholder="Access token" value={token} style={{ width: 150 }}
               onChange={(e) => { setTok(e.target.value); setToken(e.target.value); }} />
      )}
      <button onClick={async () => { try { setMsg((await api.testLlm()).message); } catch { setMsg("Could not reach the server."); } }}>Test model</button>
      {msg && <span role="status" className="muted">{msg}</span>}
    </div>
  );
}

export default function App() {
  const [page = "", id = ""] = useRoute();
  let view = <Home />;
  if (page === "new") view = <NewRun />;
  else if (page === "guide") view = <Guide />;
  else if (page === "runs" && id) view = <RunDetail id={id} key={id} />;
  else if (page === "findings" && id) view = <FindingDetail id={id} key={id} />;
  else if (page) view = <div className="card"><h1>Page not found</h1><p><a href="#/">Back to investigations</a></p></div>;
  const here = (p: string) => (page === p || (!page && p === "") ? "page" : undefined);
  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <header className="topbar">
        <div className="topbar-inner">
          <a className="brand" href="#/">Granite</a>
          <nav className="nav" aria-label="Main">
            <a href="#/" aria-current={here("")}>Investigations</a>
            <a href="#/new" aria-current={here("new")}>New run</a>
            <a href="#/guide" aria-current={here("guide")}>How it works</a>
          </nav>
          <span className="spacer" />
          <Status />
        </div>
      </header>
      <main id="main">{view}</main>
    </>
  );
}
