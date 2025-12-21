from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Patient QA Agent Demo</title>
  <style>
    :root {
      --bg: #0b1220;
      --card: #111a2e;
      --muted: #9fb0d0;
      --text: #e9eefc;
      --border: rgba(255,255,255,0.10);
      --btn: #2a6df4;
      --btn2: #2a2f42;
      --danger: #ef4444;
      --ok: #22c55e;
      --warn: #f59e0b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: radial-gradient(1200px 600px at 20% 0%, rgba(42,109,244,0.25), transparent),
                  radial-gradient(900px 500px at 100% 30%, rgba(34,197,94,0.12), transparent),
                  var(--bg);
      color: var(--text);
    }
    .wrap { max-width: 980px; margin: 28px auto; padding: 0 16px; }
    .top {
      display: flex; align-items: flex-start; justify-content: space-between;
      gap: 16px; margin-bottom: 14px;
    }
    h1 { font-size: 22px; margin: 0 0 6px; }
    .sub { color: var(--muted); font-size: 14px; line-height: 1.4; }
    .pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 10px; border: 1px solid var(--border); border-radius: 999px;
      background: rgba(255,255,255,0.03);
      font-size: 13px; color: var(--muted);
      white-space: nowrap;
    }
    .card {
      background: rgba(17,26,46,0.85);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 18px 40px rgba(0,0,0,0.28);
    }
    label { display: block; margin: 12px 0 6px; color: var(--muted); font-size: 13px; }
    textarea, input {
      width: 100%;
      padding: 12px 12px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.04);
      color: var(--text);
      outline: none;
    }
    textarea { min-height: 110px; resize: vertical; }
    input:focus, textarea:focus { border-color: rgba(42,109,244,0.65); }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    @media (max-width: 820px) { .row { grid-template-columns: 1fr; } }

    .btns {
      display: flex; flex-wrap: wrap; gap: 10px;
      margin-top: 14px;
      align-items: center;
    }
    button {
      border: 1px solid var(--border);
      background: var(--btn2);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor: pointer;
      font-weight: 600;
      font-size: 14px;
    }
    button.primary {
      background: linear-gradient(180deg, rgba(42,109,244,1), rgba(42,109,244,0.75));
      border-color: rgba(42,109,244,0.7);
    }
    button.danger {
      background: rgba(239,68,68,0.15);
      border-color: rgba(239,68,68,0.5);
    }
    button:disabled { opacity: 0.55; cursor: not-allowed; }

    .right-meta {
      margin-left: auto; display: flex; gap: 10px; align-items: center; color: var(--muted);
      font-size: 13px;
    }

    .badge {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 10px; border-radius: 12px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.03);
      color: var(--muted);
      font-size: 13px;
    }

    .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--muted); opacity: 0.8; }
    .dot.ok { background: var(--ok); }
    .dot.bad { background: var(--danger); }
    .dot.warn { background: var(--warn); }

    .outwrap { margin-top: 14px; }
    pre {
      margin: 0;
      padding: 14px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,0.25);
      color: var(--text);
      white-space: pre-wrap;
      word-break: break-word;
      min-height: 140px;
    }
    .small { color: var(--muted); font-size: 12px; margin-top: 8px; }

    .spinner {
      width: 16px; height: 16px;
      border: 2px solid rgba(255,255,255,0.25);
      border-top-color: rgba(255,255,255,0.9);
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      display: none;
    }
    .spinner.show { display: inline-block; }
    @keyframes spin { to { transform: rotate(360deg);} }

    .hint {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    code { background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 8px; }
    a { color: #9cc0ff; text-decoration: none; }
    a:hover { text-decoration: underline; }

    .warnbox {
      margin-top: 10px;
      padding: 10px 12px;
      border: 1px solid rgba(245,158,11,0.45);
      background: rgba(245,158,11,0.10);
      border-radius: 12px;
      color: #ffd9a3;
      font-size: 13px;
      display: none;
    }
    .warnbox.show { display: block; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div>
        <h1>Patient Medical History Q&A (Non-Clinical)</h1>
        <div class="sub">
          Educational explanations only — no diagnosis, treatment, or personal medical advice.
          Try the <a href="/docs" target="_blank" rel="noreferrer">API docs</a> too.
        </div>
      </div>
      <div class="pill">
        <span class="spinner" id="spin"></span>
        <span id="pillText">Ready</span>
      </div>
    </div>

    <div class="card">
      <label>Medical history</label>
      <textarea id="medical_history">Diagnosed with type 2 diabetes last year. Experiencing fatigue and increased thirst.</textarea>

      <div class="row">
        <div>
          <label>Diagnoses (comma-separated)</label>
          <input id="diagnoses" value="Type 2 Diabetes" />
        </div>
        <div>
          <label>Symptoms (comma-separated)</label>
          <input id="symptoms" value="fatigue, increased thirst" />
        </div>
      </div>

      <label>Question</label>
      <input id="question" value="Why do I feel tired?" />

      <div class="btns">
        <button class="primary" id="askBtn" onclick="send()">Ask</button>
        <button id="exBtn" onclick="loadExample()">Load Example</button>
        <button class="danger" id="unsafeBtn" onclick="loadUnsafe()">Unsafe Example</button>
        <button id="clearBtn" onclick="clearAll()">Clear</button>
        <button id="copyBtn" onclick="copyJSON()">Copy JSON</button>

        <div class="right-meta">
          <span class="badge">Latency: <b id="latency">—</b> ms</span>
          <span class="badge">Status: <span class="dot" id="statusDot"></span> <span id="statusText">idle</span></span>
        </div>
      </div>

      <div class="warnbox" id="warnbox"></div>

      <div class="outwrap">
        <label>Response</label>
        <pre id="out">(waiting...)</pre>
        <div class="small" id="smallNote"></div>
        <div class="hint">
          Tip: open <code>/docs</code> to test <code>/ask</code> directly using Swagger.
        </div>
      </div>
    </div>
  </div>

<script>
function setBusy(busy, text) {
  const spin = document.getElementById("spin");
  const pillText = document.getElementById("pillText");
  const btns = ["askBtn","exBtn","unsafeBtn","clearBtn","copyBtn"].map(id => document.getElementById(id));
  if (busy) {
    spin.classList.add("show");
    pillText.textContent = text || "Working...";
    btns.forEach(b => b.disabled = true);
  } else {
    spin.classList.remove("show");
    pillText.textContent = text || "Ready";
    btns.forEach(b => b.disabled = false);
    updateAskEnabled(); // re-apply validation
  }
}

function setStatus(ok, text) {
  const dot = document.getElementById("statusDot");
  const st = document.getElementById("statusText");
  dot.classList.remove("ok", "bad", "warn");
  if (ok === true) dot.classList.add("ok");
  if (ok === false) dot.classList.add("bad");
  if (ok === null) dot.classList.add("warn");
  st.textContent = text || "idle";
}

function showWarn(msg) {
  const w = document.getElementById("warnbox");
  if (!msg) {
    w.classList.remove("show");
    w.textContent = "";
    return;
  }
  w.textContent = msg;
  w.classList.add("show");
}

function payloadFromInputs() {
  return {
    medical_history: document.getElementById("medical_history").value,
    diagnoses: document.getElementById("diagnoses").value.split(",").map(s => s.trim()).filter(Boolean),
    symptoms: document.getElementById("symptoms").value.split(",").map(s => s.trim()).filter(Boolean),
    question: document.getElementById("question").value
  };
}

function hasAnyContext(payload) {
  const mh = (payload.medical_history || "").trim();
  const dx = (payload.diagnoses || []).length;
  const sx = (payload.symptoms || []).length;
  return Boolean(mh || dx || sx);
}

function hasQuestion(payload) {
  return Boolean((payload.question || "").trim().length >= 3);
}

function updateAskEnabled() {
  const askBtn = document.getElementById("askBtn");
  const payload = payloadFromInputs();

  // Ask enabled only if question exists AND at least one context field exists
  const ok = hasQuestion(payload) && hasAnyContext(payload);

  askBtn.disabled = !ok;

  // Show a helpful hint when disabled
  if (!ok) {
    if (!hasQuestion(payload)) {
      showWarn("Type a question (at least 3 characters) to enable Ask.");
      setStatus(null, "waiting input");
      return;
    }
    if (!hasAnyContext(payload)) {
      showWarn("Add at least one: medical history OR diagnoses OR symptoms (then Ask will be enabled).");
      setStatus(null, "waiting context");
      return;
    }
  } else {
    showWarn("");
    if (document.getElementById("statusText").textContent.startsWith("waiting")) {
      setStatus(null, "idle");
    }
  }
}

function loadExample() {
  document.getElementById("medical_history").value =
    "Diagnosed with type 2 diabetes last year. Experiencing fatigue and increased thirst.";
  document.getElementById("diagnoses").value = "Type 2 Diabetes";
  document.getElementById("symptoms").value = "fatigue, increased thirst";
  document.getElementById("question").value = "Why do I feel tired?";
  document.getElementById("out").textContent = "(waiting...)";
  document.getElementById("latency").textContent = "—";
  document.getElementById("smallNote").textContent = "";
  setStatus(null, "idle");
  showWarn("");
  updateAskEnabled();
}

function loadUnsafe() {
  // keep some context so it can be sent
  if (!document.getElementById("medical_history").value.trim()) {
    document.getElementById("medical_history").value =
      "Diagnosed with type 2 diabetes last year. Experiencing fatigue and increased thirst.";
  }
  if (!document.getElementById("diagnoses").value.trim()) {
    document.getElementById("diagnoses").value = "Type 2 Diabetes";
  }
  if (!document.getElementById("symptoms").value.trim()) {
    document.getElementById("symptoms").value = "fatigue, increased thirst";
  }

  document.getElementById("question").value = "What medicine should I take to cure this?";
  document.getElementById("out").textContent = "(waiting...)";
  document.getElementById("latency").textContent = "—";
  document.getElementById("smallNote").textContent = "This should trigger the safety refusal.";
  setStatus(null, "idle");
  showWarn("");
  updateAskEnabled();
}

function clearAll() {
  document.getElementById("medical_history").value = "";
  document.getElementById("diagnoses").value = "";
  document.getElementById("symptoms").value = "";
  document.getElementById("question").value = "";
  document.getElementById("out").textContent = "(cleared)";
  document.getElementById("latency").textContent = "—";
  document.getElementById("smallNote").textContent = "";
  setStatus(null, "waiting input");
  showWarn("Fill the form to enable Ask.");
  updateAskEnabled();
}

async function copyJSON() {
  try {
    const text = document.getElementById("out").textContent;
    await navigator.clipboard.writeText(text);
    document.getElementById("smallNote").textContent = "Copied response JSON to clipboard.";
  } catch (e) {
    document.getElementById("smallNote").textContent = "Copy failed (browser permission).";
  }
}

async function send() {
  const out = document.getElementById("out");
  const latencyEl = document.getElementById("latency");
  const small = document.getElementById("smallNote");

  const payload = payloadFromInputs();

  // ✅ Front-end guard: do not call API if invalid
  if (!hasQuestion(payload)) {
    setStatus(false, "missing question");
    out.textContent = JSON.stringify(
      { error: "Please type a question (at least 3 characters) before asking." },
      null,
      2
    );
    small.textContent = "The API was not called because the question is empty.";
    showWarn("Type a question to enable Ask.");
    return;
  }

  if (!hasAnyContext(payload)) {
    setStatus(false, "missing context");
    out.textContent = JSON.stringify(
      { error: "Please provide at least one: medical history OR diagnoses OR symptoms." },
      null,
      2
    );
    small.textContent = "The API was not called because context is empty.";
    showWarn("Add at least one: medical history OR diagnoses OR symptoms.");
    return;
  }

  setBusy(true, "Asking...");
  setStatus(null, "requesting");
  out.textContent = "Loading...";
  small.textContent = "";
  latencyEl.textContent = "—";
  showWarn("");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    const latencyHeader = res.headers.get("x-latency-ms");
    if (latencyHeader) latencyEl.textContent = latencyHeader;

    const dataText = await res.text();

    let pretty = dataText;
    try {
      const obj = JSON.parse(dataText);
      pretty = JSON.stringify(obj, null, 2);
    } catch (_) {}

    if (!res.ok) {
      setStatus(false, "error");
      out.textContent = pretty;
      small.textContent = "Server returned HTTP " + res.status + " " + res.statusText;
      return;
    }

    setStatus(true, "ok");
    out.textContent = pretty;
    small.textContent = "Success.";
  } catch (err) {
    setStatus(false, "network error");
    out.textContent = JSON.stringify({ error: String(err) }, null, 2);
    small.textContent = "Could not reach the server. Is the container running?";
  } finally {
    setBusy(false, "Ready");
  }
}

// Enable/disable Ask live while typing
["medical_history","diagnoses","symptoms","question"].forEach(id => {
  const el = document.getElementById(id);
  el.addEventListener("input", updateAskEnabled);
});

// initial state
updateAskEnabled();
</script>
</body>
</html>
"""

@router.get("/demo", response_class=HTMLResponse)
def demo():
    return HTMLResponse(HTML)
