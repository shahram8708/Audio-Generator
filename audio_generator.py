!pip install git+https://github.com/suno-ai/bark.git

from bark import SAMPLE_RATE, generate_audio, preload_models
from IPython.display import Audio

preload_models()

text_prompt = """
    Hello Ram! [smiles] How's it going? And how's your AI programming coming along? 
    I bet it's going pretty well, right? [laughs lightly] So, what are you working on right now? 
    [curious tone] Let me know, sounds interesting!
"""
audio_array = generate_audio(text_prompt)
Audio(audio_array, rate=SAMPLE_RATE)
