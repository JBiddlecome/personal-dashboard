# personal-dashboard
## README.md (learning roadmap)
```md
# Personal Dashboard – Learning Roadmap


This project is designed in **phases** so you can learn APIs step by step.


## Phase 0: Demo Data (1 hour)
- ✅ Run the app locally and on Render using the demo provider.
- ✅ Confirm `/api/summary` returns JSON and the UI updates.


## Phase 1: Zapier Bridge (no OAuth yet)
Goal: Practice **webhooks and JSON** without OAuth hurdles.


### Option A: Zapier pulls → pushes counts to your app
- Create a Zap: Gmail (New Email Matching Search) → Code by Zapier (count unread) → **Webhook POST** to a new endpoint in your app, e.g. `/api/ingest`.
- Store the latest counts in memory/file/Redis and return them from `/api/summary`.


### Option B: Zapier Storage
- Use Zapier’s built-in Storage to keep `{ gmail_unread, outlook_unread, tasks_today, events_today }`.
- Modify `providers/demo.py` to **GET** from your Storage URL.


**What you learn:** Webhooks, JSON payloads, basic authentication (e.g., a shared secret header), rate limits.


## Phase 2: Google APIs (Gmail + Calendar)
- Create a Google Cloud Project, enable **Gmail API** and **Calendar API**.
- OAuth consent screen (External), add test users (your email).
- Create OAuth Client (Web App). Set redirect URI to `https://<your-render-domain>/oauth/google/callback`.
- Implement: token exchange + refresh, store tokens (SQLite/Redis/Render Disk).
- Use Gmail API to count unread (threads.list with `q="is:unread in:inbox"`) and Calendar API to list today’s events.


**What you learn:** OAuth 2.0, access/refresh tokens, Google API client, time windows (RFC3339), pagination.


## Phase 3: Microsoft Graph (Outlook + Calendar + To Do)
- App Registration in Entra ID → get Client ID/Secret.
- Redirect URI: `https://<your-render-domain>/oauth/ms/callback`.
- Scopes: `Mail.Read`, `Calendars.Read`, `Tasks.Read` (if using To Do).
- Implement unread count: `/me/mailFolders/Inbox/messages?$filter=isRead eq false&$count=true`.
- Implement events: `/me/calendarView` with start/end for today.


**What you learn:** Graph REST, OData filters, paging, delta queries.


## Phase 4: Tasks Integration
Choices:
- **Google Tasks** (simple) OR **MS To Do** (Graph) OR a CSV/Google Sheet you control.
- Normalize to `List[str]` for the UI.


## Phase 5: Security & Polish
- Add an **Auth token** for `/api/summary` if you’ll expose it publicly.
- Add caching (e.g., cache unread counts for 60s).
- Add error handling with graceful fallbacks.
- Add a small **settings page** to switch providers without redeploy (env-driven + toggle stored server-side).


---


## FAQ
**Why start with demo data?**
So you can deploy something today, then incrementally replace demo providers.


**Do I need databases?**
Not for demo. For OAuth tokens, use SQLite or a small key-value (e.g., Redis). Render supports both.


**Mobile friendly?**
The CSS is responsive; it works on phones.
