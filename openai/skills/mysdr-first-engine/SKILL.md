---
name: mysdr-first-engine
description: Launch a first mySDR engine (who to reach, how leads come in, how outreach is drafted) and get to first outreach safely. Use when the user asks to start prospecting, find leads, launch an engine or campaign, or "get my first meetings" with mySDR.
---

# Launch a first mySDR engine

An engine in mySDR is one outbound motion: who you target, how leads come in, and how the outreach is written and sent. This skill gets a user from zero to a first reviewed outreach.

## Steps

1. Call `get_outreach_playbook`. It returns the next step to first outreach for this workspace. Follow it in order.
2. Agree on the target with the user: role or title, company size, industry, region. Keep it to one segment for the first engine.
3. Set how leads come in with `save_lead_influx` (for example a people search, a signal, or a list the user saves).
4. Preview leads with `search_people` (it may spend credits: state the cost and get a yes first). Save the ones the user approves with `save_leads`.
5. Set how outreach is drafted with `save_draft_outreach`, using `get_writing_context` for the sender's voice. Show the user one example draft.
6. Before anything is sent, call `check_before_sending` and show the result.
7. Only after an explicit "yes, send" from the user, start outreach with `start_flow` or `start_linkedin_sequence`. Then call `get_outreach_status` and summarize.

## Rules

- If the user gives an explicit instruction that narrows or redirects this workflow, follow that instruction. Do not override a refusal to send, spend credits, or contact someone on the exclusion list. Do not invent people, companies, prices, or tool results.
- Never start a sequence, send a message, or spend credits without the user's explicit yes in this conversation.
- Respect exclusions: `list_exclusions` shows who is never contacted.
- To pause or stop, use `update_campaign` or `stop_linkedin_sequence` and confirm it worked.
- Report numbers (leads found, credits spent, messages queued) in one short summary at the end.
