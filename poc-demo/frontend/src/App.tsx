import { HashRouter, Route, Routes } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { Overview } from "./pages/Overview";
import { RunsList } from "./pages/RunsList";
import { RunDetailPage } from "./pages/RunDetail";
import { Evidence } from "./pages/Evidence";

export function App() {
  return (
    <HashRouter>
      <div className="app-shell">
        <Sidebar />
        <div className="main-column">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/runs" element={<RunsList />} />
            <Route path="/runs/:id" element={<RunDetailPage />} />
            <Route path="/runs/:id/:tab" element={<RunDetailPage />} />
            <Route path="/evidence" element={<Evidence />} />
          </Routes>
        </div>
      </div>
    </HashRouter>
  );
}
