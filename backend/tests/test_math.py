"""
Testes unitários do motor matemático e do agente de calendário.
Rode com: pytest tests/
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from app.agents import calendar_agent as cal
from app.agents import math_agent

# ── Fixture de DataFrame simples ──────────────────────────────────────────────
def _df_teste():
    return pd.DataFrame([
        {
            "Consultor": "Ana",
            "Time": "Alpha",
            "Data de Entrada": None,
            "Data de Saída": None,
            "Receita Diária": 700.0,
            "Receita Mensal Estimada": 15400.0,
            "aba_origem": "2026-05",
        },
        {
            "Consultor": "Bruno",
            "Time": "Alpha",
            "Data de Entrada": pd.Timestamp("2026-05-12"),
            "Data de Saída": None,
            "Receita Diária": 900.0,
            "Receita Mensal Estimada": 19800.0,
            "aba_origem": "2026-05",
        },
        {
            "Consultor": "Carla",
            "Time": "Beta",
            "Data de Entrada": None,
            "Data de Saída": pd.Timestamp("2026-05-14"),
            "Receita Diária": 850.0,
            "Receita Mensal Estimada": 18700.0,
            "aba_origem": "2026-05",
        },
    ])

# ── Testes de calendário ──────────────────────────────────────────────────────
def test_dias_uteis_maio_2026():
    """Maio 2026 tem 21 dias úteis (sem feriados, com fins de semana excluídos)."""
    dias = cal.contar_dias_uteis(2026, 5)
    assert 18 <= dias <= 23  # margem para feriados regionais

def test_dias_trabalhados_mes_cheio():
    dias = cal.dias_trabalhados(2026, 5, None, None)
    assert dias == cal.contar_dias_uteis(2026, 5)

def test_dias_trabalhados_entrada_meio_mes():
    dias = cal.dias_trabalhados(2026, 5, "2026-05-12", None)
    total = cal.contar_dias_uteis(2026, 5)
    assert dias < total

def test_dias_trabalhados_saida_meio_mes():
    dias = cal.dias_trabalhados(2026, 5, None, "2026-05-14")
    total = cal.contar_dias_uteis(2026, 5)
    assert dias < total

# ── Testes de faturamento ─────────────────────────────────────────────────────
def test_faturamento_total_positivo():
    df = _df_teste()
    result = math_agent.faturamento_total(df, 2026, 5)
    assert result["faturamento_total"] > 0

def test_faturamento_consultor_existente():
    df = _df_teste()
    result = math_agent.faturamento_consultor(df, 2026, 5, "Ana")
    assert "erro" not in result
    assert result["receita_real"] > 0

def test_faturamento_consultor_inexistente():
    df = _df_teste()
    result = math_agent.faturamento_consultor(df, 2026, 5, "Zuleika")
    assert "erro" in result

def test_receita_real_formula():
    """Receita Real = Receita Diária × Dias Trabalhados."""
    df = _df_teste()
    df_cal = math_agent.calcular_receita_por_consultor(df, 2026, 5)
    for _, row in df_cal.iterrows():
        esperado = round(row["Receita Diária"] * row["Dias_Trabalhados"], 2)
        assert round(row["Receita_Real"], 2) == esperado

def test_projecao_sem_consultor_menor_que_total():
    df = _df_teste()
    total = math_agent.faturamento_total(df, 2026, 5)["faturamento_total"]
    proj  = math_agent.projecao_sem_consultor(df, 2026, 5, "Ana")
    assert proj["faturamento_projetado"] < total
