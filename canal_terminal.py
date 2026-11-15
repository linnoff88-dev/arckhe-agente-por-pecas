"""CANAL terminal: o pedido chega pela linha de comando.
Uso: python3 canal_terminal.py "seu pedido"  [--esperado "o que tem de aparecer"]"""
import sys
import caixa

args = sys.argv[1:]
esperado = None
if "--esperado" in args:
    i = args.index("--esperado")
    esperado, args = args[i + 1], args[:i]
print(caixa.atender(" ".join(args), canal="terminal", esperado=esperado))
