import os
import tempfile
import openai
import pygame

voice_map = {
    "Mrs. Brooks": "shimmer",
    "Ms. Taylor": "fable",
    "Mr. Thompson": "onyx",
    "Mr. Harris": "onyx",
    "Mr. Mitchell": "onyx"
}

openai.api_key = os.getenv("OPENAI_API_KEY")

def speak(text, persona_name="Mrs. Brooks"):
    voice = voice_map.get(persona_name, "shimmer")

    response = openai.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        fp.write(response.content)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(temp_path)
