"""CANAL Telegram: o pedido chega por mensagem ao seu bot.
Uso: python3 canal_telegram.py         (fica ouvindo; Ctrl+C para parar)
     python3 canal_telegram.py --uma   (atende uma mensagem e sai)
O token do bot fica no arquivo .env (TELEGRAM_TOKEN=...), nunca no código."""
import json, os, sys, urllib.request
import caixa


def ler_env():
    if os.path.exists(".env"):
        for linha in open(".env"):
            if "=" in linha and not linha.startswith("#"):
                nome, valor = linha.strip().split("=", 1)
                os.environ.setdefault(nome, valor)


ler_env()
TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
if not TOKEN:
    sys.exit("falta o TELEGRAM_TOKEN no arquivo .env")


def telegram(metodo, **dados):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    pedido = urllib.request.Request(url, json.dumps(dados).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(pedido, timeout=40) as r:
            return json.loads(r.read())["result"]
    except Exception as erro:                  # o erro traria a URL com o token: some com ele
        raise SystemExit(f"Telegram recusou {metodo}: {str(erro).replace(TOKEN, '<token>')}")


offset = int(open("telegram.offset").read()) if os.path.exists("telegram.offset") else 0
print("ouvindo o Telegram...", flush=True)
while True:
    for update in telegram("getUpdates", offset=offset, timeout=30):
        offset = update["update_id"] + 1
        open("telegram.offset", "w").write(str(offset))      # não atende a mesma mensagem duas vezes
        msg = update.get("message") or {}
        if "text" not in msg:
            continue
        print(f"(mensagem do chat {msg['chat']['id']})", flush=True)
        if msg["text"] == "/start":                           # a primeira mensagem de todo bot
            telegram("sendMessage", chat_id=msg["chat"]["id"], text="Olá! Sou o seu agente. Mande um pedido.")
            print("[telegram] boas-vindas enviadas", flush=True)
            continue
        dono = os.environ.get("TELEGRAM_DONO", "")
        if dono and str(msg["chat"]["id"]) != dono:           # regra 3: só o dono é atendido
            print("[regras] não é o dono: não atendo", flush=True)
            telegram("sendMessage", chat_id=msg["chat"]["id"], text="Este agente só atende o dono.")
            continue
        resposta = caixa.atender(msg["text"], canal="telegram")
        telegram("sendMessage", chat_id=msg["chat"]["id"], text=resposta or "(sem resposta)")
        print("[telegram] resposta enviada", flush=True)
        if "--uma" in sys.argv:
            sys.exit(0)
