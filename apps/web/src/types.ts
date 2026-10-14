// Shapes returned by the Granite API (see /docs on the running server; server models: apps/api/granite_api/schemas.py).

export type Status = "ok" | "failed" | "error";

export interface Step { id: string; agent: string; kind: string; name: string }
export interface CheckDef { id: string; name: string; scope: string; step: string }
export interface Workflow { key: string; title: string; description: string; faults: string[]; steps: Step[]; checks: CheckDef[] }
export interface Example { order_id: string; email: string; message: string; label: string }
export interface TaskInput { message: string; email: string; order_id: string }

export interface FindingSummary {
  id: string; run_id: string; kind: string; severity: string; title: string; check_id: string | null;
  symptom_step: string; status: string; verification_level: string; created_at: string;
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
/** The correction applied in the fix replays: which step, which output fields, and where the value came from. */
export interface Intervention { step_id: string; patches: Record<string, unknown>; source: string; description: string }
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
  allowed_actions: string[];
}
export interface Job {
  id: string; status: string; progress_done: number; progress_total: number; message: string;
  kind?: string; target_id?: string; created_at?: string; finished_at?: string | null;
}
export interface Health { status: string; version: string; llm_mode: string; live_model_reachable: boolean; auth_required: boolean }
/** Number of findings in each lifecycle status (GET /findings/summary). */
export type FindingCounts = Record<string, number>;
