# Granite — Layman-to-Expert Knowledge Base

*Every concept a member must be able to explain and defend. Four levels each: L1 layman analogy · L2 undergraduate definition · L3 exactly how Granite uses it · L4 the likely panel question and the answer. Only concepts actually load-bearing for Granite are included.*

---

## 1. Multi-agent system (MAS)
**L1:** A relay team instead of a solo runner — several AI workers each do part of a job and pass results along. A dropped baton anywhere ruins the finish, even if the last runner is perfect.
**L2:** Multiple LLM-driven agents with distinct roles/prompts/tools, coordinated by an orchestrator, exchanging messages and tool results to complete a task no single call handles well.
**L3:** The *subject* of Granite, not just its tool: the systems being diagnosed are MAS built on CrewAI/LangGraph. Granite's own diagnosis pipeline is also multi-stage (inherited from ErrorProbe) — but the "multi-agent" in the title refers primarily to what is diagnosed.
**L4:** *"Why must the diagnosed system be multi-agent for this to be hard?"* — Because attribution is trivial with one agent (there's only one suspect) and hard with many: the error surfaces steps after it originates, downstream agents transform or mask it, and responsibility must be traced backward through dependencies. That gap is the entire field (Who&When → ErrorProbe).

## 2. Orchestration framework (CrewAI, LangGraph)
**L1:** The stage manager that decides which actor speaks when and hands them their props.
**L2:** Libraries defining agent roles, message routing, tool bindings, and control flow. CrewAI: role/task crews, largely sequential/hierarchical. LangGraph: explicit state graphs, natively supports cycles and checkpointing.
**L3:** The two committed instrumentation targets — chosen precisely because **no paper in the 7-paper corpus used either**, which is what makes the cross-architecture claim testable. LangGraph's native cycles force extension #3 (cyclic graphs); its native checkpointing makes it the first target for Recovery Controller.
**L4:** *"Why these two?"* — Absent from every prior benchmark (the generalization claim needs that), widely adopted (the product claim needs that), and architecturally different from each other (sequential-crew vs state-graph), so generalization across them means something.

## 3. Execution trace
**L1:** The flight recorder: everything every agent said, every tool it called, and what came back, in order.
**L2:** A time-ordered log of agent actions, messages, tool invocations and results, with identifiers linking steps.
**L3:** Granite's input. The SDK's instrumentation hooks capture a normalized trace schema from either framework; everything downstream consumes only that schema (this is what makes FR5's framework-agnosticism real). Spike 2 proved a CrewAI toy workflow maps cleanly; its post-hoc timestamps are a logged limitation — real per-step hooks are build work.
**L4:** *"What if the trace is incomplete?"* — TraceElephant's finding is exactly that fuller traces improve attribution (up to 76.5% relative); we control completeness because we own the instrumentation, and malformed/partial traces are named edge cases in the test plan.

## 4. Execution graph / DAG / cycles
**L1:** A family tree of the work: which step's output fed which later step.
**L2:** Nodes = agent actions/tool calls; directed edges = data/control dependencies. A DAG if no step ever feeds an earlier one; real frameworks (LangGraph) allow cycles (retry/refine loops).
**L3:** Built by **structural parsing of message/reference identifiers** (GraphTracer's approach) — deliberately *not* by asking an LLM what depended on what: deterministic, free, byte-identical under model swap. Cycles handled with a max-revisit bound; Spike 6's control run (bound disabled → hits the 10,000-step cap) proves the bound is load-bearing.
**L4:** *"Identifier parsing will miss implicit dependencies (an agent silently used context)."* — True; conceded. The graph captures explicit data flow; implicit-influence edges are a stated limitation, and the attribution stage's evidence-grounded verification (Investigator) exists partly to catch cases where the structural graph alone misleads.

## 5. Failure attribution (agent-level vs step-level)
**L1:** Not "the cake is bad" but "the person who mismeasured the flour, at minute six."
**L2:** Given a failed trace, output the responsible agent (agent accuracy) and the originating step (step accuracy). Step-level is far harder: Who&When's baselines ~14.2%, ErrorProbe 59.5%.
**L3:** Foundational items 3–4 (Culprit Agent, Error Step Localization = the Strategist stage's two outputs), confirmed by item 5 (Verification Agent = the Investigator stage) before commitment.
**L4:** *"Isn't agent-level basically solved?"* — Close to it (~60%+ across papers), which is why our lead metric and the field's admitted frontier is step-level — where ErrorProbe still errs 4-in-10 and where our delta is measured.

## 6. Silent failure / semantic error
**L1:** A confidently wrong answer: well-formatted, polite, no error message — and false. The scariest kind, because nothing beeps.
**L2:** An output that passes structural/anomaly checks (valid JSON, no exception, no taxonomy-recognizable misbehavior) but violates the task's actual requirements.
**L3:** RQ3's target and ErrorProbe's *confessed* blind spot — its pipeline is anomaly-gated, so a failure that raises no anomaly is invisible to it by construction. Granite's Semantic Error Diagnostic checks outputs against machine-checkable constraints derived from the task spec (numeric relations, required fields, tau-bench policy/action rules), with **zero LLM calls**, and **abstains** (reported coverage) where no checkable constraint exists. Spike 4: catches known-wrong values incl. a $20.00-vs-$19.75 near-miss, zero false positives.
**L4:** *"Rules can't understand meaning."* — Scoped claim; see deliverable 02 A6 verbatim. The one-liner: we detect *constraint violations*, which is the machine-checkable subset of semantic wrongness — precisely the subset the anomaly-gated SOTA misses — and we measure how much of the space that subset covers instead of pretending it's all of it.

## 7. MAST taxonomy / anomaly gating
**L1:** A checklist of "known ways agents misbehave." Anomaly-gated tools only investigate when something on the checklist trips.
**L2:** MAST: a published taxonomy of multi-agent failure modes. Anomaly gating: triggering diagnosis only on taxonomy-recognizable signals.
**L3:** The mechanism *behind* ErrorProbe's silent-failure blind spot — no signal, no diagnosis. Granite's constraint verifier runs unconditionally on the output, independent of any signal (FR3's exact wording).
**L4:** *"Why not just extend the taxonomy?"* — A taxonomy of observable misbehaviors can't enumerate outputs whose only defect is being false; checking against task ground-truth constraints is a different axis, not a longer checklist.

## 8. Fault injection & ground truth by construction
**L1:** A fire drill: we start a small, known fire so we can grade the alarm — because with real fires you're never sure where they started.
**L2:** Deterministically corrupting a chosen step (wrong tool output, swapped value, truncated context) so the true culprit/step is known with certainty, giving labeled data without human annotation.
**L3:** AgenTracer's own methodology, adopted; it removed the 30-hr/annotator labeling cost. Spikes 3/3b: first attempt (famous-fact corruption) got *self-corrected* by the agent — kept as a finding, so the benchmark records both blind propagation and self-correction. Fault taxonomy: 1 validated type now, 3 by extension #1.
**L4:** *"Injected faults aren't natural faults."* — Deliverable 02 A9 verbatim: field-standard method; realism from real substrates (tau-bench policies, GSM8K); injection is what makes accuracy measurable at all; limitation stated in the evaluation plan.

## 9. Benchmark / baseline / reproduction
**L1:** Benchmark = the exam. Baseline = the current top student's score. Reproduction = re-marking their paper yourself before claiming you beat them.
**L2:** Benchmark: fixed labeled dataset + protocol. Baseline: the comparator method/number. Reproduction: reimplementing the published method and confirming its number under your conditions — required for a fair head-to-head.
**L3:** Who&When (184 cases, MIT, in hand) for reproduction; TracerTraj **correctly downgraded** after a direct download check showed it unreleased (R11) — a genuine integrity moment worth telling. Our own benchmark (floor 500 / stretch 1,000 traces) is the new contribution, MIT/CC-BY, with a static leaderboard as extension #13.
**L4:** *"What if you can't reach 59.5%?"* — Deliverable 02 A3: declared band; Annex A.2 transparent-reporting fallback; both numbers published either way; the cross-architecture and silent-failure results ride on our controlled implementation regardless.

## 10. ErrorProbe's pipeline (Strategist / Investigator / Arbiter + Verified Episodic Memory)
**L1:** A detective team: one proposes suspects, one checks the proposals against the actual evidence, one delivers the verdict — and the team keeps a casebook of confirmed findings.
**L2:** Stage 1 hypothesizes (agent, step); stage 2 verifies hypotheses against trajectory evidence (tool-grounded); stage 3 arbitrates; a memory of *verified* diagnostic conclusions improves later cases. 59.5% step acc. on Who&When-Algo with Claude 3.7 Sonnet.
**L3:** Adopted as the attribution core (items 3–5 are its three stages, named separately after supervisor feedback), reimplemented from the paper (no confirmed code license). **Naming caution:** ErrorProbe's *Verified Episodic Memory* stores diagnosis evidence and is part of the *baseline reproduction*; Granite's *Verified Repair Memory* (item 10) stores error→repair patterns and is a different, Granite-side mechanism.
**L4:** *"Isn't your item #10 just ErrorProbe's memory renamed?"* — No: different content (repairs, not diagnoses), different position (after verification-gated repair, not inside attribution), different purpose (reuse of fixes). And its honest status: one prior test failed on a 3B backbone; re-test gated at Mid-1.

## 11. Counterfactual reasoning & controlled replay
**L1:** "If we'd measured the flour right, would the cake have worked?" — actually re-baking from that step to find out, instead of guessing.
**L2:** Evaluating a cause by substituting the hypothesized correct value at the suspect step and re-executing downstream to observe whether the outcome recovers. Causal evidence, not correlation.
**L3:** *Verified Automatic Repair* (item 8): frozen upstream context, corrected value at the fault point, downstream re-executed under a **controlled protocol** — pinned decoding parameters (temp 0), recovery rate over N replays with variance; fully deterministic for non-LLM computation (Spike 5: 97.2 → 108.0 recovered). "Verified" = the recovery rate was measured before the fix is trusted.
**L4:** *"LLMs aren't deterministic — your replay proves nothing."* — Deliverable 02 A7 verbatim: the *protocol* is deterministic; residual model variance is measured, not ignored, and a fix accepted only on measured recovery rate is exactly the right response to nondeterminism.

## 12. Repair generation vs repair verification vs recovery vs memory (the closed loop)
**L1:** Propose the fix → prove the fix works → patch and continue from where you were → write the fix in the team playbook.
**L2:** Four separable mechanisms; conflating them is how systems end up "self-modifying" unsafely. Verification-gated acceptance is the safety property.
**L3:** Items 6 (Repair Agent, LLM-generated targeted correction: prompt / tool arg / structured output / small function — Spike 8: 4/6, both misses one interface-spec cause: model returned the *derived result* instead of the *corrected parameter*; the real interface pins the atomic field), 8 (verification via controlled replay), 9 (Recovery Controller: resume from checkpoint at the verified repair point — **no PoC yet**, LangGraph-first plan, Mid-1 gate), 10 (Verified Repair Memory — failed first test, Mid-1 re-test gate).
**L4:** *"Why not just auto-retry?"* — Considered and rejected on record: unconditional retry contradicts the confidence-gating principle; retry only fires on a verified, threshold-passing fix — a *behavior* of items 8+ext.4, not a feature.

## 13. Checkpointing
**L1:** Save points in a video game — resume from the save, not from the start screen.
**L2:** Persisting workflow state at step boundaries so execution can resume from an intermediate point. LangGraph ships it natively; 5/7 surveyed frameworks have some form.
**L4/L3:** Granite ties resumption to the *verified repair point* specifically — the survey's matrix shows no framework does that natively. Panel: *"So you're just wrapping LangGraph's checkpointer?"* — The checkpointer is infrastructure (core-assist/support); the contribution is the policy layer: which checkpoint is safe given the diagnosis, what state must be patched, and the measured re-execution-cost saving vs restart (a metric deliberately *not* claimed until this exists).

## 14. Precision / recall / coverage / F1
**L1:** Precision: when the alarm rings, how often is there a real fire? Recall: of all real fires, how many rang the alarm? Coverage: in how many buildings is the alarm even installed?
**L2:** P = TP/(TP+FP); R = TP/(TP+FN); F1 their harmonic mean; coverage/abstention = fraction of cases the detector is applicable to at all.
**L3:** Silent-failure detection reports P **and** R (the register's own 08-24 correction: recall alone can't distinguish a detector from one that flags everything) **and coverage** (the audit's addition: rules abstain where no constraint exists). Propagation-path F1 scores the traced path against the injected ground-truth path.
**L4:** *"High precision on 3 cases means nothing."* — Agreed; Spike 4 is a mechanism validation, and the statistical claim waits for the benchmark's hundreds of injected cases, where P/R/coverage have denominators that mean something.

## 15. Calibration (reliability diagram, Brier score)
**L1:** When the forecaster says 80% rain, does it rain 8 times in 10? A confident liar and an honest forecaster both say "80%" — calibration tells them apart.
**L2:** Comparing stated confidence to empirical frequency; reliability diagram bins predictions by confidence; Brier score = mean squared error of probabilistic predictions.
**L3:** Extension #4: publish the diagnosis engine's calibration curve + Brier score. This is what makes the confidence-gated fix approval (ext. #12) *meaningful* — a gate on an uncalibrated confidence is theater.
**L4:** *"Why does calibration matter more than accuracy here?"* — Because the product's safety story is "humans review low-confidence output"; that only protects anyone if confidence tracks correctness.

## 16. Ablation study
**L1:** Take one ingredient out of the recipe and re-taste — now you know what that ingredient did.
**L2:** Re-running the evaluation with one component disabled to attribute performance to components.
**L3:** Two committed: verification-gate ablation (yields **false-repair rate** — the metric that keeps "verified" honest) and, if VRM's re-test fails, memory-on/off (which converts a failed feature into an evaluation contribution).
**L4:** *"Which ablation matters most?"* — The verification gate: it directly measures the harm the system would cause without its own safety mechanism.

## 17. Cross-architecture generalization
**L1:** A mechanic trained only on Toyotas, handed a Honda. If the skill was real diagnosis, it transfers; if it was Toyota memorization, it doesn't.
**L2:** Evaluating a method on systems structurally different from those used in its development/benchmark construction; the gap between in-distribution and transfer performance measures overfitting to an ecosystem.
**L3:** RQ2, the lead research claim: no paper in the corpus has run this measurement; Granite runs ErrorProbe-method attribution on CrewAI/LangGraph traces it was never tuned for, against its home-turf Who&When numbers. This is why the single-framework scope advice was rejected (R19).
**L4:** *"Maybe it transfers trivially and your result is boring."* — Then that is a valuable, publishable negative-space finding ("attribution is architecture-robust") and the benchmark that established it remains the contribution; the claim was pre-registered either way.

## 18. Complex Computing Problem (Seoul Accord)
**L1:** The accreditation's bar for "worthy of a computing degree's final project": no copy-paste solution exists; real trade-offs; real consequences.
**L2:** Seoul Accord D.4.1's three tiers (well-defined / broadly-defined / complex); a credible claim rests on several evidenced characteristics of nine, centrally — not one, not manufactured.
**L3:** Granite claims 8 clear + 1 (stakeholders) upgraded by contact evidence; characteristic 9's resolution paragraph (three unknowns → three pipeline stages → PoC evidence) is the exemplar answer.
**L4:** *"Which characteristic is your weakest?"* — Answer honestly: #6 was, and here is the contact evidence that changed it; a short honest list defends better than nine asserted ones (the guide says exactly this).

## 19. Stream A, delta, and core-assist
**L1:** Stream A: the idea starts from a published paper. Delta: what you add beyond it. Core-assist: a tool you use that helps with the hard part — allowed, as long as it isn't itself the whole answer.
**L2:** Guide §1.1, Annex A.2, §14. The forbidden category is core-*replacement*: the external component supplying the claimed contribution itself.
**L3:** Delta = integration into an operable system + adaptation to new architectures + constraint-driven engineering (A.2's own categories). The LLM is classified core-assist with a per-component mechanism table proving the differentiators (graph, tracing, scoring, SED) never call it — the replacement test passes *byte-identically*, not just "still runs."
**L4:** *"If I swap your LLM for another, what survives?"* — Every 0%-API row unchanged to the byte; attribution accuracy may shift (reported per-backbone, as ErrorProbe itself does across its 3 backbones); the benchmark, verifier, replay protocol, and SDK are untouched.

## 20. AI-assisted development (Level 2) and the ownership standard
**L1:** You may use power tools; you must still be the carpenter — able to explain, justify, predict, and modify every joint you claim.
**L2:** Guide §8: FYPs run at AI-*assisted*, not AI-*led*; §14.1's four questions define ownership; disclosure via the AI usage log is protective, not incriminating.
**L3:** The log exists and is specific (40KB, activity-level entries); each member's slide-10 subsystem maps to spikes they can walk through without notes.
**L4:** *"How much of this did you actually write?"* — "The log answers that per activity; the test the guide applies is not keystrokes but the four ownership questions — ask me any of them about my subsystem now." Then take the question.
