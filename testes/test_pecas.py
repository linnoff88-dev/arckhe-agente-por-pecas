"""Testes das peças sem o modelo: o cérebro é trocado por um falso que responde sempre igual.
Rode na raiz do kit:  python3 -m pytest -q testes/"""
import json, os, shutil, sys
import pytest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KIT)


@pytest.fixture
def bancada(tmp_path, monkeypatch):
    for item in ("regras.md", "receitas"):
        origem = os.path.join(KIT, item)
        (shutil.copytree if os.path.isdir(origem) else shutil.copy)(origem, tmp_path / item)
    monkeypatch.chdir(tmp_path)
    import ferramentas, caixa
    monkeypatch.setattr(ferramentas, "PASTA", os.path.realpath(tmp_path / "trabalho"))
    return tmp_path


def cerebro_falso(monkeypatch, respostas):
    import cerebro
    fila = list(respostas)
    chamadas = []

    def pensar(mensagens, ferramentas=None, modelo=None):
        chamadas.append(json.loads(json.dumps(mensagens)))   # cópia: a lista original continua crescendo
        return fila.pop(0)
    monkeypatch.setattr(cerebro, "pensar", pensar)
    return chamadas


def test_receita_nao_chama_o_cerebro(bancada, monkeypatch):
    import caixa
    chamadas = cerebro_falso(monkeypatch, [])
    assert caixa.atender("Adicione pão na lista", mostrar=lambda *_: None) == "Anotei pão na lista."
    assert caixa.atender("o que tem na lista?", mostrar=lambda *_: None) == "Na lista: pão"
    assert chamadas == []


def test_regra_da_pasta_barra_leitura_de_fora(bancada, monkeypatch):
    import caixa
    (bancada / "segredo.txt").write_text("senha 1234")
    pede = {"tool_calls": [{"function": {"name": "ler", "arguments": {"nome": "../segredo.txt"}}}]}
    chamadas = cerebro_falso(monkeypatch, [pede, {"content": "não consegui"}, {"content": "SIM"}])
    caixa.atender("leia o segredo", mostrar=lambda *_: None)
    devolvido = chamadas[1][-1]["content"]
    assert "fora da pasta" in devolvido and "1234" not in devolvido


def test_substituir_fora_do_terminal_e_recusado(bancada, monkeypatch):
    import ferramentas
    os.makedirs(ferramentas.PASTA)
    ferramentas.escrever("a.txt", "velho")
    ferramentas.CANAL = "telegram"
    assert ferramentas.escrever("a.txt", "novo").startswith("recusado")
    assert open(os.path.join(ferramentas.PASTA, "a.txt")).read() == "velho"


def test_memoria_sobrevive_e_nao_repete(bancada):
    import ferramentas
    ferramentas.lembrar("O cachorro do dono se chama Thor")
    ferramentas.lembrar("O cachorro do dono se chama Thor")
    assert json.load(open("memoria.json")) == ["O cachorro do dono se chama Thor"]


def test_verificador_exato_aprova_e_cancela(bancada, monkeypatch):
    import caixa
    cerebro_falso(monkeypatch, [{"content": "A reunião é às 15h."}])
    assert caixa.atender("que horas?", mostrar=lambda *_: None, esperado="15") == "A reunião é às 15h."
    cerebro_falso(monkeypatch, [{"content": "É a Acme."}] * 3)
    assert caixa.atender("fornecedor?", mostrar=lambda *_: None, esperado="Beta").startswith("Cancelei")


def test_aviso_de_reprovacao_nao_entrega_o_esperado(bancada, monkeypatch):
    import caixa
    chamadas = cerebro_falso(monkeypatch, [{"content": "não sei"}, {"content": "Beta"}])
    caixa.atender("fornecedor?", mostrar=lambda *_: None, esperado="Beta")
    assert "Beta" not in json.dumps(chamadas[1], ensure_ascii=False)


def test_juiz_le_a_evidencia(bancada, monkeypatch):
    import caixa
    pede = {"tool_calls": [{"function": {"name": "ler", "arguments": {"nome": "n.txt"}}}]}
    os.makedirs(bancada / "trabalho")
    (bancada / "trabalho" / "n.txt").write_text("Levar o contrato.")
    chamadas = cerebro_falso(monkeypatch, [pede, {"content": "Leve o contrato."}, {"content": "SIM, está no arquivo"}])
    assert caixa.atender("o que levar?", mostrar=lambda *_: None) == "Leve o contrato."
    assert "Levar o contrato." in chamadas[2][-1]["content"]
