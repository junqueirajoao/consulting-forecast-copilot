"""
Agente Semântico (Intent Parser)
Responsabilidade: interpretar o prompt em linguagem natural e retornar
um dicionário estruturado com intenção, entidades e mês de referência.
Não usa LLM: regras + expressões regulares + fuzzy matching.
"""
import re
from rapidfuzz import process, fuzz
from app.models.enums import Intent

# ── Palavras-chave por intenção (ordem importa: mais específico primeiro) ─────
_REGRAS = [
    (Intent.TIME_MAIS_FATUROU,         r"(qual|quem).*(time|equipe).*(mais|maior|top)"),
    (Intent.COMPARACAO_TIMES,           r"(compar|ranking|classifica|tabela).*(time|equipe)"),
    (Intent.PROJECAO_COM_NOVOS,         r"(entr|adicion|inclui|novo|nova|contrat)"),
    (Intent.PROJECAO_SEM_CONSULTOR,     r"(sa[ií]da|sai|remov|sem |perda|perd|saindo|sair)"),
    (Intent.DIAS_TRABALHADOS_CONSULTOR, r"(dias? trabalh|dias? [uú]teis?.*(consultor|pessoa))"),
    (Intent.DIAS_UTEIS_MES,             r"(quantos? dias?|dias? [uú]teis?)"),
    (Intent.FATURAMENTO_TIME,           r"(time|equipe)"),
    (Intent.FATURAMENTO_CONSULTOR,      r"(consultor|pessoa|colaborador)"),
    (Intent.FATURAMENTO_TOTAL,          r"(total|projeto|fatur|receit|quanto)"),
]

_MESES_PT = {
    "janeiro":1,"fevereiro":2,"março":3,"abril":4,"maio":5,"junho":6,
    "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12,
}

def detectar_intencao(pergunta: str) -> str:
    texto = pergunta.lower()
    for intencao, padrao in _REGRAS:
        if re.search(padrao, texto):
            return intencao
    return Intent.DESCONHECIDA

def extrair_mes(pergunta: str, ano_default: int, mes_default: int):
    texto = pergunta.lower()
    m = re.search(r"(\d{4})-(\d{2})", texto)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d{2})/(\d{4})", texto)
    if m:
        return int(m.group(2)), int(m.group(1))
    for nome, num in _MESES_PT.items():
        if nome in texto:
            return ano_default, num
    if "próximo" in texto or "proximo" in texto:
        mes = mes_default + 1 if mes_default < 12 else 1
        ano = ano_default if mes_default < 12 else ano_default + 1
        return ano, mes
    return ano_default, mes_default

def extrair_entidade(pergunta: str, lista_conhecida: list) -> str:
    """Fuzzy match contra lista de consultores ou times conhecidos."""
    if not lista_conhecida:
        return None
    resultado = process.extractOne(
        pergunta, lista_conhecida,
        scorer=fuzz.partial_ratio,
        score_cutoff=55
    )
    return resultado[0] if resultado else None

def extrair_multiplas_entidades(pergunta: str, lista_conhecida: list) -> list:
    """
    Extrai múltiplos nomes de consultores da pergunta.
    Detecta conectores: 'e', 'com', 'junto', 'juntos', 'mais'.
    """
    if not lista_conhecida:
        return []
    
    # Procura por padrões de múltiplos nomes: "Ana e Henrique", "Bruno, Carla e Diego"
    conectores = r"\s+(e|com|junto|juntos|mais|,)\s+"
    if not re.search(conectores, pergunta, re.IGNORECASE):
        return []
    
    encontrados = []
    for consultor in lista_conhecida:
        # Busca por nome completo ou primeiro nome
        nome_completo = consultor.lower()
        primeiro_nome = nome_completo.split()[0]
        
        if primeiro_nome in pergunta.lower() or nome_completo in pergunta.lower():
            encontrados.append(consultor)
            continue
        
        # Fuzzy match mais rigoroso para múltiplos
        score = fuzz.partial_ratio(pergunta.lower(), nome_completo)
        if score >= 70:
            encontrados.append(consultor)
    
    return encontrados if len(encontrados) >= 2 else []

def extrair_novos_consultores(pergunta: str) -> list:
    """
    Extrai valores de receita diária citados no prompt.
    Formato: "...receita de 800 e 950..."
    """
    valores = re.findall(r"(?:r\$\s*)?(\d{3,}(?:[,.]\d+)?)", pergunta.lower())
    novos = []
    for i, v in enumerate(valores[:4]):
        try:
            receita = float(v.replace(",", "."))
            novos.append({"nome": f"Novo Consultor {i+1}", "receita_diaria": receita})
        except ValueError:
            pass
    return novos

def parsear(
    pergunta: str,
    consultores: list,
    times: list,
    ano_default: int,
    mes_default: int,
) -> dict:
    intent   = detectar_intencao(pergunta)
    ano, mes = extrair_mes(pergunta, ano_default, mes_default)

    resultado = {
        "intent": intent,
        "ano": ano,
        "mes": mes,
        "entidade_consultor": None,
        "entidade_time": None,
        "consultores_multiplos": [],
        "novos_consultores": [],
    }

    # Detecta múltiplos consultores ANTES de detectar consultor único
    multiplos = extrair_multiplas_entidades(pergunta, consultores)
    if multiplos:
        resultado["consultores_multiplos"] = multiplos
        # Força a intent para múltiplos se detectou mais de um nome
        if intent in (Intent.FATURAMENTO_CONSULTOR, Intent.FATURAMENTO_TOTAL):
            resultado["intent"] = Intent.FATURAMENTO_MULTIPLOS_CONSULTORES
            intent = Intent.FATURAMENTO_MULTIPLOS_CONSULTORES

    # Para consultor único
    if intent in (
        Intent.FATURAMENTO_CONSULTOR,
        Intent.PROJECAO_SEM_CONSULTOR,
        Intent.DIAS_TRABALHADOS_CONSULTOR,
    ) and not multiplos:
        resultado["entidade_consultor"] = extrair_entidade(pergunta, consultores)

    if intent in (Intent.FATURAMENTO_TIME, Intent.COMPARACAO_TIMES, Intent.TIME_MAIS_FATUROU):
        resultado["entidade_time"] = extrair_entidade(pergunta, times)

    if intent == Intent.PROJECAO_COM_NOVOS:
        resultado["novos_consultores"] = extrair_novos_consultores(pergunta)

    return resultado
