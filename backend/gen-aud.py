"""
Audio Generation Script
-----------------------
This script reads text prompts from 'prompts/audio_prompts.txt' and
converts them to speech using Google Cloud Text-to-Speech API.
Generated audio files are saved in the 'audios' directory.
"""

from google.cloud import texttospeech
import os
import sys

# Set Google Cloud credentials file path
CREDENTIALS_PATH = "audio-vertex-key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

def generate_audio(text, filename):
    """
    Generate audio file from text using Google Cloud Text-to-Speech.
    
    Args:
        text (str): The text to convert to speech
        filename (str): Name of the output audio file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize the Text-to-Speech client
        client = texttospeech.TextToSpeechClient()
        
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Standard-D"  # Male voice
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            effects_profile_id=["small-bluetooth-speaker-class-device"],
            speaking_rate=1.37,  # Slightly faster than normal
            pitch=0.0,  # Default pitch
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Create output directory if it doesn't exist
        os.makedirs('audios', exist_ok=True)
        
        # Write the response to the output file
        filepath = os.path.join('audios', filename)
        with open(filepath, "wb") as output:
            output.write(response.audio_content)
            print(f'✓ Audio file created: "{filepath}"')
            
        return True
    
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return False

def get_audio_prompts():
    """
    Read text prompts from the audio_prompts.txt file.
    
    Returns:
        list: List of text prompts
    """
    prompts = []
    try:
        with open('prompts/audio_prompts.txt', 'r') as file:
            prompts = [line.strip() for line in file.readlines() if line.strip()]
        
        if not prompts:
            print("Warning: No prompts found in the file.")
        else:
            print(f"Found {len(prompts)} prompts to process.")
            
    except FileNotFoundError:
        print("Error: 'prompts/audio_prompts.txt' file not found.")
        print("Create this file with one prompt per line.")
    except Exception as e:
        print(f"Error reading prompts: {str(e)}")
        
    return prompts

def generate_all_audio_files():
    """
    Main function to generate audio files for all prompts.
    """
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Error: Credentials file '{CREDENTIALS_PATH}' not found.")
        print("Download your Google Cloud service account key and save it with this name.")
        return
    
    prompts = get_audio_prompts()
    if not prompts:
        return
    
    success_count = 0
    for i, prompt in enumerate(prompts):
        print(f"\nProcessing prompt {i+1}/{len(prompts)}:")
        print(f"Text: {prompt[:75]}..." if len(prompt) > 75 else f"Text: {prompt}")
        
        filename = f"{i}.mp3"
        if generate_audio(prompt, filename):
            success_count += 1
    
    print(f"\nGeneration complete: {success_count}/{len(prompts)} audio files created.")

if __name__ == "__main__":
    print("Audio Generation Script")
    print("----------------------")
    generate_all_audio_files()