"""O MOTOR DE RECEITAS: lê os arquivos de receitas/ e executa o passo a passo, sem cérebro.
Cada receita tem três linhas:
  quando: adicione * na lista          (o pedido exato; * é a parte que muda)
  faça: acrescentar lista.txt *         (ferramenta e o que ela recebe)
  responda: Anotei * na lista.          ({resultado} = o que a ferramenta devolveu)"""
import os, re
import ferramentas


def carregar():
    lista = []
    for nome in sorted(os.listdir("receitas")):
        campos = {}
        for linha in open(os.path.join("receitas", nome)):
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                campos[chave.strip()] = valor.strip()
        lista.append((nome, campos))
    return lista


def procurar(pedido):
    texto = pedido.lower().strip(" .!?")
    for nome, r in carregar():
        molde = "^" + re.escape(r["quando"].lower()).replace(r"\*", "(.+)") + "$"
        achou = re.match(molde, texto)
        if achou:
            return nome, r, (achou.group(1) if achou.groups() else "")
    return None


def executar(receita, parte):
    nome, r, _ = receita
    ferramenta, *args = r["faça"].replace("*", parte).split(" ", 2)
    try:
        resultado = ferramentas.TODAS[ferramenta](*args)
    except FileNotFoundError:                         # "o que tem na lista?" antes de anotar a primeira coisa
        resultado = "(vazia)"
    return r["responda"].replace("*", parte).replace("{resultado}", ", ".join(resultado.split("\n")).strip(", "))
