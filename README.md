# 🔍 NexusFind AI
> **Autonomous Multi-Agent Deep Search & Answer Engine**

NexusFind AI ek intelligent answer engine hai jo real-time web exploration aur multi-agent factual synthesis ko combine karta hai. Standard search engines ki tarah sirf blue links dene ki bajaye, NexusFind AI multi-agents ka use karke real-time data fetch karta hai, verify karta hai, aur numbered inline citations (`[1]`, `[2]`) ke saath accurate Markdown answer generate karta hai.

---

## 🌟 Key Features

- **Multi-Agent Architecture:** Custom agents (Search Planner, Web Retriever, Synthesizer) CrewAI ke zariye mil kar kaam karte hain.
- **Fast Inference:** Super-fast execution ke liye **Groq API** (`llama-3.3-70b-versatile`) ka use karta hai.
- **Real-Time Web Search:** Live web search ke liye **DuckDuckGo Search Engine** ka integrate kiya gaya hai.
- **Strict Grounding & Citations:** Har factual claim ke saath verified source URLs aur inline citations include hote hain.
- **Clean Streamlit UI:** Simple, minimalist aur responsive web application.

---

## 🤖 Multi-Agent Workflow

```text
[ User Query ]
       │
       ▼
┌─────────────────────────┐
│  Search Planner Agent   │ ──► Generates 2–3 targeted search queries
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Web Retriever Agent    │ ──► Fetches real-time web snippets & URLs
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Synthesizer & Citer    │ ──► Generates response with inline links [1], [2]
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ NexusFind Streamlit UI  │ ──► Displays formatted answer + source cards
└─────────────────────────┘
