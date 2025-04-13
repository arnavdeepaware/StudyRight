from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

def parse_prompt_file(file_path):
    """
    Read a text file containing formatted prompts with headers.
    
    Args:
        file_path (str): Path to the text file containing prompts
        
    Returns:
        list: List of prompt strings
    """
    try:
        # Read the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Split content by sections (each section starts with # header)
        sections = re.split(r'\n# ', content)
        
        # Process each section (skip empty ones)
        prompts = []
        for section in sections:
            if not section.strip():
                continue
                
            # If this is the first section and doesn't start with #, add the # back
            if not section.startswith('#') and sections.index(section) == 0:
                section = '# ' + section
                
            # For other sections, add the # back since we split on \n#
            elif not section.startswith('#') and sections.index(section) > 0:
                section = section
                
            prompts.append(section.strip())
        
        print(f"Successfully parsed {len(prompts)} prompts from {file_path}")
        return prompts
        
    except Exception as e:
        print(f"Error reading prompt file: {str(e)}")
        return []

def generate_image(prompt):
    """
    Generate an image using Gemini API based on the provided prompt.
    
    Args:
        prompt (str): Text prompt describing the image to generate
        
    Returns:
        PIL.Image: Generated image object
        str: Response text if any
    """
    
    # Initialize client with API key from environment variable
    client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    
    # Send request to Gemini API
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
            # system_instruction=[
            # "You're an image generator. You role is to create simple and clean images with good colors, text-content, labels, etc. ",
            # "You will be given instructions that will have the description of the image. Use your best knowledge to create realistic content.",
        # ]
        )
    )
    
    # Process response
    response_text = None
    generated_image = None
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            response_text = part.text
            print(response_text)
        elif part.inline_data is not None:
            generated_image = Image.open(BytesIO((part.inline_data.data)))
            
    return generated_image, response_text

def main():
    """
    Main function to read image prompts from the file and generate images
    """
    # Get the absolute path to the prompts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(script_dir, 'prompts')
    image_prompts_path = os.path.join(prompts_dir, 'image_prompts.txt')
    
    # Check if the image prompts file exists
    if not os.path.exists(image_prompts_path):
        print(f"Error: Image prompts file not found at {image_prompts_path}")
        return
    
    # Parse image prompts
    image_prompts = parse_prompt_file(image_prompts_path)
    
    # Create images directory if it doesn't exist
    images_dir = os.path.join(script_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate and save images
    for i, prompt in enumerate(image_prompts):
        print(f"\nGenerating image {i} of {len(image_prompts)}:")
        print(f"{prompt[:100]}..." if len(prompt) > 100 else prompt)
        
        # Generate the image
        system_instructions = """You're an image generator. You role is to create simple and clean images with good colors, text-content, labels, etc. ",
            "You will be given instructions that will have the description of the image. Use your best knowledge to create realistic content."""
        image, text = generate_image(system_instructions + '\n' + prompt)
        
        # Save the image
        if image:
            output_path = os.path.join(images_dir, f'{i}.png')
            image.save(output_path)
            print(f"Image saved to: {output_path}")
        else:
            print(f"Failed to generate image for prompt {i}")

# Example usage
if __name__ == "__main__":
    main()

# Parse into functions to export
# Try