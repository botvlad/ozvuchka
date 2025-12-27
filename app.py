# ===== COQUI LICENSE =====
import os
os.environ["COQUI_TOS_AGREED"] = "1"

import gradio as gr
from TTS.api import TTS
import soundfile as sf

VOICES = {
    "🇪🇸 Основной": "voice_es_1.wav",
    "🎙 Голос 2": "voice_clone.wav"
}

AVAILABLE_VOICES = {k: v for k, v in VOICES.items() if os.path.exists(v)}

if not AVAILABLE_VOICES:
    raise RuntimeError("❌ Голосовые файлы не найдены")

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False,
    progress_bar=False
)

def generate_voice(text, voice_name):
    if not text or text.strip() == "":
        return None

    output_path = "output.wav"

    tts.tts_to_file(
        text=text,
        speaker_wav=AVAILABLE_VOICES[voice_name],
        language="es",
        file_path=output_path
    )

    audio, sr = sf.read(output_path)
    return sr, audio

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🎙 XTTS — Испанская озвучка")

    voice = gr.Dropdown(
        choices=list(AVAILABLE_VOICES.keys()),
        value=list(AVAILABLE_VOICES.keys())[0],
        label="🎧 Голос"
    )

    text = gr.Textbox(lines=6, placeholder="Введите текст на испанском...")

    btn = gr.Button("▶ Озвучить")

    result = gr.Audio(label="🔊 Результат (можно скачать)", type="numpy")

    btn.click(fn=generate_voice, inputs=[text, voice], outputs=result)

app.launch()
