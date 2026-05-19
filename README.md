# Consulting Forecast Copilot

A multi-agent system for consulting revenue analysis. Ask questions in natural language about billing, consultants, and teams — directly from an Excel spreadsheet — and visualize the data in a clean web interface.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Excel Structure](#excel-structure)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Supported Intents](#supported-intents)
- [Query Examples](#query-examples)
- [Tech Stack](#tech-stack)

---

## Overview

**Consulting Forecast Copilot** is a full-stack web application combining:

- **AI Chat**: ask questions in Portuguese about revenue, teams, and consultants
- **Data Viewer**: explore the Excel spreadsheet directly in the UI with month filters and search
- **Multi-agent pipeline**: a chain of specialized agents interprets your question, performs calculations, and returns a clear natural-language answer

**Example:**
> *"What is the total revenue for April?"*
> → *"The total project revenue for 2026-04 was R$ 135,360.00, with 8 active consultants across 22 business days."*

---

## Architecture

The application is split into two parts: a React frontend and a FastAPI backend.

```
┌─────────────────────────────────────┐
│           Frontend (React)          │
│                                     │
│  ┌──────────┐    ┌───────────────┐  │
│  │ Chat Tab │    │   Data Tab    │  │
│  │          │    │  (Excel table)│  │
│  │ InputBar │    │               │  │
│  └──────────┘    └───────────────┘  │
└──────────────────────┤ HTTP (REST)├──────
┌─────────────────────────────────────┐
│           Backend (FastAPI)         │
│                                     │
│  ┌────────────────────────────────┐ │
│  │           Orchestrator          │ │
│  └─┬─────┬─────┬─────┬─────┬─────┘ │
│    │     │     │     │     │      │
│  Ing.  Int.  Math  Cal. Resp.       │
│  Agent Agent Agent Agent Agent      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │      Excel (.xlsx)           │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### The 5 Backend Agents

| Agent | Responsibility |
|---|---|
| **Ingestion Agent** | Reads all Excel sheets and consolidates into a single DataFrame |
| **Intent Agent** | Parses the natural language question and identifies the intent using regex + fuzzy matching |
| **Math Agent** | Performs revenue calculations, projections, and days-worked computations |
| **Calendar Agent** | Calculates business days using the Brazilian/ANBIMA calendar |
| **Response Agent** | Formats the numeric result into a clear natural-language answer in Portuguese |

---

## Requirements

- **Python** 3.10+
- **Node.js** 18+
- **npm** 9+

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/consulting-forecast-copilot.git
cd consulting-forecast-copilot
```

### 2. Set up the Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
EXCEL_PATH=data/ficticio.xlsx
DEFAULT_YEAR=2026
DEFAULT_MONTH=4
APP_ENV=dev
```

### 3. Set up the Frontend

```bash
cd ../frontend
npm install
```

---

## Usage

### Start the Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Backend available at: `http://127.0.0.1:8000`  
Interactive API docs: `http://127.0.0.1:8000/docs`

### Start the Frontend

In a separate terminal:

```bash
cd frontend
npm run dev
```

Frontend available at: `http://localhost:5173`

### Import your Excel file

1. Open `http://localhost:5173` in your browser
2. Click **Importar Excel** in the top-right corner
3. Select your `.xlsx` file
4. Use the **Chat** tab to ask questions or switch to **Dados** to browse the table

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Excel Structure

- **Each sheet represents one month**, named in the format `YYYY-MM` (e.g. `2026-03`, `2026-04`)
- **Required columns** in each sheet:

| Column | Type | Description |
|---|---|---|
| `Consultor` | Text | Full name of the consultant |
| `Time` | Text | Team/squad name |
| `Receita Diária` | Number | Daily rate in BRL |
| `Receita Mensal Estimada` | Number | Estimated monthly revenue |

- **Optional columns:**

| Column | Type | Description |
|---|---|---|
| `Data de Entrada` | Date | Consultant start date on the project |
| `Data de Saída` | Date | Consultant end date (if applicable) |

**Example:**

| Consultor | Time | Receita Diária | Receita Mensal Estimada | Data de Entrada |
|---|---|---|---|---|
| Ana Costa | Backend | 850 | 18,700 | 01/01/2026 |
| Bruno Lima | Frontend | 780 | 17,160 | 15/02/2026 |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload a `.xlsx` file |
| `GET` | `/sheets` | List available sheets |
| `GET` | `/consultores` | List all consultants |
| `GET` | `/times` | List all teams |
| `GET` | `/dados` | Return all records as JSON |
| `GET` | `/dados?aba=2026-04` | Filter records by sheet (month) |
| `POST` | `/query` | Process a natural language question |

### Request example

```json
POST /query
{
  "pergunta": "What is the total revenue for April?",
  "mes_referencia": "2026-04"
}
```

### Response example

```json
{
  "intent": "faturamento_total",
  "mes_referencia": "2026-04",
  "resultado": {
    "faturamento_total": 135360.0,
    "total_consultores": 8,
    "dias_uteis_mes": 22
  },
  "resposta_texto": "O faturamento total do projeto em 2026-04 foi de R$ 135.360,00, com 8 consultores ativos em 22 dias úteis.",
  "premissas": {
    "intent_detectado": "faturamento_total",
    "mes_analisado": "2026-04",
    "dias_uteis": 22
  }
}
```

---

## Project Structure

```
consulting-forecast-copilot/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── ingestion_agent.py   # Reads and consolidates the Excel
│   │   │   ├── intent_agent.py      # Parses natural language intent
│   │   │   ├── math_agent.py        # Revenue and projection calculations
│   │   │   ├── calendar_agent.py    # Brazilian business day calendar (ANBIMA)
│   │   │   └── response_agent.py    # Natural language response generation
│   │   ├── models/
│   │   │   ├── schemas.py           # Pydantic request/response models
│   │   │   └── enums.py             # Intent enum definitions
│   │   ├── config.py                # Environment variables
│   │   ├── orchestrator.py          # Coordinates the agent pipeline
│   │   └── main.py                  # FastAPI routes
│   ├── data/
│   │   └── uploads/                 # Excel files uploaded at runtime
│   ├── tests/
│   │   └── test_math.py             # Unit tests
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx       # Conversation window
│   │   │   ├── MessageBubble.jsx    # Individual message bubble
│   │   │   ├── InputBar.jsx         # Text input field
│   │   │   ├── UploadBar.jsx        # Excel import button
│   │   │   └── DataTable.jsx        # Data visualization table
│   │   ├── hooks/
│   │   │   └── useChat.js           # Chat state management hook
│   │   ├── services/
│   │   │   └── api.js               # API call functions
│   │   └── App.jsx              # Root component with tab navigation
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── README-PT.md             # Portuguese version
```

---

## Supported Intents

The Intent Agent recognizes the following query types:

| Intent | Description | Example |
|---|---|---|
| `faturamento_total` | Total project revenue for a month | *"Total revenue for April"* |
| `faturamento_consultor` | Revenue for a specific consultant | *"How much did Ana earn in March?"* |
| `faturamento_multiplos_consultores` | Combined revenue for multiple consultants | *"Bruno and Diego's revenue in April"* |
| `faturamento_time` | Revenue breakdown by team | *"How much did the Backend team earn?"* |
| `time_mais_faturou` | Top-earning team | *"Which team earned the most?"* |
| `comparacao_times` | Ranking/comparison of all teams | *"Team revenue ranking for May"* |
| `dias_uteis_mes` | Number of business days in a month | *"How many business days in April?"* |
| `dias_trabalhados_consultor` | Business days worked by a consultant | *"How many days did Bruno work?"* |
| `projecao_sem_consultor` | Revenue projection after a consultant leaves | *"If Diego leaves, what is May's revenue?"* |
| `projecao_com_novos` | Revenue projection with new consultants added | *"If 2 consultants join at R$800/day, what's the forecast?"* |

---

## Query Examples

**General revenue:**
- *"What is the total revenue for April?"*
- *"How much did the project earn in March?"*

**By consultant:**
- *"How much did Ana Costa earn in April?"*
- *"Bruno and Diego's combined revenue"*

**By team:**
- *"Which team earned the most in May?"*
- *"Backend team revenue for April"*

**Projections:**
- *"If Diego leaves, what is May's projected revenue?"*
- *"If a consultant joins at R$900/day, what is the forecast?"*

**Calendar:**
- *"How many business days does April have?"*
- *"How many days did Bruno work in March?"*

---

## Tech Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) — async REST framework
- [Pandas](https://pandas.pydata.org/) — data manipulation
- [anbima_calendar](https://pypi.org/project/anbima-calendar/) — Brazilian business day calendar
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) — fuzzy name matching
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

**Frontend:**
- [React 18](https://react.dev/) — UI library
- [Vite](https://vitejs.dev/) — build tool and dev server
- [IBM Plex Sans / Mono](https://fonts.google.com/specimen/IBM+Plex+Sans) — typography

---

## License

MIT
