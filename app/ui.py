from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Patient QA Agent</title>
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

    /* Dev/test toggle */
    .dev-toggle {
      margin-top: 6px;
      font-size: 12px;
      color: var(--muted);
    }
    .dev-toggle input {
      margin-right: 6px;
    }

    /* Chat UI */
    .chat {
      margin-top: 14px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,0.20);
      border-radius: 14px;
      padding: 12px;
      min-height: 260px;
      max-height: 460px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .msg {
      padding: 10px 12px;
      border-radius: 14px;
      border: 1px solid var(--border);
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.4;
      max-width: 92%;
    }

    /* User from LEFT (your preference) */
    .msg.user {
      align-self: flex-start;
      background: rgba(42,109,244,0.15);
      border-color: rgba(42,109,244,0.45);
    }
    .msg.assistant {
      align-self: flex-start;
      background: rgba(255,255,255,0.06);
    }
    .msg.meta {
      align-self: center;
      background: rgba(245,158,11,0.12);
      border-color: rgba(245,158,11,0.35);
      color: #ffd9a3;
      font-size: 13px;
      max-width: 100%;
    }

    /* Chat input row (like ChatGPT) */
    .composer {
      margin-top: 12px;
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }
    .composer textarea {
      min-height: 44px;
      max-height: 140px;
      resize: vertical;
    }
    .small { color: var(--muted); font-size: 12px; margin-top: 8px; }
    .hint {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }
    code { background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 8px; }
    a { color: #9cc0ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
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
      <!-- Context panel -->
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

      <!-- dev/test toggle -->
      <div class="dev-toggle">
        <label>
          <input type="checkbox" id="allow_no_context" />
          Allow general questions without medical history (dev / test only)
        </label>
      </div>

      <div class="btns">
        <button id="exBtn" onclick="loadExample()">Load Example</button>
        <button class="danger" id="unsafeBtn" onclick="loadUnsafe()">Unsafe Example</button>
        <button id="clearBtn" onclick="clearAll()">Clear</button>
        <button id="resetChatBtn" onclick="resetChat(true)">New chat</button>

        <div class="right-meta">
          <span class="badge">Latency: <b id="latency">—</b> ms</span>
          <span class="badge">Status: <span class="dot" id="statusDot"></span> <span id="statusText">idle</span></span>
        </div>
      </div>

      <div class="warnbox" id="warnbox"></div>

      <!-- Chat area -->
      <div id="chat" class="chat"></div>

      <!-- ChatGPT-like input -->
      <div class="composer">
        <textarea id="chatInput" placeholder="Message... (Enter to send, Shift+Enter for new line)"></textarea>
        <button class="primary" id="sendBtn" onclick="sendChat()">Send</button>
      </div>

      <div class="small" id="smallNote"></div>
      <div class="hint">
        Chat state & context are saved in this browser until you start a new chat or clear data.
        Tip: open <code>/docs</code> to test <code>/ask</code> directly using Swagger.
      </div>
    </div>
  </div>

<script>
const STORAGE_KEY = "patient_qa_chat_v2";

let chatHistory = []; // {role:"user"|"assistant"|"meta", content:string}

function chatEl() { return document.getElementById("chat"); }
function inputEl() { return document.getElementById("chatInput"); }

function setBusy(busy, text) {
  const spin = document.getElementById("spin");
  const pillText = document.getElementById("pillText");
  const btns = ["sendBtn","exBtn","unsafeBtn","clearBtn","resetChatBtn"].map(
    id => document.getElementById(id)
  );
  if (busy) {
    spin.classList.add("show");
    pillText.textContent = text || "Working...";
    btns.forEach(b => b.disabled = true);
    inputEl().disabled = true;
  } else {
    spin.classList.remove("show");
    pillText.textContent = text || "Ready";
    btns.forEach(b => b.disabled = false);
    inputEl().disabled = false;
    updateSendEnabled();
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

function addMsg(role, text) {
  const el = document.createElement("div");
  el.className = "msg " + role;
  el.textContent = text;
  chatEl().appendChild(el);
  chatEl().scrollTop = chatEl().scrollHeight;
  return el;
}

function clearChatUI() { chatEl().innerHTML = ""; }

// ----- localStorage helpers -----
function saveState() {
  try {
    const state = {
      chatHistory,
      medical_history: document.getElementById("medical_history").value,
      diagnoses: document.getElementById("diagnoses").value,
      symptoms: document.getElementById("symptoms").value,
      allow_no_context: document.getElementById("allow_no_context").checked,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (e) {
    console.warn("localStorage save failed:", e);
  }
}

function restoreState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      resetChat(false);
      addMsg("meta", "New chat started. Add your medical context, then ask a question.");
      return;
    }
    const state = JSON.parse(raw);

    document.getElementById("medical_history").value = state.medical_history || "";
    document.getElementById("diagnoses").value = state.diagnoses || "";
    document.getElementById("symptoms").value = state.symptoms || "";
    document.getElementById("allow_no_context").checked = !!state.allow_no_context;

    chatHistory = Array.isArray(state.chatHistory) ? state.chatHistory : [];

    clearChatUI();
    if (chatHistory.length === 0) {
      addMsg("meta", "Previous session was empty. Start a new chat.");
    } else {
      for (const m of chatHistory) {
        if (!m || !m.role || !m.content) continue;
        addMsg(m.role, m.content);
      }
    }

    setStatus(null, "restored");
    document.getElementById("latency").textContent = "—";
    document.getElementById("smallNote").textContent =
      "Restored last chat from this browser.";
    showWarn("");
  } catch (e) {
    console.warn("localStorage restore failed:", e);
    resetChat(false);
    addMsg("meta", "Could not restore previous chat. Starting fresh.");
  }
}

function clearStorage() {
  try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
}

// ----- logic -----
function resetChat(clearStored = false) {
  chatHistory = [];
  clearChatUI();
  addMsg("meta", "New chat started. Type your message below.");
  setStatus(null, "idle");
  document.getElementById("latency").textContent = "—";
  document.getElementById("smallNote").textContent = "";
  showWarn("");
  inputEl().value = "";
  if (clearStored) {
    clearStorage();
  } else {
    saveState();
  }
  updateSendEnabled();
}

// Simple helper: check if we have any medical context
function hasAnyContext() {
  const mh = document.getElementById("medical_history").value.trim();
  const dx = document
    .getElementById("diagnoses")
    .value.split(",")
    .map(s => s.trim())
    .filter(Boolean);
  const sx = document
    .getElementById("symptoms")
    .value.split(",")
    .map(s => s.trim())
    .filter(Boolean);
  return Boolean(mh || dx.length || sx.length);
}

// Build payload that will be sent to /ask
function payloadFromContext(questionText) {
  const mh = document.getElementById("medical_history").value;
  const dx = document
    .getElementById("diagnoses")
    .value.split(",")
    .map(s => s.trim())
    .filter(Boolean);
  const sx = document
    .getElementById("symptoms")
    .value.split(",")
    .map(s => s.trim())
    .filter(Boolean);
  const allowNoCtx = document.getElementById("allow_no_context").checked;

  return {
    medical_history: mh,
    diagnoses: dx,
    symptoms: sx,
    question: questionText,
    messages: chatHistory.slice(-8),
    allow_no_context: allowNoCtx,
  };
}

// Enable/disable Send button
function updateSendEnabled() {
  const sendBtn = document.getElementById("sendBtn");
  const text = inputEl().value || "";
  const hasText = text.trim().length > 0;

  const allowNoCtx = document.getElementById("allow_no_context").checked;
  const hasCtx = hasAnyContext();

  // need a message AND (context OR dev flag)
  const ok = hasText && (hasCtx || allowNoCtx);
  sendBtn.disabled = !ok;

  if (!hasCtx && !allowNoCtx) {
    showWarn("Add at least one: medical history OR diagnoses OR symptoms (or enable dev option).");
    setStatus(null, "waiting context");
    return;
  }

  if (!hasText) {
    showWarn("");
    if (chatHistory.length === 0) setStatus(null, "idle");
    return;
  }

  showWarn("");
  if (document.getElementById("statusText").textContent.startsWith("waiting")) {
    setStatus(null, "idle");
  }
}

function loadExample() {
  document.getElementById("medical_history").value =
    "Diagnosed with type 2 diabetes last year. Experiencing fatigue and increased thirst.";
  document.getElementById("diagnoses").value = "Type 2 Diabetes";
  document.getElementById("symptoms").value = "fatigue, increased thirst";
  document.getElementById("allow_no_context").checked = false;

  resetChat(false);
  addMsg("meta", "Example loaded. Ask a question in the chat input below.");
  saveState();
  updateSendEnabled();
}

function loadUnsafe() {
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

  document.getElementById("allow_no_context").checked = false;

  resetChat(false);
  addMsg("meta", "Unsafe example loaded. Now type: “What medicine should I take?”");
  inputEl().value = "What medicine should I take to cure this?";
  saveState();
  updateSendEnabled();
}

function clearAll() {
  document.getElementById("medical_history").value = "";
  document.getElementById("diagnoses").value = "";
  document.getElementById("symptoms").value = "";
  // keep dev checkbox as-is
  resetChat(true);
  addMsg("meta", "All fields cleared. Add context, or enable dev option, then chat.");
  saveState();
  updateSendEnabled();
}

async function sendChat() {
  const text = (inputEl().value || "").trim();
  if (!text) return;

  const latencyEl = document.getElementById("latency");
  const small = document.getElementById("smallNote");
  const allowNoCtx = document.getElementById("allow_no_context").checked;
  const hasCtx = hasAnyContext();

  if (!hasCtx && !allowNoCtx) {
    setStatus(false, "missing context");
    addMsg("meta", "Please provide at least one: medical history OR diagnoses OR symptoms, or enable the dev option.");
    showWarn("Add context or enable the dev option to ask general questions.");
    return;
  }

  const payload = payloadFromContext(text);

  addMsg("user", text);
  chatHistory.push({ role: "user", content: text });
  saveState();

  inputEl().value = "";
  updateSendEnabled();

  setBusy(true, "Asking...");
  setStatus(null, "requesting");
  small.textContent = "";
  latencyEl.textContent = "—";

  const assistantBubble = addMsg("assistant", "…");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });

    const latencyHeader = res.headers.get("x-latency-ms");
    if (latencyHeader) latencyEl.textContent = latencyHeader;

    const dataText = await res.text();
    let obj = null;
    try { obj = JSON.parse(dataText); } catch (_) {}

    if (!res.ok) {
      setStatus(false, "error");
      const errMsg = obj?.error ? ("Error: " + obj.error) : ("Error: HTTP " + res.status);
      assistantBubble.textContent = errMsg;
      small.textContent = "Server returned HTTP " + res.status + " " + res.statusText;
      saveState();
      return;
    }

    setStatus(true, "ok");
    const answer = obj?.answer ?? dataText;
    assistantBubble.textContent = answer;
    chatHistory.push({ role: "assistant", content: answer });
    small.textContent = "Success.";
    saveState();
  } catch (err) {
    setStatus(false, "network error");
    assistantBubble.textContent = "Network error: " + String(err);
    small.textContent = "Could not reach the server. Is it running?";
  } finally {
    setBusy(false, "Ready");
  }
}

/* Enter to send, Shift+Enter for newline */
inputEl().addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    if (!document.getElementById("sendBtn").disabled) sendChat();
  }
});

/* Live validation + persistence */
["medical_history","diagnoses","symptoms"].forEach(id => {
  document.getElementById(id).addEventListener("input", () => {
    updateSendEnabled();
    saveState();
  });
});
document.getElementById("allow_no_context").addEventListener("change", () => {
  updateSendEnabled();
  saveState();
});
inputEl().addEventListener("input", () => {
  updateSendEnabled();
  saveState();
});

/* On load: restore from localStorage if possible */
restoreState();
updateSendEnabled();
</script>

</body>
</html>
"""

@router.get("/demo", response_class=HTMLResponse)
def demo():
    return HTMLResponse(HTML)
