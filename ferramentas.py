"""As FERRAMENTAS: o que o agente consegue fazer no mundo (aqui, com arquivos da pasta trabalho/).
As REGRAS que valem de verdade moram aqui, no código: o modelo pode esquecer, o código não."""
import json, os

PASTA = os.path.realpath("trabalho")
MEMORIA = "memoria.json"
CANAL = "terminal"                         # a caixa avisa de onde veio o pedido


def caminho(nome):                         # regra 1: só a pasta trabalho/
    real = os.path.realpath(os.path.join(PASTA, nome))
    if not real.startswith(PASTA + os.sep):
        raise PermissionError("fora da pasta de trabalho")
    return real


def ler(nome):
    with open(caminho(nome)) as f:
        return f.read()


def escrever(nome, texto):                 # regra 2: substituir arquivo pede o OK do dono
    real = caminho(nome)
    if os.path.exists(real):
        if CANAL != "terminal" or input(f"  substituir {nome}? [s/N] ").lower() != "s":
            return "recusado: o dono não aprovou substituir"
    with open(real, "w") as f:
        f.write(texto)
    return f"gravado: {nome}"


def acrescentar(nome, texto):
    with open(caminho(nome), "a") as f:
        f.write(texto + "\n")
    return f"acrescentado em {nome}: {texto}"


def memorias():
    return json.load(open(MEMORIA)) if os.path.exists(MEMORIA) else []


def lembrar(fato):                         # a MEMÓRIA: sobrevive de uma conversa para a outra
    if fato in memorias():
        return f"já sabia: {fato}"
    json.dump(memorias() + [fato], open(MEMORIA, "w"), ensure_ascii=False)
    return f"guardado: {fato}"


TODAS = {"ler": ler, "escrever": escrever, "acrescentar": acrescentar, "lembrar": lembrar}

# o cardápio que o cérebro lê para saber o que pode pedir
CARDAPIO = [
    {"type": "function", "function": {"name": "ler", "description": "Lê um arquivo da pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}}, "required": ["nome"]}}},
    {"type": "function", "function": {"name": "escrever", "description": "Grava um arquivo na pasta de trabalho.",
     "parameters": {"type": "object", "properties": {"nome": {"type": "string"}, "texto": {"type": "string"}},
                    "required": ["nome", "texto"]}}},
    {"type": "function", "function": {"name": "lembrar", "description": "Guarda para sempre um fato sobre o dono, como uma frase completa (ex.: O cachorro do dono se chama Rex).",
     "parameters": {"type": "object", "properties": {"fato": {"type": "string"}}, "required": ["fato"]}}},
]
