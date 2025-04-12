"""
Parse Summary Script

This script reads the 'all_prompts.json' file from the prompts directory,
extracts the voiceover and visual descriptions, and saves them to
separate files for further processing.

Functions can be imported and used in other scripts.

Output Files:
- audio_prompts.txt: Contains all voiceover instructions
- image_prompts.txt: Contains all visual descriptions
"""

import json
import os
import re


def extract_prompts(json_path):
    """
    Extract audio and image prompts from the Gemini analysis
    
    Args:
        json_path (str): Path to the JSON file containing Gemini analysis
        
    Returns:
        tuple: Lists of audio and image prompts
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    gemini_analysis = data.get('gemini_analysis', '')
    if not gemini_analysis:
        print("No Gemini analysis found in the JSON file.")
        return [], []
    
    # Extract sections with titles
    sections = re.findall(r'\*\*Title:\*\* (.*?)\n(.*?)(?=\n\n- \*\*Title:|$)', 
                         gemini_analysis, re.DOTALL)
    
    audio_prompts = []
    image_prompts = []
    
    for title, content in sections:
        # Extract voiceover content
        voiceover_match = re.search(r'\*\*Voiceover:\*\* "(.*?)"', content, re.DOTALL)
        if voiceover_match:
            voiceover = voiceover_match.group(1).strip()
            audio_prompts.append(f"# {title}\n{voiceover}\n")
        
        # Extract visual content
        visual_match = re.search(r'\*\*Visual:\*\* (.*?)(?=\n\s*-|\n\s*\*\*|$)', content, re.DOTALL)
        if visual_match:
            visual = visual_match.group(1).strip()
            image_prompts.append(f"# {title}\n{visual}\n")
    
    return audio_prompts, image_prompts


def save_prompts_to_files(audio_prompts, image_prompts, prompts_dir):
    """
    Save the extracted prompts to separate files
    
    Args:
        audio_prompts (list): List of audio prompt strings
        image_prompts (list): List of image prompt strings
        prompts_dir (str): Directory to save the files
        
    Returns:
        tuple: Paths to the created audio and image prompt files
    """
    # Write audio prompts to file
    audio_path = os.path.join(prompts_dir, 'audio_prompts.txt')
    with open(audio_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(audio_prompts))
    print(f"Audio prompts saved to {audio_path}")
    
    # Write image prompts to file
    image_path = os.path.join(prompts_dir, 'image_prompts.txt')
    with open(image_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(image_prompts))
    print(f"Image prompts saved to {image_path}")
    
    return audio_path, image_path


def process_summary_file(json_path, output_dir=None):
    """
    Process a summary JSON file to extract and save prompts
    
    Args:
        json_path (str): Path to the JSON file containing Gemini analysis
        output_dir (str, optional): Directory to save output files. 
                                   Defaults to the directory of the JSON file.
    
    Returns:
        tuple: Paths to the created audio and image prompt files, or (None, None) if failed
    """
    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return None, None
    
    # Use the JSON file directory if output_dir not specified
    if output_dir is None:
        output_dir = os.path.dirname(json_path)
    
    # Extract prompts from the JSON file
    audio_prompts, image_prompts = extract_prompts(json_path)
    
    # Save the prompts to separate files
    return save_prompts_to_files(audio_prompts, image_prompts, output_dir)


def main():
    """
    Main function to parse the summary and extract prompts
    """
    prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
    json_path = os.path.join(prompts_dir, 'all_prompts.json')
    
    process_summary_file(json_path, prompts_dir)


if __name__ == "__main__":
    main()


"""
from parse-summary import process_summary_file

# Process a specific JSON file
audio_path, image_path = process_summary_file('path/to/your/json_file.json', 'output/directory')

# Or import specific functions if needed
from parse-summary import extract_prompts, save_prompts_to_files
"""