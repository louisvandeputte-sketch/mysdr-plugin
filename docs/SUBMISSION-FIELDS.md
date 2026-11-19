# mySDR — submission field values (Claude Connectors Directory + Cursor Marketplace)

Status: **prepared only. Do not submit.** Louis submits in the name of LVDP CommV, from his own paid Claude account and his own Cursor account. Nothing in this file is a submission.

Prepared: 19 November 2026, Europe/Brussels. Based on the plugin package at commit `5f07b24` plus this document, the live MCP server at `https://mysdr.app/api/mcp` (OAuth DCR + PKCE S256 + RFC 8707 + CIMD, live since PR #1512 / main `393f8848`), and the public site pages verified the same day.

---

## Nederlands (kort)

Dit bestand vult elk indienveld voor (a) de Claude Connectors Directory en (b) de Cursor Marketplace. **Niets indienen** — Louis dient zelf in, namens LVDP CommV.

De publieke repo [louisvandeputte-sketch/mysdr-plugin](https://github.com/louisvandeputte-sketch/mysdr-plugin) bestaat (aangemaakt 19 nov 2026, 16:03 Europe/Brussels) maar was op dat moment nog leeg (geen commit, geen README, geen LICENSE). De pakketcode staat lokaal in `/workspace/mysdr-plugin`. De reviewer-testorg is **nog niet aangemaakt**; in dit document staan alleen placeholders, nooit echte inloggegevens.

Open punten voor Louis staan onderaan, samen met eisen die mySDR nog niet (volledig) haalt: vooral het Cursor-logo zonder ondoorzichtige achtergrondplaat, de nog lege remote tot de code is gepusht, de ontbrekende reviewer-org, en de bevestiging dat elke tool in Claude is getest.

---

## 1. Official sources (retrieved 19 Nov 2026)

Every field list below is taken from these pages (all HTTP 200 unless noted). The live submission portals themselves require a login (`https://claude.ai/directory/manage` returned 403 unauthenticated; `https://cursor.com/marketplace/publish` shows the form only after sign-in, but the field labels were read from the page's public JavaScript bundle).

### Claude / Anthropic

| Document | URL |
| --- | --- |
| Submit a connector (portal steps and listing limits) | https://claude.com/docs/connectors/building/submission |
| Connector pre-submission / review criteria | https://claude.com/docs/connectors/building/review-criteria |
| Publish to the directory (who can submit; connector vs plugin) | https://claude.com/docs/directory/publish |
| Authentication for connectors (DCR, CIMD, options) | https://claude.com/docs/connectors/building/authentication |
| Connectors directory overview | https://claude.com/docs/connectors/directory |
| Anthropic Software Directory Terms (16 Mar 2026) | https://support.claude.com/en/articles/13145338-anthropic-software-directory-terms |
| Anthropic Software Directory Policy | https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy |
| Developer portal (submit here; login required) | https://claude.ai/directory/manage |
| Public marketplace (category names) | https://claude.com/marketplace and https://claude.com/marketplace/connectors-plugins |
| Escalations | `mcp-review@anthropic.com` |

### Cursor

| Document | URL |
| --- | --- |
| Plugins reference (package checklist + “submit the repository link”) | https://cursor.com/docs/reference/plugins |
| Plugins overview (redirects from `/docs/plugins` and `/docs/plugins/building`) | https://cursor.com/docs/plugins |
| Publish form (“Become a plugin publisher”) | https://cursor.com/marketplace/publish |
| Cursor Marketplace Publisher Terms (last updated 6 May 2026) | https://cursor.com/marketplace-publisher-terms |
| Questions | `marketplace-publishing@cursor.com` |

Field labels on the Cursor form were read from the public JS shipped with `https://cursor.com/marketplace/publish` on 19 Nov 2026 (`0zud92engv4jn.js`): Organization name, Organization handle, Contact email, Logotype URL, Description, GitHub repository, Owner (disabled / locked to the signed-in account), Website URL, and the Submit Application acknowledgement of the Publisher Terms. Official docs describe the same flow as: sign in, submit a public GitHub repository URL, then manual review.

---

## 2. Shared facts (verified URLs)

curl on 19 Nov 2026, Europe/Brussels. Prefer the final 200 URL in listings.

| Field | Proposed value | Verification |
| --- | --- | --- |
| Legal entity / publisher | LVDP CommV (VAT BE1008270260) | LICENSE; existing package |
| Product name | mySDR | site, docs, MCP `resource_name` |
| Website | https://mysdr.app | 200, redirects to https://mysdr.app/en |
| Documentation | https://mysdr.app/docs | 200. Start / connect guide: https://mysdr.app/docs/getting-started/quickstart (200). Markdown index: https://mysdr.app/docs.md (200) |
| Privacy policy | https://mysdr.app/en/privacy | 200. https://mysdr.app/privacy redirects here. Last updated 28 Oct 2026. Contact on the page: `privacy@mysdr.app`. Covers collection, use, third-party sources, retention, and contact. |
| Terms of service | https://mysdr.app/en/terms | 200. https://mysdr.app/terms redirects here. Support address on the page: `support@mysdr.app` |
| Support page | https://mysdr.app/en/support | 200, last updated 19 Nov 2026. Mailto: `support@mysdr.app`. **Do not use** https://mysdr.app/support (404). |
| Support contact (email) | support@mysdr.app | Listed on /en/support and /en/terms. “We read it on business days and reply from that address.” |
| DPA (related, not a form field) | https://mysdr.app/en/dpa | 200 |
| Do not sell (related) | https://mysdr.app/en/do-not-sell | 200 |
| Pricing (related) | https://mysdr.app/en/pricing | 200 |
| Login (for reviewer instructions) | https://mysdr.app/en/login | 200 |
| MCP server URL | `https://mysdr.app/api/mcp` | POST without a token: 401 + `WWW-Authenticate` `resource_metadata`. GET: 405, `Allow: POST`. OPTIONS CORS: 204, `access-control-allow-origin: *` (live since PR #1512). |
| Transport | Streamable HTTP (stateless POST) | Matches Anthropic policy: remote servers should support Streamable HTTP. |
| Auth | OAuth 2.1 / MCP authorization: discovery from the 401, AS metadata, Dynamic Client Registration, Client ID Metadata Documents (`client_id_metadata_document_supported: true`), PKCE S256 only, `resource` (RFC 8707), public clients (`token_endpoint_auth_methods_supported` includes `none`), refresh tokens. No API key in the client config. | `https://mysdr.app/.well-known/oauth-authorization-server` and `https://mysdr.app/.well-known/oauth-protected-resource/api/mcp` both 200. |
| Plugin repository | https://github.com/louisvandeputte-sketch/mysdr-plugin | Public repo, created 19 Nov 2026 16:03 Europe/Brussels. Empty at creation (size 0, no commits, no README, no LICENSE). Local package is this repo. |
| Primary review contact | louis.vandeputte@gmail.com | Default requested for these forms. See open items if a form prefers a domain address. |
| Domain addresses already on the public site | support@mysdr.app, privacy@mysdr.app | Do not invent other mysdr.app mailboxes in the form without Louis confirming they are monitored. The package `plugin.json` currently has `author.email` `louis@mysdr.app` — confirm before relying on it. |
| Icon / logo in the package | `assets/logo.svg` (512×512 SVG, gradient circle) and `assets/logo.png` (512×512 PNG, RGBA). Wordmark: `assets/wordmark.svg` (not square). | See the Cursor plate gap in §7. |
| License | MIT, © 2026 LVDP CommV | `LICENSE`. Cursor Publisher Terms §3.3 allow permissive licenses (MIT, BSD, Apache 2.0) and forbid GPL/AGPL/LGPL. Listing is free; the plugin must remain free on the Marketplace (Terms §3.1). |

**Handle / slug:** `mysdr` (Claude listing slug is permanent once published).

**Short description / one-liner (179 characters, limit 200):**

> mySDR gives your AI assistant the GTM stack: find and enrich people and companies, watch buying signals, and run LinkedIn and email outreach, with a check before anything is sent.

**Tight one-liner (28 characters, only if a field is ~30 characters):** `Sales prospecting & outreach`

**Long description (1,392 characters, limit 2,000):**

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

---

## 3. Claude Connectors Directory

**Portal:** https://claude.ai/directory/manage → **Submit new** → **MCP connector**.

**Who can submit:** any paid Claude plan (Pro, Max, Ultra, Team, or Enterprise). Free accounts cannot submit. On Pro/Max/Ultra, submit from the account that should own the listing. On Team/Enterprise, an Owner submits. Source: https://claude.com/docs/directory/publish. Louis has a paid Claude account (his words, 19 Nov). Submit from that account, in the name of LVDP CommV.

**What to submit now:** one **MCP connector** (the remote server). Official docs also recommend a second, later **plugin bundle** submission from the GitHub repo if you want the skills listed as a plugin and paired with the connector. That is optional and is not prepared as a submit-now action here (see §3.11). ChatGPT / OpenAI remains parked.

Anthropic scans a connector automatically and, by default, lists it as a **Community** connector. A person may later escalate it to **Verified** review and will then email for test access. Do not put credentials in the portal.

### 3.1 Connection

| Field | Proposed value | Notes |
| --- | --- | --- |
| Server URL | `https://mysdr.app/api/mcp` | Single URL for all users. Paste this, or pick a custom connector already added in Claude. |
| Users connect to different URLs | **No** — leave this off | Docs also describe per-workspace URLs (`https://mysdr.app/api/mcp/w/<workspace-id>`). Do **not** select Multiple URLs or URL pattern. Those listings can be published only after the Verified label. The default URL already binds to the workspace that is open when the user clicks Allow; the docs page explains the `/w/` form for people who have several workspaces. |

### 3.2 Tools

The portal syncs tools, prompts, and resources from the connected server and groups them by read-only vs write annotations. If anything is flagged for a missing `title` or hint, fix it on the server before submitting.

**Summary (code audit of PR #1512 head `9f3e7fd7`, now on main `393f8848`; 79 unique tools):**

- Every tool has a `title` and `readOnlyHint` or `destructiveHint`. Longest tool name: 31 characters (limit 64). No catch-all read+write `api_request` tool.
- **32 read-only tools** — `readOnlyHint: true`, `destructiveHint: false` (some also set `idempotentHint` / `openWorldHint`).
- **47 write/spend tools** — `destructiveHint: true` (the earlier gap in #1508, modify/send tools with `destructiveHint: false`, was fixed in PR #1512).

The portal is the source of truth on submit day (it reads the live server). The inventory below is the package/server list as audited on 19 Nov 2026.

**Read-only (`readOnlyHint: true`):**
`check_before_sending` (Check before sending);
`find_technologies` (Find a technology (free));
`get_activity` (Read the activity log);
`get_agenda` (Your agenda for the day);
`get_dashboard` (What a dashboard shows now);
`get_flow` (One outreach flow);
`get_gtm_brain` (Outbound brain);
`get_lead_context` (One lead in context);
`get_linkedin_conversation` (Read a LinkedIn conversation);
`get_onboarding_context` (Onboarding status);
`get_outcome_review` (Look back at the outcomes);
`get_outreach_events` (Outreach events);
`get_outreach_playbook` (The outreach playbook: the next step to first outreach);
`get_outreach_status` (Outreach status);
`get_replies` (New replies);
`get_search_results` (Get search results (free));
`get_table_row` (One row of the tables, with its activity);
`get_usage` (Credits: balance and usage);
`get_writing_context` (Writing context);
`list_agent_signals` (Your own signals);
`list_dashboards` (The user’s dashboards);
`list_exclusions` (Who is never contacted);
`list_flows` (Outreach flows);
`list_human_tasks` (Human tasks);
`list_leads` (Leads from the user’s signals);
`list_linkedin_conversations` (List LinkedIn conversations);
`list_mentions` (List mentions (free));
`list_stages` (Your organization’s stages);
`list_table` (Read the Leads or Companies table);
`list_team` (Who is in the team);
`lookup_company` (Look up a company page (free));
`preview_cost` (Preview a cost (free)).

**Write / spend (`destructiveHint: true`):**
`add_exclusions`;
`advance_onboarding`;
`assign_flow`;
`complete_human_task`;
`create_campaign`;
`create_human_task`;
`create_monitor` (spends credits on each run);
`delete_agent_signal`;
`delete_dashboard`;
`delete_flow`;
`enrich` (spends credits);
`enrich_companies` (spends credits);
`enrich_people` (spends credits);
`find_companies_using_technology` (spends credits);
`find_phones` (spends credits);
`get_tech_stack` (spends credits);
`hand_back`;
`log_outreach_activity`;
`log_signal_hits`;
`manage_monitor` (free);
`mark_linkedin_conversation_read`;
`propose_learning`;
`remove_exclusion`;
`remove_saved`;
`reverse_email_lookup` (spends credits);
`save_agent_signal`;
`save_companies`;
`save_company_website`;
`save_dashboard`;
`save_draft_outreach`;
`save_email_signature`;
`save_flow`;
`save_gtm_brain`;
`save_lead_influx`;
`save_leads`;
`search_companies` (spends credits);
`search_people` (spends credits);
`search_signals` (spends credits);
`send_linkedin_message`;
`send_reply`;
`set_lead_status`;
`set_stages`;
`start_flow`;
`start_linkedin_sequence`;
`stop_linkedin_sequence`;
`update_campaign`;
`update_row`.

Tools whose titles include “(spends credits)” charge the workspace. `get_usage` shows the balance. LinkedIn send tools require a LinkedIn account connected in mySDR; without it they return a safe “not connected” result rather than sending.

### 3.3 Listing (public card)

| Field | Limit | Proposed value |
| --- | --- | --- |
| Server name | 100 characters | `mySDR` |
| One-liner | 200 characters | The short description in §2 (179 characters) |
| Description | 2,000 characters | The long description in §2 (1,392 characters). Anthropic cannot edit this after you write it in the portal. |
| Categories | 1–5 | **Sales & marketing** (primary), **Productivity**. Optional third: **Data analytics**. See slugs below. Do not invent names such as “Sales” or “CRM” — those are not directory categories. |
| Documentation URL | — | https://mysdr.app/docs |
| Privacy policy URL | — | https://mysdr.app/en/privacy |
| Support contact | — | `support@mysdr.app` (and, if a URL is accepted, https://mysdr.app/en/support) |
| Icon | — | `assets/logo.png` (512×512 PNG). `assets/logo.svg` is the same mark. Claude does not require a background plate. |
| URL slug | Permanent once published | `mysdr` → listing URL `https://claude.ai/directory/connectors/mysdr` |

**Official category slugs** observed on 19 Nov 2026 in the public marketplace catalogue (`https://claude.com/marketplace/connectors-plugins`, 1,031 listings). Display names follow the live HubSpot listing and slug wording:

| Slug | Display name (as shown) | Use for mySDR? |
| --- | --- | --- |
| `sales-and-marketing` | Sales & marketing (confirmed on https://claude.com/marketplace/connectors/hubspot) | **Yes, primary** |
| `productivity` | Productivity | **Yes** |
| `data-analytics` | Data analytics (slug; typography in the portal may use “Data & analytics”) | Optional third |
| `developer-tools`, `financial-services`, `communication`, `legal`, `creative`, `commerce-shopping`, `other`, `health-life-sciences`, `education`, `media-entertainment`, `travel`, `consumer-health`, `nonprofit` | — | No |
| `healthcare` | Appeared on 1 listing only | No |

mySDR is not an MCP App (no interactive UI), so carousel screenshots are not required.

**Allowed link URIs:** omit unless the server uses `ui/open-link`. Optional; if omitted, users just confirm unknown links.

### 3.4 Use cases

| Field | Proposed value |
| --- | --- |
| Primary use cases | (1) Prospecting: find and enrich people and companies. (2) List building: save leads and companies to workspace tables, set stages and statuses, keep an exclusion list, build dashboards. (3) Signal-based lead discovery: register and run buying signals, review the leads they produce. (4) Outreach: LinkedIn and email flows and sequences, with `check_before_sending` before anything is sent. (5) Follow-up: read replies and LinkedIn conversations, answer them, keep an agenda and human tasks, review outcomes. |
| What users need before they can connect | A mySDR account (free signup, starter credits; the Allow page can create one). LinkedIn send/reply tools need a LinkedIn account connected in mySDR. Search and enrichment tools spend credits; `preview_cost` and `get_usage` are free. Owners and admins can connect an assistant. |
| Reads data, writes data, or both | **Both.** Read-only tools are annotated `readOnlyHint: true` (can run without a per-call confirmation). Write and send tools are annotated `destructiveHint: true` (Claude should prompt). |

### 3.5 Company

| Field | Proposed value |
| --- | --- |
| Company name | LVDP CommV |
| Company website | https://mysdr.app |
| Primary contact for review updates | louis.vandeputte@gmail.com |

If the portal insists on a company-domain mailbox, use one Louis confirms is monitored (open item). Do not put secrets in this field.

### 3.6 Authentication

| Field | Proposed value |
| --- | --- |
| Authentication requirement | **Required** (users must sign in). The server is not authless and does not use lazy authentication: a POST without a token is 401 and starts OAuth. |
| Authentication methods | **OAuth 2.0** with Dynamic Client Registration (`oauth_dcr`) and Client ID Metadata Documents (`oauth_cimd`). Both are advertised and supported (`registration_endpoint` present; `client_id_metadata_document_supported: true`). |
| Anthropic-held OAuth client (client ID + secret) | **Leave empty.** Claude registers itself (DCR) or presents a CIMD. Do not paste a client secret into the portal. |
| Custom connection / static headers | Not used. |

### 3.7 Data handling

| Field | Proposed value |
| --- | --- |
| Underlying API | **Our own first-party API** (mySDR at mysdr.app). The product uses licensed data providers for enrichment and signals, as described in the privacy policy (HarvestAPI, SignalHire, TheirStack, Fundable, StartupMap, PredictLeads). This is first-party product functionality, not an uncontrolled third-party API wrapper. The MCP host matches the service domain. |
| Personal health data | **No** |
| Sponsored content | **No** |

### 3.8 Test & launch

| Field | Proposed value |
| --- | --- |
| Confirmation that every tool was run | Louis must tick this only after he has actually run the tools — via MCP Inspector and/or as a custom connector in Claude. This is an open item; it has not been signed off in this preparation. |
| Credentials in the portal | **None.** Policy and portal: “Don't put credentials in the portal.” If the listing is escalated to Verified review, a reviewer emails and asks for test access. |

**How Louis tests as a custom connector (before ticking the box):**

1. claude.ai → Customize → Connectors → Add custom connector.
2. Name `mySDR`, URL `https://mysdr.app/api/mcp`. When asked for an OAuth client, choose register automatically and leave client ID and secret empty → Add.
3. Connect → sign in at mysdr.app → Allow.
4. In a new chat, enable mySDR and run the example prompts in §5.
5. Confirm read-only tools run without a confirmation prompt and write/send tools ask first.
6. Disconnect when done, and confirm the grant is gone in mySDR.

**Test-account instructions to give a reviewer (only when they email; never in the portal, never in this repo):** see §5. The reviewer org is **not created yet**. Use the placeholder wording there.

### 3.9 Compliance (seven required acknowledgments)

Louis must read the Directory Terms and Policy and acknowledge all seven in the portal. Proposed stance (for his review, not a submission):

1. **Directory guidelines** — the connector will comply with the Anthropic Software Directory Terms and Policy, and LVDP CommV will maintain security and functionality, respond to security issues promptly, and keep descriptions accurate.
2. **First-party API usage** — the server calls mySDR’s own API (and licensed providers behind that product), on the mysdr.app domain.
3. **Financial transactions** — the connector does not transfer money, cryptocurrency, or other financial assets, and does not execute financial transactions autonomously. (Buying mySDR credits happens in the mySDR billing UI, not through an MCP money-transfer tool.)
4. **AI media generation** — the connector does not generate images, video, or audio through AI models.
5. **Prompt injection** — tool descriptions state what each tool does; they do not instruct Claude to call unrelated software, override system instructions, or hide instructions.
6. **Conversation data collection** — tools do not collect conversation data beyond what they need, and do not query Claude’s memory, chat history, conversation summaries, or user files.
7. **Public documentation** — https://mysdr.app/docs and https://mysdr.app/docs/getting-started/quickstart are public and will remain available by the publish date.

### 3.10 Review and submit

Check the summary for quality warnings (short answers are flagged and shown to reviewers). **Louis clicks submit.** After submit, status lives in the same portal. Default label: Community.

### 3.11 Optional later: Claude plugin bundle (not part of the connector form)

Official docs (https://claude.com/docs/directory/publish): if you also want the skills listed, submit a **plugin bundle** from the public GitHub repository as a second listing, from the same organization, and pair it with the connector. Requires the repo to contain the plugin on the tracked branch. Not required to get the connector into the directory. Do not start this until Louis decides to.

---

## 4. Cursor Marketplace

**Portal:** https://cursor.com/marketplace/publish (sign-in required: “You need to be signed in to submit a plugin publisher application.”).

This is a **publisher application + first plugin repository** form, not a multi-step MCP wizard. Plugin name, MCP URL, skills, and keywords come from the public repo (`/.cursor-plugin/plugin.json`, `mcp.json`, `skills/`, `README.md`). Clicking **Submit Application** acknowledges the [Publisher Terms](https://cursor.com/marketplace-publisher-terms). There is no fee. The plugin must remain free on the Marketplace. License must stay permissive (MIT is already in the package).

**Who submits:** Louis, signed in to the Cursor account that should own the listing. The **Owner** field is disabled and locked to that account (“Submitting as an individual.” or “Submitting as your team.”). There is no in-form control to switch an individual account to a company; the company name goes in Organization name and in `plugin.json` `author.name` (`LVDP CommV (mySDR)`).

### 4.1 Form fields (live labels, 19 Nov 2026)

| Form field | Internal id | Proposed value | Validation / notes |
| --- | --- | --- | --- |
| Organization name | `displayName` | `LVDP CommV` | Required. Placeholder on the form: “Acme Labs”. |
| Organization handle | `publisherName` | `mysdr` | Required. Hint: “Unique namespace (kebab-case, e.g. @acme-labs)”. Must match kebab-case with optional periods. Uniqueness is checked at submit. Confirm `mysdr` is still free when submitting. |
| Contact email | `contactEmail` | `louis.vandeputte@gmail.com` | Required, must be a valid email. Placeholder: `email@acme.com` (no domain-mail requirement in the script). If Louis prefers a monitored company address, swap it before submit (open item). |
| Logotype URL | `logoUrl` | After the package is on `main`: `https://raw.githubusercontent.com/louisvandeputte-sketch/mysdr-plugin/main/assets/logo.svg` | Required; must be `http` or `https`. Hint: “Link to your logo. 1:1 SVG or PNG with background plate.” **Gap:** the current `assets/logo.svg` / `assets/logo.png` are a 512×512 gradient circle on a **transparent** background (corners are fully transparent). That is 1:1 SVG/PNG, but it is not a background plate and can disappear on Cursor’s dark UI. Recommended: add a 512×512 plate asset (opaque square, e.g. white or `#14161A`, with the existing mark centred) as `assets/logo-plate.png` or `assets/logo-plate.svg`, commit it, and use that raw URL instead. Until a plate file exists, do not treat this field as ready. |
| Description | `description` | The short description in §2 | Optional in the script (an empty value is omitted), but should be filled. Placeholder: “Briefly describe what your plugin does and how it helps users.” |
| GitHub repository | `repositoryUrl` | `https://github.com/louisvandeputte-sketch/mysdr-plugin` | Required. Must match `https://github.com/org/repo`. The repository is public. It must contain the plugin package (`.cursor-plugin/plugin.json`, `mcp.json`, logo, README, LICENSE, skills) on `main` before submit. At repo creation it was empty — push the local package first. |
| Owner | `owner` | Locked to Louis’s signed-in Cursor account | Disabled. Not editable. |
| Website URL | `websiteUrl` | `https://mysdr.app` | Optional, but fill it. If present, must be `http` or `https`. |
| Submit Application | button | **Louis clicks this.** | “By clicking Submit Application, you acknowledge and agree to the Publisher Terms.” Do not click during this preparation. |

**Not on the form** (taken from the repo / manifest):

| Item | Value in the package |
| --- | --- |
| Plugin `name` | `mysdr` (kebab-case) |
| `display` / description | See `.cursor-plugin/plugin.json` |
| Version | `1.0.0` |
| Author | LVDP CommV (mySDR); email in the manifest is currently `louis@mysdr.app` |
| Homepage | https://mysdr.app |
| Repository | https://github.com/louisvandeputte-sketch/mysdr-plugin |
| License | MIT |
| Keywords | sales, gtm, outreach, linkedin, lead-generation, enrichment, crm, mcp |
| Logo path | `assets/logo.svg` (relative; Cursor docs resolve this to a raw.githubusercontent.com URL) |
| MCP server | `mcp.json` → `https://mysdr.app/api/mcp` (no headers, no env, no `${VAR}`) |
| Skills | `skills/mysdr-onboarding`, `skills/mysdr-first-engine` (valid `SKILL.md` frontmatter) |

### 4.2 Official package checklist

From https://cursor.com/docs/reference/plugins, status on this package:

| Check | Status |
| --- | --- |
| Valid `.cursor-plugin/plugin.json` | Yes |
| `name` unique, lowercase kebab-case | `mysdr` — uniqueness confirmed only at submit |
| `description` explains the purpose | Yes |
| Components have valid files and frontmatter | Yes (two skills) |
| Logo committed and referenced by relative path | Yes, but see the plate gap |
| `README.md` documents usage and configuration | Yes |
| All manifest paths relative and valid | Yes |
| No undeclared `${VAR}` in `mcp.json` | Yes — none |
| Tested locally in Cursor | **Open item** (Louis or a desktop session) |
| Single-plugin repo (no `marketplace.json` needed) | Yes |

### 4.3 Reviewer test instructions (for Cursor review / email)

Install the plugin from the public repo (or, before listing, from the GitHub URL). mySDR shows “needs login”. Click Connect, sign in at https://mysdr.app/en/login with the **reviewer test account** (credentials sent privately when a reviewer asks — never in the repo), click Allow, then ask: “What's my mySDR credit balance?” (`get_usage`). Continue with the prompts in §5. The reviewer org is not created yet; replace the placeholder only in the private message to the reviewer.

---

## 5. Reviewer test account and example prompts

### 5.1 Test account (placeholder — not created)

The Anthropic Software Directory Policy (§3.D) requires a standard testing account with sample data. Cursor reviewers may also ask.

**Do not put credentials in this file, in the repo, or in either portal.**

Placeholder instructions to send later, only when a reviewer emails:

- Organization: a separate test org named **mySDR Review** (not a customer org). **Not created yet.**
- Sign-in: https://mysdr.app/en/login with email + password. No MFA, no magic-link-only, no Google-only login.
- Email / password: **provided in a private message when you request access** (not written here).
- Sample data: fictional leads and companies, one flow, one dashboard.
- LinkedIn is **not** connected, so send tools return their safe “not connected” answer and no real messages go out.
- Starting credits sufficient to run search/enrichment examples (planned: bonus credits on that org).
- Expected first prompts: the list below.

### 5.2 Example prompts (Policy §3.E: at least three)

1. “What's my mySDR credit balance?” — `get_usage` (free, read-only).
2. “What is in my Leads table, and what is due today?” — `list_table`, `get_agenda` (free, read-only).
3. “Find 3 heads of sales at Belgian SaaS companies, and tell me the cost first.” — `preview_cost` then `search_people` (spends credits; the assistant should ask first).
4. Extra: “Show who is on the exclusion list.” — `list_exclusions`.
5. Extra: “Draft, but do not send, a first LinkedIn note to the first lead, and run `check_before_sending`.” — write path without sending.

---

## 6. Open items that need Louis

1. **Submit himself** — nothing is submitted in this preparation. Claude: paid account at https://claude.ai/directory/manage. Cursor: signed-in account at https://cursor.com/marketplace/publish. Publisher is LVDP CommV.
2. **Push / confirm `main` of https://github.com/louisvandeputte-sketch/mysdr-plugin** contains this package (README, LICENSE, manifest, skills, assets, this document). The repo existed but was empty at 16:03 Europe/Brussels on 19 Nov 2026. Cursor cannot be submitted until `main` has the package. (Local commits may already be ready; pushing needs Louis’s GitHub access if the box cannot push.)
3. **Reviewer test org** — create it only after Louis’s yes (separate org, no MFA, bonus credits, fake LinkedIn, no outbound). Then send credentials only to a reviewer who asks, never commit them.
4. **Cursor logotype with a background plate** — approve adding `assets/logo-plate.png` or `.svg` (512×512, opaque plate) and use that URL on the Cursor form. The current circle-on-transparent mark does not meet the form hint.
5. **Contact email** — forms are filled here with `louis.vandeputte@gmail.com`. Confirm, or switch to a monitored domain mailbox. Note: `plugin.json` still has `louis@mysdr.app`; `support@mysdr.app` is the public support address.
6. **Organization handle `mysdr`** — confirm it is still available on Cursor at submit time.
7. **Cursor Owner account** — which Cursor login should own the listing (the Owner field cannot be edited on the form).
8. **Test sign-off** — run every tool as a custom connector in Claude (and locally in Cursor) before ticking Test & launch / submitting Cursor. Still outstanding.
9. **Claude categories** — confirm Sales & marketing + Productivity, and whether to add Data analytics as a third.
10. **Claude slug `mysdr`** — confirm; it is permanent after publish.
11. **Optional Claude plugin bundle** — decide later whether to also submit the GitHub repo as a plugin, from the same Claude organization, and pair it with the connector.
12. **README support URL** — README still lists only `support@mysdr.app`. Optional follow-up: add https://mysdr.app/en/support (the bare `/support` path is 404).

---

## 7. Requirements mySDR does not fully meet yet

| Requirement | Source | Status on 19 Nov 2026 |
| --- | --- | --- |
| Public GitHub repo containing the plugin package on `main` | Cursor docs + form | Repo URL exists and is public, but it was **empty** at creation (no commits, no README, no LICENSE). The package lives locally until it is pushed. |
| Cursor logotype: 1:1 SVG or PNG **with background plate** | Cursor publish form hint | **Not met** by `assets/logo.svg` / `assets/logo.png` (transparent corners, no plate). |
| Standard testing account with sample data | Anthropic Software Directory Policy §3.D; also useful for Cursor review | **Not created yet.** |
| “I have tested every tool” confirmation | Claude portal, Test & launch; Cursor checklist “tested locally” | **Not signed off.** |
| Response size / frugality measured in production | Anthropic policy §5.B (frugal token use) | Read tools paginate; sizes were not re-measured in this preparation. Not a known blocker, but not proven for every tool. |
| `https://mysdr.app/support` | Convenience | **404.** Use https://mysdr.app/en/support (200). |

Items that **do** meet the published requirements (re-checked 19 Nov 2026):

- Remote HTTPS + Streamable HTTP MCP at `https://mysdr.app/api/mcp`.
- OAuth 2.0/2.1 with DCR, CIMD, PKCE S256, RFC 8707 resource, public clients, refresh tokens.
- CORS on the MCP endpoint (`Access-Control-Allow-Origin: *`, including preflight).
- Every tool has `title` + `readOnlyHint` or `destructiveHint`; write/spend tools use `destructiveHint: true`; names ≤ 64 characters; no catch-all read+write tool.
- Public docs, privacy policy, terms, and support contact (email + `/en/support`).
- Privacy policy covers collection, use, third-party sharing, retention, and contact.
- MIT license (permissive), package ships free, no secrets in client config.
- MCP host domain matches the product.

---

## 8. What this file is not

- Not a submission, and not permission to submit.
- Not a place for passwords, API keys, OAuth client secrets, or reviewer credentials.
- Not a ChatGPT / OpenAI directory package (parked).
