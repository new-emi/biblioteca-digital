"""
Sistema de Gerenciamento de Biblioteca Digital
Autor: Emily
Disciplina: Programação para Ciência de Dados - PUCPR
Hora da Prática 2
"""

import argparse
import os
import shutil
from collections import defaultdict
from datetime import datetime

# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────

FORMATOS_SUPORTADOS = {".pdf", ".epub", ".docx", ".txt", ".mobi"}
DIRETORIO_BASE = "acervo"


# ──────────────────────────────────────────────
# Utilitários internos
# ──────────────────────────────────────────────


def _garantir_diretorio(caminho: str) -> None:
    """Cria o diretório caso não exista."""
    os.makedirs(caminho, exist_ok=True)


def _caminho_completo(nome_arquivo: str) -> str:
    """Retorna o caminho completo de um arquivo dentro do acervo."""
    return os.path.join(DIRETORIO_BASE, nome_arquivo)


def _validar_formato(nome_arquivo: str) -> bool:
    """Verifica se a extensão do arquivo é suportada pelo sistema."""
    _, extensao = os.path.splitext(nome_arquivo)
    return extensao.lower() in FORMATOS_SUPORTADOS


# ──────────────────────────────────────────────
# Funções de listagem
# ──────────────────────────────────────────────


def listar_por_tipo() -> dict[str, list[str]]:
    """
    Lista todos os documentos do acervo agrupados por tipo (extensão).

    Returns:
        Dicionário onde a chave é a extensão e o valor é a lista de arquivos.
    """
    _garantir_diretorio(DIRETORIO_BASE)
    agrupado = defaultdict(list)

    for arquivo in sorted(os.listdir(DIRETORIO_BASE)):
        caminho = _caminho_completo(arquivo)
        if os.path.isfile(caminho):
            _, extensao = os.path.splitext(arquivo)
            agrupado[extensao.lower() or "sem extensão"].append(arquivo)

    return dict(agrupado)


def listar_por_ano() -> dict[str, list[str]]:
    """
    Lista todos os documentos do acervo agrupados pelo ano de modificação.

    Returns:
        Dicionário onde a chave é o ano (str) e o valor é a lista de arquivos.
    """
    _garantir_diretorio(DIRETORIO_BASE)
    agrupado = defaultdict(list)

    for arquivo in sorted(os.listdir(DIRETORIO_BASE)):
        caminho = _caminho_completo(arquivo)
        if os.path.isfile(caminho):
            timestamp = os.path.getmtime(caminho)
            ano = str(datetime.fromtimestamp(timestamp).year)
            agrupado[ano].append(arquivo)

    return dict(agrupado)


def listar_todos() -> list[str]:
    """
    Retorna a lista de todos os arquivos presentes no acervo.

    Returns:
        Lista com os nomes dos arquivos.
    """
    _garantir_diretorio(DIRETORIO_BASE)
    return [
        f
        for f in sorted(os.listdir(DIRETORIO_BASE))
        if os.path.isfile(_caminho_completo(f))
    ]


# ──────────────────────────────────────────────
# Funções de manipulação
# ──────────────────────────────────────────────


def adicionar_documento(caminho_origem: str) -> str:
    """
    Copia um documento externo para o acervo da biblioteca.

    Args:
        caminho_origem: Caminho do arquivo a ser adicionado.

    Returns:
        Mensagem de sucesso ou erro.
    """
    _garantir_diretorio(DIRETORIO_BASE)

    if not os.path.isfile(caminho_origem):
        return f"Erro: arquivo '{caminho_origem}' não encontrado."

    nome_arquivo = os.path.basename(caminho_origem)

    if not _validar_formato(nome_arquivo):
        extensoes = ", ".join(sorted(FORMATOS_SUPORTADOS))
        return f"Erro: formato não suportado. Use: {extensoes}"

    destino = _caminho_completo(nome_arquivo)

    if os.path.exists(destino):
        return f"Erro: já existe um arquivo chamado '{nome_arquivo}' no acervo."

    shutil.copy2(caminho_origem, destino)
    return f"✔ Documento '{nome_arquivo}' adicionado ao acervo com sucesso."


def renomear_documento(nome_atual: str, novo_nome: str) -> str:
    """
    Renomeia um documento existente no acervo.

    Args:
        nome_atual: Nome atual do arquivo no acervo.
        novo_nome:  Novo nome desejado para o arquivo.

    Returns:
        Mensagem de sucesso ou erro.
    """
    origem = _caminho_completo(nome_atual)
    destino = _caminho_completo(novo_nome)

    if not os.path.isfile(origem):
        return f"Erro: arquivo '{nome_atual}' não encontrado no acervo."

    if not _validar_formato(novo_nome):
        extensoes = ", ".join(sorted(FORMATOS_SUPORTADOS))
        return f"Erro: formato não suportado. Use: {extensoes}"

    if os.path.exists(destino):
        return f"Erro: já existe um arquivo chamado '{novo_nome}' no acervo."

    os.rename(origem, destino)
    return f"✔ '{nome_atual}' renomeado para '{novo_nome}' com sucesso."


def remover_documento(nome_arquivo: str, confirmar: bool = False) -> str:
    """
    Remove um documento do acervo.

    Args:
        nome_arquivo: Nome do arquivo a ser removido.
        confirmar:    Se True, pula a confirmação interativa.

    Returns:
        Mensagem de sucesso ou erro.
    """
    caminho = _caminho_completo(nome_arquivo)

    if not os.path.isfile(caminho):
        return f"Erro: arquivo '{nome_arquivo}' não encontrado no acervo."

    if not confirmar:
        resposta = (
            input(f"Confirmar remoção de '{nome_arquivo}'? [s/N]: ").strip().lower()
        )
        if resposta != "s":
            return "Remoção cancelada."

    os.remove(caminho)
    return f"✔ Documento '{nome_arquivo}' removido do acervo com sucesso."


def criar_diretorio(nome: str) -> str:
    """
    Cria um subdiretório dentro do acervo.

    Args:
        nome: Nome do subdiretório a ser criado.

    Returns:
        Mensagem de sucesso ou erro.
    """
    caminho = _caminho_completo(nome)

    if os.path.exists(caminho):
        return f"Erro: '{nome}' já existe no acervo."

    os.makedirs(caminho)
    return f"✔ Diretório '{nome}' criado com sucesso."


def remover_diretorio(nome: str, confirmar: bool = False) -> str:
    """
    Remove um subdiretório vazio do acervo.

    Args:
        nome:     Nome do subdiretório a ser removido.
        confirmar: Se True, pula a confirmação interativa.

    Returns:
        Mensagem de sucesso ou erro.
    """
    caminho = _caminho_completo(nome)

    if not os.path.isdir(caminho):
        return f"Erro: diretório '{nome}' não encontrado no acervo."

    if not confirmar:
        resposta = (
            input(f"Confirmar remoção do diretório '{nome}'? [s/N]: ").strip().lower()
        )
        if resposta != "s":
            return "Remoção cancelada."

    try:
        os.rmdir(caminho)
        return f"✔ Diretório '{nome}' removido com sucesso."
    except OSError:
        return f"Erro: o diretório '{nome}' não está vazio."


# ──────────────────────────────────────────────
# Exibição formatada
# ──────────────────────────────────────────────


def _imprimir_agrupado(titulo: str, agrupado: dict) -> None:
    """Imprime um dicionário agrupado de forma formatada."""
    print(f"\n{'=' * 50}")
    print(f"  {titulo}")
    print(f"{'=' * 50}")

    if not agrupado:
        print("  Nenhum documento encontrado no acervo.")
        return

    for chave, arquivos in sorted(agrupado.items()):
        print(f"\n  [{chave}]  ({len(arquivos)} arquivo(s))")
        for arq in arquivos:
            print(f"    • {arq}")

    total = sum(len(v) for v in agrupado.values())
    print(f"\n  Total: {total} documento(s)\n")


# ──────────────────────────────────────────────
# Interface de linha de comando (CLI)
# ──────────────────────────────────────────────


def _construir_parser() -> argparse.ArgumentParser:
    """Constrói e retorna o parser de argumentos da CLI."""
    parser = argparse.ArgumentParser(
        prog="biblioteca",
        description="Sistema de Gerenciamento de Biblioteca Digital",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # listar
    p_listar = subparsers.add_parser("listar", help="Lista os documentos do acervo")
    p_listar.add_argument(
        "--por",
        choices=["tipo", "ano", "todos"],
        default="todos",
        help="Critério de listagem (padrão: todos)",
    )

    # adicionar
    p_add = subparsers.add_parser("adicionar", help="Adiciona um documento ao acervo")
    p_add.add_argument("arquivo", help="Caminho do arquivo a ser adicionado")

    # renomear
    p_ren = subparsers.add_parser("renomear", help="Renomeia um documento no acervo")
    p_ren.add_argument("nome_atual", help="Nome atual do arquivo")
    p_ren.add_argument("novo_nome", help="Novo nome para o arquivo")

    # remover
    p_rem = subparsers.add_parser("remover", help="Remove um documento do acervo")
    p_rem.add_argument("arquivo", help="Nome do arquivo a ser removido")
    p_rem.add_argument(
        "-f",
        "--forcar",
        action="store_true",
        help="Remove sem pedir confirmação",
    )

    # mkdir
    p_mkdir = subparsers.add_parser("mkdir", help="Cria um subdiretório no acervo")
    p_mkdir.add_argument("nome", help="Nome do diretório a criar")

    # rmdir
    p_rmdir = subparsers.add_parser(
        "rmdir", help="Remove um subdiretório vazio do acervo"
    )
    p_rmdir.add_argument("nome", help="Nome do diretório a remover")
    p_rmdir.add_argument(
        "-f", "--forcar", action="store_true", help="Remove sem confirmação"
    )

    return parser


def main() -> None:
    """Ponto de entrada da aplicação via linha de comando."""
    parser = _construir_parser()
    args = parser.parse_args()

    if args.comando == "listar":
        if args.por == "tipo":
            _imprimir_agrupado("Documentos por Tipo", listar_por_tipo())
        elif args.por == "ano":
            _imprimir_agrupado("Documentos por Ano", listar_por_ano())
        else:
            arquivos = listar_todos()
            print(f"\n{'=' * 50}")
            print("  Todos os Documentos")
            print(f"{'=' * 50}")
            if arquivos:
                for arq in arquivos:
                    print(f"    • {arq}")
                print(f"\n  Total: {len(arquivos)} documento(s)\n")
            else:
                print("  Nenhum documento encontrado no acervo.\n")

    elif args.comando == "adicionar":
        print(adicionar_documento(args.arquivo))

    elif args.comando == "renomear":
        print(renomear_documento(args.nome_atual, args.novo_nome))

    elif args.comando == "remover":
        print(remover_documento(args.arquivo, confirmar=args.forcar))

    elif args.comando == "mkdir":
        print(criar_diretorio(args.nome))

    elif args.comando == "rmdir":
        print(remover_diretorio(args.nome, confirmar=args.forcar))


if __name__ == "__main__":
    main()
