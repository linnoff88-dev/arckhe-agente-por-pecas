# agente-por-pecas-kit

[![Agente por peÃ§as](guia/assets/banner.jpg)](https://inematds.github.io/agente-por-pecas-kit/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

Este Ã© o kit do curso grÃ¡tis **Agente por peÃ§as**: um agente de IA pequeno, em Python puro, em que cada peÃ§a Ã© um arquivo que vocÃª abre e lÃª. Serve para quem jÃ¡ usa o ChatGPT ou o Claude e quer ver por dentro como um agente recebe um pedido, faz a tarefa e confere o resultado. O cÃ©rebro Ã© o Codex da sua assinatura do ChatGPT, sem chave de API (ou um modelo no seu computador, se vocÃª preferir). Para usar, vocÃª precisa de um terminal, do Python 3 e do Codex instalado; o curso ensina o resto, uma aula por vez.

## ðŸ“– Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/agente-por-pecas-kit/guia/**
Curso grÃ¡tis: **https://inematds.github.io/agente-por-pecas-v73/**

ðŸŽ¬ VÃ­deo: https://www.youtube.com/watch?v=pWXLBVyJd1Y

O kit do curso **Agente por peÃ§as** (INEMA): um agente de IA montado peÃ§a por peÃ§a, onde cada peÃ§a Ã© um arquivo.

```
CANAL â”€â”€pedidoâ”€â”€â–¶ CAIXA â”€â”€Ã© exato?â”€â”€â–¶ RECEITA (sem cÃ©rebro)
(terminal, chat,    â”‚ nÃ£o
 Telegram, pasta)   â–¼
                  CÃ‰REBRO (Codex) â”€â”€pedeâ”€â”€â–¶ FERRAMENTAS
                    â”‚   â–² memÃ³ria e regras
                    â–¼
                  VERIFICADOR â”€â”€â–¶ sucesso Â· tentar de novo Â· cancelar
```

| PeÃ§a | Arquivo |
|---|---|
| Canal | `canal_terminal.py`, `canal_web.py` + `chat.html`, `canal_telegram.py`, `canal_pasta.py` |
| Caixa (a rotina) | `caixa.py` |
| CÃ©rebro | `cerebro.py` (Codex da assinatura) Â· `cerebro_local.py` (Ollama, mÃ³dulo Ã  parte: `CEREBRO=local`) |
| Receitas (RPA) | `receitas.py` + `receitas/*.txt` |
| Ferramentas | `ferramentas.py` |
| MemÃ³ria | `memoria.json` (nasce quando o agente lembra a primeira coisa) |
| Regras | `regras.md` + as travas dentro de `ferramentas.py` |
| Verificador e loop | `verificador.py` + o laÃ§o em `caixa.py` |

Cada aula do curso Ã© uma tag: `git checkout aula2` â€¦ `git checkout aula8`.

## O processo, do inÃ­cio ao fim

1. ðŸ§  Instalar o Codex e entrar com a assinatura: `npm i -g @openai/codex && codex login`.
2. ðŸ§  Baixar o kit: `git clone https://github.com/inematds/agente-por-pecas-kit && cd agente-por-pecas-kit`.
3. âš™ï¸ Aula 2 (caixa e cÃ©rebro): `git checkout aula2 && python3 canal_terminal.py "seu pedido"`.
4. âš™ï¸ Aula 3 (chat): `git checkout aula3 && python3 canal_web.py` e abrir o endereÃ§o que aparece.
5. ðŸ§  Aula 4 (Telegram): criar o bot no @BotFather, gravar `TELEGRAM_TOKEN=...` no `.env`, `python3 canal_telegram.py`.
6. âš™ï¸ Aula 5 (pasta): `git checkout aula5 && python3 canal_pasta.py` e deixar arquivos `.txt` em `entrada/`.
7. âš™ï¸ Aula 6 (receitas e ferramentas): `git checkout aula6`, pedidos exatos vÃ£o para `receitas/`.
8. âš™ï¸ Aula 7 (memÃ³ria e regras): `git checkout aula7`; no Telegram, `TELEGRAM_DONO=<seu chat>` no `.env`.
9. âš™ï¸ Aula 8 (verificador e loop): `git checkout aula8 && python3 canal_terminal.py "pedido" --esperado "o que tem de aparecer"`.
10. âš™ï¸ Testes sem modelo: `python3 -m pytest -q testes/`.

O token do bot fica sÃ³ no `.env` (fora do git). O Codex roda numa pasta vazia, em modo sÃ³ leitura: quem mexe em arquivo Ã© a caixa, pelas ferramentas.

---

Projeto adaptado da comunidade INEMA TDS - Marca Arckhe