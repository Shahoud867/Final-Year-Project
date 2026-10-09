// Shapes returned by the Granite API (see /docs on the running server).

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
export interface CheckResult {
  check_id: string; scope: string; step: string; type: string; severity: string; status: string;
  observed: unknown; expected: unknown; message: string;
}
export interface TraceStep {
  step_id: string; agent: string; kind: string; inputs: Record<string, unknown>;
  outputs: Record<string, unknown>; error: string | null;
}
export interface InjectedFault { fault_type: string; target_step: string; field_path: string; original_value: unknown; injected_value: unknown; note: string }
export interface RunDetail extends RunSummary {
  trace: { steps: TraceStep[]; run: { final_output: Record<string, unknown> } } | null;
  trace_sha256: string | null; check_results: CheckResult[]; findings: FindingSummary[];
  injected_fault: InjectedFault | null;
}
export interface GraphNode { id: string; label: string; kind: string; status: Status; symptom?: boolean }
export interface GraphEdge { source: string; target: string; field: string }
export interface Graph { nodes: GraphNode[]; edges: GraphEdge[] }

export interface Hypothesis {
  id: string; rank: number; step_id: string; agent: string; method: string; evidence_kind: string;
  score: number; rationale: string; status: string; can_verify: boolean;
}
export interface Replay { kind: string; idx: number; seed: number; completed: boolean; passed: boolean | null }
export interface ExperimentSummary {
  k_pass: number; n_completed: number; n_planned: number; c_pass: number; m_completed: number; m_planned: number;
  ci_low: number; ci_high: number; verdict: string; explanation: string; rule_version: string;
}
export interface Experiment {
  id: string; hypothesis_id: string; status: string; llm_mode: string; n: number; m: number; verdict: string | null;
  summary: ExperimentSummary | null; error: string; replays: Replay[];
}
export interface Review { id: string; reviewer: string; decision: string; comment: string; to_status: string; created_at: string }
export interface Evidence { id: string; type: string; title: string; sha256: string; hash_valid: boolean; payload: Record<string, unknown> }
export interface FindingDetail extends FindingSummary {
  detail: string; hypotheses: Hypothesis[]; experiments: Experiment[]; reviews: Review[]; evidence: Evidence[];
  allowed_actions: string[];
}
export interface Job { id: string; status: string; progress_done: number; progress_total: number; message: string }
export interface Health { status: string; version: string; llm_mode: string; live_model_reachable: boolean; auth_required: boolean }
