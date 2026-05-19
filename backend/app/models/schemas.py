from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    pergunta: str
    mes_referencia: Optional[str] = None   # formato "YYYY-MM"; usa DEFAULT_MONTH se omitido

class NovoConsultor(BaseModel):
    nome: str
    receita_diaria: float
    data_entrada: Optional[str] = None     # "YYYY-MM-DD"; None = primeiro dia útil do mês

class QueryResponse(BaseModel):
    intent: str
    mes_referencia: str
    premissas: dict
    resultado: dict
    resposta_texto: str
