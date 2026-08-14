# Mukerem Shifa

**Full-stack developer building AI-powered web applications.**
<!-- Optional: add your location and a portfolio link here, e.g. -->
<!-- Addis Ababa, Ethiopia · [portfolio](https://example.com) -->

I build AI features end to end — the retrieval pipeline, the API at the edge, the
Postgres schema underneath it, and the interface on top. Most of my work sits where
LLM features meet ordinary application concerns: multi-tenancy, row-level security,
streaming that degrades gracefully when the transport fails, and vector search that
returns the passage you actually asked for.

I'm early in my career and I learn by shipping complete systems rather than tutorials —
the projects below are deployed, tested, and documented. Open to junior / entry-level
roles in full-stack or AI application engineering.

---

## Selected work

| Project | What it does | Stack |
|---|---|---|
| **[ConverseKit](https://github.com/mukeremshifa/conversekit)** · [live](https://conversekit-widget.pages.dev/) | Multi-tenant AI chat widget that installs with one `<script>` tag. Answers from each client's own documents via embedding + cosine similarity, routes to any of eleven LLM vendors behind a single interface, and captures leads mid-conversation. Tenants are isolated by Postgres RLS, not by application code. | TypeScript · Cloudflare Workers · Cloudflare Pages · Supabase · pgvector · Hono |
| **[SynapseDeck](https://github.com/mukeremshifa/synapse-deck)** · [live](https://synapsedeck.vercel.app/) | Turns your notes into flashcards and drills you on them with a real FSRS spaced-repetition scheduler. Cards stream in as the model writes them and pass through a review gate before entering a deck. Every figure on the progress page is counted from an append-only review log. | React 19 · TypeScript · Vite · Tailwind · TanStack Query · Zod · Supabase Edge Functions · ts-fsrs · Vitest |
| **[RAG QA Bot](https://github.com/mukeremshifa/ibm-capstone-rag-bot)** | Document-based question answering over uploaded PDFs — chunking, embedding, vector retrieval, and grounded generation. Built as the capstone for IBM's AI engineering coursework. | Python · LangChain · Google Gemini · ChromaDB |
| **[Little Lemon API](https://github.com/mukeremshifa/little-lemon-api)** | Restaurant back end covering all 21 acceptance criteria of the Meta back-end capstone: role-based permissions across four user groups, cart and order flows, throttling, and 24 acceptance tests. | Python · Django · Django REST Framework |

---

## Stack

**Languages**

![TypeScript](https://img.shields.io/badge/TypeScript-30363D?style=flat-square&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-30363D?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-30363D?style=flat-square&logo=javascript&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-30363D?style=flat-square&logo=postgresql&logoColor=white)
![Java](https://img.shields.io/badge/Java-30363D?style=flat-square&logo=openjdk&logoColor=white)

**Frontend**

![React](https://img.shields.io/badge/React-30363D?style=flat-square&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-30363D?style=flat-square&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-30363D?style=flat-square&logo=tailwindcss&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack%20Query-30363D?style=flat-square&logo=reactquery&logoColor=white)

**Backend & data**

![Node.js](https://img.shields.io/badge/Node.js-30363D?style=flat-square&logo=nodedotjs&logoColor=white)
![Hono](https://img.shields.io/badge/Hono-30363D?style=flat-square&logo=hono&logoColor=white)
![Django](https://img.shields.io/badge/Django-30363D?style=flat-square&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-30363D?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-30363D?style=flat-square&logo=supabase&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare%20Workers-30363D?style=flat-square&logo=cloudflare&logoColor=white)

**AI**

![LangChain](https://img.shields.io/badge/LangChain-30363D?style=flat-square&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-30363D?style=flat-square&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-30363D?style=flat-square&logo=anthropic&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-30363D?style=flat-square&logo=googlegemini&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-30363D?style=flat-square&logo=postgresql&logoColor=white)

**Testing & tooling**

![Vitest](https://img.shields.io/badge/Vitest-30363D?style=flat-square&logo=vitest&logoColor=white)
![Git](https://img.shields.io/badge/Git-30363D?style=flat-square&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-30363D?style=flat-square&logo=githubactions&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-30363D?style=flat-square&logo=linux&logoColor=white)

---

## What I'm working on

- Extending **ConverseKit** — analytics for bot owners, and a self-serve onboarding flow.
- Post-v1 work on **SynapseDeck** — mobile layouts behind the login, and richer progress reporting.
- Going deeper on retrieval quality: chunking strategies, reranking, and evaluating RAG answers instead of eyeballing them.

---

## Contact

[![Email](https://img.shields.io/badge/Email-30363D?style=flat-square&logo=gmail&logoColor=white)](mailto:mukerem.dev@gmail.com)
<!-- Add your LinkedIn once you have the URL: -->
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-30363D?style=flat-square&logoColor=white)](https://linkedin.com/in/YOUR-HANDLE) -->
