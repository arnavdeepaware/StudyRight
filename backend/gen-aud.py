from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "audio-vertex-key.json"

client = texttospeech.TextToSpeechClient()

text_block = '''
The Bloomberg interview involves a few key stages. First, you'll have a phone screen. 
Then, if that goes well, you'll proceed to a virtual onsite, followed by further assessments by managers.
'''

def generate_audio(text, filename):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=["small-bluetooth-speaker-class-device"],
        speaking_rate=1.0,
        pitch=0.0,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    os.makedirs('audios', exist_ok=True)
    filepath = os.path.join('audios', filename)
    with open(filepath, "wb") as output:
        output.write(response.audio_content)
        print(f'Audio content written to file "{filepath}"')

def get_audio_prompts():
    prompts = []
    with open('prompts/aud-prompts-20250412-062250.txt', 'r') as file:
        prompts = [line.strip() for line in file.readlines() if line.strip()]
    return prompts

def audio_files():
    prompts = get_audio_prompts()
    for i, prompt in enumerate(prompts):
        filename = f"audio_{i}.mp3"
        generate_audio(prompt, filename)
        print(f"Generated audio for prompt: {prompt}")

# print(get_audio_prompts())
audio_files()