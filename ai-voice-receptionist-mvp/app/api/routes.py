from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.core.bootstrap import build_demo_container
from app.core.models import CallEvent, CallSource

router = APIRouter()
container = build_demo_container()

APP_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>AI Voice Receptionist MVP</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f6f7f9;
        --panel: #ffffff;
        --ink: #17202a;
        --muted: #5b6673;
        --line: #d9dee5;
        --primary: #0f766e;
        --primary-dark: #115e59;
        --danger: #b42318;
        --soft: #eef7f6;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--bg);
        color: var(--ink);
      }

      main {
        max-width: 1180px;
        margin: 0 auto;
        padding: 28px;
      }

      header {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        align-items: flex-start;
        margin-bottom: 22px;
      }

      h1 {
        margin: 0 0 6px;
        font-size: 30px;
        line-height: 1.15;
      }

      p {
        margin: 0;
        color: var(--muted);
      }

      .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-height: 36px;
        padding: 0 12px;
        border: 1px solid var(--line);
        background: var(--panel);
        border-radius: 8px;
        white-space: nowrap;
      }

      .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 999px;
        background: #22c55e;
      }

      .layout {
        display: grid;
        grid-template-columns: minmax(300px, 390px) minmax(0, 1fr);
        gap: 18px;
      }

      section {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 18px;
      }

      h2 {
        margin: 0 0 14px;
        font-size: 17px;
      }

      label {
        display: block;
        margin: 14px 0 7px;
        color: #364152;
        font-size: 13px;
        font-weight: 650;
      }

      input,
      select,
      textarea {
        width: 100%;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 10px 11px;
        color: var(--ink);
        background: #fff;
        font: inherit;
      }

      textarea {
        min-height: 84px;
        resize: vertical;
      }

      .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
      }

      button {
        border: 0;
        border-radius: 8px;
        padding: 10px 13px;
        background: var(--primary);
        color: white;
        font-weight: 700;
        cursor: pointer;
      }

      button:hover {
        background: var(--primary-dark);
      }

      button.secondary {
        background: #334155;
      }

      button.danger {
        background: var(--danger);
      }

      .quick-tests {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
      }

      .quick-tests button {
        width: 100%;
      }

      .conversation {
        display: grid;
        gap: 12px;
        min-height: 420px;
        align-content: start;
      }

      .message {
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 12px;
        background: #fff;
      }

      .message strong {
        display: block;
        margin-bottom: 5px;
        font-size: 12px;
        text-transform: uppercase;
        color: var(--muted);
      }

      .ai {
        background: var(--soft);
        border-color: #b9dfda;
      }

      .actions {
        margin-top: 9px;
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
      }

      .pill {
        display: inline-flex;
        align-items: center;
        min-height: 24px;
        padding: 0 8px;
        border-radius: 999px;
        background: #e5e7eb;
        color: #334155;
        font-size: 12px;
        font-weight: 650;
      }

      pre {
        min-height: 180px;
        max-height: 320px;
        overflow: auto;
        margin: 0;
        padding: 12px;
        border-radius: 8px;
        background: #101828;
        color: #d1fadf;
        font-size: 12px;
        line-height: 1.5;
      }

      @media (max-width: 820px) {
        main {
          padding: 18px;
        }

        header,
        .layout {
          display: block;
        }

        .status {
          margin-top: 14px;
        }

        section {
          margin-bottom: 16px;
        }
      }
    </style>
  </head>
  <body>
    <main>
      <header>
        <div>
          <h1>AI Voice Receptionist MVP</h1>
          <p>Test missed-call recovery, bookings, FAQs, human transfer, and WhatsApp follow-up.</p>
        </div>
        <div class="status"><span class="status-dot"></span><span id="health">Checking API...</span></div>
      </header>

      <div class="layout">
        <section>
          <h2>Call Simulator</h2>
          <label for="businessId">Business</label>
          <select id="businessId">
            <option value="demo-salon">Namma Glow Salon</option>
            <option value="demo-restaurant">Masala Table</option>
          </select>

          <label for="callId">Call ID</label>
          <input id="callId" />

          <label for="callerNumber">Caller Number</label>
          <input id="callerNumber" value="+919900001111" />

          <div class="button-row">
            <button id="startCall">Start Inbound Call</button>
            <button id="missedCall" class="secondary">Missed Call Recovery</button>
          </div>

          <label for="utterance">Caller Says</label>
          <textarea id="utterance">Can I book an appointment tomorrow at 5 pm? My name is Sneha.</textarea>

          <div class="button-row">
            <button id="sendTurn">Send Turn</button>
            <button id="clear" class="danger">Clear</button>
          </div>

          <label>Quick Tests</label>
          <div class="quick-tests">
            <button class="secondary" data-text="What time do you open?">FAQ</button>
            <button class="secondary" data-text="Is parking available?">Parking</button>
            <button class="secondary" data-text="What services do you offer?">Services</button>
            <button class="secondary" data-text="What is your landmark?">Landmark</button>
            <button class="secondary" data-text="Please connect me to a human">Transfer</button>
            <button class="secondary" data-business="demo-restaurant" data-text="Do you have Jain food?">Jain Food</button>
            <button class="secondary" data-business="demo-restaurant" data-text="Can I book a table for 4 tomorrow at 8 pm? My name is Rahul.">Restaurant</button>
          </div>
        </section>

        <section>
          <h2>Conversation</h2>
          <div id="conversation" class="conversation"></div>
        </section>
      </div>

      <section style="margin-top: 18px;">
        <h2>Simulated WhatsApp Outbox</h2>
        <pre id="outbox">[]</pre>
      </section>
    </main>

    <script>
      const $ = (id) => document.getElementById(id);
      let activeCallStarted = false;

      function newCallId(prefix = "call") {
        return `${prefix}-${Date.now()}`;
      }

      function payloadBase() {
        return {
          business_id: $("businessId").value,
          call_id: $("callId").value.trim(),
          caller_number: $("callerNumber").value.trim(),
        };
      }

      function addMessage(kind, body, actions = []) {
        const el = document.createElement("div");
        el.className = `message ${kind === "AI" ? "ai" : ""}`;
        const actionHtml = actions.length
          ? `<div class="actions">${actions.map((a) => `<span class="pill">${a}</span>`).join("")}</div>`
          : "";
        el.innerHTML = `<strong>${kind}</strong><div>${body}</div>${actionHtml}`;
        $("conversation").prepend(el);
      }

      async function postJson(url, body) {
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || response.statusText);
        }
        return response.json();
      }

      async function refreshOutbox() {
        const response = await fetch("/debug/whatsapp-outbox");
        $("outbox").textContent = JSON.stringify(await response.json(), null, 2);
      }

      async function checkHealth() {
        try {
          const response = await fetch("/health");
          const data = await response.json();
          $("health").textContent = `API ${data.status}`;
        } catch {
          $("health").textContent = "API unavailable";
        }
      }

      async function startInbound() {
        if (!$("callId").value.trim()) $("callId").value = newCallId();
        const result = await postJson("/webhooks/telephony/inbound-call", payloadBase());
        activeCallStarted = true;
        addMessage("AI", result.say, result.actions);
      }

      async function missedCall() {
        $("callId").value = newCallId("missed");
        const result = await postJson("/webhooks/telephony/missed-call", payloadBase());
        activeCallStarted = true;
        addMessage("AI", result.say, result.actions);
        await refreshOutbox();
      }

      async function sendTurn() {
        if (!$("callId").value.trim() || !activeCallStarted) await startInbound();
        const text = $("utterance").value.trim();
        addMessage("Caller", text);
        const result = await postJson(`/calls/${encodeURIComponent($("callId").value.trim())}/turn`, { text });
        addMessage("AI", result.say, result.actions);
        await refreshOutbox();
      }

      $("callId").value = newCallId();
      $("startCall").addEventListener("click", () => startInbound().catch((err) => addMessage("Error", err.message)));
      $("missedCall").addEventListener("click", () => missedCall().catch((err) => addMessage("Error", err.message)));
      $("sendTurn").addEventListener("click", () => sendTurn().catch((err) => addMessage("Error", err.message)));
      $("clear").addEventListener("click", () => {
        $("conversation").innerHTML = "";
        $("callId").value = newCallId();
        activeCallStarted = false;
      });
      $("businessId").addEventListener("change", () => {
        $("conversation").innerHTML = "";
        $("callId").value = newCallId();
        activeCallStarted = false;
      });
      document.querySelectorAll("[data-text]").forEach((button) => {
        button.addEventListener("click", () => {
          if (button.dataset.business) {
            if ($("businessId").value !== button.dataset.business) {
              $("conversation").innerHTML = "";
              $("callId").value = newCallId();
              activeCallStarted = false;
            }
            $("businessId").value = button.dataset.business;
          }
          $("utterance").value = button.dataset.text;
        });
      });

      checkHealth();
      refreshOutbox();
    </script>
  </body>
</html>
"""


class InboundCallPayload(BaseModel):
    business_id: str = Field(..., examples=["demo-salon"])
    call_id: str = Field(..., examples=["call-1"])
    caller_number: str = Field(..., examples=["+919900001111"])


class MissedCallPayload(InboundCallPayload):
    pass


class TurnPayload(BaseModel):
    text: str = Field(..., examples=["Can I book a haircut tomorrow at 5 pm?"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def app_home() -> str:
    return APP_HTML


@router.post("/webhooks/telephony/inbound-call")
def inbound_call(payload: InboundCallPayload) -> dict[str, object]:
    event = CallEvent(
        business_id=payload.business_id,
        call_id=payload.call_id,
        caller_number=payload.caller_number,
        source=CallSource.INBOUND,
    )
    return container.workflow.handle_call_started(event).model_dump(mode="json")


@router.post("/webhooks/telephony/missed-call")
def missed_call(payload: MissedCallPayload) -> dict[str, object]:
    event = CallEvent(
        business_id=payload.business_id,
        call_id=payload.call_id,
        caller_number=payload.caller_number,
        source=CallSource.MISSED_CALLBACK,
    )
    return container.workflow.handle_missed_call(event).model_dump(mode="json")


@router.post("/calls/{call_id}/turn")
def call_turn(call_id: str, payload: TurnPayload) -> dict[str, object]:
    try:
        result = container.workflow.handle_caller_turn(call_id, payload.text)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result.model_dump(mode="json")


@router.get("/debug/whatsapp-outbox")
def whatsapp_outbox() -> list[dict[str, object]]:
    return [message.model_dump(mode="json") for message in container.whatsapp.messages]
