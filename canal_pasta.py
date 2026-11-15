"""CANAL pasta: ninguém conversa. Quem quer algo deixa um arquivo .txt em entrada/;
o robô atende, grava o resultado em feito/ e apaga o pedido.
Uma linha "esperado: ..." no arquivo é o exemplo concreto que o verificador confere.
Uso: python3 canal_pasta.py            (vigia a pasta a cada 2 s; Ctrl+C para parar)
     python3 canal_pasta.py --uma-vez  (atende o que já está lá e sai)"""
import os, sys, time
import caixa

os.makedirs("entrada", exist_ok=True)
os.makedirs("feito", exist_ok=True)
print("vigiando a pasta entrada/...", flush=True)
while True:
    for nome in sorted(os.listdir("entrada")):
        if not nome.endswith(".txt"):
            continue
        linhas = open(os.path.join("entrada", nome)).read().strip().splitlines()
        esperado = next((l.split(":", 1)[1].strip() for l in linhas if l.lower().startswith("esperado:")), None)
        pedido = " ".join(l for l in linhas if not l.lower().startswith("esperado:"))
        resposta = caixa.atender(pedido, canal=f"pasta {nome}", esperado=esperado)
        with open(os.path.join("feito", nome), "w") as f:
            f.write(f"PEDIDO: {pedido}\nRESULTADO: {resposta}\n")
        os.remove(os.path.join("entrada", nome))
        print(f"[pasta] feito/{nome} gravado", flush=True)
    if "--uma-vez" in sys.argv:
        break
    time.sleep(2)
