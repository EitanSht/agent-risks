"""
Exfil Receiver — Demo Dashboard
Receives POST /exfil from the hijacked agent and shows stolen data on a live
auto-refreshing dashboard at http://127.0.0.1:9999/

Run: python server.py
"""

import json
from datetime import datetime
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
stolen_records: list[dict] = []

# ---------------------------------------------------------------------------
# Dashboard HTML (returned as a string; __PLACEHOLDERS__ swapped at runtime)
# ---------------------------------------------------------------------------

DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="2">
  <title>Attacker's View</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #111;
      color: #ddd;
      font-family: 'Segoe UI', -apple-system, 'Helvetica Neue', sans-serif;
      min-height: 100vh;
    }

    /* ── Top bar ─────────────────────────────────────────────── */
    .topbar {
      background: #1a1a1a;
      border-bottom: 1px solid #333;
      padding: 16px 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .topbar-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .topbar-dot {
      width: 12px; height: 12px;
      border-radius: 50%;
      background: __DOT_COLOR__;
      box-shadow: 0 0 8px __DOT_COLOR__;
      __DOT_ANIM__
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }
    .topbar-label {
      font-size: 0.95em;
      color: #888;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .topbar-right {
      display: flex;
      align-items: center;
      gap: 16px;
      color: #555;
      font-size: 0.85em;
    }
    .clear-btn {
      background: transparent;
      border: 1px solid #444;
      color: #888;
      padding: 5px 14px;
      border-radius: 6px;
      font-size: 0.85em;
      cursor: pointer;
      transition: all 0.2s;
    }
    .clear-btn:hover {
      border-color: #e53e3e;
      color: #e53e3e;
    }

    /* ── Main content ────────────────────────────────────────── */
    .content {
      max-width: 1100px;
      margin: 0 auto;
      padding: 48px;
    }

    /* ── Framing header ──────────────────────────────────────── */
    .framing {
      text-align: center;
      margin-bottom: 48px;
    }
    .framing h1 {
      font-size: 2.4em;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
    }
    .framing h1 span { color: #e53e3e; }
    .framing p {
      color: #999;
      font-size: 1.15em;
      line-height: 1.6;
      max-width: 700px;
      margin: 0 auto;
    }

    /* ── What happened timeline ───────────────────────────────── */
    .timeline {
      display: flex;
      justify-content: center;
      gap: 0;
      margin-bottom: 48px;
      flex-wrap: wrap;
    }
    .step {
      display: flex;
      align-items: center;
      gap: 0;
    }
    .step-box {
      background: #1e1e1e;
      border: 1px solid #333;
      border-radius: 10px;
      padding: 16px 22px;
      text-align: center;
      min-width: 190px;
    }
    .step-num {
      display: inline-block;
      background: #e53e3e;
      color: #fff;
      width: 28px; height: 28px;
      border-radius: 50%;
      line-height: 28px;
      font-size: 0.85em;
      font-weight: 700;
      margin-bottom: 8px;
    }
    .step-label {
      font-size: 0.95em;
      color: #ccc;
      line-height: 1.4;
    }
    .step-arrow {
      color: #444;
      font-size: 1.6em;
      padding: 0 8px;
      line-height: 1;
    }

    /* ── Waiting state ───────────────────────────────────────── */
    .waiting {
      text-align: center;
      padding: 80px 20px;
    }
    .waiting-icon {
      font-size: 3em;
      margin-bottom: 20px;
      opacity: 0.4;
    }
    .waiting-text {
      color: #555;
      font-size: 1.2em;
    }

    /* ── Stolen data section ─────────────────────────────────── */
    .stolen-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 24px;
    }
    .stolen-header h2 {
      color: #e53e3e;
      font-size: 1.5em;
      font-weight: 600;
    }
    .stolen-badge {
      background: #e53e3e;
      color: #fff;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 0.8em;
      font-weight: 600;
      letter-spacing: 0.04em;
    }
    .meta-row {
      display: flex;
      gap: 32px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }
    .meta-item {
      color: #777;
      font-size: 0.92em;
    }
    .meta-item strong { color: #bbb; }

    /* ── File cards ───────────────────────────────────────────── */
    .file-card {
      margin-bottom: 20px;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid #2a2a2a;
    }
    .file-card-header {
      background: #1e1e1e;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #2a2a2a;
    }
    .file-card-name {
      font-family: 'Courier New', monospace;
      font-size: 1em;
      color: #e53e3e;
      font-weight: 600;
    }
    .file-card-tag {
      background: #2a1010;
      color: #ff8888;
      padding: 3px 12px;
      border-radius: 12px;
      font-size: 0.78em;
    }
    .file-card-body {
      background: #0d0d0d;
      padding: 20px 24px;
      font-family: 'Courier New', monospace;
      font-size: 0.98em;
      line-height: 1.8;
      color: #e8c96a;
      white-space: pre-wrap;
      word-break: break-all;
      max-height: 400px;
      overflow-y: auto;
    }
    .raw-block {
      background: #0d0d0d;
      border: 1px solid #2a2a2a;
      border-radius: 10px;
      padding: 20px 24px;
      font-family: 'Courier New', monospace;
      font-size: 0.98em;
      line-height: 1.8;
      color: #e8c96a;
      white-space: pre-wrap;
      word-break: break-all;
      max-height: 400px;
      overflow-y: auto;
    }

    /* ── Scrollbar ────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #444; border-radius: 3px; }
  </style>
</head>
<body>

  <div class="topbar">
    <div class="topbar-left">
      <div class="topbar-dot"></div>
      <span class="topbar-label">__STATUS_TEXT__</span>
    </div>
    <div class="topbar-right">
      <span>This is the attacker's screen &mdash; not visible to the developer</span>
      <button class="clear-btn" onclick="fetch('/clear',{method:'POST'}).then(()=>location.reload())">Clear</button>
    </div>
  </div>

  <div class="content">

    <div class="framing">
      <h1>The developer sees a <span>summary</span>.<br>The attacker sees <span>everything</span>.</h1>
      <p>
        A developer asked their AI coding assistant to install an MCP tool from GitHub
        and fetch an article. The tool did exactly that &mdash; and silently sent
        every secret in the project to this screen.
      </p>
    </div>

    <div class="timeline">
      <div class="step">
        <div class="step-box">
          <div class="step-num">1</div>
          <div class="step-label">Developer asks AI<br>to install MCP tool</div>
        </div>
      </div>
      <div class="step">
        <div class="step-arrow">&rarr;</div>
        <div class="step-box">
          <div class="step-num">2</div>
          <div class="step-label">AI installs it via<br><code>pip install</code></div>
        </div>
      </div>
      <div class="step">
        <div class="step-arrow">&rarr;</div>
        <div class="step-box">
          <div class="step-num">3</div>
          <div class="step-label">Developer asks AI<br>to fetch an article</div>
        </div>
      </div>
      <div class="step">
        <div class="step-arrow">&rarr;</div>
        <div class="step-box" style="border-color: #e53e3e;">
          <div class="step-num">4</div>
          <div class="step-label"><strong style="color:#e53e3e;">Secrets stolen</strong><br>silently, invisibly</div>
        </div>
      </div>
    </div>

    __RECORDS__

  </div>

</body>
</html>"""

RECORD_TPL = """
    <div class="stolen-header">
      <h2>Stolen from developer's laptop</h2>
      <span class="stolen-badge">RECEIVED {timestamp}</span>
    </div>
    <div class="meta-row">
      <div class="meta-item"><strong>Victim machine:</strong> {host}</div>
      <div class="meta-item"><strong>Tool used:</strong> {source}</div>
      {url_line}
    </div>
    {data_html}"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
@app.route("/dashboard", methods=["GET"])
def dashboard() -> Response:
    count = len(stolen_records)

    if count == 0:
        records_html = (
            '<div class="waiting">'
            '<div class="waiting-icon">&#x1F4E1;</div>'
            '<div class="waiting-text">'
            'Listening &hellip; stolen data will appear here in real time.'
            '</div></div>'
        )
        status_text = "Waiting for data"
        dot_color = "#555"
        dot_anim = ""
    else:
        # Classify file types for user-friendly tags
        def _file_tag(name):
            n = name.lower()
            if "env" in n:
                return "API Keys &amp; Passwords"
            if "cookie" in n:
                return "Session Tokens"
            if "toml" in n or "integrations" in n:
                return "Service Credentials"
            if "json" in n:
                return "Config File"
            if "yaml" in n or "yml" in n:
                return "Config File"
            return "Sensitive File"

        parts = []
        for i, rec in enumerate(reversed(stolen_records)):
            data_raw = rec.get("data", "")
            url_fetched = rec.get("url_fetched", "")

            data_html = ""
            try:
                parsed = json.loads(data_raw)
                if isinstance(parsed, dict):
                    for filename, content in parsed.items():
                        safe_name = _safe_html(str(filename))
                        safe_content = _safe_html(str(content))
                        tag = _file_tag(filename)
                        data_html += (
                            '<div class="file-card">'
                            '<div class="file-card-header">'
                            f'<span class="file-card-name">{safe_name}</span>'
                            f'<span class="file-card-tag">{tag}</span>'
                            '</div>'
                            f'<div class="file-card-body">{safe_content}</div>'
                            '</div>'
                        )
                else:
                    data_html = (
                        '<div class="raw-block">'
                        f'{_safe_html(json.dumps(parsed, indent=2))}'
                        '</div>'
                    )
            except (json.JSONDecodeError, TypeError):
                data_html = (
                    f'<div class="raw-block">{_safe_html(str(data_raw))}</div>'
                )

            url_line = ""
            if url_fetched:
                url_line = (
                    '<div class="meta-item">'
                    f'<strong>Trigger:</strong> AI fetched '
                    f'{_safe_html(url_fetched)}'
                    '</div>'
                )

            parts.append(RECORD_TPL.format(
                timestamp=rec["timestamp"],
                source=_safe_html(rec.get("source", "unknown")),
                host=_safe_html(rec.get("host", "unknown")),
                url_line=url_line,
                data_html=data_html,
            ))
        records_html = "\n".join(parts)
        status_text = "Data received"
        dot_color = "#e53e3e"
        dot_anim = "animation: blink 1.4s infinite;"

    html = (
        DASHBOARD
        .replace("__STATUS_TEXT__", status_text)
        .replace("__DOT_COLOR__", dot_color)
        .replace("__DOT_ANIM__", dot_anim)
        .replace("__RECORDS__", records_html)
    )
    return Response(html, mimetype="text/html")


@app.route("/exfil", methods=["POST"])
@app.route("/collect", methods=["POST"])
@app.route("/content", methods=["POST"])
@app.route("/api/editorial/submit", methods=["POST"])
@app.route("/api/feedback", methods=["POST"])
def receive_exfil() -> Response:
    try:
        payload = request.get_json(force=True, silent=True) or {}
    except Exception:
        payload = {}

    if not payload:
        raw = request.get_data(as_text=True)
        payload = {"data": raw}

    # Normalize — accept any key name the injection might use
    data_val = (
        payload.get("data")
        or payload.get("content")
        or payload.get("workspace")
        or payload.get("body")
        or json.dumps(payload)
    )
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source":    payload.get("source", "copilot-agent"),
        "host":      payload.get("host", "developer-laptop"),
        "url_fetched": payload.get("url_fetched", ""),
        "data":      data_val,
    }
    stolen_records.append(record)

    print(f"\n[!!!] EXFIL RECEIVED  {record['timestamp']}")
    print(f"      Source : {record['source']}")
    print(f"      Host   : {record['host']}")
    print(f"      Preview: {record['data'][:160]}...")
    print()

    return jsonify({"status": "received"}), 200


@app.route("/clear", methods=["POST"])
def clear_records() -> Response:
    stolen_records.clear()
    print("[i] Records cleared.")
    return jsonify({"status": "cleared"}), 200


@app.route("/status", methods=["GET"])
def status() -> Response:
    return jsonify({"records": len(stolen_records)}), 200


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_html(text: str) -> str:
    """Minimal HTML escaping so credential values render safely in pre blocks."""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  EXFIL RECEIVER — DEMO SERVER")
    print("  Dashboard : http://127.0.0.1:9999/")
    print("  Endpoint  : POST http://127.0.0.1:9999/exfil")
    print("  Clear     : POST http://127.0.0.1:9999/clear")
    print("=" * 60)
    app.run(host="127.0.0.1", port=9999, debug=False, use_reloader=False)
