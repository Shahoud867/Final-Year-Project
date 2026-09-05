import { HashRouter, Route, Routes } from "react-router-dom";
import { Sidebar } from "./components/Sidebar";
import { Overview } from "./pages/Overview";
import { RunsList } from "./pages/RunsList";
import { RunDetailPage } from "./pages/RunDetail";
import { Evidence } from "./pages/Evidence";
import { ProductVision } from "./pages/ProductVision";
import { LiveDemo } from "./pages/LiveDemo";
import { Slides } from "./pages/Slides";

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
            <Route path="/product" element={<ProductVision />} />
            <Route path="/demo" element={<LiveDemo />} />
            <Route path="/slides" element={<Slides />} />
          </Routes>
        </div>
      </div>
    </HashRouter>
  );
}
