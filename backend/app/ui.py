from fastapi.responses import HTMLResponse


def render_home_page() -> HTMLResponse:
    """Return the human-facing demo page for WorkflowGym."""
    html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>WorkflowGym</title>
    <style>
      :root {
        --bg: #f4f7fb;
        --surface: #ffffff;
        --surface-2: #f8fafc;
        --ink: #101828;
        --muted: #64748b;
        --line: #d8e0ea;
        --teal: #0f766e;
        --teal-dark: #0b5f59;
        --blue: #2563eb;
        --amber: #b45309;
        --green: #15803d;
        --red: #b91c1c;
        --shadow: 0 18px 45px rgba(15, 23, 42, 0.1);
        --radius: 8px;
      }

      * {
        box-sizing: border-box;
      }

      html {
        scroll-behavior: smooth;
      }

      body {
        margin: 0;
        min-width: 320px;
        background:
          linear-gradient(180deg, rgba(15, 118, 110, 0.08), transparent 430px),
          radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.1), transparent 320px),
          var(--bg);
        color: var(--ink);
        font-family:
          Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
          "Segoe UI", sans-serif;
        line-height: 1.5;
      }

      a {
        color: var(--teal-dark);
        font-weight: 720;
        text-decoration: none;
      }

      a:hover {
        text-decoration: underline;
      }

      button,
      .button {
        min-height: 42px;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        padding: 0 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: var(--surface);
        color: var(--ink);
        font: inherit;
        font-size: 14px;
        font-weight: 780;
        cursor: pointer;
        box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
      }

      button.primary {
        color: #ffffff;
        border-color: var(--teal);
        background: var(--teal);
      }

      button.primary:hover {
        background: var(--teal-dark);
      }

      button:disabled {
        cursor: wait;
        opacity: 0.72;
      }

      .shell {
        width: min(1240px, calc(100% - 32px));
        margin: 0 auto;
      }

      header {
        position: sticky;
        top: 0;
        z-index: 20;
        border-bottom: 1px solid rgba(216, 224, 234, 0.9);
        background: rgba(255, 255, 255, 0.86);
        backdrop-filter: blur(14px);
      }

      .nav {
        min-height: 66px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        font-size: 18px;
        font-weight: 860;
        letter-spacing: 0;
      }

      .mark {
        width: 36px;
        height: 36px;
        border-radius: var(--radius);
        display: grid;
        place-items: center;
        color: #ffffff;
        background:
          linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent),
          var(--teal);
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.24);
      }

      .nav-links {
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 14px;
      }

      main {
        padding: 42px 0 52px;
      }

      .hero {
        display: grid;
        grid-template-columns: minmax(0, 1.02fr) minmax(380px, 0.98fr);
        gap: 28px;
        align-items: stretch;
      }

      .hero-copy {
        padding: 26px 0 12px;
      }

      .eyebrow {
        margin: 0 0 12px;
        color: var(--teal-dark);
        font-size: 13px;
        font-weight: 850;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      h1,
      h2,
      h3,
      p {
        margin-top: 0;
      }

      h1 {
        margin-bottom: 18px;
        max-width: 780px;
        font-size: clamp(42px, 6vw, 72px);
        line-height: 0.98;
        letter-spacing: 0;
      }

      .lede {
        max-width: 720px;
        color: #475569;
        font-size: 18px;
      }

      .actions {
        margin-top: 26px;
        display: flex;
        flex-wrap: wrap;
        gap: 11px;
      }

      .source-strip {
        margin-top: 24px;
        max-width: 760px;
        display: grid;
        gap: 8px;
      }

      .source-row {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        color: #405168;
        font-size: 14px;
      }

      .source-dot {
        width: 8px;
        height: 8px;
        margin-top: 7px;
        border-radius: 999px;
        flex: 0 0 auto;
      }

      .source-dot.real {
        background: var(--green);
      }

      .source-dot.synthetic {
        background: var(--amber);
      }

      .hero-board {
        border: 1px solid rgba(185, 198, 212, 0.8);
        border-radius: var(--radius);
        background: rgba(255, 255, 255, 0.82);
        box-shadow: var(--shadow);
        overflow: hidden;
      }

      .board-head {
        min-height: 54px;
        padding: 0 18px;
        border-bottom: 1px solid var(--line);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: rgba(248, 250, 252, 0.85);
      }

      .board-title {
        font-weight: 820;
      }

      .status-pill,
      .badge,
      .chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        white-space: nowrap;
      }

      .status-pill {
        min-height: 28px;
        padding: 0 10px;
        color: var(--green);
        background: #dcfce7;
        font-size: 12px;
        font-weight: 820;
      }

      .board-body {
        padding: 18px;
      }

      .pipeline {
        display: grid;
        gap: 10px;
      }

      .pipeline-step {
        display: grid;
        grid-template-columns: 34px minmax(0, 1fr) auto;
        gap: 12px;
        align-items: center;
        padding: 12px;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        background: #ffffff;
      }

      .step-index {
        width: 34px;
        height: 34px;
        display: grid;
        place-items: center;
        border-radius: var(--radius);
        color: #ffffff;
        background: var(--ink);
        font-weight: 850;
      }

      .pipeline-step strong {
        display: block;
        font-size: 14px;
      }

      .pipeline-step span {
        display: block;
        color: var(--muted);
        font-size: 13px;
      }

      .hero-metrics {
        margin-top: 16px;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
      }

      .hero-metric {
        min-height: 86px;
        padding: 12px;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        background: var(--surface-2);
      }

      .hero-metric span {
        color: var(--muted);
        font-size: 12px;
        font-weight: 720;
      }

      .hero-metric strong {
        display: block;
        margin-top: 8px;
        font-size: 24px;
        line-height: 1;
      }

      section {
        margin-top: 34px;
      }

      .section-head {
        margin-bottom: 16px;
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 18px;
      }

      h2 {
        margin-bottom: 4px;
        font-size: 26px;
        line-height: 1.15;
        letter-spacing: 0;
      }

      .section-copy {
        margin: 0;
        max-width: 760px;
        color: var(--muted);
      }

      .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
      }

      .metric-card,
      .panel,
      .scenario-card {
        border: 1px solid var(--line);
        border-radius: var(--radius);
        background: var(--surface);
      }

      .metric-card {
        min-height: 132px;
        padding: 18px;
      }

      .metric-label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 760;
      }

      .metric-value {
        margin-top: 12px;
        font-size: 32px;
        line-height: 1;
        font-weight: 890;
      }

      .metric-detail {
        margin-top: 10px;
        color: var(--muted);
        font-size: 13px;
      }

      .workbench {
        display: grid;
        grid-template-columns: minmax(0, 0.92fr) minmax(420px, 1.08fr);
        gap: 16px;
      }

      .panel {
        padding: 18px;
      }

      .panel h3 {
        margin-bottom: 12px;
        font-size: 17px;
      }

      .facts {
        margin: 0;
        padding-left: 18px;
        color: #475569;
      }

      .facts li {
        margin: 8px 0;
      }

      .trace-list {
        display: grid;
        gap: 10px;
      }

      .trace-row {
        display: grid;
        grid-template-columns: 32px minmax(0, 1fr) auto;
        gap: 11px;
        align-items: center;
        padding: 11px;
        border: 1px solid var(--line);
        border-radius: var(--radius);
        background: var(--surface-2);
      }

      .trace-row strong {
        display: block;
        font-size: 14px;
      }

      .trace-row span {
        display: block;
        color: var(--muted);
        font-size: 13px;
      }

      .badge {
        min-height: 28px;
        padding: 0 10px;
        color: var(--green);
        background: #dcfce7;
        font-size: 12px;
        font-weight: 840;
      }

      .badge.warn {
        color: var(--amber);
        background: #fef3c7;
      }

      .badge.info {
        color: var(--blue);
        background: #dbeafe;
      }

      .scenario-list {
        display: grid;
        gap: 14px;
      }

      .scenario-card {
        overflow: hidden;
        box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
      }

      .scenario-top {
        padding: 16px;
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto;
        gap: 16px;
        border-bottom: 1px solid var(--line);
        background: linear-gradient(180deg, #ffffff, #fbfdff);
      }

      .scenario-title {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 9px;
      }

      .scenario-title strong {
        font-size: 17px;
      }

      .scenario-subtitle {
        margin-top: 5px;
        color: var(--muted);
        font-size: 13px;
      }

      .chip {
        min-height: 25px;
        padding: 0 9px;
        color: var(--teal-dark);
        border: 1px solid #99f6e4;
        background: #ccfbf1;
        font-size: 12px;
        font-weight: 820;
      }

      .chip.synthetic {
        color: var(--amber);
        border-color: #fde68a;
        background: #fffbeb;
      }

      .scenario-score {
        text-align: right;
      }

      .scenario-score strong {
        display: block;
        font-size: 26px;
        line-height: 1;
      }

      .scenario-score span {
        color: var(--muted);
        font-size: 12px;
        font-weight: 720;
      }

      .scenario-body {
        padding: 16px;
        display: grid;
        gap: 14px;
      }

      .scenario-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
      }

      .info-box,
      .invoice-cell {
        border: 1px solid var(--line);
        border-radius: var(--radius);
        background: var(--surface-2);
      }

      .info-box {
        padding: 12px;
      }

      .info-label,
      .mini-label {
        display: block;
        color: var(--muted);
        font-size: 11px;
        font-weight: 820;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }

      .info-value {
        display: block;
        margin-top: 5px;
        color: var(--ink);
        font-size: 14px;
        font-weight: 680;
      }

      .provenance {
        padding: 13px;
        border: 1px solid #bfdbfe;
        border-radius: var(--radius);
        background: #eff6ff;
        color: #1e3a8a;
        font-size: 13px;
      }

      .provenance strong {
        color: #172554;
      }

      .invoice-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(130px, 1fr));
        gap: 9px;
      }

      .invoice-cell {
        padding: 10px;
      }

      .mini-value {
        display: block;
        margin-top: 4px;
        color: var(--ink);
        font-size: 14px;
        font-weight: 820;
        overflow-wrap: anywhere;
      }

      .impact {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 9px;
      }

      .impact .invoice-cell:nth-child(3) .mini-value {
        color: var(--red);
      }

      .code-panel {
        min-height: 100%;
        padding: 0;
        overflow: hidden;
        background: #0f172a;
        color: #d7fbe8;
      }

      .code-head {
        min-height: 45px;
        padding: 0 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: #e5f3ff;
        font-size: 13px;
        font-weight: 780;
      }

      .dots {
        display: flex;
        gap: 6px;
      }

      .dot {
        width: 10px;
        height: 10px;
        border-radius: 999px;
        background: #ef4444;
      }

      .dot:nth-child(2) {
        background: #f59e0b;
      }

      .dot:nth-child(3) {
        background: #22c55e;
      }

      pre {
        margin: 0;
        padding: 16px;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        font-size: 13px;
      }

      footer {
        margin-top: 34px;
        padding-top: 22px;
        border-top: 1px solid var(--line);
        color: var(--muted);
        font-size: 14px;
      }

      @media (max-width: 980px) {
        .hero,
        .workbench {
          grid-template-columns: 1fr;
        }

        .metric-grid,
        .invoice-grid {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }

      @media (max-width: 720px) {
        main {
          padding-top: 28px;
        }

        .nav-links {
          display: none;
        }

        .hero-metrics,
        .metric-grid,
        .scenario-grid,
        .impact {
          grid-template-columns: 1fr;
        }

        .scenario-top {
          grid-template-columns: 1fr;
        }

        .scenario-score {
          text-align: left;
        }
      }

      @media (max-width: 520px) {
        .invoice-grid {
          grid-template-columns: 1fr;
        }

        .pipeline-step,
        .trace-row {
          grid-template-columns: 32px minmax(0, 1fr);
        }

        .pipeline-step .badge,
        .trace-row .badge {
          grid-column: 2;
          justify-self: start;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <div class="shell nav">
        <div class="brand">
          <span class="mark">W</span>
          <span>WorkflowGym</span>
        </div>
        <nav class="nav-links" aria-label="Primary navigation">
          <a href="#benchmark">Benchmark</a>
          <a href="#scenarios">Scenarios</a>
          <a href="/api/demo">Raw JSON</a>
          <a href="/docs">API Docs</a>
          <a href="https://github.com/ChanakyaG2004/WorkflowGym">GitHub</a>
        </nav>
      </div>
    </header>

    <main class="shell">
      <section class="hero" aria-label="WorkflowGym overview">
        <div class="hero-copy">
          <p class="eyebrow">FinanceOps agent evaluation platform</p>
          <h1>Test tool-using AI agents on invoice investigations.</h1>
          <p class="lede">
            WorkflowGym seeds billing disputes, makes an agent call deterministic
            finance tools, stores every step, and scores the answer against
            hidden ground truth.
          </p>
          <div class="actions">
            <button class="primary" id="runButton" type="button">Run Benchmark</button>
            <a class="button" href="#scenarios">Review Scenarios</a>
            <a class="button" href="/docs">Open API Docs</a>
          </div>
          <div class="source-strip" aria-label="Data provenance summary">
            <div class="source-row">
              <span class="source-dot real"></span>
              <span>
                <strong>Real source:</strong>
                AWS API Gateway public pricing is linked in every scenario as
                the reference pricing context.
              </span>
            </div>
            <div class="source-row">
              <span class="source-dot synthetic"></span>
              <span>
                <strong>Synthetic benchmark data:</strong>
                customers, invoice line items, usage quantities, injected errors,
                and hidden labels are generated fixtures for deterministic scoring.
              </span>
            </div>
          </div>
        </div>

        <aside class="hero-board" aria-label="Agent pipeline">
          <div class="board-head">
            <span class="board-title">Agent Investigation Pipeline</span>
            <span class="status-pill" id="runStatus">Ready</span>
          </div>
          <div class="board-body">
            <div class="pipeline" id="pipeline"></div>
            <div class="hero-metrics">
              <div class="hero-metric">
                <span>Scenarios</span>
                <strong id="heroScenarios">20</strong>
              </div>
              <div class="hero-metric">
                <span>Required Tools</span>
                <strong>5</strong>
              </div>
              <div class="hero-metric">
                <span>Trace Storage</span>
                <strong>100</strong>
              </div>
            </div>
          </div>
        </aside>
      </section>

      <section id="benchmark" aria-label="Benchmark metrics">
        <div class="section-head">
          <div>
            <h2>Benchmark Metrics</h2>
            <p class="section-copy">
              Quantified results from running all seeded FinanceOps scenarios
              through the rule-based investigation agent.
            </p>
          </div>
        </div>
        <div class="metric-grid">
          <div class="metric-card">
            <div class="metric-label">Pass Rate</div>
            <div class="metric-value" id="passRate">--</div>
            <div class="metric-detail">Runs that matched hidden ground truth</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Average Score</div>
            <div class="metric-value" id="score">--</div>
            <div class="metric-detail">Decision, cause, and tool coverage</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Tool Calls Traced</div>
            <div class="metric-value" id="tools">--</div>
            <div class="metric-detail">Stored tool-call audit records</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Overcharge Found</div>
            <div class="metric-value" id="overcharge">--</div>
            <div class="metric-detail">Aggregate detected invoice impact</div>
          </div>
        </div>
      </section>

      <section class="workbench" aria-label="Evaluation workbench">
        <div class="panel">
          <h3>What The Benchmark Tests</h3>
          <ul class="facts">
            <li>Duplicate usage events that inflate invoice quantity</li>
            <li>Contracted overage rates that differ from invoice rates</li>
            <li>Included API-call allowances that were not applied</li>
            <li>Overage charges while the customer stayed below allowance</li>
            <li>Invoice usage that exceeds the recorded usage system</li>
            <li>Clean control invoices where the agent should avoid false positives</li>
          </ul>
        </div>
        <div class="panel code-panel" aria-label="Latest run summary">
          <div class="code-head">
            <span>latest_run_summary.json</span>
            <span class="dots" aria-hidden="true">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </span>
          </div>
          <pre id="preview">Loading benchmark...</pre>
        </div>
      </section>

      <section aria-label="Tool trace">
        <div class="section-head">
          <div>
            <h2>Stored Tool Trace</h2>
            <p class="section-copy">
              Each scenario uses the same five deterministic finance tools, and
              each call is stored as an auditable AgentStep.
            </p>
          </div>
        </div>
        <div class="trace-list" id="trace"></div>
      </section>

      <section id="scenarios" aria-label="Scenario results">
        <div class="section-head">
          <div>
            <h2>Scenario Results And Invoices</h2>
            <p class="section-copy">
              Every card shows what was tested, which parts are real or
              synthetic, the invoice calculation, and the agent's final result.
            </p>
          </div>
        </div>
        <div class="scenario-list" id="results">
          <div class="scenario-card">
            <div class="scenario-top">
              <div>
                <div class="scenario-title">
                  <strong>Benchmark loading</strong>
                  <span class="chip">Pending</span>
                </div>
                <div class="scenario-subtitle">The public demo runs automatically.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer>
        Backend: FastAPI, SQLAlchemy, PostgreSQL-ready schema, Docker, Vercel
        serverless demo. The live deployment uses SQLite per request for a
        stateless public benchmark run.
      </footer>
    </main>

    <script>
      const runButton = document.getElementById("runButton");
      const runStatus = document.getElementById("runStatus");
      const preview = document.getElementById("preview");
      const pipeline = document.getElementById("pipeline");
      const trace = document.getElementById("trace");
      const results = document.getElementById("results");
      const passRate = document.getElementById("passRate");
      const score = document.getElementById("score");
      const tools = document.getElementById("tools");
      const overcharge = document.getElementById("overcharge");
      const heroScenarios = document.getElementById("heroScenarios");

      const formatter = new Intl.NumberFormat("en-US");
      const dollars = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0
      });

      const toolDescriptions = [
        ["get_customer", "Load the customer account tied to the dispute."],
        ["get_invoice", "Read the disputed invoice and overage line item."],
        ["get_usage_events", "Separate valid usage from duplicate or extra records."],
        ["get_contract_terms", "Fetch included allowance and contract rate."],
        ["compare_usage_to_invoice", "Recompute expected charge and compare to invoice."]
      ];

      const causeDescriptions = {
        duplicate_usage_events:
          "Duplicate usage detection: verifies that repeated usage events are excluded before billing.",
        overage_rate_mismatch:
          "Rate validation: compares the invoice unit price against the contracted overage rate.",
        included_allowance_not_applied:
          "Allowance application: confirms included API calls were subtracted before overage billing.",
        below_allowance_overage_charged:
          "Below-allowance control: catches an overage charge when usage stayed below included calls.",
        invoice_usage_exceeds_recorded_usage:
          "Usage reconciliation: compares invoice quantity with recorded usage and finds unexplained extra calls.",
        no_issue_found:
          "Clean invoice control: verifies the agent does not invent a billing issue when the invoice is correct."
      };

      function safeText(value, fallback = "--") {
        return value === null || value === undefined || value === "" ? fallback : value;
      }

      function renderPipeline(status = "Waiting") {
        pipeline.innerHTML = toolDescriptions.map(([name, text], index) => `
          <div class="pipeline-step">
            <div class="step-index">${index + 1}</div>
            <div>
              <strong>${name}</strong>
              <span>${text}</span>
            </div>
            <span class="badge ${status === "Waiting" ? "warn" : ""}">${status}</span>
          </div>
        `).join("");
      }

      function renderTrace() {
        trace.innerHTML = toolDescriptions.map(([name, text], index) => `
          <div class="trace-row">
            <div class="step-index">${index + 1}</div>
            <div>
              <strong>${name}</strong>
              <span>${text}</span>
            </div>
            <span class="badge">Stored</span>
          </div>
        `).join("");
      }

      function renderInvoice(item) {
        const invoice = item.invoice || {};
        return `
          <div class="invoice-grid">
            <div class="invoice-cell">
              <span class="mini-label">Valid Usage</span>
              <span class="mini-value">${formatter.format(invoice.valid_usage_quantity || 0)} calls</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Recorded Usage</span>
              <span class="mini-value">${formatter.format(invoice.total_recorded_usage_quantity || 0)} calls</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Invoice Usage</span>
              <span class="mini-value">${formatter.format(invoice.invoice_usage_quantity || 0)} calls</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Included Allowance</span>
              <span class="mini-value">${formatter.format(invoice.included_api_calls || 0)} calls</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Contract Rate</span>
              <span class="mini-value">${safeText(invoice.contract_overage_rate_cents)}c / call</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Invoice Rate</span>
              <span class="mini-value">${safeText(invoice.invoice_unit_price_cents)}c / call</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Correct Overage</span>
              <span class="mini-value">${formatter.format(invoice.correct_billable_overage_calls || 0)} calls</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Charged Overage</span>
              <span class="mini-value">${formatter.format(invoice.actual_charged_overage_calls || 0)} calls</span>
            </div>
          </div>
          <div class="impact">
            <div class="invoice-cell">
              <span class="mini-label">Expected Overage Charge</span>
              <span class="mini-value">${dollars.format(invoice.expected_overage_dollars || 0)}</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Actual Overage Charge</span>
              <span class="mini-value">${dollars.format(invoice.actual_overage_dollars || 0)}</span>
            </div>
            <div class="invoice-cell">
              <span class="mini-label">Detected Overcharge</span>
              <span class="mini-value">${dollars.format(invoice.overcharge_dollars || 0)}</span>
            </div>
          </div>
        `;
      }

      function renderScenarioResults(items) {
        results.innerHTML = items.map((item) => {
          const sourceFacts = (item.real_source_facts || []).join(" ");
          return `
            <article class="scenario-card">
              <div class="scenario-top">
                <div>
                  <div class="scenario-title">
                    <strong>${item.scenario}</strong>
                    <span class="chip">Real source linked</span>
                    <span class="chip synthetic">Synthetic invoice fixture</span>
                  </div>
                  <div class="scenario-subtitle">
                    ${item.customer} · ${item.month} · ${item.test_prompt}
                  </div>
                </div>
                <div class="scenario-score">
                  <strong>${item.score}/100</strong>
                  <span>${item.required_tools_called} required tools</span>
                </div>
              </div>
              <div class="scenario-body">
                <div class="scenario-grid">
                  <div class="info-box">
                    <span class="info-label">What Is Tested</span>
                    <span class="info-value">${causeDescriptions[item.expected_cause] || "FinanceOps invoice investigation."}</span>
                  </div>
                  <div class="info-box">
                    <span class="info-label">Ground Truth</span>
                    <span class="info-value">${item.expected_outcome} · ${item.expected_cause}</span>
                  </div>
                  <div class="info-box">
                    <span class="info-label">Agent Result</span>
                    <span class="info-value">${item.decision} · ${item.cause} · ${item.tool_calls_traced} traced calls</span>
                  </div>
                </div>
                <div class="provenance">
                  <strong>Data label:</strong> ${item.data_source_label}
                  <br />
                  <strong>Real reference:</strong>
                  <a href="${item.data_source_url}" target="_blank" rel="noreferrer">AWS API Gateway pricing</a>
                  <br />
                  <strong>Real facts used:</strong> ${sourceFacts}
                </div>
                ${renderInvoice(item)}
              </div>
            </article>
          `;
        }).join("");
      }

      async function runDemo() {
        runButton.disabled = true;
        runButton.textContent = "Running...";
        runStatus.textContent = "Running";
        preview.textContent = "Seeding scenarios, running agent, storing traces, and evaluating results...";
        renderPipeline("Running");

        try {
          const response = await fetch("/api/demo", { cache: "no-store" });
          if (!response.ok) {
            throw new Error(`Demo failed with status ${response.status}`);
          }

          const data = await response.json();
          const summary = data.metrics_summary || {};
          const scenarioResults = data.scenario_results || [];
          const totalOverchargeDollars = (summary.total_detected_overcharge_cents || 0) / 100;

          heroScenarios.textContent = formatter.format(summary.total_scenarios || scenarioResults.length);
          passRate.textContent = `${safeText(summary.pass_rate, 0)}%`;
          score.textContent = `${safeText(summary.average_score, data.score)}/100`;
          tools.textContent = formatter.format(summary.total_tool_calls || data.tool_calls_traced || 0);
          overcharge.textContent = dollars.format(totalOverchargeDollars || data.overcharge_detected_dollars || 0);

          renderPipeline("Stored");
          renderTrace();
          renderScenarioResults(scenarioResults);

          preview.textContent = JSON.stringify({
            scenarios: summary.total_scenarios,
            runs: summary.total_runs,
            passed_runs: summary.passed_runs,
            pass_rate: `${summary.pass_rate}%`,
            average_score: summary.average_score,
            average_tool_accuracy: `${summary.average_tool_accuracy}%`,
            tool_calls_traced: summary.total_tool_calls,
            duplicate_usage_detected: summary.total_duplicate_usage_quantity,
            overcharge_detected: dollars.format(totalOverchargeDollars),
            data_provenance: "Real AWS pricing reference + synthetic invoice fixtures"
          }, null, 2);

          runStatus.textContent = scenarioResults.every((item) => item.passed)
            ? "20/20 Passed"
            : "Review";
        } catch (error) {
          preview.textContent = error.message;
          runStatus.textContent = "Error";
          renderPipeline("Waiting");
        } finally {
          runButton.disabled = false;
          runButton.textContent = "Run Benchmark";
        }
      }

      renderPipeline("Waiting");
      renderTrace();
      runButton.addEventListener("click", runDemo);
      runDemo();
    </script>
  </body>
</html>
"""
    return HTMLResponse(html)
