// Shapes returned by the Granite API (see /docs on the running server; server models: apps/api/granite_api/schemas.py).

export type Status = "ok" | "failed" | "error";

export interface Step { id: string; agent: string; kind: string; name: string }
export interface CheckDef { id: string; name: string; scope: string; step: string }
export interface Workflow { key: string; title: string; description: string; faults: string[]; steps: Step[]; checks: CheckDef[] }
export interface Example { order_id: string; email: string; message: string; label: string }
export interface TaskInput { message: string; email: string; order_id: string }

/** The suspect a finding leads with (confirmed by replay, else first-ranked) and its latest replay counts. */
export interface Lead {
  step_id: string; agent: string; status: string;
  fix_pass: number | null; fix_n: number | null; control_pass: number | null; control_n: number | null;
}
export interface FindingSummary {
  id: string; run_id: string; kind: string; severity: string; title: string; check_id: string | null;
  symptom_step: string; status: string; verification_level: string; created_at: string; lead?: Lead | null;
}
export interface RunSummary {
  id: string; workflow_key: string; status: string; llm_mode: string; model: string; seed: number;
  fault_type: string | null; task_input: TaskInput; error: string; created_at: string; finished_at: string | null;
  finding_count: number; failed_checks: number;
}

/**
 * A call a check made to the source of truth (for example the catalogue), with what it returned. The server shortens
 * very long arguments to a string ending in "...", so `arguments` is a list or that string.
 */
export interface TruthCall { function: string; arguments: unknown; returned: unknown }
/** How a check result was computed: the expression, the values it read and the source-of-truth calls. */
export interface Computation {
  expression?: string; tolerance?: number; value?: unknown; resolved?: Record<string, unknown>;
  truth_calls?: TruthCall[]; operands?: unknown[] | null;
}
export interface CheckResult {
  check_id: string; scope: string; step: string; type: string; severity: string; status: string;
  observed: unknown; expected: unknown; message: string; check_version?: number; computation?: Computation;
}
/** Per-step model settings recorded in the trace. `recorded: true` means a saved answer was replayed. */
export interface StepParams {
  provider?: string; recorded?: boolean; temperature?: number; max_tokens?: number; seed?: number; calls?: number;
  tokens_in?: number; tokens_out?: number; [key: string]: unknown;
}
export interface TraceStep {
  step_id: string; agent: string; kind: string; inputs: Record<string, unknown>;
  outputs: Record<string, unknown>; error: string | null;
  name?: string; reads?: string[]; model?: string | null; params?: StepParams | null; prompt_hash?: string | null;
  started_at?: string | null; ended_at?: string | null;
}
export interface TraceRun {
  final_output: Record<string, unknown>; external_id?: string | null; workflow?: string; runtime?: string; status?: string;
  task_input?: Record<string, unknown>; started_at?: string | null; ended_at?: string | null;
}
export interface Trace { steps: TraceStep[]; run: TraceRun; schema_version?: string }
export interface InjectedFault { fault_type: string; target_step: string; field_path: string; original_value: unknown; injected_value: unknown; note: string }
export interface RunDetail extends RunSummary {
  trace: Trace | null;
  trace_sha256: string | null; check_results: CheckResult[]; findings: FindingSummary[];
  injected_fault: InjectedFault | null;
}
export interface GraphNode { id: string; label: string; kind: string; status: Status; symptom?: boolean }
export interface GraphEdge { source: string; target: string; field: string }
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[] }

/** One hop of the recorded data-flow path from a suspected step to the symptom step. */
export interface PathHop { step_id: string; agent: string; carries?: string }
/** Evidence attached to a hypothesis: the provenance path, a check result, or a hand-off difference. */
export interface HypothesisEvidence {
  type: string; from?: string; to?: string; path?: PathHop[];
  check_id?: string; status?: string; observed?: unknown; expected?: unknown; computation?: Computation;
  read?: string; received?: unknown; produced_upstream?: unknown;
}
export interface Hypothesis {
  id: string; rank: number; step_id: string; agent: string; method: string; evidence_kind: string;
  score: number; rationale: string; status: string; can_verify: boolean; evidence?: HypothesisEvidence[];
}
/** Why a replay passed or not: target checks fixed, still failing, and checks it broke (regression guard). */
export interface Judgement { passed: boolean; fixed: string[]; still_failing: string[]; regressions: string[] }
export interface Replay {
  kind: string; idx: number; seed: number; completed: boolean; passed: boolean | null;
  judgement?: Judgement | null; final_output?: Record<string, unknown>;
}
export interface ExperimentSummary {
  k_pass: number; n_completed: number; n_planned: number; c_pass: number; m_completed: number; m_planned: number;
  ci_low: number; ci_high: number; verdict: string; explanation: string; rule_version: string;
}
/**
 * The correction applied in the fix replays: which step, which output fields, and where the value came from.
 * `source: "check"` means the value was taken from the failed check named in `derived_from` (no hand-written rule).
 */
export interface Intervention {
  step_id: string; patches: Record<string, unknown>; source: string; description: string; derived_from?: string[];
}
/** One suspect tried by an investigation, in ranked order. */
export interface Attempt {
  step_id: string; agent?: string; hypothesis_id?: string; status: "verified" | "skipped" | "not_reached";
  verdict?: string | null; replays_used: number; reason: string; experiment_id?: string | null;
}
/** Verified attribution in one action: suspects verified in order until one is confirmed or the budget is spent. */
export interface Investigation {
  id: string; finding_id: string; status: string; llm_mode: string; n: number; m: number; budget: number;
  replays_used: number; outcome: "confirmed" | "exhausted" | "no_candidate" | null; confirmed_step: string | null;
  attempts: Attempt[]; error: string; created_at: string; finished_at: string | null;
}
/** Counts for one condition of a Fault Lab batch ("none" is the clean condition). */
export interface BatchGroup { runs: number; finished: number; completed: number; errored: number; with_finding: number }
export interface Batch {
  id: string; workflow_key: string; status: string; llm_mode: string; faults: string[]; task_count: number; seed: number;
  created_at: string; finished_at: string | null; groups: Record<string, BatchGroup>; runs: RunSummary[];
}
/** A rate with its Wilson 95% interval, as the evaluation harness writes it. */
export interface Rate { k: number; n: number; rate: number | null; ci95: [number, number] }
export interface EvalMetrics {
  runs_completed?: Rate; detection?: Rate; detection_by_fault?: Record<string, Rate>; clean_runs_with_finding?: Rate;
  top1?: Record<string, Record<string, Rate | Record<string, Record<string, Rate>>>>; llm_judge_top1?: Rate;
  replays_per_investigation_full?: number | null;
  nondeterminism?: Record<string, Rate>;
}
export interface EvaluationSummary {
  id: string; date: string | null; mode: string | null; model: string | null; runs: number; complete: boolean;
  metrics: EvalMetrics;
}
export interface EvaluationMeta {
  date?: string; model?: string; mode?: string; prereg_sha256?: string; git_head?: string; git_dirty?: boolean;
  n_tasks?: number; faults?: string[]; levels?: Record<string, number>; n?: number; m?: number; budget?: number;
}
export interface EvaluationRow {
  order_id: string; fault: string; status: string; detected: boolean; origin?: string; symptom?: string;
  findings: string[]; llm_judge?: { answer: string | null };
  coverage?: { level: string; draw: number; answers: Record<string, string | null>; origin_check_kept: boolean }[];
}
export interface Evaluation { id: string; meta: EvaluationMeta; metrics: EvalMetrics; rows: EvaluationRow[] }
export interface Experiment {
  id: string; hypothesis_id: string; status: string; llm_mode: string; n: number; m: number; verdict: string | null;
  summary: ExperimentSummary | null; error: string; replays: Replay[];
  finding_id?: string; rule_version?: string; intervention?: Intervention | null; created_at?: string; finished_at?: string | null;
}
export interface Review { id: string; reviewer: string; decision: string; comment: string; to_status: string; created_at: string; from_status?: string }
export interface Evidence {
  id: string; type: string; title: string; sha256: string; hash_valid: boolean; payload: Record<string, unknown>;
  run_id?: string; finding_id?: string | null; reproduce?: string; created_at?: string;
}
export interface FindingDetail extends FindingSummary {
  detail: string; hypotheses: Hypothesis[]; experiments: Experiment[]; reviews: Review[]; evidence: Evidence[];
  allowed_actions: string[]; investigations?: Investigation[]; can_export_regression?: boolean;
}
export interface Job {
  id: string; status: string; progress_done: number; progress_total: number; message: string;
  kind?: string; target_id?: string; created_at?: string; finished_at?: string | null;
}
export interface Health { status: string; version: string; llm_mode: string; live_model_reachable: boolean; auth_required: boolean }
/** Number of findings in each lifecycle status (GET /findings/summary). */
export type FindingCounts = Record<string, number>;
/** A Phoenix or Langfuse project Granite imports traces from and writes verdicts to (keys stay on the server). */
export interface Connection {
  id: string; kind: "phoenix" | "langfuse"; name: string; base_url: string; project: string; workflow_key: string;
  profile: { steps?: Record<string, string> }; created_at: string; last_sync_at: string | null; last_error: string;
  keys_configured: boolean; imported_runs: number; exported_runs: number;
}
/** How a read between two steps was established when a trace was imported. */
export interface LineageEdge { read: string; step_id: string; tier: "declared" | "value" | "order" }
export interface TraceLink {
  connection_id: string; run_id: string; direction: "imported" | "exported"; external_trace_id: string;
  root_span_id: string; span_ids: Record<string, string>; lineage: LineageEdge[]; created_at: string;
}
export interface ImportResult {
  connection_id: string; fetched: number;
  imported: { trace_id: string; run_id: string; findings: number; lineage: string[]; status: string }[];
  skipped: { trace_id: string; reason: string }[];
}
export interface ExportResult { connection_id: string; run_id: string; trace_id: string; spans_sent: number; spans_total: number }
export interface WriteBackResult {
  finding_id: string; label: string; step_id: string | null; explanation: string;
  written: { connection_id: string; kind: string; span_id: string; ref: string }[];
}
