"""
Parser Script for Gemini Analysis Output

This script processes all_prompts.json from the prompts directory and
separates the content into audio and image descriptions.
"""

import json
import os
import re
from pathlib import Path

def parse_gemini_output():
    """
    Parse the Gemini analysis output and separate into audio/image prompts
    """
    # Define paths
    base_dir = Path(__file__).parent
    prompts_dir = base_dir / 'prompts'
    json_path = prompts_dir / 'all_prompts.json'
    
    try:
        # Check if JSON file exists
        if not json_path.exists():
            raise FileNotFoundError(f"Could not find {json_path}")
            
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract Gemini analysis
        analysis = data.get('gemini_analysis')
        if not analysis:
            raise ValueError("No gemini_analysis found in JSON")
            
        # Initialize prompt lists
        audio_prompts = []
        image_prompts = []
        
        # Updated regex pattern to match exactly with Gemini output
        pattern = r'\*\*(\d+)\.\s*Title:\s*(.*?)\*\*\s*\*\*Caption:\*\*\s*(.*?)\s*\*\*Visual:\*\*\s*(.*?)\s*\*\*Voiceover:\*\*\s*"(.*?)"'
        
        sections = re.findall(pattern, analysis, re.DOTALL)
        
        # Process each section with updated tuple unpacking
        for section_num, title, caption, visual, voiceover in sections:
            # Clean up the extracted text
            title = title.strip()
            caption = caption.strip()
            visual = visual.strip()
            voiceover = voiceover.strip()
            
            # Format audio prompts with section number
            audio_prompts.append(f"# Section {section_num}: {title}\n{voiceover}\n")
            
            # Format image prompts with section number and caption
            image_prompts.append(f"# Section {section_num}: {title}\n{caption}\n\n{visual}\n")
        
        # Save audio prompts
        audio_path = prompts_dir / 'audio_prompts.txt'
        with open(audio_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(audio_prompts))
            
        # Save image prompts
        image_path = prompts_dir / 'image_prompts.txt'
        with open(image_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(image_prompts))
            
        print(f"Successfully parsed {len(sections)} sections:")
        print(f"- Audio prompts saved to: {audio_path}")
        print(f"- Image prompts saved to: {image_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parse_gemini_output()