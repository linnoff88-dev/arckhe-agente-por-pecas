"""CANAL chat: uma página web local. Uso: python3 canal_web.py  (o endereço sai na tela e no arquivo web.url)"""
import json, http.server
import caixa


class Chat(http.server.BaseHTTPRequestHandler):
    def do_GET(self):                                  # a página do chat
        corpo = open("chat.html", "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):                                 # cada mensagem do chat chega aqui
        pedido = json.loads(self.rfile.read(int(self.headers["Content-Length"])))["texto"]
        trilha = []
        resposta = caixa.atender(pedido, canal="chat", mostrar=trilha.append)
        print("\n".join(trilha), flush=True)
        corpo = json.dumps({"resposta": resposta, "trilha": trilha}, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, *args):                      # sem o log padrão de cada acesso
        pass


servidor = http.server.HTTPServer(("127.0.0.1", 0), Chat)   # porta 0: o sistema escolhe uma livre
url = f"http://127.0.0.1:{servidor.server_port}/"
open("web.url", "w").write(url)
print(f"chat no ar: {url}", flush=True)
servidor.serve_forever()
