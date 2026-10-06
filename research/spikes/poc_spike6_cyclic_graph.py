"""
POC Spike 6 — Cyclic/dynamic graph support (extension #3 in the frozen 14)

Real risk this tests: backward causal tracing (spike 2 / the core attribution
algorithm) was only ever tested on a simple 3-node DAG. LangGraph — one of the
two committed core architectures — natively supports cyclic workflows (retry
loops, iterative refinement). Without cycle handling, backward tracing could
infinite-loop the moment it hits a real LangGraph trace with a loop in it.

This spike builds a small graph WITH a real cycle (simulating a retry loop:
Researcher -> Critic -> Researcher, i.e. the Critic sends work back for
another pass, then eventually exits to a Writer), and tests whether a
bounded backward traversal (max-revisit-per-node) terminates correctly and
still visits every relevant node, instead of hanging.
"""

import json
import networkx as nx

def build_looped_trace():
    """
    Planner -> Researcher -> Critic -> Researcher (retry loop, x2) -> Writer -> FAILURE
    The loop: Researcher and Critic exchange twice before Critic approves and
    hands off to Writer, where the final failure is observed.
    """
    g = nx.DiGraph()
    edges = [
        ("Planner", "Researcher_pass1"),
        ("Researcher_pass1", "Critic_pass1"),
        ("Critic_pass1", "Researcher_pass2"),   # retry edge back into Researcher
        ("Researcher_pass2", "Critic_pass2"),
        ("Critic_pass2", "Writer"),
        ("Writer", "FAILURE"),
    ]
    g.add_edges_from(edges)
    return g


def build_TRUE_cyclic_trace():
    """
    A harder case: an actual cycle in the graph itself (not just two passes
    of a linearly-unrolled loop) — Researcher and Critic point back at the
    *same* two nodes repeatedly, which is what a real execution-graph model
    would look like if nodes are keyed by agent role rather than by
    invocation instance.
    """
    g = nx.DiGraph()
    g.add_edge("Planner", "Researcher")
    g.add_edge("Researcher", "Critic")
    g.add_edge("Critic", "Researcher")   # <-- real cycle: Researcher <-> Critic
    g.add_edge("Critic", "Writer")
    g.add_edge("Writer", "FAILURE")
    return g


def bounded_backward_trace(graph, start_node, max_revisits_per_node=3):
    """
    The mechanism under test: BFS backward from the failure node through
    predecessors, with a per-node revisit cap so a real cycle can't cause
    an infinite loop. Returns (visited_order, terminated_cleanly).
    """
    visit_counts = {}
    visited_order = []
    queue = [start_node]
    steps = 0
    max_steps = 10_000  # hard safety cap in case the bound logic itself is broken

    while queue:
        steps += 1
        if steps > max_steps:
            return visited_order, False  # did NOT terminate cleanly

        node = queue.pop(0)
        visit_counts[node] = visit_counts.get(node, 0) + 1
        visited_order.append(node)

        if visit_counts[node] > max_revisits_per_node:
            continue  # bound hit for this node, don't expand its predecessors again

        for pred in graph.predecessors(node):
            queue.append(pred)

    return visited_order, True


if __name__ == "__main__":
    results = {}

    # Case A: unrolled retry loop (no true cycle, but tests the realistic shape)
    g_unrolled = build_looped_trace()
    order_a, clean_a = bounded_backward_trace(g_unrolled, "FAILURE")
    results["case_a_unrolled_retry"] = {
        "nodes_in_graph": list(g_unrolled.nodes()),
        "has_true_cycle": not nx.is_directed_acyclic_graph(g_unrolled),
        "traversal_terminated_cleanly": clean_a,
        "visited_order": order_a,
        "all_nodes_reached": set(order_a) == set(g_unrolled.nodes()),
    }

    # Case B: a real cycle (Researcher <-> Critic)
    g_cyclic = build_TRUE_cyclic_trace()
    order_b, clean_b = bounded_backward_trace(g_cyclic, "FAILURE", max_revisits_per_node=3)
    results["case_b_true_cycle"] = {
        "nodes_in_graph": list(g_cyclic.nodes()),
        "has_true_cycle": not nx.is_directed_acyclic_graph(g_cyclic),
        "traversal_terminated_cleanly": clean_b,
        "visited_order": order_b,
        "all_nodes_reached": set(order_b) == set(g_cyclic.nodes()),
        "revisit_count_researcher": order_b.count("Researcher"),
        "revisit_count_critic": order_b.count("Critic"),
    }

    # Control: what happens with NO bound at all, on the true-cycle graph
    # (expected: this should hang / hit the safety cap, proving the bound is
    # actually load-bearing and not just a no-op)
    order_c, clean_c = bounded_backward_trace(g_cyclic, "FAILURE", max_revisits_per_node=10**9)
    results["control_unbounded_on_true_cycle"] = {
        "traversal_terminated_cleanly": clean_c,
        "steps_before_safety_cap": len(order_c),
        "note": "Expected False / hit the 10,000-step safety cap — confirms the "
                "revisit bound is doing real work, not passing by coincidence.",
    }

    print(json.dumps(results, indent=2))
    with open("poc_spike6_output.json", "w") as f:
        json.dump(results, f, indent=2)
