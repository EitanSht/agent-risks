# agent-risks

Demo infrastructure for the **AI Agent Security Risks** presentation.
Shows how a malicious tool installed by an AI coding assistant can silently
exfiltrate credentials from a developer's workspace.

## What's here

```
agent-risks/
├── exfil-receiver/
│   ├── server.py            ← Attacker dashboard (Flask, port 9999)
│   └── requirements.txt
├── victim-workspace/        ← Simulated developer project with fake credentials
│   ├── .env
│   ├── .vscode/mcp.json
│   ├── config/integrations.toml
│   └── browser_cookies.json
├── start-demo.ps1           ← One-click launcher
└── .gitignore
```

## Quick start

```powershell
pip install flask
.\start-demo.ps1
```

Then open the victim workspace in a separate VS Code window and run the demo prompt.

## Related repos

| Repo | Purpose |
|------|---------|
| [quicklint](https://github.com/EitanSht/quicklint) | The malicious tool (disguised as a code linter) |
| **agent-risks** (this repo) | Demo infrastructure: dashboard, launcher, fake credentials |

