export type RunStatus =
  | "attributed_correct"
  | "attributed_partial"
  | "attributed_incorrect"
  | "clean_no_fault"
  | "self_corrected"
  | "fault_propagated"
  | "repaired_verified"
  | "repair_failed"
  | "cyclic_bounded"
  | "classified_correct"
  | "classified_incorrect";

export interface RunSummary {
  id: string;
  spike: string;
  scenario: string;
  framework: string;
  question: string;
  status: RunStatus;
  confidence: number | null;
  has_fault: boolean;
  has_repair: boolean;
  has_sed: boolean;
  has_classifier: boolean;
}

export interface GraphNode {
  id: string;
  agent: string;
  role: string;
  label: string;
  is_culprit?: boolean;
  is_fault_injected?: boolean;
}

export interface GraphEdge {
  from: string;
  to: string;
}

export interface Graph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface Attribution {
  gt_agent: string | null;
  gt_step: string | number | null;
  pred_agent: string | null;
  pred_step: string | number | null;
  confidence: number | null;
  agent_correct: boolean | null;
  step_correct_as_scored: boolean | null;
  step_correct_type_safe: boolean | null;
  hypotheses: { step: number; agent: string; reason: string }[];
}

export interface SedData {
  correct_answer: number;
  stated_answer: number;
  verdict: string;
  model_was_actually_wrong: boolean;
  structurally_normal: boolean;
}

export interface FaultData {
  type: string;
  origin_node: string;
  true_value: string;
  corrupted_value: string;
  propagation_verdict: string;
}

export interface RepairData {
  candidate_value: number | string;
  reasoning: string;
  exact_match: boolean;
  repair_success: boolean;
}

export interface ReplayData {
  before: number | null;
  after: number | null;
  expected: number | null;
  recovery_success: boolean;
  n_replays: number;
}

export interface ClassifierData {
  true_label: "clean" | "corrupted";
  predicted_label: "clean" | "corrupted";
  correct: boolean;
  method: string;
}

export interface RunDetail extends RunSummary {
  final_answer: string | null;
  graph: Graph;
  attribution: Attribution | null;
  sed: SedData | null;
  fault: FaultData | null;
  repair: RepairData | null;
  replay: ReplayData | null;
  classifier: ClassifierData | null;
  ground_truth_note: string | null;
  elapsed_sec: number | null;
}

export interface SpikeMeta {
  id: string;
  name: string;
  n_cases: number;
  result: string;
}

export interface Stats {
  agent_accuracy_mean: number;
  agent_accuracy_min: number | null;
  agent_accuracy_max: number | null;
  step_accuracy_mean: number;
  step_accuracy_min: number | null;
  step_accuracy_max: number | null;
  n_reproduction_runs: number;
  reproduction_bug_fixed: boolean;
  reproduction_bug_note: string;
  agent_accuracy: number;
  step_accuracy_raw: number;
  step_accuracy_type_safe: number;
  step_accuracy_discrepancy_flag: boolean;
  n_reproduction_cases: number;
  sed_natural_failures_observed: number;
  sed_note: string;
  recovery_rate_n: number;
  recovery_success: boolean;
  repair_success_rate: number;
  repair_exact_match_rate: number;
  repair_n_cases: number;
  cyclic_cases_bounded: number;
  cyclic_cases_total: number;
  preventive_classifier: {
    n_total: number;
    n_test: number;
    precision: number;
    recall: number;
    f1: number;
    honest_caveat: string;
  };
  total_runs: number;
  n_spikes: number;
  spikes: SpikeMeta[];
}
