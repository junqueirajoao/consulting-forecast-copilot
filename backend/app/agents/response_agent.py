"""
Agente de Resposta
Responsabilidade: transformar o resultado numérico em texto claro em português,
explicando as premissas usadas.
"""
def formatar_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_resposta(intent: str, resultado: dict, mes_ref: str) -> str:
    r = resultado

    if "erro" in r:
        return f"⚠️ {r['erro']}"

    if intent == "faturamento_total":
        return (
            f"O faturamento total do projeto em {mes_ref} foi de "
            f"{formatar_brl(r['faturamento_total'])}, com "
            f"{r['total_consultores']} consultores ativos em "
            f"{r['dias_uteis_mes']} dias úteis."
        )
    
    if intent == "faturamento_multiplos_consultores":
        nomes = r.get("consultores", [])

        if len(nomes) == 2:
            nomes_txt = f"{nomes[0]} e {nomes[1]}"
        elif len(nomes) > 2:
            nomes_txt = ", ".join(nomes[:-1]) + f" e {nomes[-1]}"
        else:
            nomes_txt = ", ".join(nomes)

        detalhes = []
        for d in r.get("detalhes", []):
            detalhes.append(
                f"{d['consultor']} ({d['time']}) faturou {formatar_brl(d['receita_real'])}, "
                f"em {d['dias_trabalhados']} dias úteis, com diária de {formatar_brl(d['receita_diaria'])}."
            )

        return (
            f"Em {mes_ref}, {nomes_txt} faturaram juntos {formatar_brl(r['total_somado'])}. "
            + " ".join(detalhes)
    )
    
    if intent == "time_mais_faturou":
        return (
            f"O time que mais faturou em {mes_ref} foi o **{r['time']}**, "
            f"com {formatar_brl(r['faturamento'])}."
        )
    
    if intent == "faturamento_time":
        times = r.get("faturamento_por_time", {})
        linhas = [f"  • {t}: {formatar_brl(v)}" for t, v in times.items()]
        return "Faturamento por time em " + mes_ref + ":\n" + "\n".join(linhas)

    if intent == "faturamento_consultor":
        return (
            f"O consultor **{r['consultor']}** ({r['time']}) faturou "
            f"{formatar_brl(r['receita_real'])} em {mes_ref}, "
            f"trabalhando {r['dias_trabalhados']} dias úteis "
            f"(receita diária: {formatar_brl(r['receita_diaria'])})."
        )
    
    if intent == "dias_uteis_mes":
        return f"O mês {mes_ref} tem {r['dias_uteis_mes']} dias úteis."

    if intent == "dias_trabalhados_consultor":
        return (
            f"O consultor **{r['consultor']}** trabalhou "
            f"{r['dias_trabalhados']} dias úteis em {mes_ref}."
        )
    
    if intent == "projecao_sem_consultor":
        saindo = r.get("consultores_removidos", [])

    if len(saindo) == 1:
        quem_sai = saindo[0]
    elif len(saindo) == 2:
        quem_sai = f"{saindo[0]} e {saindo[1]}"
    else:
        quem_sai = ", ".join(saindo[:-1]) + f" e {saindo[-1]}"

    return (
        f"Sem {quem_sai}, o faturamento projetado "
        f"para {r['mes_projetado']} é de {formatar_brl(r['faturamento_projetado'])}, "
        f"considerando {r['dias_uteis']} dias úteis e "
        f"{r['consultores_ativos']} consultores ativos."
    )

    
    if intent == "projecao_com_novos":
        detalhes = "\n".join(
            f"  • {n['nome']}: {formatar_brl(n['receita_projetada'])} "
            f"({n['dias_trabalhados']} dias)"
            for n in r.get("detalhes_novos", [])
        )
        return (
            f"Com os novos consultores, o faturamento projetado para "
            f"{r['mes_projetado']} é de "
            f"{formatar_brl(r['faturamento_total_projetado'])}\n"
            f"  Base atual: {formatar_brl(r['faturamento_base_projetado'])}\n"
            f"  Novos consultores:\n{detalhes}"
        )
    
    if intent == "comparacao_times":
        times = r.get("faturamento_por_time", {})
        linhas = [f"  {i+1}. {t}: {formatar_brl(v)}" for i, (t, v) in enumerate(times.items())]
        return "Ranking de times em " + mes_ref + ":\n" + "\n".join(linhas)

    return "Não consegui interpretar a pergunta. Tente reformular com o nome do consultor, time ou período."
