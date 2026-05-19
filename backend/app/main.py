import os
import shutil
from pathlib import Path
import pandas as pd

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import QueryRequest, QueryResponse
from app.orchestrator import processar_query
from app.agents.ingestion_agent import listar_abas, listar_consultores, listar_times
import app.config as _cfg

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Consulting Forecast Copilot",
    description="Sistema multiagente para análise de faturamento de consultores.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok", "mensagem": "Ambiente preparado com sucesso", "excel_ativo": _cfg.EXCEL_PATH}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    """Recebe um arquivo .xlsx e o define como fonte de dados ativa."""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Apenas arquivos .xlsx ou .xls são aceitos.")

    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Atualiza o path em runtime (sem reiniciar o servidor)
    _cfg.EXCEL_PATH = str(dest)
    os.environ["EXCEL_PATH"] = str(dest)

    abas = listar_abas(str(dest))
    return {
        "mensagem": f"Arquivo '{file.filename}' carregado com sucesso.",
        "excel_ativo": str(dest),
        "abas": abas,
    }

@app.get("/sheets")
def get_sheets():
    """Lista todas as abas disponíveis no arquivo Excel."""
    return {"abas": listar_abas(_cfg.EXCEL_PATH)}

@app.get("/consultores")
def get_consultores():
    """Lista todos os consultores encontrados no Excel."""
    return {"consultores": listar_consultores(_cfg.EXCEL_PATH)}

@app.get("/times")
def get_times():
    """Lista todos os times encontrados no Excel."""
    return {"times": listar_times(_cfg.EXCEL_PATH)}

@app.get("/dados")
def get_dados(aba: str = None):
    """Retorna os dados do Excel como lista de registros JSON."""
    try:
        from app.agents.ingestion_agent import carregar_workbook
        df = carregar_workbook(_cfg.EXCEL_PATH)
        if aba:
            df = df[df["aba_origem"] == aba]
        df = df.copy()
        # Converte datas para string para serialização JSON
        for col in ["Data de Entrada", "Data de Saída"]:
            if col in df.columns:
                df[col] = df[col].dt.strftime("%d/%m/%Y").fillna("")
        # Remove NaN
        df = df.where(pd.notnull(df), None)
        df = df.rename(columns={"aba_origem": "Referência"})
        colunas_sem_ref = [c for c in df.columns if c != "Referência"]
        colunas = ["Referência"] + colunas_sem_ref
        return {
            "colunas": colunas,
            "registros": df[colunas].to_dict(orient="records"),
            "total": len(df),
            "abas": df["Referência"].unique().tolist() if "Referência" in df.columns else [],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    """
    Recebe uma pergunta em linguagem natural e retorna o resultado calculado.

    Exemplos de pergunta:
    - "Quanto o projeto faturou em maio?"
    - "Qual time mais faturou?"
    - "Quanto o consultor Bruno faturou?"
    - "Com a saída do consultor Diego, qual o faturamento do próximo mês?"
    - "Se entrarem 2 consultores com receita de 800 e 950, qual a projeção?"
    """
    try:
        return processar_query(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
