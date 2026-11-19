# mySDR: submission prep (Cursor marketplace + Claude Connectors Directory)

Status: **prepared, nothing submitted.** Louis submits in the name of LVDP CommV.
Prepared 19 Nov 2026. ChatGPT / OpenAI plugin directory: **parked** (Louis, 19 Nov); the OAuth setup stays MCP-standard so it can be added later.

## Shared facts

| Field | Value |
| --- | --- |
| Legal entity / org name | LVDP CommV (VAT BE1008270260) |
| Product name | mySDR |
| Handle / slug | `mysdr` (permanent once published on Claude) |
| Contact email (review updates) | support@mysdr.app (decided by Louis, 19 Nov 2026) |
| Support contact | support@mysdr.app (listed in the terms). Canonical page: https://mysdr.app/en/support. https://mysdr.app/support redirects there (308, PR #1514, live since 19 Nov 2026 16:29 Europe/Brussels). |
| Website | https://mysdr.app |
| Documentation | https://mysdr.app/docs (start: https://mysdr.app/docs/getting-started/quickstart) |
| Privacy policy | https://mysdr.app/en/privacy (200; `/privacy` redirects here) |
| Terms of service | https://mysdr.app/en/terms (200; `/terms` redirects here) |
| MCP server URL | `https://mysdr.app/api/mcp` |
| Transport | Streamable HTTP (stateless POST; GET/DELETE return 405) |
| Auth type | OAuth 2.1 (MCP authorization spec): PRM discovery from the 401, AS metadata, Dynamic Client Registration, PKCE S256 only, `resource` (RFC 8707) checked, public clients (`none`) allowed, refresh tokens rotate. No API key or headers needed in config. |
| Icon | `assets/logo.svg` (512×512 square, gradient ball) and `assets/logo.png` (512×512) |
| Wordmark | `assets/wordmark.svg` |
| Plugin repo | https://github.com/louisvandeputte-sketch/mysdr-plugin (to be created, see below) |

**Short description (≤ 200 chars):**
> mySDR gives your AI assistant the GTM stack: find and enrich people and companies, watch buying signals, and run LinkedIn and email outreach, with a check before anything is sent.

**One-liner (≤ 30 chars, for tight fields):** `Sales prospecting & outreach`

**Long description (≤ 2,000 chars):**
> mySDR is the GTM layer for AI agents. Connect it once and your assistant can do the work of an SDR from the chat.
>
> Find: search people by role, company, region and seniority; find companies by the technology they use; enrich with full profiles, work emails and phone numbers. Tools that spend credits say so in their title, and `get_usage` shows the balance.
>
> Organize: save people and companies to your Leads and Companies tables, set stages and statuses, keep an exclusion list of people who are never contacted, and build dashboards.
>
> Signals: register and run signals that give a reason to reach out now, and review the leads they produce.
>
> Outreach: build flows, draft messages in the sender's own voice, run LinkedIn and email sequences, and pause or stop them at any time. Every send goes through `check_before_sending`, and sending tools are annotated so the assistant asks for confirmation.
>
> Follow-up: read replies and LinkedIn conversations, answer them, keep an agenda and human tasks, and look back at outcomes.
>
> Sign-in is OAuth: paste the URL (or install the plugin), sign in on mysdr.app and click Allow. Who it's for: founders, SDRs and sales teams who work with Claude, Cursor or another MCP client. Limitations: a mySDR account is required (free signup with starter credits); LinkedIn actions need a connected LinkedIn account in mySDR; searches and enrichment use credits.

**Categories:** Sales (primary), Productivity, CRM / Data enrichment, Marketing.

**Reads/writes:** both (read-only tools are annotated `readOnlyHint: true`; changing and sending tools are write tools).

## Reviewer test account (plan, NOT created)

- Separate test org "mySDR Review" (not a customer org, not ea1b38e0), owner `review@mysdr.app` (or a `+review` alias on louis@mysdr.app).
- Sign-in with email + password, **no MFA, no magic link, no Google-only login**, so a reviewer can log in at https://mysdr.app/en/login and click Allow.
- Bonus credits, e.g. 1,000 with the same grant mechanism as the 19 Nov gift (key `bonus:reviewer-2026-11:<org8>`, valid 12 months, reason "directory review").
- Sample data: ~20 fictional leads/companies, one flow, one dashboard. No LinkedIn account connected, so no real messages can be sent; outreach tools show their safe "not connected" answer.
- Credentials are given only in the secure portal form or by email when a reviewer asks (Claude Verified review), never in the repo.
- Needs Louis' OK before it is created.

---

## 1. Cursor marketplace (cursor.com/marketplace/publish)

The publish form loads behind a Cursor login, so the exact fields could not be read. Per the Cursor plugin docs the submission is a **public Git repo link** plus a review by the Cursor team. Prepare:

| Field | Value |
| --- | --- |
| Repository URL | https://github.com/louisvandeputte-sketch/mysdr-plugin |
| Plugin name (manifest `name`) | `mysdr` |
| Publisher / org | LVDP CommV |
| Contact email | support@mysdr.app |
| Description | short description above |
| Keywords | sales, gtm, outreach, linkedin, lead-generation, enrichment, crm, mcp |
| Logo | `assets/logo.svg` (relative path in manifest) |
| License | MIT |
| How a reviewer tests | Install the plugin → mySDR shows "needs login" → Connect → sign in with the reviewer account → Allow → ask "What's my mySDR credit balance?" (`get_usage`) |

Submission checklist (from cursor.com/docs/plugins/building), status:

- [x] Valid `.cursor-plugin/plugin.json`, `name` lowercase kebab-case
- [x] `description` explains the purpose
- [x] Skills have valid `SKILL.md` frontmatter (`name`, `description`)
- [x] Logo committed and referenced by relative path
- [x] `README.md` documents usage
- [x] All manifest paths relative, no `..`
- [x] No `${VAR}` in `mcp.json` (OAuth, no secrets), so no `variables` needed
- [x] `scripts/validate.sh` passes (package + live discovery)
- [ ] Tested locally in Cursor (Louis or a desktop session): install from local folder, Connect, Allow, call `get_usage`

Grok Bot: uses the same remote MCP URL and OAuth flow; the listing route for Grok Bot's connector catalog is not public yet. Same fields apply.

## 2. Claude Connectors Directory (claude.ai/directory/manage → Submit new → MCP connector)

Sources: claude.com/docs/connectors/building/submission and /review-criteria. Any paid Claude plan can submit (Louis has one).

| Portal step | What to enter |
| --- | --- |
| 1. Connection | `https://mysdr.app/api/mcp` (single URL for all users) |
| 2. Tools | Syncs automatically. 69 tools; all have `title` + `readOnlyHint`/`destructiveHint`. Fix #1508 first (destructive hints on modify/send tools). |
| 3. Listing | Name: `mySDR` · One-liner: short description · Description: long description · Categories: Sales, Productivity · Docs URL: https://mysdr.app/docs · Privacy: https://mysdr.app/en/privacy · Support: support@mysdr.app · Icon: `assets/logo.png` · Slug: `mysdr` |
| 4. Use cases | Prospecting (find + enrich), list building in Leads/Companies tables, signal-based lead discovery, LinkedIn/email outreach with pre-send checks, reply handling. Prerequisites: mySDR account (free signup); LinkedIn connected in mySDR for LinkedIn actions; credits for search/enrichment. Reads and writes. |
| 5. Company | LVDP CommV · https://mysdr.app · primary contact support@mysdr.app |
| 6. Authentication | Required · OAuth (Dynamic Client Registration; no Anthropic-held client needed) |
| 7. Data handling | Own first-party API (mySDR), which uses licensed data providers for enrichment; no personal health data; no sponsored content |
| 8. Test & launch | Confirm every tool was run via MCP Inspector and as a custom connector in Claude. No credentials in the portal. |
| 9. Compliance | Seven acknowledgments (directory guidelines, first-party API use, financial transactions: none, AI media generation: none, prompt injection, conversation data collection, public documentation) |
| 10. Review | Check for quality warnings, then Louis submits |

Requirement status (audit 19 Nov 2026):

| Requirement | Status | Evidence |
| --- | --- | --- |
| Remote HTTPS + Streamable HTTP | ok | `POST /api/mcp` → 401 JSON; stateless, GET/DELETE 405 |
| OAuth 2.0 | ok | 401 `WWW-Authenticate` with `resource_metadata`; PRM, AS metadata, DCR, S256, refresh; Claude callbacks accepted |
| Every tool: `title` + read-only/destructive hint | ok (review hints: partial) | 69/69 have both; modify/send tools have `destructiveHint: false`, see #1508 |
| No catch-all read+write tool | ok | No generic request tool |
| Tool names ≤ 64 chars | ok | Longest 31 |
| Actionable errors | ok | 401 explains how to connect; OAuth errors carry `error_description` |
| Frugal responses | partial | Read tools paginate (`limit` max 50–500); sizes not measured yet (#1508) |
| Public docs page | ok | https://mysdr.app/docs |
| Privacy policy URL | ok | https://mysdr.app/en/privacy |
| Support contact | ok | support@mysdr.app; https://mysdr.app/en/support (canonical); `/support` redirects there |
| Icon | ok | 512×512 square |
| CORS on MCP endpoint | missing | Needed for browser clients like MCP Inspector web (#1509) |

### Test as a custom connector in Claude (Louis, paid plan)

1. claude.ai → Settings → Connectors → **Add custom connector**.
2. Name `mySDR`, URL `https://mysdr.app/api/mcp`, leave OAuth client ID/secret empty → **Add**.
3. Click **Connect** → mysdr.app opens → sign in → **Allow** → back in Claude, mySDR shows as connected.
4. In a new chat, turn on mySDR under the tools menu and run: "What's my mySDR credit balance?" (`get_usage`), "Show my mySDR agenda for today" (`get_agenda`), "List my Leads table, 5 rows" (`list_table`), "Find 3 heads of sales at Belgian SaaS companies, tell me the cost first" (`search_people`, confirm first).
5. Check that read-only tools run without a prompt and that write/send tools ask for confirmation.
6. Settings → Connectors → mySDR → **Disconnect**, then confirm the link is gone in mySDR.
