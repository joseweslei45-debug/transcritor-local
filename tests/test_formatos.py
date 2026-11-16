import pytest

from transcritor.formatos import Segmento, formatar_tempo, para_srt, para_txt, para_vtt, quebrar_linhas

SEGMENTOS = [
    Segmento(0.0, 2.5, " Olá, mundo!"),
    Segmento(2.5, 5.0, "Segundo trecho"),
]


@pytest.mark.parametrize(
    "segundos, esperado",
    [
        (0, "00:00:00,000"),
        (2.5, "00:00:02,500"),
        (3661.5, "01:01:01,500"),
        (59.9996, "00:01:00,000"),
    ],
)
def test_formatar_tempo(segundos, esperado):
    assert formatar_tempo(segundos) == esperado


def test_formatar_tempo_vtt_usa_ponto():
    assert formatar_tempo(1.25, ".") == "00:00:01.250"


def test_formatar_tempo_negativo():
    with pytest.raises(ValueError):
        formatar_tempo(-1)


def test_para_srt():
    esperado = (
        "1\n00:00:00,000 --> 00:00:02,500\nOlá, mundo!\n"
        "\n"
        "2\n00:00:02,500 --> 00:00:05,000\nSegundo trecho\n"
    )
    assert para_srt(SEGMENTOS) == esperado


def test_para_vtt():
    saida = para_vtt(SEGMENTOS)
    assert saida.startswith("WEBVTT\n\n")
    assert "00:00:02.500 --> 00:00:05.000\nSegundo trecho" in saida


def test_para_txt():
    assert para_txt(SEGMENTOS) == "Olá, mundo!\nSegundo trecho\n"


def test_quebrar_linhas_respeita_largura():
    texto = "uma frase bem longa que precisa ser quebrada em mais de uma linha de legenda"
    linhas = quebrar_linhas(texto, 30).split("\n")
    assert len(linhas) > 1
    assert all(len(linha) <= 30 for linha in linhas)
