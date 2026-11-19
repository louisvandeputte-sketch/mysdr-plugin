---
name: mysdr-onboarding
description: Set up a new mySDR workspace from the assistant after the mySDR connector is connected. Use when the user just connected mySDR, asks how to get started with mySDR, or a mySDR tool says onboarding is still open.
---

# mySDR onboarding

Use this after the user has connected the mySDR MCP server (OAuth: sign in on mysdr.app and click **Allow**). If no mySDR tools are available, tell the user to connect first: add `https://mysdr.app/api/mcp` as a connector (or install this plugin), then sign in and click **Allow**. Never ask for or paste an API key.

## Steps

1. Call `get_onboarding_context` to read where the workspace stands. Follow what it says is the next step; do not invent steps.
2. If the company website is missing, ask the user for it and save it with `save_company_website`.
3. Call `get_writing_context` to learn who sends outreach (name, role, company, language). Ask the user only for what is missing.
4. When a step is done, call `advance_onboarding` so mySDR records progress.
5. Call `get_usage` and tell the user their credit balance in one sentence, so they know what searches and enrichment will cost before they start.
6. Finish with one concrete next step, usually: "Shall we launch your first engine?" (see the `mysdr-first-engine` skill).

## Rules

- Tools whose title says "(spends credits)" cost credits. Say what it will cost and get a yes before calling them.
- Never send a LinkedIn message, email or connection request during onboarding.
- Keep answers short; show at most 10 rows of any list and offer to show more.
