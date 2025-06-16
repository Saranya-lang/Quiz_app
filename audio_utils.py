from gtts import gTTS
import os
import uuid

def generate_audio(question_text, options):
    full_text = question_text.strip() + ". " + " ".join([f"{chr(97+i)}) {opt}" for i, opt in enumerate(options)])
    tts = gTTS(full_text)
    os.makedirs("temp_audios", exist_ok=True)
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("temp_audios", filename)
    tts.save(filepath)
    return filepath
if __name__ == "__main__":
    # Example usage
    question = "What is the capital of France?"
    options = ["Berlin", "Madrid", "Paris", "Rome"]
    audio_file = generate_audio(question, options)
    print(f"Audio saved to: {audio_file}")

