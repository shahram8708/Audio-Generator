import gradio as gr
import os
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write

preload_models()

OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_and_save_audio(text_prompt):
    try:
        audio_array = generate_audio(text_prompt)
        file_path = os.path.join(OUTPUT_DIR, "generated_audio.wav")

        write(file_path, SAMPLE_RATE, audio_array)
        return file_path
    except Exception as e:
        return str(e)

CUSTOM_CSS = """
body {
    background-color: #f4f4f9;
    font-family: 'Arial', sans-serif;
}

.gradio-container {
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #ccc;
    background-color: white;
}

footer {
    visibility: hidden;
}

h1 {
    font-size: 2.5rem;
    color: #2c3e50;
    text-align: center;
}

.button {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 1rem;
    cursor: pointer;
}

.button:hover {
    background-color: #2980b9;
}

input {
    font-size: 1.1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    padding: 10px;
}

.audio-box {
    margin-top: 20px;
    text-align: center;
}

.download-link {
    font-size: 1rem;
    color: #2980b9;
    text-decoration: none;
    margin-top: 10px;
    display: inline-block;
}
.download-link:hover {
    text-decoration: underline;
}
"""

def gradio_app():
    with gr.Blocks(css=CUSTOM_CSS) as app:
        gr.Markdown("""
        # 🌟 AI Audio Generator 🌟
        Convert your text into lifelike audio instantly! Provide a text prompt, click generate, and download your personalized audio file.
        """)

        with gr.Row():
            text_input = gr.Textbox(
                label="Enter your text prompt here:",
                placeholder="Type something interesting!",
                lines=5,
            )

        with gr.Row():
            generate_button = gr.Button("Generate Audio", elem_classes="button")

        with gr.Row():
            audio_output = gr.Audio(label="Generated Audio", type="filepath")

        with gr.Row():
            download_link = gr.Markdown("""<span class='download-link'>Your download link will appear here after generation.</span>""")

        def process_audio(input_text):
            result = generate_and_save_audio(input_text)
            if os.path.exists(result):
                return result, f"[Download your audio file](file://{os.path.abspath(result)})"
            else:
                return None, f"Error: {result}"

        generate_button.click(
            fn=process_audio, inputs=[text_input], outputs=[audio_output, download_link]
        )

    return app

app = gradio_app()
app.launch(debug=True)
