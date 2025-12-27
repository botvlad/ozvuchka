import os
os.environ["COQUI_TOS_AGREED"] = "1"

import gradio as gr

VOICE_1 = "voice_es_1.wav"
VOICE_2 = "voice_clone.wav"

def load_voices():
    voices = {}
    if os.path.exists(VOICE_1):
        voices["🇪🇸 Основной"] = VOICE_1
    if os.path.exists(VOICE_2):
        voices["🎙 Голос 2"] = VOICE_2
    return voices

voices = load_voices()

def generate(text, voice):
    if not text or voice not in voices:
        return None

    from TTS.api import TTS

    tts = TTS(
        model_name="tts_models/multilingual/multi-dataset/xtts_v2",
        gpu=False
    )

    out = "output.wav"
    tts.tts_to_file(
        text=text,
        speaker_wav=voices[voice],
        language="es",
        file_path=out
    )
    return out

with gr.Blocks() as demo:
    gr.Markdown("## 🎙 Испанская озвучка (XTTS v2)")

    if voices:
        voice = gr.Dropdown(
            choices=list(voices.keys()),
            value=list(voices.keys())[0],
            label="Голос"
        )
    else:
        voice = gr.Dropdown(
            choices=["Нет голосов"],
            value="Нет голосов",
            label="Голос"
        )

    text = gr.Textbox(label="Текст", lines=5)
    btn = gr.Button("Озвучить")
    audio = gr.Audio(type="filepath", label="Результат (можно скачать)")

    btn.click(generate, [text, voice], audio)

demo.launch(server_name="0.0.0.0", server_port=7860)
