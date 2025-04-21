## 📡 API Endpoints (MVP Optimized)

### 🔐 Authentication

- POST `/auth/login` — Supabase login
- POST `/auth/social` — OAuth login (Facebook, LinkedIn)
- POST `/auth/reset-password` — Trigger password reset
- POST `/auth/set-password` — Complete reset with token
- GET `/auth/me` — Return authenticated user

---

### 📇 Leads

- POST `/leads/generate` — Generate leads by ZIP
- POST `/leads/upload` — Upload CSV
- POST `/leads/enrich` — Run MLS + OSINT enrichments
- GET `/leads` — Filterable list of leads
- PATCH `/leads/{lead_id}` — Update lead (status, tags, etc.)
- POST `/leads/schedule-call` — Queue VAPI call for a lead

---

### 🤖 VAPI Assistant & Call Management

#### **Assistant Management**

- POST `/vapi/assistants` — Create a VAPI assistant
- GET `/vapi/assistants` — List all assistants for user/org
- PATCH `/vapi/assistants/{assistant_id}` — Update assistant (prompt, config)
- DELETE `/vapi/assistants/{assistant_id}` — Remove assistant

#### **Call Handling**

- POST `/vapi/calls` — Start a VAPI call (assistant_id, lead_id, etc.)
- POST `/vapi/calls/end-webhook` — Handle call result (summary, outcome) **[Implemented]**
- POST `/vapi/calls/status-webhook` — Monitor live call state (ringing, voicemail, error) **[Implemented]**
- GET `/vapi/calls` — List recent calls (filter by status, lead, assistant)
- GET `/vapi/calls/{call_id}` — Get call details and transcript

---

### 📣 ElevenLabs Voice Cloning & Vapi Integration

- POST `/elevenlabs/clone-voice` — Clone a new custom voice using ElevenLabs API (uploads audio, returns `voice_id`).
- POST `/vapi/voice/upload-elevenlabs-voice` — Register (sync) the ElevenLabs `voice_id` to Vapi for a specific customer/user.
- Both endpoints now use shared backend logic for DRY, secure, and robust integration.
- The Vapi sync endpoint uses the Vapi SDK to register the voice for the customer (not just a placeholder).

#### Integration Steps (Completed)
1. Clone voice via `/elevenlabs/clone-voice` (returns `voice_id`).
2. Register voice to Vapi via `/vapi/voice/upload-elevenlabs-voice` (requires `customer_id`).
3. Voice is now available for use in Vapi assistants/calls for that customer.

#### Next Steps / Remaining Work
- [ ] Add authentication and authorization to these endpoints (ensure only valid users/customers can register voices).
- [ ] Store voice metadata and mapping (`voice_id`, `customer_id`, label, etc.) in the database for auditing and UI display.
- [ ] Add automated tests for voice cloning and registration flows.
- [ ] Add error handling for edge cases (e.g., duplicate voices, failed syncs, quota limits).
- [ ] Integrate frontend UI for voice management (upload, view, assign to assistant).
- [ ] Update onboarding flows to include voice registration if needed.
- [ ] Document API usage and required payloads for frontend/devs.

---

### 🔄 GHL Sync

- POST `/ghl/create-subaccount` — Create subaccount from snapshot **[Implemented]**
- POST `/ghl/upload-contact` — Send lead/contact to subaccount **[Implemented]**
- POST `/ghl/apply-tag` — Add “to-call” tag **[Implemented]**
- POST `/ghl/schedule-appointment` — Schedule callback/follow-up **[Implemented]**

> **Note:**
> Contact tag trigger logic (e.g., when a contact is tagged with "to-call") will be handled entirely within Go High Level Workflows. The `/ghl/webhook/contact-tagged` endpoint is not required in this backend and has been removed from the API plan. All automations and follow-ups based on tagging should be configured in GHL Workflows directly for simplicity and reliability.

---

### 📊 OSINT & MLS

- POST `/osint/email` — Run email intelligence **[Implemented, uses email2phonenumber]**
- POST `/osint/phone` — Run phone intelligence **[Implemented, uses Phunter]**
- POST `/mls/property-info` — Lookup property by address **[Implemented, uses HomeHarvest]**

---

#### Integration Notes / Updates

- All OSINT and MLS endpoints now use their respective libraries for real data enrichment:
  - `/osint/email` → `email2phonenumber` (calls `start_scrapping`)
  - `/osint/phone` → `Phunter` (calls `phunter_service` async)
  - `/mls/property-info` → `HomeHarvest` (calls `scrape_property`)
- All new routers are wired into the FastAPI app in `api/main.py`.
- Endpoints return structured JSON for easy frontend consumption.
- GHL, VAPI, and OSINT/MLS endpoints are all modular and independently testable.

---

# 🏗 MVP Development Plan – Lead Ignite(v2)

## 🚀 Overview

Lead Ignite automates lead generation, qualification, and contact for real estate professionals using voice AI (VAPI), CRM(GoHighLevel), OSINT tools, MLS data, and orchestrated backend flows(FastAPI + Supabase + MCP).

---

## 🔧 Tech Stack

- ** Frontend **: Next.js(TypeScript), Zustand(state), Zod(validation)
- ** Backend **: FastAPI(Python), Supabase(Postgres, Auth, Edge Functions)
- ** Voice **: VAPI
- ** CRM **: GoHighLevel
- ** AI Layer **: MCP(Model Context Protocol)
- ** External Integrations **: Facebook, LinkedIn, MLS API, OSINT(Email + Phone)

---

## ✅ MVP Features (Key Integration Updates)

### 1. 🧾 Lead Intake & Upload

- User defines target ZIPs or uploads CSV
- Validate contacts(Zod)
- Enrich with:
  - **Email OSINT** (`/osint/email`)
  - **Phone OSINT** (`/osint/phone`)
  - **MLS Lookup** (`/mls/property-info`)
- Queue VAPI calls and sync to GHL as needed

### 2. 🤖 Voice AI (VAPI)

- Full CRUD for assistants and calls
- Webhooks for call status/results now live

### 3. 🔄 GHL Integration

- All major endpoints implemented
- Contact tagging handled in GHL workflows

### 4. 📊 OSINT & MLS

- All enrichment endpoints implemented and integrated with their respective libraries

---

## 🔁 Next Steps

- Continue E2E testing with real data
- Add frontend integration for new endpoints
- Monitor and optimize for performance, error handling, and security

---

### 2. 🔐 Authentication

    - ** Sign Up / Login(Supabase) **

- ** Login with Facebook & LinkedIn **
- ** Forgot Password / Reset Password Flow **
  - Save provider tokens for user context in backend

### 3. 📞 Call Scheduling(VAPI)

    - Schedule only during business hours
        - Triggered by tag in GHL("to-call")
            - AI assistant:

- Detects voicemail
  - Leaves custom recording
    - Gathers qualifying info
      - Post - call:
- Updates GHL tags, pipeline stage
  - Saves call log to DB

### 4. 🏷️ Lead Categorization

    - Leads tagged post - call(interested, follow - up, etc.)
        - Pipeline stage updated
            - Follow - up appointment scheduled in GHL if needed

### 5. 📊 Dashboard

    - View lead stages, call history
        - Filter by tag, pipeline, campaign
            - Call outcomes & next scheduled call batches

🧠 MCP Protocol(Model Context Protocol)

Internal AI Orchestration Layer powered by Anthropic’s MCP and VAPI’s MCP Server
🧩 Role

Acts as the central intelligence layer for AI decision - making, call prompt engineering, lead routing, and enrichment.This module is designed to be model - agnostic and fully extensible.
🔍 Reads From:

    Enriched lead records(phone / email OSINT)

    VAPI logs + transcriptions

    Call summaries(intent + metadata)

    MLS API(property comps, listings)

    Time zone & business hour configs

    User preferences & past interaction logs

📝 Writes To:

    Lead tags(e.g.interested, follow - up, DNC)

    Pipeline stages in GHL

AI - generated prompt fields for VAPI

    Follow - up tasks(schedule calls, notes, appointments)

    Internal logging / audits for traceable AI reasoning

🔐 MCP Access Scope:

    ✅ Read / Write: Leads, Calls, GHL Sync

    ✅ Trigger Workflows: Tag updates, appointment creation

    ✅ Enrichment Layer:

        OSINT Modules: Phone / email risk & persona data

        MLS Integration: Inject property - level insight into call flows

🧠 VAPI Integration

    Compatible with VAPI’s MCP Server SDK

    Uses AssistantContext, FunctionCall, LeadSnapshot to interact with VAPI Assistants

    Supports auto - updating call prompts via vector or function embeddings

🤖 VAPI MCP Integration

    Uses VAPI’s MCP Server SDK

    Accepts leadSnapshot, functionCall, contextLog to dynamically adapt call behavior

    Automatically adjusts voice assistant strategy in response to AI - classified lead traits

🧬 Supabase eMCP Integration(Edge Context)

    Enhances API logic with contextual metadata at the edge

    Injects user identity, project data, and roles directly into FastAPI / Supabase queries

    Use Cases:

        Personalize query outputs per user or subaccount

        Safely expose derived AI recommendations from vector search

        Execute low - latency RLS - filtered data transformations

// Example: Using eMCP context inside Supabase Edge Function
const userContext = getMCPContext(req); // pulls org, lead_id, tags, etc.
if (userContext.tags.includes("interested")) {
forwardToPipeline("FollowUp", lead_id)
}

📚 Stretch Goal: Vector - Based Knowledge Base

    Vector DB(e.g.pgvector or Pinecone) for:

        Lead history embedding

        Company SOPs, scripts, FAQs

        Past VAPI interactions and summaries

    Used by MCP layer for:

        Prompt generation

Context - aware responses

        Internal Q & A for team workflows

## 🗃️ Key Data Models

### Lead

    ```ts

{
id: string
name: string
phone: string
email?: string
address: string
tags: string[]
status: "new" | "contacted" | "qualified" | "callback"
osint: { phone: Record<string, any>, email: Record<string, any> }
mls: Record<string, any>
callLogs: CallLog[]
}

````

### CallLog

    ```ts
{
  id: string
  leadId: string
  timestamp: string
  duration: number
  outcome: string
  notes: string
  audioUrl?: string
}
````

---

## ⏱️ Scheduling Logic

    - Validate against per - user business hours
        - Store window:

```json
{ "start": "09:00", "end": "17:00", "timezone": "America/New_York" }
```

    - If out of bounds → store in retry queue(Redis or Supabase scheduled tasks)

---

## 🔁 Webhooks

    | Source | Event | URL | Purpose |

| ------ | -------------- | ----------------------------- | ----------------------------- |
| GHL | Contact Tagged | `/ghl/webhook/contact-tagged` | Start call flow |
| VAPI | Call Ended | `/vapi/call-end-webhook` | Log result, update tag / status |
| VAPI | Call Status | `/vapi/call-status-webhook` | Retry or voicemail detection |

    ---

## ✅ Launch Checklist

    - [] GHL API Key & Snapshot ID
        - [] VAPI Assistant, Twilio number
            - [] Social logins working(Facebook, LinkedIn)
                - [] Password reset flow implemented
                    - [] Supabase schema set(Leads, Calls, Users)
                        - [] MLS + OSINT APIs integrated and tested
                            - [] Business hour logic applied to all calls
                                - [] Working frontend UI for all flows
                                    - [] MCP layer wired to all core actions
                                        - [] Logging, error handling & retries

---

## 🧪 Optional Post - MVP

    - Live chat funnel using same lead data

- Audio review & transcription UX

  - Real - time coaching feedback on call tags

    - Lead score prediction with weighted inputs

      ```

      ```

---

Would you like:

- Supabase table schemas for Leads, Calls, Users?
- Auth UI (social login + reset password) starter?
- GitHub repo layout suggestion for frontend/backend?

Let me know how you'd like to break down dev sprints or if you want a task list for Notion/Jira setup.
