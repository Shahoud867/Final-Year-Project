// Real API payloads captured from a local Granite server in recorded mode (2026-10-13): the first example task with
// the stale-price fault, the same task clean, the cancelled-order edge case, an errored run, and the finding of the
// first run before and after two verifications (Refund Calculator refuted, Order Lookup confirmed).
// Regenerate by replaying those requests against a running server; do not edit values by hand.
import type { Example, FindingDetail, Graph, Health, RunDetail, Workflow } from "../src/types";

export const health: Health = {
 "status": "ok",
 "version": "0.1.0",
 "llm_mode": "recorded",
 "live_model_reachable": false,
 "auth_required": false
};

export const workflows: Workflow[] = [
 {
  "key": "refund_desk",
  "title": "Refund Desk",
  "description": "Five-step customer-support refund workflow on synthetic tau-bench retail data.",
  "faults": [
   "stale_price"
  ],
  "steps": [
   {
    "id": "s1",
    "agent": "Intake",
    "kind": "llm",
    "name": "extract order and items"
   },
   {
    "id": "s2",
    "agent": "Order Lookup",
    "kind": "tool",
    "name": "get_order_details"
   },
   {
    "id": "s3",
    "agent": "Policy",
    "kind": "code",
    "name": "decide eligibility"
   },
   {
    "id": "s4",
    "agent": "Refund Calculator",
    "kind": "llm",
    "name": "compute refund"
   },
   {
    "id": "s5",
    "agent": "Writer",
    "kind": "llm",
    "name": "write customer message"
   }
  ],
  "checks": [
   {
    "id": "CHK-OUT-1",
    "name": "Stated refund equals the catalogue total of the refunded items",
    "scope": "outcome",
    "step": "s5"
   },
   {
    "id": "CHK-OUT-2",
    "name": "Refund decision follows policy (delivered order owned by the customer)",
    "scope": "outcome",
    "step": "s3"
   },
   {
    "id": "CT-INTAKE",
    "name": "Intake kept the order id and found items",
    "scope": "step",
    "step": "s1"
   },
   {
    "id": "CT-LOOKUP",
    "name": "Lookup prices match the catalogue",
    "scope": "step",
    "step": "s2"
   },
   {
    "id": "CT-POLICY",
    "name": "Refunded items carry the prices the lookup reported",
    "scope": "step",
    "step": "s3"
   },
   {
    "id": "CT-CALC",
    "name": "Refund equals the sum of the prices the calculator received",
    "scope": "step",
    "step": "s4"
   },
   {
    "id": "CT-WRITER",
    "name": "Message states the computed refund",
    "scope": "step",
    "step": "s5"
   }
  ]
 }
];

export const examples: Example[] = [
 {
  "order_id": "#W1023987",
  "email": "sophia.garcia9791@example.com",
  "message": "Please return the Luggage Set and the Pet Bed from order #W1023987.",
  "label": "#W1023987 (delivered): Luggage Set, Pet Bed"
 },
 {
  "order_id": "#W1052399",
  "email": "yusuf.patel5348@example.com",
  "message": "Please return the Tea Kettle and the Makeup Kit from order #W1052399.",
  "label": "#W1052399 (delivered): Tea Kettle, Makeup Kit"
 },
 {
  "order_id": "#W1006327",
  "email": "james.johnson7869@example.com",
  "message": "I want to return the Action Camera from order #W1006327.",
  "label": "#W1006327 (pending): Action Camera"
 },
 {
  "order_id": "#W1106948",
  "email": "omar.lopez9490@example.com",
  "message": "I want to return the Laptop from order #W1106948.",
  "label": "#W1106948 (cancelled): Laptop"
 }
];

export const silentRun: RunDetail = {
 "id": "run_67a305834a29",
 "workflow_key": "refund_desk",
 "status": "completed",
 "llm_mode": "recorded",
 "model": "llama3.2:3b",
 "seed": 1,
 "fault_type": "stale_price",
 "task_input": {
  "message": "Please return the Luggage Set and the Pet Bed from order #W1023987.",
  "email": "sophia.garcia9791@example.com",
  "order_id": "#W1023987"
 },
 "error": "",
 "created_at": "2026-10-13T19:11:28.763574",
 "finished_at": "2026-10-13T19:11:28.986987",
 "finding_count": 1,
 "failed_checks": 3,
 "trace": {
  "schema_version": "granite.trace/v1",
  "run": {
   "external_id": "run_67a305834a29",
   "workflow": "refund_desk",
   "runtime": "granite",
   "status": "completed",
   "task_input": {
    "message": "Please return the Luggage Set and the Pet Bed from order #W1023987.",
    "email": "sophia.garcia9791@example.com",
    "order_id": "#W1023987"
   },
   "final_output": {
    "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
   },
   "started_at": "2026-10-13T19:11:28.833820Z",
   "ended_at": "2026-10-13T19:11:28.973291Z"
  },
  "steps": [
   {
    "step_id": "s1",
    "agent": "Intake",
    "kind": "llm",
    "name": "extract order and items",
    "inputs": {
     "task.message": "Please return the Luggage Set and the Pet Bed from order #W1023987."
    },
    "outputs": {
     "order_id": "#W1023987",
     "item_names": [
      "Luggage Set",
      "Pet Bed"
     ]
    },
    "reads": [
     "task.message"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.0,
     "max_tokens": 120,
     "seed": 1,
     "json_mode": true,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 122,
     "tokens_out": 24
    },
    "prompt_hash": "866ff2c3959b2c69",
    "error": null,
    "started_at": "2026-10-13T19:11:28.833820Z",
    "ended_at": "2026-10-13T19:11:28.950069Z"
   },
   {
    "step_id": "s2",
    "agent": "Order Lookup",
    "kind": "tool",
    "name": "get_order_details",
    "inputs": {
     "s1.order_id": "#W1023987"
    },
    "outputs": {
     "order_id": "#W1023987",
     "user_id": "sophia_garcia_1101",
     "status": "delivered",
     "payment_method": "gift_card_9450778",
     "items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "reads": [
     "s1.order_id"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:28.950069Z",
    "ended_at": "2026-10-13T19:11:28.950069Z"
   },
   {
    "step_id": "s3",
    "agent": "Policy",
    "kind": "code",
    "name": "decide eligibility",
    "inputs": {
     "s2.status": "delivered",
     "s2.user_id": "sophia_garcia_1101",
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "s2.payment_method": "gift_card_9450778",
     "s1.item_names": [
      "Luggage Set",
      "Pet Bed"
     ],
     "task.email": "sophia.garcia9791@example.com"
    },
    "outputs": {
     "eligible": true,
     "reason": "delivered order owned by the customer",
     "items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "refund_method": "gift_card_9450778"
    },
    "reads": [
     "s2.status",
     "s2.user_id",
     "s2.items",
     "s2.payment_method",
     "s1.item_names",
     "task.email"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:28.951070Z",
    "ended_at": "2026-10-13T19:11:28.951070Z"
   },
   {
    "step_id": "s4",
    "agent": "Refund Calculator",
    "kind": "llm",
    "name": "compute refund",
    "inputs": {
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "outputs": {
     "prices_used": [
      452.03,
      209.95
     ],
     "refund_amount": 662.0
    },
    "reads": [
     "s3.items_to_refund"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.2,
     "max_tokens": 120,
     "seed": 1,
     "json_mode": true,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 120,
     "tokens_out": 24
    },
    "prompt_hash": "8cceb804dabf828b",
    "error": null,
    "started_at": "2026-10-13T19:11:28.951070Z",
    "ended_at": "2026-10-13T19:11:28.967276Z"
   },
   {
    "step_id": "s5",
    "agent": "Writer",
    "kind": "llm",
    "name": "write customer message",
    "inputs": {
     "s4.refund_amount": 662.0,
     "s3.refund_method": "gift_card_9450778",
     "s3.eligible": true,
     "s3.reason": "delivered order owned by the customer"
    },
    "outputs": {
     "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
    },
    "reads": [
     "s4.refund_amount",
     "s3.refund_method",
     "s3.eligible",
     "s3.reason"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.2,
     "max_tokens": 160,
     "seed": 1,
     "json_mode": false,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 130,
     "tokens_out": 34
    },
    "prompt_hash": "b9936591a2e8caa3",
    "error": null,
    "started_at": "2026-10-13T19:11:28.967276Z",
    "ended_at": "2026-10-13T19:11:28.973291Z"
   }
  ]
 },
 "trace_sha256": "44afbdcdf1b58f7794309b2b4ea8fab6e995366b67abdba6146241ef295195ee",
 "check_results": [
  {
   "check_id": "CHK-OUT-1",
   "check_version": 1,
   "scope": "outcome",
   "step": "s5",
   "type": "truth",
   "severity": "high",
   "status": "fail",
   "observed": 662,
   "expected": 662.23,
   "message": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
   "computation": {
    "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
    "tolerance": 0.01,
    "value": false,
    "resolved": {
     "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "catalog_total",
      "arguments": [
       [
        "8926329222",
        "5067898160"
       ]
      ],
      "returned": 662.23
     }
    ],
    "operands": [
     662.0,
     662.23
    ]
   }
  },
  {
   "check_id": "CHK-OUT-2",
   "check_version": 1,
   "scope": "outcome",
   "step": "s3",
   "type": "policy",
   "severity": "critical",
   "status": "pass",
   "observed": true,
   "expected": true,
   "message": "Refund decision follows policy (delivered order owned by the customer)",
   "computation": {
    "expression": "s3.eligible == truth.refund_allowed(task.order_id, task.email)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.eligible": true,
     "task.order_id": "#W1023987",
     "task.email": "sophia.garcia9791@example.com"
    },
    "truth_calls": [
     {
      "function": "refund_allowed",
      "arguments": [
       "#W1023987",
       "sophia.garcia9791@example.com"
      ],
      "returned": true
     }
    ],
    "operands": [
     true,
     true
    ]
   }
  },
  {
   "check_id": "CT-INTAKE",
   "check_version": 1,
   "scope": "step",
   "step": "s1",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Intake kept the order id and found items",
   "computation": {
    "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s1.order_id": "#W1023987",
     "task.order_id": "#W1023987",
     "s1.item_names": [
      "Luggage Set",
      "Pet Bed"
     ]
    },
    "truth_calls": [],
    "operands": null
   }
  },
  {
   "check_id": "CT-LOOKUP",
   "check_version": 1,
   "scope": "step",
   "step": "s2",
   "type": "truth",
   "severity": "high",
   "status": "fail",
   "observed": 661.98,
   "expected": 662.23,
   "message": "Lookup prices match the catalogue: observed 661.98, expected 662.23",
   "computation": {
    "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
    "tolerance": 0.005,
    "value": false,
    "resolved": {
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "catalog_total",
      "arguments": [
       [
        "8926329222",
        "5067898160"
       ]
      ],
      "returned": 662.23
     }
    ],
    "operands": [
     661.98,
     662.23
    ]
   }
  },
  {
   "check_id": "CT-POLICY",
   "check_version": 1,
   "scope": "step",
   "step": "s3",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Refunded items carry the prices the lookup reported",
   "computation": {
    "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "same_prices",
      "arguments": [
       [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ],
       [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      ],
      "returned": true
     }
    ],
    "operands": null
   }
  },
  {
   "check_id": "CT-CALC",
   "check_version": 1,
   "scope": "step",
   "step": "s4",
   "type": "assert",
   "severity": "high",
   "status": "fail",
   "observed": 662,
   "expected": 661.98,
   "message": "Refund equals the sum of the prices the calculator received: observed 662.0, expected 661.98",
   "computation": {
    "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    "tolerance": 0.01,
    "value": false,
    "resolved": {
     "s4.refund_amount": 662.0,
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.03
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [],
    "operands": [
     662.0,
     661.98
    ]
   }
  },
  {
   "check_id": "CT-WRITER",
   "check_version": 1,
   "scope": "step",
   "step": "s5",
   "type": "assert",
   "severity": "high",
   "status": "pass",
   "observed": 662,
   "expected": 662,
   "message": "Message states the computed refund",
   "computation": {
    "expression": "approx(number_in(s5.message), s4.refund_amount)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
     "s4.refund_amount": 662.0
    },
    "truth_calls": [],
    "operands": [
     662.0,
     662.0
    ]
   }
  }
 ],
 "findings": [
  {
   "id": "fnd_986513aaeef0",
   "run_id": "run_67a305834a29",
   "kind": "silent_failure",
   "severity": "high",
   "title": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
   "check_id": "CHK-OUT-1",
   "symptom_step": "s5",
   "status": "hypothesized",
   "verification_level": "V1",
   "created_at": "2026-10-13T19:11:29.086864"
  }
 ],
 "injected_fault": {
  "fault_type": "stale_price",
  "target_step": "s2",
  "field_path": "items[0].price",
  "original_value": 452.28,
  "injected_value": 452.03,
  "note": "the lookup tool returned an outdated cached price; no error was raised"
 }
};

export const cleanRun: RunDetail = {
 "id": "run_daeef5de5bb5",
 "workflow_key": "refund_desk",
 "status": "completed",
 "llm_mode": "recorded",
 "model": "llama3.2:3b",
 "seed": 1,
 "fault_type": null,
 "task_input": {
  "message": "Please return the Luggage Set and the Pet Bed from order #W1023987.",
  "email": "sophia.garcia9791@example.com",
  "order_id": "#W1023987"
 },
 "error": "",
 "created_at": "2026-10-13T19:11:29.168996",
 "finished_at": "2026-10-13T19:11:29.200414",
 "finding_count": 0,
 "failed_checks": 0,
 "trace": {
  "schema_version": "granite.trace/v1",
  "run": {
   "external_id": "run_daeef5de5bb5",
   "workflow": "refund_desk",
   "runtime": "granite",
   "status": "completed",
   "task_input": {
    "message": "Please return the Luggage Set and the Pet Bed from order #W1023987.",
    "email": "sophia.garcia9791@example.com",
    "order_id": "#W1023987"
   },
   "final_output": {
    "message": "Dear valued customer, your refund of $662.23 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your patience as we process this refund."
   },
   "started_at": "2026-10-13T19:11:29.184757Z",
   "ended_at": "2026-10-13T19:11:29.184757Z"
  },
  "steps": [
   {
    "step_id": "s1",
    "agent": "Intake",
    "kind": "llm",
    "name": "extract order and items",
    "inputs": {
     "task.message": "Please return the Luggage Set and the Pet Bed from order #W1023987."
    },
    "outputs": {
     "order_id": "#W1023987",
     "item_names": [
      "Luggage Set",
      "Pet Bed"
     ]
    },
    "reads": [
     "task.message"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.0,
     "max_tokens": 120,
     "seed": 1,
     "json_mode": true,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 122,
     "tokens_out": 24
    },
    "prompt_hash": "866ff2c3959b2c69",
    "error": null,
    "started_at": "2026-10-13T19:11:29.184757Z",
    "ended_at": "2026-10-13T19:11:29.184757Z"
   },
   {
    "step_id": "s2",
    "agent": "Order Lookup",
    "kind": "tool",
    "name": "get_order_details",
    "inputs": {
     "s1.order_id": "#W1023987"
    },
    "outputs": {
     "order_id": "#W1023987",
     "user_id": "sophia_garcia_1101",
     "status": "delivered",
     "payment_method": "gift_card_9450778",
     "items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "reads": [
     "s1.order_id"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:29.184757Z",
    "ended_at": "2026-10-13T19:11:29.184757Z"
   },
   {
    "step_id": "s3",
    "agent": "Policy",
    "kind": "code",
    "name": "decide eligibility",
    "inputs": {
     "s2.status": "delivered",
     "s2.user_id": "sophia_garcia_1101",
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "s2.payment_method": "gift_card_9450778",
     "s1.item_names": [
      "Luggage Set",
      "Pet Bed"
     ],
     "task.email": "sophia.garcia9791@example.com"
    },
    "outputs": {
     "eligible": true,
     "reason": "delivered order owned by the customer",
     "items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "refund_method": "gift_card_9450778"
    },
    "reads": [
     "s2.status",
     "s2.user_id",
     "s2.items",
     "s2.payment_method",
     "s1.item_names",
     "task.email"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:29.184757Z",
    "ended_at": "2026-10-13T19:11:29.184757Z"
   },
   {
    "step_id": "s4",
    "agent": "Refund Calculator",
    "kind": "llm",
    "name": "compute refund",
    "inputs": {
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "outputs": {
     "prices_used": [
      452.28,
      209.95
     ],
     "refund_amount": 662.23
    },
    "reads": [
     "s3.items_to_refund"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.2,
     "max_tokens": 120,
     "seed": 1,
     "json_mode": true,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 120,
     "tokens_out": 24
    },
    "prompt_hash": "b3c65d663928fb94",
    "error": null,
    "started_at": "2026-10-13T19:11:29.184757Z",
    "ended_at": "2026-10-13T19:11:29.184757Z"
   },
   {
    "step_id": "s5",
    "agent": "Writer",
    "kind": "llm",
    "name": "write customer message",
    "inputs": {
     "s4.refund_amount": 662.23,
     "s3.refund_method": "gift_card_9450778",
     "s3.eligible": true,
     "s3.reason": "delivered order owned by the customer"
    },
    "outputs": {
     "message": "Dear valued customer, your refund of $662.23 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your patience as we process this refund."
    },
    "reads": [
     "s4.refund_amount",
     "s3.refund_method",
     "s3.eligible",
     "s3.reason"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.2,
     "max_tokens": 160,
     "seed": 1,
     "json_mode": false,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 130,
     "tokens_out": 39
    },
    "prompt_hash": "83da0b0dff115050",
    "error": null,
    "started_at": "2026-10-13T19:11:29.184757Z",
    "ended_at": "2026-10-13T19:11:29.184757Z"
   }
  ]
 },
 "trace_sha256": "8b35b12dc68aa7786e68b132872c07c1bb1aafc410502387f8e060ab1310e7be",
 "check_results": [
  {
   "check_id": "CHK-OUT-1",
   "check_version": 1,
   "scope": "outcome",
   "step": "s5",
   "type": "truth",
   "severity": "high",
   "status": "pass",
   "observed": 662.23,
   "expected": 662.23,
   "message": "Stated refund equals the catalogue total of the refunded items",
   "computation": {
    "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s5.message": "Dear valued customer, your refund of $662.23 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your patience as we process this refund.",
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "catalog_total",
      "arguments": [
       [
        "8926329222",
        "5067898160"
       ]
      ],
      "returned": 662.23
     }
    ],
    "operands": [
     662.23,
     662.23
    ]
   }
  },
  {
   "check_id": "CHK-OUT-2",
   "check_version": 1,
   "scope": "outcome",
   "step": "s3",
   "type": "policy",
   "severity": "critical",
   "status": "pass",
   "observed": true,
   "expected": true,
   "message": "Refund decision follows policy (delivered order owned by the customer)",
   "computation": {
    "expression": "s3.eligible == truth.refund_allowed(task.order_id, task.email)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.eligible": true,
     "task.order_id": "#W1023987",
     "task.email": "sophia.garcia9791@example.com"
    },
    "truth_calls": [
     {
      "function": "refund_allowed",
      "arguments": [
       "#W1023987",
       "sophia.garcia9791@example.com"
      ],
      "returned": true
     }
    ],
    "operands": [
     true,
     true
    ]
   }
  },
  {
   "check_id": "CT-INTAKE",
   "check_version": 1,
   "scope": "step",
   "step": "s1",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Intake kept the order id and found items",
   "computation": {
    "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s1.order_id": "#W1023987",
     "task.order_id": "#W1023987",
     "s1.item_names": [
      "Luggage Set",
      "Pet Bed"
     ]
    },
    "truth_calls": [],
    "operands": null
   }
  },
  {
   "check_id": "CT-LOOKUP",
   "check_version": 1,
   "scope": "step",
   "step": "s2",
   "type": "truth",
   "severity": "high",
   "status": "pass",
   "observed": 662.23,
   "expected": 662.23,
   "message": "Lookup prices match the catalogue",
   "computation": {
    "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
    "tolerance": 0.005,
    "value": true,
    "resolved": {
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "catalog_total",
      "arguments": [
       [
        "8926329222",
        "5067898160"
       ]
      ],
      "returned": 662.23
     }
    ],
    "operands": [
     662.23,
     662.23
    ]
   }
  },
  {
   "check_id": "CT-POLICY",
   "check_version": 1,
   "scope": "step",
   "step": "s3",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Refunded items carry the prices the lookup reported",
   "computation": {
    "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ],
     "s2.items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [
     {
      "function": "same_prices",
      "arguments": [
       [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.28
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ],
       [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.28
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      ],
      "returned": true
     }
    ],
    "operands": null
   }
  },
  {
   "check_id": "CT-CALC",
   "check_version": 1,
   "scope": "step",
   "step": "s4",
   "type": "assert",
   "severity": "high",
   "status": "pass",
   "observed": 662.23,
   "expected": 662.23,
   "message": "Refund equals the sum of the prices the calculator received",
   "computation": {
    "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s4.refund_amount": 662.23,
     "s3.items_to_refund": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "truth_calls": [],
    "operands": [
     662.23,
     662.23
    ]
   }
  },
  {
   "check_id": "CT-WRITER",
   "check_version": 1,
   "scope": "step",
   "step": "s5",
   "type": "assert",
   "severity": "high",
   "status": "pass",
   "observed": 662.23,
   "expected": 662.23,
   "message": "Message states the computed refund",
   "computation": {
    "expression": "approx(number_in(s5.message), s4.refund_amount)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s5.message": "Dear valued customer, your refund of $662.23 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your patience as we process this refund.",
     "s4.refund_amount": 662.23
    },
    "truth_calls": [],
    "operands": [
     662.23,
     662.23
    ]
   }
  }
 ],
 "findings": [],
 "injected_fault": null
};

export const cancelledRun: RunDetail = {
 "id": "run_a8dbe035fc1f",
 "workflow_key": "refund_desk",
 "status": "completed",
 "llm_mode": "recorded",
 "model": "llama3.2:3b",
 "seed": 1,
 "fault_type": "stale_price",
 "task_input": {
  "message": "I want to return the Laptop from order #W1106948.",
  "email": "omar.lopez9490@example.com",
  "order_id": "#W1106948"
 },
 "error": "",
 "created_at": "2026-10-13T19:11:29.560020",
 "finished_at": "2026-10-13T19:11:29.683474",
 "finding_count": 0,
 "failed_checks": 1,
 "trace": {
  "schema_version": "granite.trace/v1",
  "run": {
   "external_id": "run_a8dbe035fc1f",
   "workflow": "refund_desk",
   "runtime": "granite",
   "status": "completed",
   "task_input": {
    "message": "I want to return the Laptop from order #W1106948.",
    "email": "omar.lopez9490@example.com",
    "order_id": "#W1106948"
   },
   "final_output": {
    "message": "Dear valued customer,\n\nUnfortunately, your order has been cancelled and we are unable to process a refund. Please note that refunds are only available for delivered orders and not for cancelled ones."
   },
   "started_at": "2026-10-13T19:11:29.679866Z",
   "ended_at": "2026-10-13T19:11:29.681377Z"
  },
  "steps": [
   {
    "step_id": "s1",
    "agent": "Intake",
    "kind": "llm",
    "name": "extract order and items",
    "inputs": {
     "task.message": "I want to return the Laptop from order #W1106948."
    },
    "outputs": {
     "order_id": "#W1106948",
     "item_names": [
      "Laptop"
     ]
    },
    "reads": [
     "task.message"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.0,
     "max_tokens": 120,
     "seed": 1,
     "json_mode": true,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 118,
     "tokens_out": 19
    },
    "prompt_hash": "0f9c98b9067f9581",
    "error": null,
    "started_at": "2026-10-13T19:11:29.679866Z",
    "ended_at": "2026-10-13T19:11:29.679866Z"
   },
   {
    "step_id": "s2",
    "agent": "Order Lookup",
    "kind": "tool",
    "name": "get_order_details",
    "inputs": {
     "s1.order_id": "#W1106948"
    },
    "outputs": {
     "order_id": "#W1106948",
     "user_id": "omar_lopez_7451",
     "status": "cancelled",
     "payment_method": "paypal_2167589",
     "items": [
      {
       "item_id": "5052031638",
       "name": "Laptop",
       "price": 2621.52
      },
      {
       "item_id": "9991484137",
       "name": "Mechanical Keyboard",
       "price": 240.97
      },
      {
       "item_id": "1434748144",
       "name": "Water Bottle",
       "price": 49.72
      },
      {
       "item_id": "8106223139",
       "name": "Hiking Boots",
       "price": 249.12
      },
      {
       "item_id": "8479046075",
       "name": "Bookshelf",
       "price": 451.01
      }
     ]
    },
    "reads": [
     "s1.order_id"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:29.679866Z",
    "ended_at": "2026-10-13T19:11:29.681377Z"
   },
   {
    "step_id": "s3",
    "agent": "Policy",
    "kind": "code",
    "name": "decide eligibility",
    "inputs": {
     "s2.status": "cancelled",
     "s2.user_id": "omar_lopez_7451",
     "s2.items": [
      {
       "item_id": "5052031638",
       "name": "Laptop",
       "price": 2621.52
      },
      {
       "item_id": "9991484137",
       "name": "Mechanical Keyboard",
       "price": 240.97
      },
      {
       "item_id": "1434748144",
       "name": "Water Bottle",
       "price": 49.72
      },
      {
       "item_id": "8106223139",
       "name": "Hiking Boots",
       "price": 249.12
      },
      {
       "item_id": "8479046075",
       "name": "Bookshelf",
       "price": 451.01
      }
     ],
     "s2.payment_method": "paypal_2167589",
     "s1.item_names": [
      "Laptop"
     ],
     "task.email": "omar.lopez9490@example.com"
    },
    "outputs": {
     "eligible": false,
     "reason": "the order is cancelled, and only delivered orders can be returned",
     "items_to_refund": [],
     "refund_method": "paypal_2167589"
    },
    "reads": [
     "s2.status",
     "s2.user_id",
     "s2.items",
     "s2.payment_method",
     "s1.item_names",
     "task.email"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:29.681377Z",
    "ended_at": "2026-10-13T19:11:29.681377Z"
   },
   {
    "step_id": "s4",
    "agent": "Refund Calculator",
    "kind": "llm",
    "name": "compute refund",
    "inputs": {
     "s3.items_to_refund": []
    },
    "outputs": {
     "prices_used": [],
     "refund_amount": 0.0
    },
    "reads": [
     "s3.items_to_refund"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": null,
    "started_at": "2026-10-13T19:11:29.681377Z",
    "ended_at": "2026-10-13T19:11:29.681377Z"
   },
   {
    "step_id": "s5",
    "agent": "Writer",
    "kind": "llm",
    "name": "write customer message",
    "inputs": {
     "s4.refund_amount": 0.0,
     "s3.refund_method": "paypal_2167589",
     "s3.eligible": false,
     "s3.reason": "the order is cancelled, and only delivered orders can be returned"
    },
    "outputs": {
     "message": "Dear valued customer,\n\nUnfortunately, your order has been cancelled and we are unable to process a refund. Please note that refunds are only available for delivered orders and not for cancelled ones."
    },
    "reads": [
     "s4.refund_amount",
     "s3.refund_method",
     "s3.eligible",
     "s3.reason"
    ],
    "model": "llama3.2:3b",
    "params": {
     "temperature": 0.2,
     "max_tokens": 160,
     "seed": 1,
     "json_mode": false,
     "provider": "recorded",
     "recorded": true,
     "calls": 1,
     "tokens_in": 130,
     "tokens_out": 37
    },
    "prompt_hash": "4d6a69cd015e73ea",
    "error": null,
    "started_at": "2026-10-13T19:11:29.681377Z",
    "ended_at": "2026-10-13T19:11:29.681377Z"
   }
  ]
 },
 "trace_sha256": "b47832a4c529095a144a5025878c8ffd9cf7a85be6adda51bcfe7e0adb7c9fce",
 "check_results": [
  {
   "check_id": "CHK-OUT-1",
   "check_version": 1,
   "scope": "outcome",
   "step": "s5",
   "type": "truth",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "no number found in text",
   "computation": {
    "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CHK-OUT-2",
   "check_version": 1,
   "scope": "outcome",
   "step": "s3",
   "type": "policy",
   "severity": "critical",
   "status": "pass",
   "observed": false,
   "expected": false,
   "message": "Refund decision follows policy (delivered order owned by the customer)",
   "computation": {
    "expression": "s3.eligible == truth.refund_allowed(task.order_id, task.email)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.eligible": false,
     "task.order_id": "#W1106948",
     "task.email": "omar.lopez9490@example.com"
    },
    "truth_calls": [
     {
      "function": "refund_allowed",
      "arguments": [
       "#W1106948",
       "omar.lopez9490@example.com"
      ],
      "returned": false
     }
    ],
    "operands": [
     false,
     false
    ]
   }
  },
  {
   "check_id": "CT-INTAKE",
   "check_version": 1,
   "scope": "step",
   "step": "s1",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Intake kept the order id and found items",
   "computation": {
    "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s1.order_id": "#W1106948",
     "task.order_id": "#W1106948",
     "s1.item_names": [
      "Laptop"
     ]
    },
    "truth_calls": [],
    "operands": null
   }
  },
  {
   "check_id": "CT-LOOKUP",
   "check_version": 1,
   "scope": "step",
   "step": "s2",
   "type": "truth",
   "severity": "high",
   "status": "fail",
   "observed": 3612.34,
   "expected": 3612.59,
   "message": "Lookup prices match the catalogue: observed 3612.34, expected 3612.59",
   "computation": {
    "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
    "tolerance": 0.005,
    "value": false,
    "resolved": {
     "s2.items": "[{'item_id': '5052031638', 'name': 'Laptop', 'price': 2621.52}, {'item_id': '9991484137', 'name': 'Mechanical Keyboard', 'price': 240.97}, {'item_id': '1434748144', 'name': 'Water Bottle', 'price': 49.72}, {'item_id': '8106223139', 'name': 'Hiking Boots', 'price': 249.12}, {'item_id': '8479046075', ..."
    },
    "truth_calls": [
     {
      "function": "catalog_total",
      "arguments": [
       [
        "5052031638",
        "9991484137",
        "1434748144",
        "8106223139",
        "8479046075"
       ]
      ],
      "returned": 3612.59
     }
    ],
    "operands": [
     3612.34,
     3612.59
    ]
   }
  },
  {
   "check_id": "CT-POLICY",
   "check_version": 1,
   "scope": "step",
   "step": "s3",
   "type": "assert",
   "severity": "medium",
   "status": "pass",
   "observed": null,
   "expected": null,
   "message": "Refunded items carry the prices the lookup reported",
   "computation": {
    "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s3.items_to_refund": [],
     "s2.items": "[{'item_id': '5052031638', 'name': 'Laptop', 'price': 2621.52}, {'item_id': '9991484137', 'name': 'Mechanical Keyboard', 'price': 240.97}, {'item_id': '1434748144', 'name': 'Water Bottle', 'price': 49.72}, {'item_id': '8106223139', 'name': 'Hiking Boots', 'price': 249.12}, {'item_id': '8479046075', ..."
    },
    "truth_calls": [
     {
      "function": "same_prices",
      "arguments": "[[], [{'item_id': '5052031638', 'name': 'Laptop', 'price': 2621.52}, {'item_id': '9991484137', 'name': 'Mechanical Keyboard', 'price': 240.97}, {'item_id': '1434748144', 'name': 'Water Bottle', 'price': 49.72}, {'item_id': '8106223139', 'name': 'Hiking Boots', 'price': 249.12}, {'item_id': '84790460...",
      "returned": true
     }
    ],
    "operands": null
   }
  },
  {
   "check_id": "CT-CALC",
   "check_version": 1,
   "scope": "step",
   "step": "s4",
   "type": "assert",
   "severity": "high",
   "status": "pass",
   "observed": 0,
   "expected": 0,
   "message": "Refund equals the sum of the prices the calculator received",
   "computation": {
    "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    "tolerance": 0.01,
    "value": true,
    "resolved": {
     "s4.refund_amount": 0.0,
     "s3.items_to_refund": []
    },
    "truth_calls": [],
    "operands": [
     0.0,
     0.0
    ]
   }
  },
  {
   "check_id": "CT-WRITER",
   "check_version": 1,
   "scope": "step",
   "step": "s5",
   "type": "assert",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "no number found in text",
   "computation": {
    "expression": "approx(number_in(s5.message), s4.refund_amount)",
    "tolerance": 0.01
   }
  }
 ],
 "findings": [],
 "injected_fault": {
  "fault_type": "stale_price",
  "target_step": "s2",
  "field_path": "items[0].price",
  "original_value": 2621.77,
  "injected_value": 2621.52,
  "note": "the lookup tool returned an outdated cached price; no error was raised"
 }
};

export const erroredRun: RunDetail = {
 "id": "run_bcc1cc609d51",
 "workflow_key": "refund_desk",
 "status": "errored",
 "llm_mode": "recorded",
 "model": "llama3.2:3b",
 "seed": 1,
 "fault_type": null,
 "task_input": {
  "message": "Please refund everything in my order.",
  "email": "sophia.garcia9791@example.com",
  "order_id": "#W1023987"
 },
 "error": "Intake: RecordedMiss: this exact request was never recorded; run once in live mode with recording enabled (model=llama3.2:3b, seed=1) Recorded mode can only replay the saved example tasks; start Ollama (or set a hosted endpoint) and use live mode to run your own task.",
 "created_at": "2026-10-13T19:11:30.384067",
 "finished_at": "2026-10-13T19:11:30.421341",
 "finding_count": 1,
 "failed_checks": 0,
 "trace": {
  "schema_version": "granite.trace/v1",
  "run": {
   "external_id": "run_bcc1cc609d51",
   "workflow": "refund_desk",
   "runtime": "granite",
   "status": "errored",
   "task_input": {
    "message": "Please refund everything in my order.",
    "email": "sophia.garcia9791@example.com",
    "order_id": "#W1023987"
   },
   "final_output": {},
   "started_at": "2026-10-13T19:11:30.418340Z",
   "ended_at": "2026-10-13T19:11:30.418340Z"
  },
  "steps": [
   {
    "step_id": "s1",
    "agent": "Intake",
    "kind": "llm",
    "name": "extract order and items",
    "inputs": {
     "task.message": "Please refund everything in my order."
    },
    "outputs": {},
    "reads": [
     "task.message"
    ],
    "model": null,
    "params": null,
    "prompt_hash": null,
    "error": "RecordedMiss: this exact request was never recorded; run once in live mode with recording enabled (model=llama3.2:3b, seed=1)",
    "started_at": "2026-10-13T19:11:30.418340Z",
    "ended_at": "2026-10-13T19:11:30.418340Z"
   }
  ]
 },
 "trace_sha256": "f51bb1bc264d31e5ca447ee9bade1e20fcfe4182167c99a0856a636828abda96",
 "check_results": [
  {
   "check_id": "CHK-OUT-1",
   "check_version": 1,
   "scope": "outcome",
   "step": "s5",
   "type": "truth",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's5' is not in this trace",
   "computation": {
    "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CHK-OUT-2",
   "check_version": 1,
   "scope": "outcome",
   "step": "s3",
   "type": "policy",
   "severity": "critical",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's3' is not in this trace",
   "computation": {
    "expression": "s3.eligible == truth.refund_allowed(task.order_id, task.email)",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CT-INTAKE",
   "check_version": 1,
   "scope": "step",
   "step": "s1",
   "type": "assert",
   "severity": "medium",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "field 'order_id' is missing (reading s1.order_id)",
   "computation": {
    "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CT-LOOKUP",
   "check_version": 1,
   "scope": "step",
   "step": "s2",
   "type": "truth",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's2' is not in this trace",
   "computation": {
    "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
    "tolerance": 0.005
   }
  },
  {
   "check_id": "CT-POLICY",
   "check_version": 1,
   "scope": "step",
   "step": "s3",
   "type": "assert",
   "severity": "medium",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's3' is not in this trace",
   "computation": {
    "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CT-CALC",
   "check_version": 1,
   "scope": "step",
   "step": "s4",
   "type": "assert",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's4' is not in this trace",
   "computation": {
    "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    "tolerance": 0.01
   }
  },
  {
   "check_id": "CT-WRITER",
   "check_version": 1,
   "scope": "step",
   "step": "s5",
   "type": "assert",
   "severity": "high",
   "status": "abstain",
   "observed": null,
   "expected": null,
   "message": "step 's5' is not in this trace",
   "computation": {
    "expression": "approx(number_in(s5.message), s4.refund_amount)",
    "tolerance": 0.01
   }
  }
 ],
 "findings": [
  {
   "id": "fnd_961f19a22a5a",
   "run_id": "run_bcc1cc609d51",
   "kind": "explicit_error",
   "severity": "high",
   "title": "Run errored at Intake",
   "check_id": null,
   "symptom_step": "s1",
   "status": "hypothesized",
   "verification_level": "V1",
   "created_at": "2026-10-13T19:11:30.423336"
  }
 ],
 "injected_fault": null
};

export const silentGraph: Graph = {
 "nodes": [
  {
   "id": "task",
   "label": "Task input",
   "kind": "input",
   "status": "ok"
  },
  {
   "id": "s1",
   "label": "Intake",
   "kind": "llm",
   "status": "ok",
   "symptom": false
  },
  {
   "id": "s2",
   "label": "Order Lookup",
   "kind": "tool",
   "status": "failed",
   "symptom": false
  },
  {
   "id": "s3",
   "label": "Policy",
   "kind": "code",
   "status": "ok",
   "symptom": false
  },
  {
   "id": "s4",
   "label": "Refund Calculator",
   "kind": "llm",
   "status": "failed",
   "symptom": false
  },
  {
   "id": "s5",
   "label": "Writer",
   "kind": "llm",
   "status": "failed",
   "symptom": true
  }
 ],
 "edges": [
  {
   "source": "s1",
   "target": "s2",
   "field": "order_id"
  },
  {
   "source": "s2",
   "target": "s3",
   "field": "status"
  },
  {
   "source": "s2",
   "target": "s3",
   "field": "user_id"
  },
  {
   "source": "s2",
   "target": "s3",
   "field": "items"
  },
  {
   "source": "s2",
   "target": "s3",
   "field": "payment_method"
  },
  {
   "source": "s1",
   "target": "s3",
   "field": "item_names"
  },
  {
   "source": "s3",
   "target": "s4",
   "field": "items_to_refund"
  },
  {
   "source": "s4",
   "target": "s5",
   "field": "refund_amount"
  },
  {
   "source": "s3",
   "target": "s5",
   "field": "refund_method"
  },
  {
   "source": "s3",
   "target": "s5",
   "field": "eligible"
  },
  {
   "source": "s3",
   "target": "s5",
   "field": "reason"
  },
  {
   "source": "task",
   "target": "s1",
   "field": "message"
  },
  {
   "source": "task",
   "target": "s3",
   "field": "email"
  }
 ]
};

export const findingTraced: FindingDetail = {
 "id": "fnd_986513aaeef0",
 "run_id": "run_67a305834a29",
 "kind": "silent_failure",
 "severity": "high",
 "title": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
 "check_id": "CHK-OUT-1",
 "symptom_step": "s5",
 "status": "hypothesized",
 "verification_level": "V1",
 "created_at": "2026-10-13T19:11:29.086864",
 "detail": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
 "hypotheses": [
  {
   "id": "hyp_11c2d01cb85d",
   "rank": 1,
   "step_id": "s2",
   "agent": "Order Lookup",
   "method": "provenance",
   "evidence_kind": "truth_mismatch",
   "score": 0.81,
   "rationale": "Order Lookup's output contradicts the source of truth (CT-LOOKUP): observed 661.98, expected 662.23.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s2",
     "to": "s5",
     "path": [
      {
       "step_id": "s2",
       "agent": "Order Lookup",
       "carries": "payment_method"
      },
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-LOOKUP",
     "status": "fail",
     "observed": 661.98,
     "expected": 662.23,
     "computation": {
      "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
      "tolerance": 0.005,
      "value": false,
      "resolved": {
       "s2.items": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [
       {
        "function": "catalog_total",
        "arguments": [
         [
          "8926329222",
          "5067898160"
         ]
        ],
        "returned": 662.23
       }
      ],
      "operands": [
       661.98,
       662.23
      ]
     }
    }
   ],
   "status": "open",
   "can_verify": true
  },
  {
   "id": "hyp_c6de0839f6a9",
   "rank": 2,
   "step_id": "s4",
   "agent": "Refund Calculator",
   "method": "provenance",
   "evidence_kind": "contract_fail",
   "score": 0.72,
   "rationale": "Refund Calculator broke its own contract (CT-CALC): observed 662.0, expected 661.98.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s4",
     "to": "s5",
     "path": [
      {
       "step_id": "s4",
       "agent": "Refund Calculator",
       "carries": "refund_amount"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-CALC",
     "status": "fail",
     "observed": 662.0,
     "expected": 661.98,
     "computation": {
      "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
      "tolerance": 0.01,
      "value": false,
      "resolved": {
       "s4.refund_amount": 662.0,
       "s3.items_to_refund": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [],
      "operands": [
       662.0,
       661.98
      ]
     }
    }
   ],
   "status": "open",
   "can_verify": true
  },
  {
   "id": "hyp_fd03c7a0e027",
   "rank": 3,
   "step_id": "s1",
   "agent": "Intake",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.081,
   "rationale": "Intake is consistent with its inputs (CT-INTAKE passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s1",
     "to": "s5",
     "path": [
      {
       "step_id": "s1",
       "agent": "Intake",
       "carries": "item_names"
      },
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-INTAKE",
     "status": "pass",
     "observed": null,
     "expected": null,
     "computation": {
      "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s1.order_id": "#W1023987",
       "task.order_id": "#W1023987",
       "s1.item_names": [
        "Luggage Set",
        "Pet Bed"
       ]
      },
      "truth_calls": [],
      "operands": null
     }
    }
   ],
   "status": "open",
   "can_verify": true
  },
  {
   "id": "hyp_b98a1809c5e3",
   "rank": 4,
   "step_id": "s3",
   "agent": "Policy",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.09,
   "rationale": "Policy is consistent with its inputs (CT-POLICY passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s3",
     "to": "s5",
     "path": [
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-POLICY",
     "status": "pass",
     "observed": null,
     "expected": null,
     "computation": {
      "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s3.items_to_refund": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ],
       "s2.items": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [
       {
        "function": "same_prices",
        "arguments": [
         [
          {
           "item_id": "8926329222",
           "name": "Luggage Set",
           "price": 452.03
          },
          {
           "item_id": "5067898160",
           "name": "Pet Bed",
           "price": 209.95
          }
         ],
         [
          {
           "item_id": "8926329222",
           "name": "Luggage Set",
           "price": 452.03
          },
          {
           "item_id": "5067898160",
           "name": "Pet Bed",
           "price": 209.95
          }
         ]
        ],
        "returned": true
       }
      ],
      "operands": null
     }
    }
   ],
   "status": "open",
   "can_verify": false
  },
  {
   "id": "hyp_1cefb482cab9",
   "rank": 5,
   "step_id": "s5",
   "agent": "Writer",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.1,
   "rationale": "Writer is consistent with its inputs (CT-WRITER passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s5",
     "to": "s5",
     "path": [
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-WRITER",
     "status": "pass",
     "observed": 662.0,
     "expected": 662.0,
     "computation": {
      "expression": "approx(number_in(s5.message), s4.refund_amount)",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
       "s4.refund_amount": 662.0
      },
      "truth_calls": [],
      "operands": [
       662.0,
       662.0
      ]
     }
    }
   ],
   "status": "open",
   "can_verify": false
  }
 ],
 "experiments": [],
 "reviews": [],
 "evidence": [
  {
   "id": "ev_a5889094984b",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "check_computation",
   "title": "Check CHK-OUT-1 computation",
   "payload": {
    "check_id": "CHK-OUT-1",
    "check_version": 1,
    "scope": "outcome",
    "step": "s5",
    "type": "truth",
    "severity": "high",
    "status": "fail",
    "observed": 662.0,
    "expected": 662.23,
    "message": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
    "computation": {
     "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
     "tolerance": 0.01,
     "value": false,
     "resolved": {
      "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
      "s3.items_to_refund": [
       {
        "item_id": "8926329222",
        "name": "Luggage Set",
        "price": 452.03
       },
       {
        "item_id": "5067898160",
        "name": "Pet Bed",
        "price": 209.95
       }
      ]
     },
     "truth_calls": [
      {
       "function": "catalog_total",
       "arguments": [
        [
         "8926329222",
         "5067898160"
        ]
       ],
       "returned": 662.23
      }
     ],
     "operands": [
      662.0,
      662.23
     ]
    },
    "data_snapshot": "taubench_retail_v1"
   },
   "sha256": "36e4a44e6b102c90ec90175b146f339421e7a81ec0c4f41613e68cdb981c95b4",
   "reproduce": "Re-evaluate check CHK-OUT-1 on run run_67a305834a29; data snapshot taubench_retail_v1",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_5dbe8c57953a",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "step_snapshot",
   "title": "Step s5 (Writer) snapshot",
   "payload": {
    "step_id": "s5",
    "agent": "Writer",
    "inputs": {
     "s4.refund_amount": 662.0,
     "s3.refund_method": "gift_card_9450778",
     "s3.eligible": true,
     "s3.reason": "delivered order owned by the customer"
    },
    "outputs": {
     "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
    },
    "error": null
   },
   "sha256": "5418d67087da67a730bc730b4da93b47aefc4d568fb61674e0b967bda21c55f5",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_ddb94881d498",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 1: Order Lookup (provenance)",
   "payload": {
    "rank": 1,
    "step_id": "s2",
    "agent": "Order Lookup",
    "method": "provenance",
    "evidence_kind": "truth_mismatch",
    "score": 0.81,
    "rationale": "Order Lookup's output contradicts the source of truth (CT-LOOKUP): observed 661.98, expected 662.23.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s2",
      "to": "s5",
      "path": [
       {
        "step_id": "s2",
        "agent": "Order Lookup",
        "carries": "payment_method"
       },
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-LOOKUP",
      "status": "fail",
      "observed": 661.98,
      "expected": 662.23,
      "computation": {
       "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
       "tolerance": 0.005,
       "value": false,
       "resolved": {
        "s2.items": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [
        {
         "function": "catalog_total",
         "arguments": [
          [
           "8926329222",
           "5067898160"
          ]
         ],
         "returned": 662.23
        }
       ],
       "operands": [
        661.98,
        662.23
       ]
      }
     }
    ]
   },
   "sha256": "22b358c252107ba1466373a5e07bb3271fd893a158f32122d73749c52b4366f8",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_164a4ad2251e",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 2: Refund Calculator (provenance)",
   "payload": {
    "rank": 2,
    "step_id": "s4",
    "agent": "Refund Calculator",
    "method": "provenance",
    "evidence_kind": "contract_fail",
    "score": 0.72,
    "rationale": "Refund Calculator broke its own contract (CT-CALC): observed 662.0, expected 661.98.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s4",
      "to": "s5",
      "path": [
       {
        "step_id": "s4",
        "agent": "Refund Calculator",
        "carries": "refund_amount"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-CALC",
      "status": "fail",
      "observed": 662.0,
      "expected": 661.98,
      "computation": {
       "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
       "tolerance": 0.01,
       "value": false,
       "resolved": {
        "s4.refund_amount": 662.0,
        "s3.items_to_refund": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [],
       "operands": [
        662.0,
        661.98
       ]
      }
     }
    ]
   },
   "sha256": "c198214eb78358f2264e251bb03931609459d9af648746c3a547e74cf617b4e3",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_211d774ffd11",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 3: Intake (provenance)",
   "payload": {
    "rank": 3,
    "step_id": "s1",
    "agent": "Intake",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.081,
    "rationale": "Intake is consistent with its inputs (CT-INTAKE passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s1",
      "to": "s5",
      "path": [
       {
        "step_id": "s1",
        "agent": "Intake",
        "carries": "item_names"
       },
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-INTAKE",
      "status": "pass",
      "observed": null,
      "expected": null,
      "computation": {
       "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s1.order_id": "#W1023987",
        "task.order_id": "#W1023987",
        "s1.item_names": [
         "Luggage Set",
         "Pet Bed"
        ]
       },
       "truth_calls": [],
       "operands": null
      }
     }
    ]
   },
   "sha256": "1913c4784c75777e910345273fa76de1241d58bc5c4673a5b9bfd5c07a9d46a1",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_be1136540c3b",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 4: Policy (provenance)",
   "payload": {
    "rank": 4,
    "step_id": "s3",
    "agent": "Policy",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.09,
    "rationale": "Policy is consistent with its inputs (CT-POLICY passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s3",
      "to": "s5",
      "path": [
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-POLICY",
      "status": "pass",
      "observed": null,
      "expected": null,
      "computation": {
       "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s3.items_to_refund": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ],
        "s2.items": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [
        {
         "function": "same_prices",
         "arguments": [
          [
           {
            "item_id": "8926329222",
            "name": "Luggage Set",
            "price": 452.03
           },
           {
            "item_id": "5067898160",
            "name": "Pet Bed",
            "price": 209.95
           }
          ],
          [
           {
            "item_id": "8926329222",
            "name": "Luggage Set",
            "price": 452.03
           },
           {
            "item_id": "5067898160",
            "name": "Pet Bed",
            "price": 209.95
           }
          ]
         ],
         "returned": true
        }
       ],
       "operands": null
      }
     }
    ]
   },
   "sha256": "5195f2efc283a76a9411de4acaa5fc4d38e7326dde45dbc4384517ed101ddf7d",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_3ffdbdb385a0",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 5: Writer (provenance)",
   "payload": {
    "rank": 5,
    "step_id": "s5",
    "agent": "Writer",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.1,
    "rationale": "Writer is consistent with its inputs (CT-WRITER passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s5",
      "to": "s5",
      "path": [
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-WRITER",
      "status": "pass",
      "observed": 662.0,
      "expected": 662.0,
      "computation": {
       "expression": "approx(number_in(s5.message), s4.refund_amount)",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
        "s4.refund_amount": 662.0
       },
       "truth_calls": [],
       "operands": [
        662.0,
        662.0
       ]
      }
     }
    ]
   },
   "sha256": "4ddba862f9afc8f07ae1b027390e3db7dc5cde39c04b5c14e4919059b9e946fd",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  }
 ],
 "allowed_actions": [
  "verify"
 ]
};

export const findingConfirmed: FindingDetail = {
 "id": "fnd_986513aaeef0",
 "run_id": "run_67a305834a29",
 "kind": "silent_failure",
 "severity": "high",
 "title": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
 "check_id": "CHK-OUT-1",
 "symptom_step": "s5",
 "status": "confirmed",
 "verification_level": "V2",
 "created_at": "2026-10-13T19:11:29.086864",
 "detail": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
 "hypotheses": [
  {
   "id": "hyp_11c2d01cb85d",
   "rank": 1,
   "step_id": "s2",
   "agent": "Order Lookup",
   "method": "provenance",
   "evidence_kind": "truth_mismatch",
   "score": 0.81,
   "rationale": "Order Lookup's output contradicts the source of truth (CT-LOOKUP): observed 661.98, expected 662.23.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s2",
     "to": "s5",
     "path": [
      {
       "step_id": "s2",
       "agent": "Order Lookup",
       "carries": "payment_method"
      },
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-LOOKUP",
     "status": "fail",
     "observed": 661.98,
     "expected": 662.23,
     "computation": {
      "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
      "tolerance": 0.005,
      "value": false,
      "resolved": {
       "s2.items": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [
       {
        "function": "catalog_total",
        "arguments": [
         [
          "8926329222",
          "5067898160"
         ]
        ],
        "returned": 662.23
       }
      ],
      "operands": [
       661.98,
       662.23
      ]
     }
    }
   ],
   "status": "confirmed",
   "can_verify": true
  },
  {
   "id": "hyp_c6de0839f6a9",
   "rank": 2,
   "step_id": "s4",
   "agent": "Refund Calculator",
   "method": "provenance",
   "evidence_kind": "contract_fail",
   "score": 0.72,
   "rationale": "Refund Calculator broke its own contract (CT-CALC): observed 662.0, expected 661.98.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s4",
     "to": "s5",
     "path": [
      {
       "step_id": "s4",
       "agent": "Refund Calculator",
       "carries": "refund_amount"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-CALC",
     "status": "fail",
     "observed": 662.0,
     "expected": 661.98,
     "computation": {
      "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
      "tolerance": 0.01,
      "value": false,
      "resolved": {
       "s4.refund_amount": 662.0,
       "s3.items_to_refund": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [],
      "operands": [
       662.0,
       661.98
      ]
     }
    }
   ],
   "status": "refuted",
   "can_verify": true
  },
  {
   "id": "hyp_fd03c7a0e027",
   "rank": 3,
   "step_id": "s1",
   "agent": "Intake",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.081,
   "rationale": "Intake is consistent with its inputs (CT-INTAKE passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s1",
     "to": "s5",
     "path": [
      {
       "step_id": "s1",
       "agent": "Intake",
       "carries": "item_names"
      },
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-INTAKE",
     "status": "pass",
     "observed": null,
     "expected": null,
     "computation": {
      "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s1.order_id": "#W1023987",
       "task.order_id": "#W1023987",
       "s1.item_names": [
        "Luggage Set",
        "Pet Bed"
       ]
      },
      "truth_calls": [],
      "operands": null
     }
    }
   ],
   "status": "open",
   "can_verify": true
  },
  {
   "id": "hyp_b98a1809c5e3",
   "rank": 4,
   "step_id": "s3",
   "agent": "Policy",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.09,
   "rationale": "Policy is consistent with its inputs (CT-POLICY passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s3",
     "to": "s5",
     "path": [
      {
       "step_id": "s3",
       "agent": "Policy",
       "carries": "reason"
      },
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-POLICY",
     "status": "pass",
     "observed": null,
     "expected": null,
     "computation": {
      "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s3.items_to_refund": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ],
       "s2.items": [
        {
         "item_id": "8926329222",
         "name": "Luggage Set",
         "price": 452.03
        },
        {
         "item_id": "5067898160",
         "name": "Pet Bed",
         "price": 209.95
        }
       ]
      },
      "truth_calls": [
       {
        "function": "same_prices",
        "arguments": [
         [
          {
           "item_id": "8926329222",
           "name": "Luggage Set",
           "price": 452.03
          },
          {
           "item_id": "5067898160",
           "name": "Pet Bed",
           "price": 209.95
          }
         ],
         [
          {
           "item_id": "8926329222",
           "name": "Luggage Set",
           "price": 452.03
          },
          {
           "item_id": "5067898160",
           "name": "Pet Bed",
           "price": 209.95
          }
         ]
        ],
        "returned": true
       }
      ],
      "operands": null
     }
    }
   ],
   "status": "open",
   "can_verify": false
  },
  {
   "id": "hyp_1cefb482cab9",
   "rank": 5,
   "step_id": "s5",
   "agent": "Writer",
   "method": "provenance",
   "evidence_kind": "consistent",
   "score": 0.1,
   "rationale": "Writer is consistent with its inputs (CT-WRITER passed): it passed on what it was given.",
   "evidence": [
    {
     "type": "provenance_path",
     "from": "s5",
     "to": "s5",
     "path": [
      {
       "step_id": "s5",
       "agent": "Writer"
      }
     ]
    },
    {
     "type": "check",
     "check_id": "CT-WRITER",
     "status": "pass",
     "observed": 662.0,
     "expected": 662.0,
     "computation": {
      "expression": "approx(number_in(s5.message), s4.refund_amount)",
      "tolerance": 0.01,
      "value": true,
      "resolved": {
       "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
       "s4.refund_amount": 662.0
      },
      "truth_calls": [],
      "operands": [
       662.0,
       662.0
      ]
     }
    }
   ],
   "status": "open",
   "can_verify": false
  }
 ],
 "experiments": [
  {
   "id": "exp_528356da88e0",
   "hypothesis_id": "hyp_11c2d01cb85d",
   "finding_id": "fnd_986513aaeef0",
   "status": "done",
   "llm_mode": "recorded",
   "n": 5,
   "m": 2,
   "rule_version": "VR-1",
   "intervention": {
    "step_id": "s2",
    "patches": {
     "items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    },
    "source": "truth",
    "description": "Set Order Lookup.items to the value its contract or the source of truth requires"
   },
   "summary": {
    "rule_version": "VR-1",
    "n_planned": 5,
    "n_completed": 5,
    "k_pass": 5,
    "m_planned": 2,
    "m_completed": 2,
    "c_pass": 0,
    "ci_low": 0.5655,
    "ci_high": 1.0,
    "verdict": "confirmed",
    "explanation": "With the fix applied the outcome was correct in 5/5 replays, and in 0/2 controls without it: the fix, not luck, changed the result."
   },
   "verdict": "confirmed",
   "error": "",
   "created_at": "2026-10-13T19:11:31.173522",
   "finished_at": "2026-10-13T19:11:31.289771",
   "replays": [
    {
     "kind": "intervention",
     "idx": 0,
     "seed": 1000,
     "completed": true,
     "passed": true,
     "judgement": {
      "passed": true,
      "fixed": [
       "CHK-OUT-1"
      ],
      "still_failing": [],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 1,
     "seed": 1001,
     "completed": true,
     "passed": true,
     "judgement": {
      "passed": true,
      "fixed": [
       "CHK-OUT-1"
      ],
      "still_failing": [],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 2,
     "seed": 1002,
     "completed": true,
     "passed": true,
     "judgement": {
      "passed": true,
      "fixed": [
       "CHK-OUT-1"
      ],
      "still_failing": [],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 3,
     "seed": 1003,
     "completed": true,
     "passed": true,
     "judgement": {
      "passed": true,
      "fixed": [
       "CHK-OUT-1"
      ],
      "still_failing": [],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing your refund of $662.23 to the original gift card associated with your purchase. This amount will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 4,
     "seed": 1004,
     "completed": true,
     "passed": true,
     "judgement": {
      "passed": true,
      "fixed": [
       "CHK-OUT-1"
      ],
      "still_failing": [],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "control",
     "idx": 0,
     "seed": 1500,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "control",
     "idx": 1,
     "seed": 1501,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase. The refund will be returned to the same gift card balance."
     }
    }
   ]
  },
  {
   "id": "exp_530d2d009849",
   "hypothesis_id": "hyp_c6de0839f6a9",
   "finding_id": "fnd_986513aaeef0",
   "status": "done",
   "llm_mode": "recorded",
   "n": 5,
   "m": 2,
   "rule_version": "VR-1",
   "intervention": {
    "step_id": "s4",
    "patches": {
     "refund_amount": 661.98
    },
    "source": "truth",
    "description": "Set Refund Calculator.refund_amount to the value its contract or the source of truth requires"
   },
   "summary": {
    "rule_version": "VR-1",
    "n_planned": 5,
    "n_completed": 5,
    "k_pass": 0,
    "m_planned": 2,
    "m_completed": 2,
    "c_pass": 0,
    "ci_low": 0.0,
    "ci_high": 0.4345,
    "verdict": "refuted",
    "explanation": "Fixing this step did not change the outcome (0/5 replays passed): it is not the origin."
   },
   "verdict": "refuted",
   "error": "",
   "created_at": "2026-10-13T19:11:30.850545",
   "finished_at": "2026-10-13T19:11:31.095547",
   "replays": [
    {
     "kind": "intervention",
     "idx": 0,
     "seed": 1000,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your account, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 1,
     "seed": 1001,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 2,
     "seed": 1002,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your account, which will be returned to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 3,
     "seed": 1003,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing your refund of $661.98 to the original gift card used for payment, which will be credited back to you shortly."
     }
    },
    {
     "kind": "intervention",
     "idx": 4,
     "seed": 1004,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "control",
     "idx": 0,
     "seed": 1500,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.00 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    },
    {
     "kind": "control",
     "idx": 1,
     "seed": 1501,
     "completed": true,
     "passed": false,
     "judgement": {
      "passed": false,
      "fixed": [],
      "still_failing": [
       "CHK-OUT-1"
      ],
      "regressions": []
     },
     "final_output": {
      "message": "We are processing a refund of $662.00 to the original gift card associated with your purchase, which will be returned to you shortly."
     }
    }
   ]
  }
 ],
 "reviews": [],
 "evidence": [
  {
   "id": "ev_a5889094984b",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "check_computation",
   "title": "Check CHK-OUT-1 computation",
   "payload": {
    "check_id": "CHK-OUT-1",
    "check_version": 1,
    "scope": "outcome",
    "step": "s5",
    "type": "truth",
    "severity": "high",
    "status": "fail",
    "observed": 662.0,
    "expected": 662.23,
    "message": "Stated refund equals the catalogue total of the refunded items: observed 662.0, expected 662.23",
    "computation": {
     "expression": "approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
     "tolerance": 0.01,
     "value": false,
     "resolved": {
      "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
      "s3.items_to_refund": [
       {
        "item_id": "8926329222",
        "name": "Luggage Set",
        "price": 452.03
       },
       {
        "item_id": "5067898160",
        "name": "Pet Bed",
        "price": 209.95
       }
      ]
     },
     "truth_calls": [
      {
       "function": "catalog_total",
       "arguments": [
        [
         "8926329222",
         "5067898160"
        ]
       ],
       "returned": 662.23
      }
     ],
     "operands": [
      662.0,
      662.23
     ]
    },
    "data_snapshot": "taubench_retail_v1"
   },
   "sha256": "36e4a44e6b102c90ec90175b146f339421e7a81ec0c4f41613e68cdb981c95b4",
   "reproduce": "Re-evaluate check CHK-OUT-1 on run run_67a305834a29; data snapshot taubench_retail_v1",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_5dbe8c57953a",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "step_snapshot",
   "title": "Step s5 (Writer) snapshot",
   "payload": {
    "step_id": "s5",
    "agent": "Writer",
    "inputs": {
     "s4.refund_amount": 662.0,
     "s3.refund_method": "gift_card_9450778",
     "s3.eligible": true,
     "s3.reason": "delivered order owned by the customer"
    },
    "outputs": {
     "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
    },
    "error": null
   },
   "sha256": "5418d67087da67a730bc730b4da93b47aefc4d568fb61674e0b967bda21c55f5",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_ddb94881d498",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 1: Order Lookup (provenance)",
   "payload": {
    "rank": 1,
    "step_id": "s2",
    "agent": "Order Lookup",
    "method": "provenance",
    "evidence_kind": "truth_mismatch",
    "score": 0.81,
    "rationale": "Order Lookup's output contradicts the source of truth (CT-LOOKUP): observed 661.98, expected 662.23.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s2",
      "to": "s5",
      "path": [
       {
        "step_id": "s2",
        "agent": "Order Lookup",
        "carries": "payment_method"
       },
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-LOOKUP",
      "status": "fail",
      "observed": 661.98,
      "expected": 662.23,
      "computation": {
       "expression": "approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
       "tolerance": 0.005,
       "value": false,
       "resolved": {
        "s2.items": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [
        {
         "function": "catalog_total",
         "arguments": [
          [
           "8926329222",
           "5067898160"
          ]
         ],
         "returned": 662.23
        }
       ],
       "operands": [
        661.98,
        662.23
       ]
      }
     }
    ]
   },
   "sha256": "22b358c252107ba1466373a5e07bb3271fd893a158f32122d73749c52b4366f8",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_164a4ad2251e",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 2: Refund Calculator (provenance)",
   "payload": {
    "rank": 2,
    "step_id": "s4",
    "agent": "Refund Calculator",
    "method": "provenance",
    "evidence_kind": "contract_fail",
    "score": 0.72,
    "rationale": "Refund Calculator broke its own contract (CT-CALC): observed 662.0, expected 661.98.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s4",
      "to": "s5",
      "path": [
       {
        "step_id": "s4",
        "agent": "Refund Calculator",
        "carries": "refund_amount"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-CALC",
      "status": "fail",
      "observed": 662.0,
      "expected": 661.98,
      "computation": {
       "expression": "approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
       "tolerance": 0.01,
       "value": false,
       "resolved": {
        "s4.refund_amount": 662.0,
        "s3.items_to_refund": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [],
       "operands": [
        662.0,
        661.98
       ]
      }
     }
    ]
   },
   "sha256": "c198214eb78358f2264e251bb03931609459d9af648746c3a547e74cf617b4e3",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_211d774ffd11",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 3: Intake (provenance)",
   "payload": {
    "rank": 3,
    "step_id": "s1",
    "agent": "Intake",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.081,
    "rationale": "Intake is consistent with its inputs (CT-INTAKE passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s1",
      "to": "s5",
      "path": [
       {
        "step_id": "s1",
        "agent": "Intake",
        "carries": "item_names"
       },
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-INTAKE",
      "status": "pass",
      "observed": null,
      "expected": null,
      "computation": {
       "expression": "s1.order_id == task.order_id and len(s1.item_names) > 0",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s1.order_id": "#W1023987",
        "task.order_id": "#W1023987",
        "s1.item_names": [
         "Luggage Set",
         "Pet Bed"
        ]
       },
       "truth_calls": [],
       "operands": null
      }
     }
    ]
   },
   "sha256": "1913c4784c75777e910345273fa76de1241d58bc5c4673a5b9bfd5c07a9d46a1",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_be1136540c3b",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 4: Policy (provenance)",
   "payload": {
    "rank": 4,
    "step_id": "s3",
    "agent": "Policy",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.09,
    "rationale": "Policy is consistent with its inputs (CT-POLICY passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s3",
      "to": "s5",
      "path": [
       {
        "step_id": "s3",
        "agent": "Policy",
        "carries": "reason"
       },
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-POLICY",
      "status": "pass",
      "observed": null,
      "expected": null,
      "computation": {
       "expression": "truth.same_prices(s3.items_to_refund, s2.items)",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s3.items_to_refund": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ],
        "s2.items": [
         {
          "item_id": "8926329222",
          "name": "Luggage Set",
          "price": 452.03
         },
         {
          "item_id": "5067898160",
          "name": "Pet Bed",
          "price": 209.95
         }
        ]
       },
       "truth_calls": [
        {
         "function": "same_prices",
         "arguments": [
          [
           {
            "item_id": "8926329222",
            "name": "Luggage Set",
            "price": 452.03
           },
           {
            "item_id": "5067898160",
            "name": "Pet Bed",
            "price": 209.95
           }
          ],
          [
           {
            "item_id": "8926329222",
            "name": "Luggage Set",
            "price": 452.03
           },
           {
            "item_id": "5067898160",
            "name": "Pet Bed",
            "price": 209.95
           }
          ]
         ],
         "returned": true
        }
       ],
       "operands": null
      }
     }
    ]
   },
   "sha256": "5195f2efc283a76a9411de4acaa5fc4d38e7326dde45dbc4384517ed101ddf7d",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_3ffdbdb385a0",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "provenance_path",
   "title": "Hypothesis 5: Writer (provenance)",
   "payload": {
    "rank": 5,
    "step_id": "s5",
    "agent": "Writer",
    "method": "provenance",
    "evidence_kind": "consistent",
    "score": 0.1,
    "rationale": "Writer is consistent with its inputs (CT-WRITER passed): it passed on what it was given.",
    "evidence": [
     {
      "type": "provenance_path",
      "from": "s5",
      "to": "s5",
      "path": [
       {
        "step_id": "s5",
        "agent": "Writer"
       }
      ]
     },
     {
      "type": "check",
      "check_id": "CT-WRITER",
      "status": "pass",
      "observed": 662.0,
      "expected": 662.0,
      "computation": {
       "expression": "approx(number_in(s5.message), s4.refund_amount)",
       "tolerance": 0.01,
       "value": true,
       "resolved": {
        "s5.message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business.",
        "s4.refund_amount": 662.0
       },
       "truth_calls": [],
       "operands": [
        662.0,
        662.0
       ]
      }
     }
    ]
   },
   "sha256": "4ddba862f9afc8f07ae1b027390e3db7dc5cde39c04b5c14e4919059b9e946fd",
   "reproduce": "Rank origin hypotheses with granite_core.attribution.attribute on the stored trace",
   "created_at": "2026-10-13T19:11:29.089883",
   "hash_valid": true
  },
  {
   "id": "ev_16e073d4ab00",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "verdict_computation",
   "title": "Verdict for Refund Calculator: refuted",
   "payload": {
    "rule": "VR-1",
    "summary": {
     "rule_version": "VR-1",
     "n_planned": 5,
     "n_completed": 5,
     "k_pass": 0,
     "m_planned": 2,
     "m_completed": 2,
     "c_pass": 0,
     "ci_low": 0.0,
     "ci_high": 0.4345,
     "verdict": "refuted",
     "explanation": "Fixing this step did not change the outcome (0/5 replays passed): it is not the origin."
    },
    "intervention": {
     "step_id": "s4",
     "patches": {
      "refund_amount": 661.98
     },
     "source": "truth",
     "description": "Set Refund Calculator.refund_amount to the value its contract or the source of truth requires"
    },
    "seeds": {
     "intervention-1": 1000,
     "intervention-2": 1001,
     "intervention-3": 1002,
     "intervention-4": 1003,
     "intervention-5": 1004,
     "control-1": 1500,
     "control-2": 1501
    }
   },
   "sha256": "d324651049828b2e5f9da6c2245caf708dca290c6a89845dee3c033209515027",
   "reproduce": "Re-run experiment exp_530d2d009849 with the same seeds; replays are deterministic given the recording",
   "created_at": "2026-10-13T19:11:31.098552",
   "hash_valid": true
  },
  {
   "id": "ev_be0f917cf21c",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "verdict_computation",
   "title": "Verdict for Order Lookup: confirmed",
   "payload": {
    "rule": "VR-1",
    "summary": {
     "rule_version": "VR-1",
     "n_planned": 5,
     "n_completed": 5,
     "k_pass": 5,
     "m_planned": 2,
     "m_completed": 2,
     "c_pass": 0,
     "ci_low": 0.5655,
     "ci_high": 1.0,
     "verdict": "confirmed",
     "explanation": "With the fix applied the outcome was correct in 5/5 replays, and in 0/2 controls without it: the fix, not luck, changed the result."
    },
    "intervention": {
     "step_id": "s2",
     "patches": {
      "items": [
       {
        "item_id": "8926329222",
        "name": "Luggage Set",
        "price": 452.28
       },
       {
        "item_id": "5067898160",
        "name": "Pet Bed",
        "price": 209.95
       }
      ]
     },
     "source": "truth",
     "description": "Set Order Lookup.items to the value its contract or the source of truth requires"
    },
    "seeds": {
     "intervention-1": 1000,
     "intervention-2": 1001,
     "intervention-3": 1002,
     "intervention-4": 1003,
     "intervention-5": 1004,
     "control-1": 1500,
     "control-2": 1501
    }
   },
   "sha256": "a335d1e193afb5b99688397b74b2be342192cce23c623c17424e7cf14de7405b",
   "reproduce": "Re-run experiment exp_528356da88e0 with the same seeds; replays are deterministic given the recording",
   "created_at": "2026-10-13T19:11:31.303771",
   "hash_valid": true
  },
  {
   "id": "ev_fc96178c5025",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "replay_output",
   "title": "Replay outputs for Refund Calculator",
   "payload": {
    "replays": [
     {
      "kind": "intervention",
      "index": 0,
      "seed": 1000,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your account, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 1,
      "seed": 1001,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 2,
      "seed": 1002,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your account, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 3,
      "seed": 1003,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing your refund of $661.98 to the original gift card used for payment, which will be credited back to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 4,
      "seed": 1004,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "control",
      "index": 0,
      "seed": 1500,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $662.00 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "control",
      "index": 1,
      "seed": 1501,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $662.00 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     }
    ]
   },
   "sha256": "269e037cd18893030034518e49894d04e20ef91725bb443183ef2605485e0926",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:31.098552",
   "hash_valid": true
  },
  {
   "id": "ev_afc8f3556948",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "replay_output",
   "title": "Replay outputs for Order Lookup",
   "payload": {
    "replays": [
     {
      "kind": "intervention",
      "index": 0,
      "seed": 1000,
      "completed": true,
      "passed": true,
      "final_output": {
       "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 1,
      "seed": 1001,
      "completed": true,
      "passed": true,
      "final_output": {
       "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 2,
      "seed": 1002,
      "completed": true,
      "passed": true,
      "final_output": {
       "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 3,
      "seed": 1003,
      "completed": true,
      "passed": true,
      "final_output": {
       "message": "We are processing your refund of $662.23 to the original gift card associated with your purchase. This amount will be returned to you shortly."
      }
     },
     {
      "kind": "intervention",
      "index": 4,
      "seed": 1004,
      "completed": true,
      "passed": true,
      "final_output": {
       "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "control",
      "index": 0,
      "seed": 1500,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase, which will be returned to you shortly."
      }
     },
     {
      "kind": "control",
      "index": 1,
      "seed": 1501,
      "completed": true,
      "passed": false,
      "final_output": {
       "message": "We are processing a refund of $661.98 to the original gift card associated with your purchase. The refund will be returned to the same gift card balance."
      }
     }
    ]
   },
   "sha256": "b58d5cfb0f185e9c107070758cd4a5da40d3d76a9c29fd8b7eb7e7d524219d17",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:31.303771",
   "hash_valid": true
  },
  {
   "id": "ev_6fe011fa1d08",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "diff",
   "title": "Original vs fixed output (Refund Calculator)",
   "payload": {
    "original": {
     "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
    },
    "with_fix": {
     "message": "We are processing a refund of $661.98 to the original gift card associated with your account, which will be returned to you shortly."
    },
    "patched": {
     "refund_amount": 661.98
    }
   },
   "sha256": "c653d9ae082a1a780a13b13a2280241341e3cad755095530afe51d61962d2f37",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:31.098552",
   "hash_valid": true
  },
  {
   "id": "ev_62059336d9f5",
   "run_id": "run_67a305834a29",
   "finding_id": "fnd_986513aaeef0",
   "type": "diff",
   "title": "Original vs fixed output (Order Lookup)",
   "payload": {
    "original": {
     "message": "Dear valued customer, your refund of $662.00 will be returned to the original gift card used for payment. We apologize for any inconvenience and appreciate your business."
    },
    "with_fix": {
     "message": "We are processing a refund of $662.23 to the original gift card associated with your purchase, which will be returned to you shortly."
    },
    "patched": {
     "items": [
      {
       "item_id": "8926329222",
       "name": "Luggage Set",
       "price": 452.28
      },
      {
       "item_id": "5067898160",
       "name": "Pet Bed",
       "price": 209.95
      }
     ]
    }
   },
   "sha256": "cf7b72d2a91ce7150eea64947cd3d025939ede4e9fdf9bc29f4f18af662954b6",
   "reproduce": "",
   "created_at": "2026-10-13T19:11:31.303771",
   "hash_valid": true
  }
 ],
 "allowed_actions": [
  "accept",
  "reject",
  "request_info"
 ]
};
