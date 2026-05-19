from enum import Enum

class Intent(str, Enum):
    FATURAMENTO_TOTAL              = "faturamento_total"
    TIME_MAIS_FATUROU              = "time_mais_faturou"
    FATURAMENTO_TIME               = "faturamento_time"
    FATURAMENTO_CONSULTOR          = "faturamento_consultor"
    FATURAMENTO_MULTIPLOS_CONSULTORES = "faturamento_multiplos_consultores"
    DIAS_UTEIS_MES                 = "dias_uteis_mes"
    DIAS_TRABALHADOS_CONSULTOR     = "dias_trabalhados_consultor"
    PROJECAO_SEM_CONSULTOR         = "projecao_sem_consultor"
    PROJECAO_COM_NOVOS             = "projecao_com_novos"
    COMPARACAO_TIMES               = "comparacao_times"
    DESCONHECIDA                   = "desconhecida"
