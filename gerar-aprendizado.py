#!/usr/bin/env python3
"""
Gera aprendizado.html a partir de duas fontes:

  1. Mensagens de commit que contenham um bloco "Aprendi:"
  2. O arquivo APRENDIZADO.md (para registros anteriores à convenção)

Não precisa ser executado à mão — o workflow do GitHub Actions roda a cada
push e publica o resultado. Se rodar local: python3 gerar-aprendizado.py
"""

import html
import re
import subprocess
from pathlib import Path

SEPARADOR = "\x1e"   # separa commits
CAMPOS = "\x1f"      # separa campos dentro do commit

MESES = ["", "jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]


def data_legivel(iso):
    """2026-08-17 -> 17 de ago de 2026"""
    try:
        ano, mes, dia = iso.split("-")
        return f"{int(dia)} de {MESES[int(mes)]} de {ano}"
    except (ValueError, IndexError):
        return iso


def separar_titulo(primeira_linha):
    """Divide a primeira linha do bloco em (título, sobra).

    A convenção original pedia o título numa linha e o texto na seguinte —
    fácil de esquecer no meio de um commit, e quando esquece, o título sai
    cortado onde o editor quebrou a linha. Então: se a primeira linha já
    termina uma frase no meio dela, o título vai até ali e o resto desce
    para o corpo. Se não termina, a linha inteira é o título — que é o
    comportamento da convenção original, preservado.
    """
    m = re.search(r"(?<=[.!?])\s+", primeira_linha)
    if not m:
        return primeira_linha.strip(), ""
    return primeira_linha[:m.start()].strip(), primeira_linha[m.end():].strip()


def do_git():
    """Lê o histórico e extrai os blocos 'Aprendi:'."""
    try:
        bruto = subprocess.run(
            ["git", "log", f"--format={SEPARADOR}%H{CAMPOS}%ad{CAMPOS}%s{CAMPOS}%b", "--date=short"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    registros = []
    for commit in bruto.split(SEPARADOR):
        if not commit.strip():
            continue
        partes = commit.split(CAMPOS)
        if len(partes) < 4:
            continue
        commit_hash, data, assunto, corpo = partes[0], partes[1], partes[2], partes[3]

        # "Aprendi:" abre o bloco; ele vai até uma linha em branco ou o fim
        for m in re.finditer(r"^Aprendi:[ \t]*(.*)$", corpo, re.M):
            resto = corpo[m.end():]
            # $ com re.M casa ANTES do \n, então resto começa com a quebra da
            # própria linha do "Aprendi:". Sem descartar essa quebra, a primeira
            # linha do split é "" e o laço abaixo parava de cara — todo commit
            # saía com o corpo vazio. Descarta exatamente UMA quebra: uma linha
            # em branco de verdade logo abaixo continua significando "sem corpo".
            if resto.startswith("\n"):
                resto = resto[1:]

            titulo, sobra = separar_titulo(m.group(1).strip())

            linhas = [sobra] if sobra else []
            for linha in resto.split("\n"):
                if not linha.strip():
                    break
                linhas.append(linha.strip())
            texto = " ".join(linhas).strip()
            registros.append({
                "titulo": titulo,
                "texto": texto,
                "data": data,
                "origem": assunto.strip(),
                "hash": commit_hash[:7],
            })
    return registros


def do_arquivo():
    """
    Lê APRENDIZADO.md. Formato de cada entrada:

        ## título curto
        data: 2026-08-17
        origem: mensagem ou contexto
        texto livre...
    """
    caminho = Path("APRENDIZADO.md")
    if not caminho.exists():
        return []

    texto = caminho.read_text(encoding="utf-8")

    # Remove blocos de código antes de parsear. Sem isso o EXEMPLO de formato
    # que está documentado dentro do próprio arquivo (com "## título curto")
    # é lido como se fosse uma entrada real. Documentação não é dado.
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)

    registros = []
    for bloco in re.split(r"^## ", texto, flags=re.M)[1:]:
        linhas = bloco.strip().split("\n")
        titulo = linhas[0].strip()
        data, origem, corpo = "", "", []
        for linha in linhas[1:]:
            if linha.lower().startswith("data:"):
                data = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("origem:"):
                origem = linha.split(":", 1)[1].strip()
            elif linha.strip():
                corpo.append(linha.strip())
        registros.append({
            "titulo": titulo, "texto": " ".join(corpo),
            "data": data, "origem": origem, "hash": "",
        })
    return registros


def montar_itens(registros):
    if not registros:
        return """
      <div class="vazio">
        <p>Ainda não há registros.</p>
        <p>Esta página é gerada automaticamente a partir dos commits. Para
        adicionar um registro, basta escrever <code>Aprendi:</code> na mensagem
        de commit — o resto acontece sozinho.</p>
      </div>"""

    partes = []
    for r in registros:
        meta = []
        if r["data"]:
            meta.append(data_legivel(r["data"]))
        if r["origem"]:
            meta.append(html.escape(r["origem"]))
        if r["hash"]:
            meta.append(f'<code>{r["hash"]}</code>')

        # Registro sem corpo é legítimo (título já diz tudo). Só não pode
        # sobrar um <p> vazio ocupando espaço na página.
        corpo_html = (f'\n          <p class="licao__texto">{html.escape(r["texto"])}</p>'
                      if r["texto"] else "")

        partes.append(f"""
        <article class="licao">
          <h2 class="licao__titulo">{html.escape(r["titulo"])}</h2>
          <p class="licao__meta">{' · '.join(meta)}</p>{corpo_html}
        </article>""")
    return "\n".join(partes)


def main():
    registros = do_git() + do_arquivo()
    # mais recentes primeiro; sem data vai pro fim
    registros.sort(key=lambda r: r["data"] or "0000-00-00", reverse=True)

    modelo = Path("modelo-aprendizado.html").read_text(encoding="utf-8")

    # count=1: troca apenas a PRIMEIRA ocorrência. Se um dia alguém escrever o
    # marcador dentro de um comentário do modelo, a página não duplica.
    saida = (modelo
             .replace("<!--ITENS-->", montar_itens(registros), 1)
             .replace("<!--TOTAL-->", str(len(registros)), 1))

    Path("aprendizado.html").write_text(saida, encoding="utf-8")
    print(f"aprendizado.html gerado com {len(registros)} registro(s)")


if __name__ == "__main__":
    main()
