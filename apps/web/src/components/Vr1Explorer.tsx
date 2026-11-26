import { useState } from "react";
import { label } from "../format";
import { CONFIRM_MIN_RATE, CONTROL_MAX_RATE, DEFAULT_CONTROLS, DEFAULT_REPLAYS, MAX_CONTROLS, MAX_REPLAYS, REFUTE_MAX_RATE, decide, wilson } from "../lib/vr1";
import { RateAxis } from "./Replay";
import { Badge } from "./ui";

const clamp = (v: number, lo: number, hi: number) => (Number.isFinite(v) ? Math.min(hi, Math.max(lo, Math.round(v))) : lo);

/**
 * Try rule VR-1 on counts of your own. This is an explanation, not a result: the numbers are typed here and the
 * verdict is computed in the browser from the published rule. Real verdicts are decided by the server.
 */
export function Vr1Explorer() {
  const [n, setN] = useState(DEFAULT_REPLAYS);
  const [k, setK] = useState(DEFAULT_REPLAYS);
  const [m, setM] = useState(DEFAULT_CONTROLS);
  const [c, setC] = useState(0);
  const kk = Math.min(k, n), cc = Math.min(c, m);
  const verdict = decide(kk, n, cc, m);
  const [lo, hi] = wilson(kk, n);
  const num = (id: string, text: string, value: number, min: number, max: number, set: (v: number) => void) => (
    <div className="field">
      <label htmlFor={id}>{text}</label>
      <input id={id} type="number" className="mono" min={min} max={max} step={1} value={value} onChange={(e) => set(clamp(e.target.valueAsNumber, min, max))} />
    </div>
  );
  return (
    <div className="vr1x">
      <div className="vr1x-inputs">
        {num("vx-n", "Fix replays (N)", n, 1, MAX_REPLAYS, setN)}
        {num("vx-k", "Correct with the fix", kk, 0, n, setK)}
        {num("vx-m", "Controls (M)", m, 0, MAX_CONTROLS, setM)}
        {num("vx-c", "Controls correct", cc, 0, m, setC)}
      </div>
      <div className="vr1x-out" aria-live="polite">
        <div className="row"><span className="eyebrow">Verdict under VR-1</span><Badge value={verdict} large text={label(verdict)} /></div>
        <RateAxis fix={kk / n} control={m > 0 ? cc / m : null} ciLow={lo} ciHigh={hi} />
        <p className="small muted">
          Confirmed needs at least {CONFIRM_MIN_RATE * 100}% of fix replays correct and at most {CONTROL_MAX_RATE * 100}% of controls correct. Refuted
          means at most {REFUTE_MAX_RATE * 100}% of fix replays correct. Anything between is inconclusive.
        </p>
      </div>
      <p className="small dim vr1x-note">Explorer: computed in your browser from the published rule. Real verdicts are computed by the server and shown on the finding.</p>
    </div>
  );
}
