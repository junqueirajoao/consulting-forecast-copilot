# Consulting Forecast Copilot

Sistema multiagente de análise de faturamento para consultorias. Permite fazer perguntas em linguagem natural sobre receita, consultores e times a partir de uma planilha Excel — e também visualizar os dados diretamente na interface.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Excel](#estrutura-do-excel)
- [Endpoints da API](#endpoints-da-api)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos de Perguntas](#exemplos-de-perguntas)

---

## Visão Geral

O **Consulting Forecast Copilot** é uma aplicação web que combina:

- **Chat com IA**: faça perguntas em português sobre faturamento, times e consultores
- **Visualização de dados**: explore a tabela do Excel diretamente na interface, com filtros por mês e busca
- **Análise multiagente**: uma cadeia de agentes especialistas interpreta sua pergunta, calcula o resultado e gera uma resposta clara

**Exemplo de uso:**
> *"Qual é o faturamento total do mês de abril?"*
> → *"O faturamento total do projeto em 2026-04 foi de R$ 135.360,00, com 8 consultores ativos em 22 dias úteis."*

---

## Arquitetura

A aplicação é dividida em duas partes: frontend (React) e backend (FastAPI).

```
┌─────────────────────────────────────┐
│           Frontend (React)          │
│                                     │
│  ┌──────────┐    ┌───────────────┐  │
│  │ Aba Chat │    │  Aba Dados    │  │
│  │          │    │  (tabela do   │  │
│  │ InputBar │    │   Excel)      │  │
│  └──────────┘    └───────────────┘  │
└──────────────────────┤ HTTP (REST)├──────
┌─────────────────────────────────────┐
│           Backend (FastAPI)         │
│                                     │
│  ┌────────────────────────────────┐ │
│  │          Orquestrador          │ │
│  └─┬─────┬─────┬─────┬─────┬─────┘ │
│    │     │     │     │     │      │
│  Ing.  Int.  Math  Cal. Resp.       │
│  Agent Agent Agent Agent Agent      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │      Excel (.xlsx)          │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Os 5 Agentes/Módulos do Backend

| Agente/Módulo | Responsabilidade |
|---|---|
| **Ingestion Agent** | Lê todas as abas do Excel e consolida em um único DataFrame |
| **Intent Agent** | Interpreta a pergunta do usuário e identifica a intenção (faturamento total, por consultor, projeção, etc.) |
| **Math Agent** | Executa os cálculos de receita, faturamento, projeções e apoio aos dias trabalhados |
| **Response Agent** | Formata o resultado em linguagem natural em português |
| **Calendar Agent** | Calcula dias úteis com base no calendário brasileiro/ANBIMA e apoia perguntas sobre mês útil e dias trabalhados |

---

## Pré-requisitos

- **Python** 3.10 ou superior
- **Node.js** 18 ou superior
- **npm** 9 ou superior

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/consulting-forecast-copilot.git
cd consulting-forecast-copilot
```

### 2. Configure o Backend

```bash
cd backend

# Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

Crie o arquivo `.env` na pasta `backend/`:

```env
EXCEL_PATH=data/ficticio.xlsx
DEFAULT_YEAR=2026
DEFAULT_MONTH=4
```

### 3. Configure o Frontend

```bash
cd ../frontend

# Instale as dependências
npm install
```

---

## Como Usar

### Inicie o Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

O backend estará disponível em: `http://127.0.0.1:8000`
Documentação interativa da API: `http://127.0.0.1:8000/docs`

### Inicie o Frontend

Em outro terminal:

```bash
cd frontend
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

### Importe seu Excel

1. Abra o navegador em `http://localhost:5173`
2. Clique em **Importar Excel** no canto superior direito
3. Selecione seu arquivo `.xlsx`
4. Após o upload, use o **Chat** para fazer perguntas ou clique na aba **Dados** para visualizar a tabela

---

## Estrutura do Excel

O arquivo Excel deve seguir o seguinte formato:

- **Cada aba representa um mês**, nomeada no padrão `YYYY-MM` (ex: `2026-03`, `2026-04`)
- **Colunas obrigatórias** em cada aba:

| Coluna | Tipo | Descrição |
|---|---|---|
| `Consultor` | Texto | Nome completo do consultor |
| `Time` | Texto | Nome do time/squad |
| `Receita Diária` | Número | Valor diário em R$ |
| `Receita Mensal Estimada` | Número | Receita estimada para o mês |

- **Colunas opcionais:**

| Coluna | Tipo | Descrição |
|---|---|---|
| `Data de Entrada` | Data | Início do consultor no projeto |
| `Data de Saída` | Data | Saída do consultor (se aplicável) |

**Exemplo de estrutura:**

| Consultor | Time | Receita Diária | Receita Mensal Estimada | Data de Entrada |
|---|---|---|---|---|
| Ana Costa | Backend | 850 | 18.700 | 01/01/2026 |
| Bruno Lima | Frontend | 780 | 17.160 | 15/02/2026 |

---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Faz upload de um arquivo `.xlsx` |
| `GET` | `/sheets` | Lista as abas disponíveis no Excel |
| `GET` | `/consultores` | Lista todos os consultores |
| `GET` | `/times` | Lista todos os times |
| `GET` | `/dados` | Retorna todos os registros do Excel como JSON |
| `GET` | `/dados?aba=2026-04` | Filtra registros por aba (mês) |
| `POST` | `/query` | Processa uma pergunta em linguagem natural |

### Exemplo de requisição ao `/query`

```json
POST /query
{
  "pergunta": "Qual o faturamento total de abril?",
  "mes_referencia": "2026-04"
}
```

### Exemplo de resposta

```json
{
  "intent": "faturamento_total",
  "mes_referencia": "2026-04",
  "resultado": {
    "total": 135360.0,
    "consultores_ativos": 8,
    "dias_uteis": 22
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

## Estrutura do Projeto

```
consulting-forecast-copilot/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── ingestion_agent.py   # Lê e consolida o Excel
│   │   │   ├── intent_agent.py      # Interpreta a intenção da pergunta
│   │   │   ├── math_agent.py        # Cálculos de faturamento
│   │   │   ├── response_agent.py    # Geração de resposta em texto
│   │   │   └── calendar_agent.py    # Cálculo de dias úteis (ANBIMA)
│   │   ├── models/
│   │   │   ├── schemas.py           # Modelos Pydantic (request/response)
│   │   │   └── enums.py             # Enumerações de intenções
│   │   ├── config.py                # Configurações e variáveis de ambiente
│   │   ├── orchestrator.py          # Coordena os agentes em sequência
│   │   └── main.py                  # Rotas FastAPI
│   ├── data/
│   │   └── uploads/                 # Excel carregado via upload
│   ├── tests/
│   │   └── test_math.py             # Testes unitários
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx       # Janela de conversa
│   │   │   ├── MessageBubble.jsx    # Balão de mensagem individual
│   │   │   ├── InputBar.jsx         # Campo de entrada de texto
│   │   │   ├── UploadBar.jsx        # Botão de importação de Excel
│   │   │   └── DataTable.jsx        # Tabela de visualização de dados
│   │   ├── hooks/
│   │   │   └── useChat.js           # Hook de gerenciamento do chat
│   │   ├── services/
│   │   │   └── api.js               # Funções de chamada à API
│   │   └── App.jsx              # Componente raiz com navegação por abas
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Exemplos de Perguntas

O sistema entende perguntas em linguagem natural em português:

**Faturamento geral:**
- *"Qual é o faturamento total do mês de abril?"*
- *"Quanto o projeto faturou em março?"*

**Por consultor:**
- *"Quanto a Ana Costa faturou em abril?"*
- *"Qual o faturamento do Bruno e do Diego juntos?"*

**Por time:**
- *"Qual time mais faturou em maio?"*
- *"Quanto o time de Backend faturou?"*

**Projeções:**
- *"Se o Diego sair, qual seria o faturamento de maio?"*
- *"Se entrar um consultor com R$ 900/dia, qual a projeção?"*

**Calendário:**
- *"Quantos dias úteis tem abril?"*
- *"Quantos dias o Bruno trabalhou em março?"*

---

## Tecnologias Utilizadas

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) — framework web assíncrono
- [Pandas](https://pandas.pydata.org/) — manipulação de dados
- [anbima_calendar](https://pypi.org/project/anbima-calendar/) — calendário de dias úteis brasileiro
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) — busca fuzzy de nomes de consultores
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI

**Frontend:**
- [React 18](https://react.dev/) — biblioteca de interface
- [Vite](https://vitejs.dev/) — bundler e dev server
- [IBM Plex Sans / Mono](https://fonts.google.com/specimen/IBM+Plex+Sans) — tipografia

---

## Licença

MIT
