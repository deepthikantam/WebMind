# 🧠 WebMind : Autonomous Web Agent
> Built for the **Anakin Forge Hackathon 2026** — *"Build AI Agents That Read, Reason, and Act."*

WebMind is an autonomous AI agent that goes beyond passive chatbots. It accepts complex, real-world research or procurement goals, searches and reads live web pages via **Anakin.io**, reasons through tradeoffs and observations using **Google Gemini**, and executes an actionable workflow by compiling verified decision shortlists and battlecards with ground-truth citations.

---

## 🎯 What Makes WebMind an AI Agent?

Unlike a standard chatbot that provides a static, single-turn answer based on stale training data, WebMind executes an **observable, closed-loop agentic workflow**:

$$\text{PLAN} \longrightarrow \text{TOOL} \longrightarrow \text{OBSERVE} \longrightarrow \text{REASON} \longrightarrow \text{ACT} \longrightarrow \text{VERIFY} \longrightarrow \text{RESULT}$$

1. **Active Perception**: Proactively gathers live web evidence via the official **Anakin Search** and **URL Scraper** APIs.
2. **Multi-Step Cognition**: Audits incoming evidence, detects information gaps, and reasons about next actions.
3. **Action Execution**: Produces structured decision matrices, triggers deep page verification, and dispatches external webhook alerts.
4. **Self-Verification**: Automatically audits its synthesized outcome against the user's original constraints before returning the final result.

---

## 🔄 The 7-Stage Agent Workflow

```text
               USER OBJECTIVE
                     ↓
[Stage 1: PLAN]   🧠 Gemini deconstructs goal into queries & evaluation criteria
                     ↓
[Stage 2: TOOL]   🔎 Anakin Search queries live web for authoritative sources
                     ↓
[Stage 3: OBSERVE]📖 Agent parses and digests raw live content into evidence buffer
                     ↓
[Stage 4: REASON] 🧠 Gemini evaluates observations, checks for gaps, decides next tool
                     ↓
[Stage 5: ACT]    ⚡ Anakin Scraper verifies target URL + compiles decision matrix
                     ↓
[Stage 6: VERIFY] ✅ Gemini audits final result against initial constraints
                     ↓
[Stage 7: RESULT] 🎯 Final Executive Dossier (.md) & Structured JSON ready for download
```

---

## 🛠️ Technology Synergy: Anakin + Gemini

| Layer | Component | Official API / SDK | Exact Responsibility |
| :--- | :--- | :--- | :--- |
| **Web Perception & Execution** | **Anakin.io** | `anakin-sdk` (Python) | • `client.search()`: Live web search + content retrieval<br>• `client.scrape()`: Deep markdown extraction for verification<br>• `client.agentic_search()`: Multi-stage research pipeline |
| **Cognitive & Planning Brain** | **Google Gemini** | `google-genai` (Python) | • `plan_research()`: Task deconstruction<br>• `reason_over_observation()`: Gap detection & action selection<br>• `generate_battlecard()`: Structured synthesis<br>• `verify_result()`: Constraint audit |
| **Interface & Presentation** | **Streamlit** | `streamlit` | • Single-page reactive dashboard<br>• Real-time observable trace stepper<br>• One-click Markdown & JSON artifact exports |

---

## 🏆 Featured Hackathon Demo Task

> **“Find relevant AI hackathons, compare their deadline, prize, eligibility and format, verify the best option from the official page, and prepare a submission-ready shortlist.”**

### What the Agent Produces:
* 🏆 **Top Recommendation**: Identifies the primary target (e.g. *Anakin Forge Hackathon 2026*).
* 📊 **Comparative Shortlist Matrix**: Compares options across Theme, Prize & Grants, Deadlines, and Format.
* ✅ **Agent Verification Audit**: 3-point checklist validating constraint match, source grounding, and actionability.
* ⚠️ **Risk & Caution Factors**: Timeline cutoffs, evaluation rubrics, and video limits.
* 🚀 **Actionable Next Steps**: Concrete steps for submission.
* 🔗 **Live Ground-Truth Citations**: Direct links with extracted snippets from live web sources.

---

## 📦 Setup & Run Instructions

### 1. Clone & Install Dependencies
```bash
git clone <your-repo-url>
cd WebMind
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional in `.env` or in UI)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Populate your keys:
```env
ANAKIN_API_KEY=your_anakin_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ACTION_WEBHOOK_URL=https://webhook.site/your-id  # Optional
```
*(Note: You can also paste your keys directly into the Streamlit sidebar during a live demo).*

### 3. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎥 3-Minute Video Demo Script

1. **The Hook (0:00 - 0:30)**:
   * Explain: *"Most hackathon entries are chatbots that guess answers from old data. WebMind is an autonomous agent that reads live web pages via Anakin.io, reasons over observations with Gemini, and executes verified workflows."*
2. **The Dispatch (0:30 - 1:30)**:
   * Select the featured preset: *"🏆 AI Hackathon Scout (Deadlines, prizes, format & shortlist)"*.
   * Click **"Dispatch Autonomous Agent Loop"**.
   * Walk the judges through the observable 7-stage pipeline:
      * 🧠 **PLAN**: Gemini formulated targeted search queries and evaluation criteria.
      * 🔎 **TOOL**: Anakin Search queried live web sources.
      * 📖 **OBSERVE**: Ingested live web results into the observation buffer.
      * 🧠 **REASON**: Gemini evaluated candidates, selected the top choice, and targeted the official URL.
      * ⚡ **ACT**: Agent actively opened official page via Anakin URL Scraper, extracted verified registration gateway, deadlines, and required fields into an Action Execution Card.
      * ✅ **VERIFY**: Self-audit verified official portal access and registration link validity.
3. **The Results (1:30 - 2:30)**:
    * Show the **⚡ Verified Action Execution Card** with Anakin Scraper execution proof and direct registration gateway.
    * Show the **Comparative Shortlist Matrix** table.
    * Highlight the **Verification Audit** (Status: `VERIFIED`, 95%+ confidence).
    * Click one of the live ground-truth citations to prove real web grounding.
4. **The Action Artifacts (2:30 - 3:00)**:
    * Click **"Download Executive Dossier (.md)"**, **"Download Structured Battlecard (.json)"**, and **"Download Action Execution Card (.json)"** to show the finalized, submission-ready deliverables.

---

## 📂 Minimal File Architecture

```
WebMind/
├── .env.example          # Template for credentials
├── .gitignore            # Secret & cache protection
├── requirements.txt      # Pinned Python dependencies
├── app.py                # Streamlit UI & observable agent pipeline
├── config.py             # Environment configuration & credential helpers
├── anakin_service.py     # Official Anakin SDK integration (search, scrape)
├── gemini_service.py     # Gemini reasoning, gap checking & verification
├── agent.py              # 7-stage state machine (PLAN -> TOOL -> OBSERVE -> REASON -> ACT -> VERIFY -> RESULT)
├── test_flow.py          # End-to-end verification test suite
└── README.md             # Complete project documentation & pitch guide
```
