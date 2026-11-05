#!/usr/bin/env python3
"""
Gera sitemap.xml e sincroniza o dateModified do JSON-LD.

As duas coisas são a mesma ideia: data de alteração de página não se escreve
à mão, se pergunta ao git. O último commit que tocou o arquivo é a resposta,
e ela não envelhece sozinha nem depende de ninguém lembrar.

  sitemap.xml           <lastmod> de cada página
  *.html                "dateModified" dentro do JSON-LD

As datas são medidas UMA vez, para todas as páginas, ANTES de qualquer
escrita — e esse mesmo valor vai para os dois lugares. Medir de novo depois
de escrever devolve outra resposta: ver medir_datas().

Por que isso importa: o rastreador usa o <lastmod> para decidir se vale a pena
reler a página. Se o arquivo diz "mudou hoje" toda vez e nada mudou, ele
aprende a ignorar o sitemap — e aí demora a perceber a mudança que importa.

Roda no GitHub Actions a cada push. Local: python3 gerar-sitemap.py
"""

import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

BASE = "https://digitaldroids.com.br/"

# Arquivos .html que NÃO são páginas navegáveis.
# modelo-aprendizado.html é gabarito do gerador, não conteúdo.
IGNORAR = {"modelo-aprendizado.html"}

# index.html vira a raiz do site, não "/index.html" — endereço duplicado para
# a mesma página divide sinal entre as duas versões.
RAIZ = "index.html"


def mudou_agora(caminho):
    """O arquivo está diferente do último commit (ou ainda não foi commitado)?

    Importa porque este script roda ANTES do commit do Actions, no mesmo job
    que acabou de regenerar aprendizado.html. Sem esta checagem, a página
    recém-alterada entraria no sitemap com a data da alteração ANTERIOR.
    """
    try:
        saida = subprocess.run(
            ["git", "status", "--porcelain", "--", caminho],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    return bool(saida)


def data_do_git(caminho):
    """Data da última alteração do arquivo (AAAA-MM-DD), ou None."""
    if mudou_agora(caminho):
        return date.today().isoformat()
    try:
        saida = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", caminho],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    # Sem data é melhor que data inventada: a tag simplesmente não é escrita.
    return saida or None


def medir_datas(nomes):
    """Mede a data de CADA pagina UMA vez, antes de qualquer escrita.

    Existe por causa de um defeito medido em 05/11/2026: o sitemap dizia
    2026-11-05 e o dateModified da mesma pagina dizia 2026-11-04.

    Mecanismo: sincronizar_datemodified() chamava data_do_git(), ESCREVIA no
    arquivo, e depois o sitemap chamava data_do_git() DE NOVO sobre o mesmo
    arquivo -- que a essa altura estava sujo por causa da propria escrita.
    A segunda chamada caia no ramo mudou_agora() e devolvia date.today() do
    runner (UTC), enquanto a primeira tinha devolvido a data do commit. O
    script mudava a resposta que ia consultar em seguida.

    A regra geral: quando a medicao e sobre algo que o proprio programa vai
    alterar, meca ANTES e guarde o valor. Medir duas vezes nao e conferir --
    e perguntar a dois mundos diferentes.
    """
    return {nome: data_do_git(nome) for nome in nomes}


def paginas():
    """Os .html da raiz, com index primeiro e o resto em ordem alfabética."""
    achados = sorted(p.name for p in Path(".").glob("*.html")
                     if p.name not in IGNORAR)
    if RAIZ in achados:
        achados.remove(RAIZ)
        achados.insert(0, RAIZ)
    return achados


def sincronizar_datemodified(nomes, datas):
    """Ajusta o "dateModified" do JSON-LD de cada página para a data do git.

    Só mexe em quem já tem o campo — não inventa dado estruturado em página
    que não pedia. E só age se houver EXATAMENTE uma ocorrência: mais de uma
    significa que a página mudou de forma que este script não entende, e
    nesse caso é melhor não tocar do que corromper em silêncio.

    "datePublished" nunca é alterado: publicação acontece uma vez só.
    """
    padrao = re.compile(r'("dateModified"\s*:\s*")(\d{4}-\d{2}-\d{2})(")')
    tocados = 0

    for nome in nomes:
        caminho = Path(nome)
        texto = caminho.read_text(encoding="utf-8")

        achados = padrao.findall(texto)
        if len(achados) != 1:
            if achados:
                print(f"  ! {nome}: {len(achados)} dateModified, nao mexi")
            continue

        data = datas.get(nome)
        if not data or achados[0][1] == data:
            continue

        caminho.write_text(padrao.sub(rf"\g<1>{data}\g<3>", texto, count=1),
                           encoding="utf-8")
        print(f"  · {nome}: dateModified {achados[0][1]} -> {data}")
        tocados += 1

    return tocados


def main():
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    urlset = ET.Element(f"{{{ns}}}urlset")

    lista = paginas()

    # A ORDEM AQUI E O CONSERTO: medir primeiro, escrever depois. O
    # dicionario e a unica fonte das datas daqui pra frente -- ninguem
    # pergunta ao git de novo depois que este script comecou a escrever.
    datas = medir_datas(lista)

    tocados = sincronizar_datemodified(lista, datas)

    total_com_data = 0
    for nome in lista:
        url = ET.SubElement(urlset, f"{{{ns}}}url")
        ET.SubElement(url, f"{{{ns}}}loc").text = BASE + ("" if nome == RAIZ else nome)

        data = datas.get(nome)
        if data:
            ET.SubElement(url, f"{{{ns}}}lastmod").text = data
            total_com_data += 1

    # changefreq e priority não entram de propósito: o Google declara que
    # ignora os dois. Campo ignorado só cria mais uma coisa para manter
    # sincronizada com a realidade.
    ET.indent(urlset, space="  ")
    arvore = ET.ElementTree(urlset)

    with open("sitemap.xml", "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b"<!-- Gerado por gerar-sitemap.py. Nao editar a mao: as datas\n")
        f.write(b"     vem do git e qualquer mudanca aqui e sobrescrita. -->\n")
        arvore.write(f, encoding="utf-8", xml_declaration=False)
        f.write(b"\n")

    print(f"sitemap.xml gerado com {len(lista)} pagina(s), "
          f"{total_com_data} com data do git · "
          f"{tocados} dateModified ajustado(s)")


if __name__ == "__main__":
    main()
