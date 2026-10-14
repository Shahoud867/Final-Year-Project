import { Check, Minus, X } from "lucide-react";
import { pct } from "../format";
import { CONFIRM_MIN_RATE, REFUTE_MAX_RATE } from "../lib/vr1";
import type { Replay } from "../types";

const word = (r: Replay | undefined): string => (!r || !r.completed || r.passed === null ? "not finished" : r.passed ? "correct" : "still wrong");

/**
 * One mark per planned replay of a kind ("intervention" = with the fix, "control" = without it). A mark is filled only
 * by a replay the server has stored, so during a running experiment the row fills in as real results arrive.
 */
export function ReplayDots({ replays, kind, planned, label }: { replays: Replay[]; kind: "intervention" | "control"; planned: number; label: string }) {
  const mine = replays.filter((r) => r.kind === kind);
  const name = kind === "control" ? "control" : "fix";
  const count = Math.max(planned, mine.length);
  if (count === 0) return <span className="dim small">none requested</span>;
  return (
    <ul className="replay-dots" aria-label={label}>
      {Array.from({ length: count }, (_, i) => {
        const r = mine.find((x) => x.idx === i);
        const state = !r || !r.completed || r.passed === null ? "pending" : r.passed ? "pass" : "fail";
        const text = `${name} ${i + 1}: ${word(r)}${r ? `, seed ${r.seed}` : ""}`;
        return (
          <li key={i}>
            <span className={`replay-dot ${state}${kind === "control" ? " control" : ""}`} role="img" aria-label={text} title={text}>
              {state === "pass" ? <Check size={12} aria-hidden="true" /> : state === "fail" ? <X size={12} aria-hidden="true" /> : <Minus size={12} aria-hidden="true" />}
            </span>
          </li>
        );
      })}
    </ul>
  );
}

const left = (x: number) => `${Math.min(100, Math.max(0, x * 100))}%`;

/**
 * Rates on a 0 to 100% axis against the two VR-1 thresholds: the share of fix replays that came out correct (with its
 * 95% Wilson interval), and the share of controls that did. Pass the numbers of a real experiment, or of the explorer.
 */
export function RateAxis({ fix, control, ciLow, ciHigh }: { fix: number | null; control: number | null; ciLow?: number; ciHigh?: number }) {
  const hasCi = fix !== null && ciLow !== undefined && ciHigh !== undefined;
  const said = [
    fix === null ? "No fix replay finished" : `Fix replays correct ${pct(fix)}`,
    hasCi ? `95% interval ${pct(ciLow)} to ${pct(ciHigh)}` : "",
    control === null ? "no control rate" : `control replays correct ${pct(control)}`,
    `thresholds at ${pct(REFUTE_MAX_RATE)} and ${pct(CONFIRM_MIN_RATE)}`,
  ].filter(Boolean).join("; ");
  return (
    <div className="rate">
      <div className="rate-track" role="img" aria-label={said}>
        <div className="rate-plot">
          <span className="rate-zone refute" style={{ width: left(REFUTE_MAX_RATE) }} />
          <span className="rate-zone confirm" style={{ width: left(1 - CONFIRM_MIN_RATE) }} />
          <span className="rate-line" style={{ left: left(REFUTE_MAX_RATE) }} />
          <span className="rate-line" style={{ left: left(CONFIRM_MIN_RATE) }} />
          {hasCi ? <span className="rate-ci" style={{ left: left(ciLow), width: left(ciHigh - ciLow) }} /> : null}
          {control !== null ? <span className="rate-mark control" style={{ left: left(control) }} /> : null}
          {fix !== null ? <span className="rate-mark" style={{ left: left(fix) }} /> : null}
        </div>
      </div>
      <div className="rate-scale" aria-hidden="true">
        <span style={{ left: 0 }}>0%</span>
        <span style={{ left: left(REFUTE_MAX_RATE) }}>{pct(REFUTE_MAX_RATE)}</span>
        <span style={{ left: left(CONFIRM_MIN_RATE) }}>{pct(CONFIRM_MIN_RATE)}</span>
        <span style={{ left: "100%" }}>100%</span>
      </div>
      <div className="rate-key">
        <span><i />fix replays correct{fix !== null ? ` ${pct(fix)}` : ": n/a"}</span>
        <span><i className="control" />controls correct{control !== null ? ` ${pct(control)}` : ": n/a"}</span>
        {hasCi ? <span><i className="ci" />95% interval {pct(ciLow)} to {pct(ciHigh)}</span> : null}
      </div>
    </div>
  );
}
