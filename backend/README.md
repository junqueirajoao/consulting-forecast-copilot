# Consulting Forecast Copilot

Sistema multiagente em Python para análise de faturamento de consultores a partir de planilhas Excel.

## Pré-requisitos

- Python 3.11+
- pip

## Instalação

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

## Rodar a API

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Documentação interativa: http://127.0.0.1:8000/docs

## Endpoints

| Método | Rota           | Descrição                              |
|--------|---------------|----------------------------------------|
| GET    | /             | Health check                           |
| GET    | /sheets       | Lista abas do Excel                    |
| GET    | /consultores  | Lista consultores                      |
| GET    | /times        | Lista times                            |
| POST   | /query        | Faz uma pergunta em linguagem natural  |

## Exemplo de uso

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Quanto o consultor Bruno faturou em maio?"}'
```

## Rodar testes

```bash
cd backend
pytest tests/ -v
```

## Estrutura

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── orchestrator.py      # Coordena todos os agentes
│   ├── config.py            # Variáveis de ambiente
│   ├── agents/
│   │   ├── ingestion_agent.py   # Lê todas as abas do Excel
│   │   ├── calendar_agent.py    # Dias úteis e dias trabalhados
│   │   ├── intent_agent.py      # Parser de linguagem natural
│   │   ├── math_agent.py        # Cálculos de faturamento
│   │   └── response_agent.py    # Formata a resposta em português
│   └── models/
│       ├── schemas.py       # Pydantic models
│       └── enums.py         # Intenções
├── data/
│   └── ficticio.xlsx        # Planilha de exemplo (3 abas mensais)
├── tests/
│   └── test_math.py
├── .env
└── requirements.txt
```
