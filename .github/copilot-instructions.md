# 🤖 GitHub Copilot Instructions — Clear Stack (AI-Powered Unified Notification Hub)

## 👤 About Me (The Developer)

I am a **Computer Science (AI) student** learning full-stack development while building this project.
I want to understand **every line of code** — not just have it written for me.

**My learning goals:**

- Understand backend architecture (APIs, databases, queues, auth)
- Understand frontend structure (components, state, routing, UI)
- Learn how AI/NLP integrates into a real product
- Build this as a **startup-ready** product, not just a college project

### How Copilot Should Help Me Learn

- **Always explain WHY** before writing code — what pattern is being used and why it's the right choice
- **Add comments** in every file explaining what each section does
- When I ask to "add a feature", first explain the approach, then write the code
- If there's a simpler vs. better-practice way to do something, **show me both** briefly
- Point out when I'm making a mistake and explain the correct way
- Suggest **what to search/read** when I'm touching a new concept (e.g., "Read about JWT refresh tokens before continuing")
- Use **beginner-friendly variable names** and avoid unexplained abbreviations

---

## 🚀 Project Overview

**Project Name:** Clear Stack
**Tagline:** _Your notifications, intelligently unified._

Clear stack is an AI-powered notification aggregation platform that:

- Pulls notifications from **Gmail, WhatsApp, LinkedIn, Google Calendar**
- Uses **NLP** to summarize, prioritize, and group related notifications
- Presents everything in a **clean unified dashboard**
- Learns from **user behavior** to improve prioritization over time
- Sends **smart daily digests** to reduce information overload

**This is being built as a startup product** — code must be clean, scalable, and production-ready from day one.

---

## 🛠️ Tech Stack (Chosen for Startup Scalability)

### Frontend

| Tool                       | Version          | Why                                                                  |
| -------------------------- | ---------------- | -------------------------------------------------------------------- |
| **Next.js**                | 14+ (App Router) | Full-stack React framework; great SEO, server components, API routes |
| **TypeScript**             | 5+               | Catches bugs early; essential for team/startup work                  |
| **Tailwind CSS**           | 3+               | Rapid styling without leaving HTML                                   |
| **shadcn/ui**              | latest           | High-quality accessible components built on Radix UI                 |
| **Zustand**                | latest           | Simple, scalable client state management                             |
| **React Query (TanStack)** | v5               | Server state, caching, background refetching                         |
| **Socket.io Client**       | latest           | Real-time notification updates in the dashboard                      |

### Backend (Python — AI Services)

| Tool                          | Version | Why                                                             |
| ----------------------------- | ------- | --------------------------------------------------------------- |
| **FastAPI**                   | latest  | Async Python API; perfect for AI/NLP workloads                  |
| **Pydantic v2**               | latest  | Data validation and settings management                         |
| **Celery + Redis**            | latest  | Background job processing (fetching, summarizing notifications) |
| **LangChain**                 | latest  | Orchestrating LLM calls for summarization & prioritization      |
| **OpenAI API (GPT-4o)**       | latest  | NLP: summarization, urgency detection, context linking          |
| **Hugging Face Transformers** | latest  | For offline/cheaper NLP alternatives                            |

### Database & Storage

| Tool                          | Why                                                     |
| ----------------------------- | ------------------------------------------------------- |
| **PostgreSQL (via Supabase)** | Primary database; handles users, notifications, digests |
| **Redis (via Upstash)**       | Caching, job queues, real-time pub/sub                  |
| **Prisma ORM**                | Type-safe DB queries from Next.js backend               |

### Auth & Integrations

| Tool                      | Why                                                     |
| ------------------------- | ------------------------------------------------------- |
| **Clerk**                 | Auth with OAuth (Google, GitHub); handles JWT, sessions |
| **Gmail API**             | Fetch email notifications                               |
| **Google Calendar API**   | Fetch calendar events                                   |
| **WhatsApp Business API** | Fetch WhatsApp messages                                 |
| **LinkedIn API**          | Fetch LinkedIn notifications                            |

### Infrastructure & DevOps

| Tool               | Why                                                        |
| ------------------ | ---------------------------------------------------------- |
| **Turborepo**      | Monorepo management for frontend + backend packages        |
| **Vercel**         | Deploy Next.js frontend (free tier → scales automatically) |
| **Railway**        | Deploy FastAPI backend + Celery workers                    |
| **Docker**         | Containerize FastAPI service for consistency               |
| **GitHub Actions** | CI/CD pipeline — auto test and deploy on push              |

---

## 📁 Project Structure

```
ClearStack/
├── apps/
│   ├── web/                        # Next.js frontend (App Router)
│   │   ├── app/
│   │   │   ├── (auth)/             # Login, signup pages
│   │   │   ├── (dashboard)/        # Main app after login
│   │   │   │   ├── page.tsx        # Dashboard home
│   │   │   │   ├── digest/         # Daily digest view
│   │   │   │   └── settings/       # User settings & integrations
│   │   │   ├── api/                # Next.js API routes (thin layer)
│   │   │   │   ├── notifications/
│   │   │   │   └── webhooks/
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── ui/                 # shadcn/ui components
│   │   │   ├── notifications/      # NotificationCard, PriorityBadge, etc.
│   │   │   └── dashboard/          # Sidebar, Header, DigestPanel
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── lib/                    # Utility functions, API clients
│   │   ├── store/                  # Zustand state stores
│   │   └── types/                  # TypeScript type definitions
│   │
│   └── ai-service/                 # FastAPI Python backend (AI/NLP)
│       ├── main.py                 # FastAPI app entry point
│       ├── routers/
│       │   ├── notifications.py    # Notification processing endpoints
│       │   ├── digest.py           # Daily digest generation
│       │   └── integrations.py     # Gmail, Calendar, WhatsApp connectors
│       ├── services/
│       │   ├── summarizer.py       # NLP summarization logic
│       │   ├── prioritizer.py      # Urgency & priority scoring
│       │   ├── linker.py           # Context-aware notification linking
│       │   └── fetchers/           # Per-platform notification fetchers
│       ├── models/                 # Pydantic data models
│       ├── workers/                # Celery background tasks
│       └── core/                   # Config, database connection, auth
│
├── packages/
│   ├── types/                      # Shared TypeScript types (frontend ↔ backend)
│   └── config/                     # Shared ESLint, TS config
│
├── docker-compose.yml              # Local dev: FastAPI + Redis + Postgres
├── turbo.json                      # Turborepo config
└── .github/
    └── workflows/                  # GitHub Actions CI/CD
```

---

## 🧠 Core Feature Architecture

### 1. Notification Pipeline (Most Important — Learn This First)

```
Platform APIs → Fetcher (Celery task) → Raw Notification stored in DB
→ NLP Pipeline (FastAPI):
    ├── Summarizer: Condense long notifications
    ├── Prioritizer: Score urgency (0-100) using LLM
    └── Linker: Find related notifications (e.g., email + calendar event)
→ Processed Notification → Real-time push to frontend (Socket.io)
→ Dashboard renders updated notification list
```

### 2. Priority Scoring System

- **High (80-100):** Deadlines, meeting now, financial alerts
- **Medium (40-79):** Replies, updates requiring action
- **Low (0-39):** Newsletter, social likes, FYI notifications

### 3. Daily Digest

- Celery beat scheduler triggers digest generation at 8 AM
- LLM groups and summarizes all notifications from last 24h
- Sent via email + shown in dashboard digest panel

---

## 📐 Code Standards

### TypeScript / Next.js

- Use `async/await` — never raw `.then()` chains
- Always define prop types with TypeScript interfaces (never `any`)
- Use **Server Components** by default; add `"use client"` only when needed (interactivity, hooks)
- API routes return consistent shape: `{ data, error, message }`
- Always handle loading and error states in UI

### Python / FastAPI

- Use **async def** for all route handlers
- Validate all inputs with Pydantic models — never trust raw request data
- Use dependency injection (`Depends()`) for auth, DB sessions
- Log every significant action with Python `logging` (not `print`)
- Write docstrings for every function explaining what it does

### General

- **No magic numbers** — use named constants
- **No hardcoded secrets** — everything in `.env` files
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Every new feature needs a corresponding type definition before code is written

---

## 🔐 Environment Variables

```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# .env (FastAPI)
OPENAI_API_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GMAIL_API_KEY=
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
CELERY_BROKER_URL=redis://...
```

---

## 🧪 Testing Strategy

- **Unit tests** for all NLP/AI service functions (pytest)
- **Component tests** for React components (Vitest + Testing Library)
- **API integration tests** for FastAPI routes (pytest + httpx)
- Test files live alongside source: `summarizer.py` → `summarizer.test.py`

---

## 🚫 What NOT To Do

- Do **not** put business logic inside React components — logic goes in hooks or server actions
- Do **not** call the OpenAI API directly from the frontend — always go through FastAPI
- Do **not** store access tokens in localStorage — use httpOnly cookies (handled by Clerk)
- Do **not** block the FastAPI event loop with synchronous code — use `asyncio` or `run_in_executor`
- Do **not** skip TypeScript types to save time — types are the documentation

---

## 📚 Learning Path (Follow This Order)

1. **Next.js App Router** — understand layouts, server vs client components
2. **Clerk Auth** — OAuth flow, session management, protected routes
3. **Prisma + PostgreSQL** — schema design, migrations, querying
4. **FastAPI basics** — routes, Pydantic, dependency injection
5. **Celery + Redis** — background tasks, scheduling
6. **OpenAI API + LangChain** — prompting, chains, summarization
7. **Socket.io** — real-time events, rooms, client-server sync
8. **Google/Gmail APIs** — OAuth scopes, fetching data
9. **Docker + Railway deployment** — containerizing the AI service
10. **GitHub Actions** — writing CI/CD pipelines

---

## 💡 Copilot Behavior Reminders

- When suggesting code, **always add inline comments** explaining each non-obvious line
- When I ask "how does X work?", explain the concept **before** showing code
- Remind me to **add the environment variable** when you introduce a new API key
- If you write a function, also suggest **what test cases I should write**
- When introducing a new library, add a one-line comment at the top: `// React Query — handles server state, caching, and background refetching`
- Flag **security concerns** immediately (exposed secrets, unvalidated inputs, open CORS)
