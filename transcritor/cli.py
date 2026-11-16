"""Interface de linha de comando: transcritor <arquivo-ou-pasta> [opções]."""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

from . import __version__
from .formatos import FORMATADORES

EXTENSOES = {".mp3", ".wav", ".m4a", ".ogg", ".opus", ".flac", ".mp4", ".mkv", ".webm", ".mov"}
MODELOS = ["tiny", "base", "small", "medium", "large-v3"]


def coletar_arquivos(entrada: Path) -> List[Path]:
    """Retorna o próprio arquivo ou todos os arquivos de mídia de uma pasta (recursivo)."""
    if entrada.is_dir():
        return sorted(p for p in entrada.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSOES)
    if entrada.is_file():
        return [entrada]
    return []


def interpretar_formatos(valor: str) -> List[str]:
    formatos = [f.strip().lower() for f in valor.split(",") if f.strip()]
    invalidos = [f for f in formatos if f not in FORMATADORES]
    if not formatos or invalidos:
        opcoes = ", ".join(FORMATADORES)
        raise argparse.ArgumentTypeError(f"formato inválido: {valor!r} (use: {opcoes})")
    return formatos


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="transcritor",
        description="Transcreve áudios/vídeos localmente e gera legendas.",
    )
    parser.add_argument("entrada", type=Path, help="arquivo de áudio/vídeo ou pasta")
    parser.add_argument("-m", "--modelo", default="small", choices=MODELOS)
    parser.add_argument("-i", "--idioma", default=None, help="ex.: pt, en, es (padrão: detectar)")
    parser.add_argument("-f", "--formatos", default="srt,txt", type=interpretar_formatos,
                        help="lista separada por vírgula: srt,vtt,txt")
    parser.add_argument("-o", "--saida", default="transcricoes", type=Path, help="pasta de destino")
    parser.add_argument("--dispositivo", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = criar_parser().parse_args(argv)

    arquivos = coletar_arquivos(args.entrada)
    if not arquivos:
        print(f"Nenhum arquivo de áudio/vídeo encontrado em: {args.entrada}", file=sys.stderr)
        return 1

    from .motor import Transcritor  # só carrega a IA quando realmente necessário

    print(f"Carregando modelo '{args.modelo}'... (o primeiro uso baixa o modelo)")
    transcritor = Transcritor(args.modelo, args.dispositivo)
    args.saida.mkdir(parents=True, exist_ok=True)

    for arquivo in arquivos:
        inicio = time.perf_counter()

        def progresso(fracao: float, nome: str = arquivo.name) -> None:
            print(f"\r  {nome}: {fracao:6.1%}", end="", flush=True)

        resultado = transcritor.transcrever(arquivo, args.idioma, progresso)
        print()

        for formato in args.formatos:
            destino = args.saida / f"{arquivo.stem}.{formato}"
            destino.write_text(FORMATADORES[formato](resultado.segmentos), encoding="utf-8")

        decorrido = time.perf_counter() - inicio
        velocidade = resultado.duracao / decorrido if decorrido else 0.0
        print(
            f"  ✔ idioma: {resultado.idioma} ({resultado.probabilidade_idioma:.0%}) · "
            f"{len(resultado.segmentos)} trechos · {velocidade:.1f}x tempo real"
        )

    print(f"Arquivos salvos em: {args.saida.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
