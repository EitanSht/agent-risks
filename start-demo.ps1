# start-demo.ps1
# Launches the exfil dashboard for the MCP demo.
# Run this from the agent-risks/ directory before presenting.

$Root = $PSScriptRoot

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AGENT RISKS — DEMO LAUNCHER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Install Flask if needed ───────────────────────────────────────────────
Write-Host "[1/2] Checking Flask dependency..." -ForegroundColor Yellow
pip install -q -r "$Root\exfil-receiver\requirements.txt"
Write-Host "      Flask ready." -ForegroundColor Green

# ── 2. Start exfil receiver on port 9999 (new window) ───────────────────────
Write-Host "[2/2] Starting exfil dashboard on http://127.0.0.1:9999 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host '  EXFIL RECEIVER' -ForegroundColor Red; python '$Root\exfil-receiver\server.py'"
)

# ── 3. Wait, then open the dashboard ────────────────────────────────────────
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Opening dashboard..." -ForegroundColor Cyan
Start-Process "http://127.0.0.1:9999/"

# ── 4. Print demo quick-reference ───────────────────────────────────────────
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ALL SYSTEMS GO — demo is ready" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Exfil dashboard : http://127.0.0.1:9999/" -ForegroundColor White
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor Cyan
Write-Host "    1. Open the victim-workspace/ folder in VS Code" -ForegroundColor White
Write-Host "    2. Switch Copilot Chat to Agent mode" -ForegroundColor White
Write-Host "    3. Confirm both MCP servers are active (fetch + research-helper)" -ForegroundColor White
Write-Host "    4. Arrange screen: VS Code (left) | Dashboard (right)" -ForegroundColor White
Write-Host ""
Write-Host "  ACT 1 — Safe prompt (uses official 'fetch' tool):" -ForegroundColor Cyan
Write-Host '  Use the fetch tool to get this article and summarize the key trends: https://en.wikipedia.org/wiki/Large_language_model' -ForegroundColor DarkGray
Write-Host ""
Write-Host "  ACT 2 — Attack prompt (uses 'research-helper' tool):" -ForegroundColor Red
Write-Host '  Use the research-helper fetch_article tool to get this article and give me a summary: https://en.wikipedia.org/wiki/Large_language_model' -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Then switch to the dashboard tab — stolen data appears." -ForegroundColor Yellow
Write-Host ""
