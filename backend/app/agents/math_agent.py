"""
Agente Matemático
Regras:
  Receita Real = Receita Diária x Dias Trabalhados
  Faturamento Time = soma Receita Real dos consultores do time
  Faturamento Total = soma Receita Real de todos
  Projeção = soma (Receita Diária x Dias úteis do próximo mês) para ativos
"""
import pandas as pd
from app.agents import calendar_agent as cal

def _filtrar_mes(df: pd.DataFrame, ano: int, mes: int) -> pd.DataFrame:
    aba = f"{ano}-{mes:02d}"
    if "aba_origem" in df.columns and aba in df["aba_origem"].values:
        return df[df["aba_origem"] == aba].copy()
    return df.copy()

def _is_null(v) -> bool:
    try:
        return pd.isnull(v)
    except Exception:
        return v is None

def calcular_receita_por_consultor(df: pd.DataFrame, ano: int, mes: int) -> pd.DataFrame:
    df = _filtrar_mes(df, ano, mes).copy()
    df["Dias_Trabalhados"] = df.apply(
        lambda r: cal.dias_trabalhados(
            ano, mes,
            None if _is_null(r.get("Data de Entrada")) else r.get("Data de Entrada"),
            None if _is_null(r.get("Data de Saída")) else r.get("Data de Saída"),
        ), axis=1
    )
    df["Receita_Real"] = df["Receita Diária"] * df["Dias_Trabalhados"]
    return df

def faturamento_total(df: pd.DataFrame, ano: int, mes: int) -> dict:
    df_cal = calcular_receita_por_consultor(df, ano, mes)
    return {
        "faturamento_total":  round(df_cal["Receita_Real"].sum(), 2),
        "dias_uteis_mes":     cal.contar_dias_uteis(ano, mes),
        "total_consultores":  len(df_cal),
    }

def faturamento_por_time(df: pd.DataFrame, ano: int, mes: int) -> dict:
    df_cal = calcular_receita_por_consultor(df, ano, mes)
    por_time = (
        df_cal.groupby("Time")["Receita_Real"]
        .sum().sort_values(ascending=False).round(2).to_dict()
    )
    return {"faturamento_por_time": por_time}

def time_mais_faturou(df: pd.DataFrame, ano: int, mes: int) -> dict:
    dados = faturamento_por_time(df, ano, mes)["faturamento_por_time"]
    melhor = max(dados, key=dados.get)
    return {"time": melhor, "faturamento": dados[melhor], "ranking": dados}

def faturamento_consultor(df: pd.DataFrame, ano: int, mes: int, nome: str) -> dict:
    if not nome:
        return {"erro": "Nome do consultor não identificado na pergunta."}
    df_cal = calcular_receita_por_consultor(df, ano, mes)
    match  = df_cal[df_cal["Consultor"].str.lower() == nome.lower()]
    if match.empty:
        # tenta busca parcial
        match = df_cal[df_cal["Consultor"].str.lower().str.contains(nome.lower(), na=False)]
    if match.empty:
        return {"erro": f"Consultor '{nome}' não encontrado no mês {ano}-{mes:02d}."}
    row = match.iloc[0]
    return {
        "consultor":        row["Consultor"],
        "time":             row["Time"],
        "receita_diaria":   round(row["Receita Diária"], 2),
        "dias_trabalhados": int(row["Dias_Trabalhados"]),
        "receita_real":     round(row["Receita_Real"], 2),
    }

def faturamento_multiplos_consultores(
    df: pd.DataFrame, ano: int, mes: int, nomes: list
) -> dict:
    """
    Calcula o faturamento somado de múltiplos consultores.
    """
    if not nomes:
        return {"erro": "Nenhum consultor identificado na pergunta."}
    
    df_cal = calcular_receita_por_consultor(df, ano, mes)
    
    detalhes = []
    total = 0.0
    
    for nome in nomes:
        match = df_cal[df_cal["Consultor"].str.lower() == nome.lower()]
        if match.empty:
            match = df_cal[df_cal["Consultor"].str.lower().str.contains(nome.lower(), na=False)]
        
        if not match.empty:
            row = match.iloc[0]
            receita = round(row["Receita_Real"], 2)
            total += receita
            detalhes.append({
                "consultor":        row["Consultor"],
                "time":             row["Time"],
                "receita_diaria":   round(row["Receita Diária"], 2),
                "dias_trabalhados": int(row["Dias_Trabalhados"]),
                "receita_real":     receita,
            })
    
    if not detalhes:
        return {"erro": f"Nenhum dos consultores {nomes} foi encontrado no mês {ano}-{mes:02d}."}
    
    return {
        "consultores":      [d["consultor"] for d in detalhes],
        "total_somado":     round(total, 2),
        "detalhes":         detalhes,
        "dias_uteis_mes":   cal.contar_dias_uteis(ano, mes),
    }

def projecao_sem_consultor(
    df: pd.DataFrame, ano_base: int, mes_base: int, nome
) -> dict:
    # aceita string ou lista
    nomes = nome if isinstance(nome, list) else [nome]
    nomes = [n for n in nomes if n]  # remove vazios

    if not nomes:
        return {"erro": "Nome do consultor a ser removido não identificado."}

    mes_proj = mes_base + 1 if mes_base < 12 else 1
    ano_proj = ano_base if mes_base < 12 else ano_base + 1

    df_base = _filtrar_mes(df, ano_base, mes_base).copy()

    # remove todos os consultores da lista usando isin()
    nomes_lower = [n.lower() for n in nomes]
    df_base = df_base[
        ~df_base["Consultor"].str.lower().isin(nomes_lower)
    ]

    # mantém apenas quem continua ativo
    df_base = df_base[df_base["Data de Saída"].apply(lambda v: _is_null(v))]

    dias = cal.contar_dias_uteis(ano_proj, mes_proj)
    total = round((df_base["Receita Diária"] * dias).sum(), 2)

    return {
        "mes_projetado":         f"{ano_proj}-{mes_proj:02d}",
        "dias_uteis":             dias,
        "consultores_removidos":  nomes,       # ← lista agora
        "faturamento_projetado":  total,
        "consultores_ativos":     len(df_base),
    }


def projecao_com_novos_consultores(
    df: pd.DataFrame, ano_base: int, mes_base: int, novos: list
) -> dict:
    mes_proj = mes_base + 1 if mes_base < 12 else 1
    ano_proj = ano_base if mes_base < 12 else ano_base + 1

    df_base = _filtrar_mes(df, ano_base, mes_base).copy()
    df_base = df_base[df_base["Data de Saída"].apply(lambda v: _is_null(v))]

    dias_mes  = cal.contar_dias_uteis(ano_proj, mes_proj)
    base_proj = round((df_base["Receita Diária"] * dias_mes).sum(), 2)

    novos_proj = []
    for n in novos:
        dt_e   = n.get("data_entrada")
        dias_n = cal.dias_trabalhados(ano_proj, mes_proj, dt_e, None)
        receita = round(n["receita_diaria"] * dias_n, 2)
        novos_proj.append({
            "nome":             n["nome"],
            "receita_diaria":   n["receita_diaria"],
            "dias_trabalhados": dias_n,
            "receita_projetada": receita,
        })

    adicional = sum(x["receita_projetada"] for x in novos_proj)
    return {
        "mes_projetado":               f"{ano_proj}-{mes_proj:02d}",
        "dias_uteis":                   dias_mes,
        "faturamento_base_projetado":   base_proj,
        "faturamento_novos":            round(adicional, 2),
        "faturamento_total_projetado":  round(base_proj + adicional, 2),
        "detalhes_novos":               novos_proj,
    }
