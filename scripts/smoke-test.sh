#!/usr/bin/env bash
# Smoke test against a running Granite server: health, UI, and one recorded end-to-end run that must open a finding.
#   scripts/smoke-test.sh http://127.0.0.1:8000     (set PYTHON=/path/to/python to choose the interpreter)
set -euo pipefail
BASE="${1:-http://127.0.0.1:8000}"
PY="${PYTHON:-$(command -v python3 || command -v python)}"

for _ in $(seq 1 30); do
  curl -fs "$BASE/api/health" >/dev/null 2>&1 && break
  sleep 1
done
curl -fs "$BASE/api/health" | grep -q '"status":"ok"' || { echo "FAIL: server not healthy"; exit 1; }
curl -fs -o /dev/null "$BASE/" || { echo "FAIL: web UI not served"; exit 1; }

BODY=$(curl -fs "$BASE/api/workflows/refund_desk/examples" | "$PY" -c "
import sys, json
t = json.load(sys.stdin)[0]
print(json.dumps({'workflow': 'refund_desk', 'fault': 'stale_price', 'mode': 'recorded',
                  'task_input': {k: t[k] for k in ('message', 'email', 'order_id')}}))")
RUN=$(curl -fs -X POST "$BASE/api/runs" -H "Content-Type: application/json" -d "$BODY" \
  | "$PY" -c "import sys, json; print(json.load(sys.stdin)['run_id'])")

for _ in $(seq 1 30); do
  STATUS=$(curl -fs "$BASE/api/runs/$RUN" | "$PY" -c "import sys, json; print(json.load(sys.stdin)['status'])")
  [ "$STATUS" = "completed" ] || [ "$STATUS" = "errored" ] && break
  sleep 1
done
curl -fs "$BASE/api/runs/$RUN" | "$PY" -c "
import sys, json
r = json.load(sys.stdin)
assert r['status'] == 'completed', 'run status: ' + r['status'] + ' ' + r['error']
assert len(r['findings']) == 1, 'expected one finding, got ' + str(len(r['findings']))
print('OK: run', r['id'], 'completed with finding', r['findings'][0]['id'], r['findings'][0]['status'])"
