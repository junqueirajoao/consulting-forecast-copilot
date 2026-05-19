"""
Orquestrador
Responsabilidade: coordenar os agentes em sequência para responder à pergunta.
"""
import numpy as np
from app.agents import ingestion_agent, intent_agent, math_agent, response_agent
from app.agents import calendar_agent as cal
from app.config import DEFAULT_YEAR, DEFAULT_MONTH, EXCEL_PATH
from app.models.schemas import QueryRequest, QueryResponse


def _sanitize(obj):
    """Converte tipos numpy/pandas para tipos nativos Python recursivamente."""
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def processar_query(req: QueryRequest) -> QueryResponse:
    # 1. Inger dados de todas as abas
    df          = ingestion_agent.carregar_workbook(EXCEL_PATH)
    consultores = ingestion_agent.listar_consultores(EXCEL_PATH)
    times       = ingestion_agent.listar_times(EXCEL_PATH)

    # 2. Mês de referência
    if req.mes_referencia:
        partes = req.mes_referencia.split("-")
        ano, mes = int(partes[0]), int(partes[1])
    else:
        ano, mes = DEFAULT_YEAR, DEFAULT_MONTH

    # 3. Interpretar intenção
    parsed  = intent_agent.parsear(req.pergunta, consultores, times, ano, mes)
    intent  = parsed["intent"]
    ano     = parsed["ano"]
    mes     = parsed["mes"]
    mes_ref = f"{ano}-{mes:02d}"

    # 4. Cálculo
    resultado = {}

    if intent == "faturamento_total":
        resultado = math_agent.faturamento_total(df, ano, mes)

    elif intent == "time_mais_faturou":
        resultado = math_agent.time_mais_faturou(df, ano, mes)

    elif intent in ("faturamento_time", "comparacao_times"):
        resultado = math_agent.faturamento_por_time(df, ano, mes)

    elif intent == "faturamento_consultor":
        nome = parsed.get("entidade_consultor") or ""
        resultado = math_agent.faturamento_consultor(df, ano, mes, nome)

    elif intent == "faturamento_multiplos_consultores":
        nomes = parsed.get("consultores_multiplos") or []
        resultado = math_agent.faturamento_multiplos_consultores(df, ano, mes, nomes)

    elif intent == "dias_uteis_mes":
        resultado = {"dias_uteis_mes": cal.contar_dias_uteis(ano, mes)}

    elif intent == "dias_trabalhados_consultor":
        nome = parsed.get("entidade_consultor") or ""
        r    = math_agent.faturamento_consultor(df, ano, mes, nome)
        resultado = {
            "consultor":        r.get("consultor", nome),
            "dias_trabalhados":  r.get("dias_trabalhados", 0),
        }


    elif intent == "projecao_sem_consultor":
        nomes = (
            parsed.get("consultores_multiplos")
            or parsed.get("entidade_consultor")
            or ""
        )
        resultado = math_agent.projecao_sem_consultor(df, ano, mes, nomes)


    elif intent == "projecao_com_novos":
        novos = parsed.get("novos_consultores", [])
        resultado = math_agent.projecao_com_novos_consultores(df, ano, mes, novos)

    else:
        resultado = {"mensagem": "Intenção não reconhecida. Tente reformular com o nome do consultor, time ou período."}

    # 5. Sanitizar tipos numpy → Python nativo
    resultado = _sanitize(resultado)

    # 6. Gerar texto de resposta
    texto = response_agent.gerar_resposta(intent, resultado, mes_ref)

    # 7. Premissas para auditoria
    entidade_info = parsed.get("consultores_multiplos") or parsed.get("entidade_consultor") or parsed.get("entidade_time")
    
    premissas = _sanitize({
        "intent_detectado": intent,
        "mes_analisado":    mes_ref,
        "entidade":         entidade_info,
        "dias_uteis":       cal.contar_dias_uteis(ano, mes),
    })

    return QueryResponse(
        intent=intent,
        mes_referencia=mes_ref,
        premissas=premissas,
        resultado=resultado,
        resposta_texto=texto,
    )
