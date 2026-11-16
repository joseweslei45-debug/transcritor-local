"""Interface web local para o transcritor (requer: pip install -e ".[web]")."""

import tempfile
from pathlib import Path

import gradio as gr

from transcritor.formatos import para_srt, para_txt
from transcritor.motor import Transcritor

_modelos = {}


def obter_transcritor(nome: str) -> Transcritor:
    if nome not in _modelos:
        _modelos[nome] = Transcritor(nome)
    return _modelos[nome]


def transcrever(audio, modelo, idioma):
    if not audio:
        raise gr.Error("Envie ou grave um áudio primeiro.")
    resultado = obter_transcritor(modelo).transcrever(audio, None if idioma == "auto" else idioma)

    legenda = Path(tempfile.mkdtemp()) / "legenda.srt"
    legenda.write_text(para_srt(resultado.segmentos), encoding="utf-8")
    status = f"Idioma detectado: **{resultado.idioma}** ({resultado.probabilidade_idioma:.0%})"
    return para_txt(resultado.segmentos), str(legenda), status


with gr.Blocks(title="Transcritor Local") as demo:
    gr.Markdown(
        "# 🎙️ Transcritor Local\n"
        "Transcrição 100% offline com Whisper — seu áudio não sai do seu computador."
    )
    with gr.Row():
        with gr.Column():
            audio = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Áudio")
            modelo = gr.Dropdown(["tiny", "base", "small", "medium", "large-v3"], value="small", label="Modelo")
            idioma = gr.Dropdown(["auto", "pt", "en", "es"], value="pt", label="Idioma")
            botao = gr.Button("Transcrever", variant="primary")
        with gr.Column():
            texto = gr.Textbox(label="Transcrição", lines=14)
            arquivo = gr.File(label="Legenda (.srt)")
            status = gr.Markdown()

    botao.click(transcrever, [audio, modelo, idioma], [texto, arquivo, status])


if __name__ == "__main__":
    demo.launch()
