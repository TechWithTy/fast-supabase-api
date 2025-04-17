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
- POST `/leads/enrich` — Run MLS + OSINT enrichments (future, optional)
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
- POST `/vapi/calls/end-webhook` — Handle call result (summary, outcome)
- POST `/vapi/calls/status-webhook` — Monitor live call state (ringing, voicemail, error)
- GET `/vapi/calls` — List recent calls (filter by status, lead, assistant)
- GET `/vapi/calls/{call_id}` — Get call details and transcript

---

### 🔄 GHL Sync

- POST `/ghl/create-subaccount` — Create subaccount from snapshot
- POST `/ghl/upload-contact` — Send lead/contact to subaccount
- POST `/ghl/apply-tag` — Add “to-call” tag
- POST `/ghl/webhook/contact-tagged` — Webhook: contact tagged (triggers call workflow)
- POST `/ghl/schedule-appointment` — Schedule callback/follow-up

---

### 📊 OSINT & MLS (Planned/Future)

- POST `/osint/email` — Run email intelligence (future)
- POST `/osint/phone` — Run phone intelligence (future)
- POST `/mls/property-info` — Lookup property by address (future)

  - Social login(Facebook & LinkedIn)
    - Password reset
      - MCP access to all key endpoint flows
        - MLS data integration
          - Email + phone number OSINT projects

Below is the ** revised plan ** in Markdown with a clear structure for implementation and integration points.

---

    ````markdown

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

## ✅ MVP Features

### 1. 🧾 Lead Intake & Upload

    - User defines target ZIPs or uploads CSV
        - Validate contacts(Zod)
            - Enrich with:

- ** Email OSINT **
- ** Phone OSINT **
- ** MLS Property Info **
  - Store to Supabase + Push to GHL subaccount

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

`````
            ````
`````
