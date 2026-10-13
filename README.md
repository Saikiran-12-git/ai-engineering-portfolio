# AI Engineering Portfolio

Six projects inspired by the supplied video transcript, focused on observable,
testable engineering behavior. This repository is a work in progress.

| Project | Status |
| --- | --- |
| 01 MCP engineering task manager | Implemented; local storage and protocol tests provided |
| 02 Offline Java code-review assistant | Planned |
| 03 Runbook RAG with telemetry and evaluations | Planned |
| 04 Incident-investigation agent workflow | Planned |
| 05 Voice Java interview coach | Planned |
| 06 Incident-report fine-tuning pipeline | Planned; training requires suitable hardware |

Start with [the MCP project](projects/01-mcp-task-manager/README.md).
No API key, paid service, or downloaded model is required for project 01.

## Publishing to GitHub

Create an empty repository named `ai-engineering-portfolio` under your account.
Do not initialize the remote with a README if using these first-push commands.
From the extracted `ai-engineering-portfolio` directory:

```bash
git init -b main
git add .
git commit -m "Add MCP engineering task manager and portfolio roadmap"
git remote add origin https://github.com/Saikiran-12-git/ai-engineering-portfolio.git
git push -u origin main
```

These commands assume a new empty remote, not an existing repository with history.
Authenticate through your Git client; never put a token in this repository.

## Scope

Use synthetic engineering tasks and documents. Completed milestones should record
measured results, known limitations, and reproducible demo commands. No training,
voice, retrieval, or model-quality results are claimed for planned projects.
