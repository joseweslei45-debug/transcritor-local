"""Wrapper do faster-whisper. A importação é tardia para que o restante
do pacote (e os testes) funcione mesmo sem o modelo instalado."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Union

from .formatos import Segmento


@dataclass
class Resultado:
    segmentos: List[Segmento]
    idioma: str
    probabilidade_idioma: float
    duracao: float


class Transcritor:
    def __init__(self, modelo: str = "small", dispositivo: str = "auto", precisao: str = "default"):
        from faster_whisper import WhisperModel

        self._modelo = WhisperModel(modelo, device=dispositivo, compute_type=precisao)

    def transcrever(
        self,
        arquivo: Union[str, Path],
        idioma: Optional[str] = None,
        ao_progredir: Optional[Callable[[float], None]] = None,
    ) -> Resultado:
        brutos, info = self._modelo.transcribe(
            str(arquivo),
            language=idioma,
            beam_size=5,
            vad_filter=True,  # ignora silêncios longos
        )

        segmentos: List[Segmento] = []
        for seg in brutos:  # gerador: a transcrição acontece durante a iteração
            segmentos.append(Segmento(seg.start, seg.end, seg.text))
            if ao_progredir and info.duration:
                ao_progredir(min(seg.end / info.duration, 1.0))

        if ao_progredir:
            ao_progredir(1.0)
        return Resultado(segmentos, info.language, info.language_probability, info.duration)
