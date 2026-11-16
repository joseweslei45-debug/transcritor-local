import argparse

import pytest

from transcritor.cli import coletar_arquivos, interpretar_formatos


def test_coletar_arquivos_de_pasta(tmp_path):
    (tmp_path / "a.mp3").write_bytes(b"")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.MP4").write_bytes(b"")
    (tmp_path / "notas.txt").write_text("ignorar")

    nomes = [p.name for p in coletar_arquivos(tmp_path)]

    assert nomes == ["a.mp3", "b.MP4"]


def test_coletar_arquivo_unico(tmp_path):
    arquivo = tmp_path / "aula.wav"
    arquivo.write_bytes(b"")
    assert coletar_arquivos(arquivo) == [arquivo]


def test_coletar_caminho_inexistente(tmp_path):
    assert coletar_arquivos(tmp_path / "nao-existe.mp3") == []


def test_interpretar_formatos():
    assert interpretar_formatos(" SRT, vtt ") == ["srt", "vtt"]
    with pytest.raises(argparse.ArgumentTypeError):
        interpretar_formatos("srt,pdf")
