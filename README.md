# 🎙️ Transcritor Local

Transcreva áudios e vídeos e gere **legendas SRT/VTT** usando IA open source — **100% offline**, no seu computador, sem assinaturas e sem enviar seus arquivos para a nuvem.

Construído sobre o [faster-whisper](https://github.com/SYSTRAN/faster-whisper), uma implementação otimizada do modelo **Whisper** (até 4x mais rápida que a original e usando menos memória).

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/IA-Whisper-412991)
![Offline](https://img.shields.io/badge/100%25-offline-2ea043)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Funcionalidades

- 🔒 **Privacidade total**: o áudio nunca sai da sua máquina
- 🌎 Detecção automática de idioma (ou force `--idioma pt`)
- 📝 Exporta **SRT**, **VTT** e **TXT**, com quebra de linha adequada para legendas
- 📂 Processa um arquivo ou uma **pasta inteira** (inclusive subpastas)
- 🎞️ Aceita áudio e vídeo: mp3, wav, m4a, ogg, flac, mp4, mkv, webm, mov
- 🔇 Filtro de silêncio (VAD) para evitar "alucinações" em trechos mudos
- ⚡ Usa GPU NVIDIA (CUDA) automaticamente quando disponível
- 🖥️ Interface web opcional com **Gradio** (inclusive gravação pelo microfone)

## 🚀 Instalação

```bash
git clone https://github.com/joseweslei45-debug/transcritor-local.git
cd transcritor-local
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -e .            # somente a CLI
pip install -e ".[web]"     # CLI + interface web
```

> Na primeira execução o modelo escolhido é baixado automaticamente (uma única vez). Depois disso, tudo funciona sem internet.

## 🧑‍💻 Uso pela linha de comando

```bash
# Um arquivo, gerando .srt e .txt (padrão)
transcritor aula.mp3

# Pasta inteira, em português, com modelo maior e legendas VTT
transcritor ./gravacoes --idioma pt --modelo medium --formatos srt,vtt -o legendas
```

Saída:

```
Carregando modelo 'small'... (o primeiro uso baixa o modelo)
  aula.mp3: 100.0%
  ✔ idioma: pt (99%) · 142 trechos · 6.3x tempo real
Arquivos salvos em: /home/weslei/transcricoes
```

| Opção | Padrão | Descrição |
|------|--------|-----------|
| `-m, --modelo` | `small` | tiny, base, small, medium, large-v3 |
| `-i, --idioma` | automático | Código do idioma (pt, en, es...) |
| `-f, --formatos` | `srt,txt` | Qualquer combinação de srt, vtt, txt |
| `-o, --saida` | `transcricoes` | Pasta de destino |
| `--dispositivo` | `auto` | auto, cpu ou cuda |

## 🌐 Interface web

```bash
python app.py
```

Abra o endereço exibido no terminal, envie ou grave um áudio e baixe a legenda pronta.

## 📊 Qual modelo escolher?

| Modelo | Velocidade | Precisão | Indicado para |
|-------|-----------|---------|---------------|
| tiny / base | ⚡⚡⚡ | ⭐ | Testes rápidos, PCs modestos |
| small | ⚡⚡ | ⭐⭐ | Melhor custo-benefício em CPU |
| medium | ⚡ | ⭐⭐⭐ | Aulas, reuniões, podcasts |
| large-v3 | 🐢 | ⭐⭐⭐⭐ | Máxima qualidade (ideal com GPU) |

## 🏗️ Estrutura

```
transcritor/
├── formatos.py   # Conversão para SRT/VTT/TXT (funções puras, testadas)
├── motor.py      # Wrapper do faster-whisper
└── cli.py        # Linha de comando
app.py            # Interface web (Gradio)
tests/            # pytest
```

## 🧪 Testes

```bash
pip install -e ".[dev]"
pytest
```

## 🗺️ Roadmap

- [ ] Diarização (identificar quem está falando)
- [ ] Tradução automática da legenda
- [ ] Síntese de voz local (TTS) para gerar narração a partir do texto

---
Desenvolvido por [Weslei Sousa](https://github.com/joseweslei45-debug) · Licença MIT
