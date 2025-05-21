import gradio as gr

from app.asr import translate


def build_interface():
    iface = gr.Interface(
        fn=translate,
        inputs=[
            gr.Audio(type="filepath", label="Upload Audio File"),
            gr.Checkbox(label="Include timestamps in transcript?")
        ],
        outputs=gr.Textbox(label="Transcript", lines=10),
        title="Whisper.cpp Transcription Tool",
        # description="Upload an audio file and get a English transcript using whisper.cpp. Optionally include timestamps.",
        allow_flagging="never",
        analytics_enabled=False,
    )
    return iface
