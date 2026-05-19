"""
Agente de Ingestão
Responsabilidade: ler TODAS as abas do Excel e consolidar em um único DataFrame.
"""
import pandas as pd
from app.config import EXCEL_PATH

COLUNAS_OBRIGATORIAS = [
    "Consultor", "Time", "Receita Diária", "Receita Mensal Estimada"
]

def carregar_workbook(caminho: str = EXCEL_PATH) -> pd.DataFrame:
    """Lê todas as abas do Excel e retorna um DataFrame consolidado."""
    xls = pd.ExcelFile(caminho)
    abas = xls.sheet_names
    dfs = []

    for aba in abas:
        df = xls.parse(aba)
        df.columns = df.columns.str.strip()
        _validar_colunas(df, aba)
        df["aba_origem"] = aba
        dfs.append(df)

    base = pd.concat(dfs, ignore_index=True)
    base = _normalizar(base)
    return base

def _validar_colunas(df: pd.DataFrame, aba: str):
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Aba '{aba}' está faltando as colunas: {faltando}")

def _normalizar(df: pd.DataFrame) -> pd.DataFrame:
    df["Consultor"] = df["Consultor"].astype(str).str.strip()
    df["Time"]      = df["Time"].astype(str).str.strip()
    df["Receita Diária"]            = pd.to_numeric(df["Receita Diária"], errors="coerce").fillna(0)
    df["Receita Mensal Estimada"]   = pd.to_numeric(df["Receita Mensal Estimada"], errors="coerce").fillna(0)
    df["Data de Entrada"] = pd.to_datetime(df.get("Data de Entrada"), errors="coerce")
    df["Data de Saída"]   = pd.to_datetime(df.get("Data de Saída"),   errors="coerce")
    return df

def listar_abas(caminho: str = EXCEL_PATH):
    return pd.ExcelFile(caminho).sheet_names

def listar_consultores(caminho: str = EXCEL_PATH):
    df = carregar_workbook(caminho)
    return sorted(df["Consultor"].unique().tolist())

def listar_times(caminho: str = EXCEL_PATH):
    df = carregar_workbook(caminho)
    return sorted(df["Time"].unique().tolist())
