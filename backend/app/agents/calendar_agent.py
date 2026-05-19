"""
Agente de Calendário
Responsabilidade: calcular dias úteis do mês e dias efetivamente
trabalhados por cada consultor, considerando feriados brasileiros.
"""
import calendar
from datetime import date

try:
    from anbima_calendar.main import Calendario
    _cal = Calendario()
    USE_ANBIMA = True
except Exception:
    USE_ANBIMA = False

def _is_util(d: date) -> bool:
    if d.weekday() >= 5:
        return False
    if USE_ANBIMA:
        return _cal.is_working_day(d)
    return True

def dias_uteis_do_mes(ano: int, mes: int) -> list:
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return [
        date(ano, mes, d)
        for d in range(1, ultimo_dia + 1)
        if _is_util(date(ano, mes, d))
    ]

def contar_dias_uteis(ano: int, mes: int) -> int:
    return len(dias_uteis_do_mes(ano, mes))

def _to_date(v) -> date:
    """Converte Timestamp, string ou date para datetime.date."""
    if v is None:
        return None
    import pandas as pd
    if pd.isnull(v):
        return None
    if isinstance(v, date) and not hasattr(v, 'date'):
        return v
    try:
        return pd.Timestamp(v).date()
    except Exception:
        return None

def dias_trabalhados(
    ano: int,
    mes: int,
    data_entrada=None,
    data_saida=None
) -> int:
    """
    Conta quantos dias úteis o consultor trabalhou no mês.
    - data_entrada ausente → considera o primeiro dia útil do mês.
    - data_saida ausente   → considera o último dia útil do mês.
    """
    uteis = dias_uteis_do_mes(ano, mes)
    if not uteis:
        return 0

    inicio = uteis[0]
    fim    = uteis[-1]

    dt_e = _to_date(data_entrada)
    if dt_e is not None and dt_e > inicio:
        inicio = dt_e

    dt_s = _to_date(data_saida)
    if dt_s is not None and dt_s < fim:
        fim = dt_s

    return sum(1 for d in uteis if inicio <= d <= fim)
