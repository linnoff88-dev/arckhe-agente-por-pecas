"""O VERIFICADOR: confere se o resultado cumpre o pedido.
Com exemplo concreto (esperado) -> conferência exata, feita pelo código: acerta sempre.
Sem exemplo -> um segundo cérebro faz de juiz: ajuda, mas também erra."""
import os
import cerebro

JUIZ = os.environ.get("MODELO_JUIZ", cerebro.MODELO)    # o juiz pode ser outro cérebro, maior


def conferir(pedido, resultado, esperado=None, evidencia=()):
    if esperado:
        ok = esperado.lower() in resultado.lower()
        return ok, f"exato: {'achei' if ok else 'não achei'} \"{esperado}\" no resultado"
    lido = "\n".join(evidencia) or "(nada)"
    juiz = [{"role": "system", "content": "Você é um verificador justo. Não resolva o pedido: só julgue."},
            {"role": "user", "content": f"PEDIDO: {pedido}\nO QUE O AGENTE SABIA (memória) E O QUE AS FERRAMENTAS DEVOLVERAM:\n{lido}\n"
             f"RESULTADO: {resultado}\n\n"
             "O resultado cumpre o pedido? Responda numa linha só, começando por SIM ou NAO, e o motivo."}]
    veredito = cerebro.pensar(juiz, modelo=JUIZ).get("content", "").strip()
    return veredito.upper().startswith("SIM"), f"juiz {JUIZ}: {veredito[:90]}"
