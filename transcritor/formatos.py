"""Conversão de segmentos transcritos para formatos de legenda e texto."""

import textwrap
from dataclasses import dataclass
from typing import Callable, Dict, Iterable

LARGURA_LEGENDA = 42  # caracteres por linha, padrão comum em legendas


@dataclass(frozen=True)
class Segmento:
    inicio: float
    fim: float
    texto: str


def formatar_tempo(segundos: float, separador: str = ",") -> str:
    """3661.5 -> '01:01:01,500' (SRT usa vírgula, VTT usa ponto)."""
    if segundos < 0:
        raise ValueError("O tempo não pode ser negativo")
    total_ms = round(segundos * 1000)
    horas, resto = divmod(total_ms, 3_600_000)
    minutos, resto = divmod(resto, 60_000)
    seg, ms = divmod(resto, 1000)
    return f"{horas:02d}:{minutos:02d}:{seg:02d}{separador}{ms:03d}"


def quebrar_linhas(texto: str, largura: int = LARGURA_LEGENDA) -> str:
    return "\n".join(textwrap.wrap(texto.strip(), largura)) or texto.strip()


def para_srt(segmentos: Iterable[Segmento]) -> str:
    blocos = []
    for i, seg in enumerate(segmentos, start=1):
        blocos.append(
            f"{i}\n"
            f"{formatar_tempo(seg.inicio)} --> {formatar_tempo(seg.fim)}\n"
            f"{quebrar_linhas(seg.texto)}\n"
        )
    return "\n".join(blocos)


def para_vtt(segmentos: Iterable[Segmento]) -> str:
    linhas = ["WEBVTT", ""]
    for seg in segmentos:
        linhas.append(f"{formatar_tempo(seg.inicio, '.')} --> {formatar_tempo(seg.fim, '.')}")
        linhas.append(quebrar_linhas(seg.texto))
        linhas.append("")
    return "\n".join(linhas)


def para_txt(segmentos: Iterable[Segmento]) -> str:
    return "\n".join(seg.texto.strip() for seg in segmentos) + "\n"


FORMATADORES: Dict[str, Callable[[Iterable[Segmento]], str]] = {
    "srt": para_srt,
    "vtt": para_vtt,
    "txt": para_txt,
}
