"""A CAIXA: a rotina que recebe o pedido de qualquer canal e decide quem faz.
Pedido exato -> receita (sem cérebro). Pedido aberto -> cérebro, que pode pedir ferramentas,
e o verificador confere: sucesso, tentar de novo ou cancelar."""
import json, os
import cerebro, ferramentas, receitas, verificador

MAX_RODADAS = 5         # o freio de cada tentativa: no máximo 5 idas ao cérebro
MAX_TENTATIVAS = 3      # o freio do loop: reprovou 3 vezes, cancela


def atender(pedido, canal="terminal", mostrar=print, esperado=None):
    os.makedirs(ferramentas.PASTA, exist_ok=True)
    ferramentas.CANAL = canal
    mostrar(f"[canal {canal}] {pedido}")
    receita = receitas.procurar(pedido)
    if receita:                                        # é exato: a receita faz, o cérebro nem acorda
        mostrar(f"[receita {receita[0]}] sem cérebro")
        return receitas.executar(receita, receita[2])
    mostrar("[caixa] nenhuma receita serve: chamo o cérebro")
    aviso = ""
    for tentativa in range(1, MAX_TENTATIVAS + 1):     # o LOOP: fazer, medir, decidir
        resultado, evidencia = fazer(pedido + aviso, mostrar)
        ok, motivo = verificador.conferir(pedido, resultado, esperado, evidencia)
        mostrar(f"[verificador] {'aprovado' if ok else 'reprovado'} · {motivo}")
        if ok:
            mostrar(f"[resultado] sucesso na tentativa {tentativa}")
            return resultado
        aviso = "\n\n(Sua resposta anterior foi reprovada pelo verificador. Releia o pedido e tente de novo.)"
    mostrar(f"[resultado] cancelado depois de {MAX_TENTATIVAS} tentativas")
    return f"Cancelei: o verificador reprovou {MAX_TENTATIVAS} vezes. Último motivo: {motivo}"


def fazer(pedido, mostrar):
    lembrancas = "\n".join(f"- {m}" for m in ferramentas.memorias()) or "(nada ainda)"
    mostrar(f"[memória] {len(ferramentas.memorias())} fato(s) · [regras] regras.md")
    mensagens = [{"role": "system", "content": f"{open('regras.md').read()}\nO que você sabe do dono:\n{lembrancas}"},
                 {"role": "user", "content": pedido}]
    evidencia = [f"memória -> {m}" for m in ferramentas.memorias()]   # o que o juiz vai ler para julgar
    for rodada in range(MAX_RODADAS):
        msg = cerebro.pensar(mensagens, ferramentas.CARDAPIO)
        mensagens.append(msg)
        if not msg.get("tool_calls"):
            mostrar(f"[cérebro {cerebro.MODELO}] respondeu ({rodada + 1} rodada(s))")
            return msg.get("content", ""), evidencia
        for chamada in msg["tool_calls"]:              # o cérebro pede, a caixa executa
            nome, args = chamada["function"]["name"], chamada["function"].get("arguments") or {}
            try:
                saida = ferramentas.TODAS[nome](**args)
            except Exception as erro:
                saida = f"erro: {erro}".replace(ferramentas.PASTA + os.sep, "")
            mostrar(f"[ferramenta {nome}] {json.dumps(args, ensure_ascii=False)} -> {' '.join(saida.split())[:70]}")
            mensagens.append({"role": "tool", "content": saida})
            evidencia.append(f"{nome} -> {saida}")
    return "Parei: cheguei ao limite de rodadas.", evidencia
