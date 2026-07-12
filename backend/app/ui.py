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
        --bg: #f7f8fb;
        --panel: #ffffff;
        --ink: #172033;
        --muted: #607089;
        --line: #dfe5ee;
        --accent: #0f766e;
        --accent-dark: #115e59;
        --good: #15803d;
        --warn: #b45309;
        --code: #101827;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        background: var(--bg);
        color: var(--ink);
        font-family:
          Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
          "Segoe UI", sans-serif;
        line-height: 1.5;
      }

      a {
        color: var(--accent-dark);
        text-decoration: none;
        font-weight: 650;
      }

      a:hover {
        text-decoration: underline;
      }

      .shell {
        width: min(1120px, calc(100% - 32px));
        margin: 0 auto;
      }

      header {
        border-bottom: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.86);
        position: sticky;
        top: 0;
        z-index: 5;
        backdrop-filter: blur(10px);
      }

      .nav {
        min-height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 760;
        font-size: 18px;
      }

      .mark {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        display: grid;
        place-items: center;
        background: var(--accent);
        color: white;
        font-weight: 800;
      }

      .links {
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 14px;
      }

      main {
        padding: 48px 0 56px;
      }

      .hero {
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
        gap: 28px;
        align-items: stretch;
      }

      .eyebrow {
        color: var(--accent-dark);
        font-weight: 760;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin: 0 0 12px;
      }

      h1 {
        margin: 0;
        font-size: clamp(36px, 6vw, 64px);
        line-height: 1.02;
        letter-spacing: 0;
      }

      .lede {
        max-width: 680px;
        margin: 20px 0 0;
        color: var(--muted);
        font-size: 18px;
      }

      .actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 28px;
      }

      button,
      .button {
        min-height: 44px;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 0 16px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: white;
        color: var(--ink);
        font-weight: 720;
        cursor: pointer;
        font-size: 14px;
      }

      button.primary {
        background: var(--accent);
        border-color: var(--accent);
        color: white;
      }

      button.primary:hover {
        background: var(--accent-dark);
      }

      button:disabled {
        opacity: 0.7;
        cursor: wait;
      }

      .terminal {
        background: var(--code);
        color: #d8f3e7;
        border-radius: 8px;
        padding: 18px;
        min-height: 100%;
        box-shadow: 0 24px 50px rgba(16, 24, 39, 0.16);
      }

      .terminal-bar {
        display: flex;
        gap: 6px;
        margin-bottom: 18px;
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
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        font-size: 13px;
      }

      section {
        margin-top: 34px;
      }

      h2 {
        margin: 0 0 16px;
        font-size: 24px;
        letter-spacing: 0;
      }

      .grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
      }

      .metric,
      .panel,
      .step {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
      }

      .metric {
        padding: 18px;
        min-height: 116px;
      }

      .metric .label {
        color: var(--muted);
        font-size: 13px;
        font-weight: 650;
      }

      .metric .value {
        margin-top: 10px;
        font-size: 30px;
        line-height: 1;
        font-weight: 820;
      }

      .metric .detail {
        margin-top: 8px;
        color: var(--muted);
        font-size: 13px;
      }

      .two-col {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
        gap: 16px;
      }

      .panel {
        padding: 20px;
      }

      .panel h3 {
        margin: 0 0 12px;
        font-size: 17px;
      }

      .facts {
        margin: 0;
        padding-left: 20px;
        color: var(--muted);
      }

      .facts li {
        margin: 7px 0;
      }

      .trace {
        display: grid;
        gap: 10px;
      }

      .step {
        padding: 14px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
      }

      .step strong {
        font-size: 14px;
      }

      .step span {
        color: var(--muted);
        font-size: 13px;
      }

      .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 78px;
        min-height: 28px;
        padding: 0 10px;
        border-radius: 999px;
        background: #dcfce7;
        color: var(--good);
        font-weight: 780;
        font-size: 12px;
      }

      .footer {
        margin-top: 36px;
        color: var(--muted);
        font-size: 14px;
      }

      @media (max-width: 860px) {
        .hero,
        .two-col {
          grid-template-columns: 1fr;
        }

        .grid {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .links {
          display: none;
        }
      }

      @media (max-width: 540px) {
        main {
          padding-top: 30px;
        }

        .grid {
          grid-template-columns: 1fr;
        }

        .step {
          align-items: flex-start;
          flex-direction: column;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <div class="shell nav">
        <div class="brand"><span class="mark">W</span> WorkflowGym</div>
        <nav class="links">
          <a href="/docs">API Docs</a>
          <a href="/demo">Raw Demo JSON</a>
          <a href="https://github.com/ChanakyaG2004/WorkflowGym">GitHub</a>
        </nav>
      </div>
    </header>

    <main class="shell">
      <div class="hero">
        <div>
          <p class="eyebrow">Tool-Using Agent Evaluation</p>
          <h1>FinanceOps simulator for testing AI agent investigations.</h1>
          <p class="lede">
            WorkflowGym runs six billing investigation scenarios, records every
            tool call, and scores whether the agent found each hidden invoice
            issue.
          </p>
          <div class="actions">
            <button class="primary" id="runButton" type="button">Run Live Demo</button>
            <a class="button" href="/docs">Open API Docs</a>
            <a class="button" href="https://github.com/ChanakyaG2004/WorkflowGym">View GitHub</a>
          </div>
        </div>

        <div class="terminal" aria-label="Demo output preview">
          <div class="terminal-bar">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
          <pre id="preview">Ready.

Click "Run Live Demo" to seed six scenarios, run the agent, evaluate each trace, and display metrics.</pre>
        </div>
      </div>

      <section aria-label="Key metrics">
        <h2>Evaluation Metrics</h2>
        <div class="grid">
          <div class="metric">
            <div class="label">Average Score</div>
            <div class="value" id="score">--</div>
            <div class="detail">Weighted decision, cause, and tool score</div>
          </div>
          <div class="metric">
            <div class="label">Tool Calls</div>
            <div class="value" id="tools">--</div>
            <div class="detail">Expected investigation coverage</div>
          </div>
          <div class="metric">
            <div class="label">Duplicate Calls</div>
            <div class="value" id="duplicates">--</div>
            <div class="detail">Hidden issue detected</div>
          </div>
          <div class="metric">
            <div class="label">Total Overcharge</div>
            <div class="value" id="overcharge">--</div>
            <div class="detail">Invoice amount identified</div>
          </div>
        </div>
      </section>

      <section>
        <h2>Scenario Results</h2>
        <div class="trace" id="results">
          <div class="step">
            <div>
              <strong>No benchmark run yet</strong><br />
              <span>Run the demo to evaluate all six seeded scenarios.</span>
            </div>
            <span class="badge">Waiting</span>
          </div>
        </div>
      </section>

      <section class="two-col">
        <div class="panel">
          <h3>Scenario</h3>
          <ul class="facts">
            <li>Six seeded FinanceOps investigations</li>
            <li>Five incorrect invoices and one clean control case</li>
            <li>All scenarios use the same deterministic finance tools</li>
            <li>Every run stores a five-step tool trace</li>
            <li>Metrics aggregate score, pass rate, tool calls, and overcharge</li>
          </ul>
        </div>
        <div class="panel">
          <h3>Agent Decision</h3>
          <ul class="facts">
            <li>Decision: <strong id="decision">not run yet</strong></li>
            <li>Cause: <strong id="cause">not run yet</strong></li>
            <li>Pass status: <strong id="passed">not run yet</strong></li>
            <li>Pass rate: <strong id="passRate">not run yet</strong></li>
          </ul>
        </div>
      </section>

      <section>
        <h2>Tool Trace</h2>
        <div class="trace" id="trace">
          <div class="step">
            <div>
              <strong>No run yet</strong><br />
              <span>Run the demo to see the five stored tool calls.</span>
            </div>
            <span class="badge">Waiting</span>
          </div>
        </div>
      </section>

      <p class="footer">
        Backend: FastAPI, SQLAlchemy, PostgreSQL-ready schema, Docker, Vercel demo.
        The public demo uses SQLite for stateless serverless hosting.
      </p>
    </main>

    <script>
      const runButton = document.getElementById("runButton");
      const preview = document.getElementById("preview");
      const score = document.getElementById("score");
      const tools = document.getElementById("tools");
      const duplicates = document.getElementById("duplicates");
      const overcharge = document.getElementById("overcharge");
      const decision = document.getElementById("decision");
      const cause = document.getElementById("cause");
      const passed = document.getElementById("passed");
      const passRate = document.getElementById("passRate");
      const trace = document.getElementById("trace");
      const results = document.getElementById("results");

      const formatter = new Intl.NumberFormat("en-US");
      const dollars = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0
      });

      const toolDescriptions = [
        ["get_customer", "Loaded Acme AI customer record"],
        ["get_invoice", "Loaded June 2026 invoice and line items"],
        ["get_usage_events", "Separated valid usage from duplicate usage"],
        ["get_contract_terms", "Loaded included calls and overage rate"],
        ["compare_usage_to_invoice", "Compared valid usage against invoice charge"]
      ];

      function renderTrace() {
        trace.innerHTML = toolDescriptions.map(([name, text], index) => `
          <div class="step">
            <div>
              <strong>${index + 1}. ${name}</strong><br />
              <span>${text}</span>
            </div>
            <span class="badge">Stored</span>
          </div>
        `).join("");
      }

      function renderScenarioResults(items) {
        results.innerHTML = items.map((item) => `
          <div class="step">
            <div>
              <strong>${item.scenario}</strong><br />
              <span>${item.customer} · ${item.decision} · ${item.cause}</span>
            </div>
            <span class="badge">${item.score}/100</span>
          </div>
        `).join("");
      }

      async function runDemo() {
        runButton.disabled = true;
        runButton.textContent = "Running...";
        preview.textContent = "Running scenario duplicate_usage_001...";

        try {
          const response = await fetch("/demo", { cache: "no-store" });
          if (!response.ok) {
            throw new Error(`Demo failed with status ${response.status}`);
          }
          const data = await response.json();
          const summary = data.metrics_summary || {};
          const scenarioResults = data.scenario_results || [];
          const firstScenario = scenarioResults[0] || data;

          score.textContent = `${summary.average_score || data.score}/100`;
          tools.textContent = formatter.format(summary.total_tool_calls || data.tool_calls_traced);
          duplicates.textContent = formatter.format(summary.total_duplicate_usage_quantity || data.duplicate_usage_detected);
          overcharge.textContent = dollars.format((summary.total_detected_overcharge_cents || 0) / 100 || data.overcharge_detected_dollars);
          decision.textContent = firstScenario.decision;
          cause.textContent = firstScenario.cause;
          passed.textContent = scenarioResults.every((item) => item.passed) ? "all passed" : "review needed";
          passRate.textContent = `${summary.pass_rate || "--"}%`;

          renderTrace();
          renderScenarioResults(scenarioResults);
          preview.textContent = JSON.stringify({
            scenarios: summary.total_scenarios,
            runs: summary.total_runs,
            pass_rate: summary.pass_rate,
            average_score: summary.average_score,
            average_tool_accuracy: summary.average_tool_accuracy,
            total_tool_calls: summary.total_tool_calls,
            total_duplicate_usage_quantity: summary.total_duplicate_usage_quantity,
            total_overcharge_dollars: (summary.total_detected_overcharge_cents || 0) / 100
          }, null, 2);
        } catch (error) {
          preview.textContent = error.message;
        } finally {
          runButton.disabled = false;
          runButton.textContent = "Run Live Demo";
        }
      }

      runButton.addEventListener("click", runDemo);
      runDemo();
    </script>
  </body>
</html>
"""
    return HTMLResponse(html)
