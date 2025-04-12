from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def parse_prompt_file(file_path):
    """
    Read a text file and parse it into an array of prompts.
    
    Args:
        file_path (str): Path to the text file containing prompts
        
    Returns:
        list: List of prompt strings
    """
    try:
        # Read the file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Split by commas and clean up each prompt
        prompts = []
        for prompt in content.splitlines():
            cleaned_prompt = prompt.strip()
            if cleaned_prompt:  # Only add non-empty prompts
                prompts.append(cleaned_prompt)
        
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
            
    # Save the image
    
    return generated_image, response_text

# Example usage
if __name__ == "__main__":
    sample_prompt = ('An educational infographic showing a horizontal timeline with three labeled segments: '
                    '\"Phone Screen\", \"Onsite Interview\", and \"Decision\". Each stage includes an icon: '
                    'a phone, a laptop with video call, and a thumbs-up/checkmark. Use clean vector-style visuals '
                    'with shades of blue, white, and black. College-style slide design, no clutter, minimalistic font.')
    
    #image, text = generate_image(sample_prompt)

    # Parse image prompts
    img_prompt_file = '/Users/arnav/Desktop/projects/bitcamp/backend/prompts/img-prompts-20250412-062250.txt'
    image_prompts = parse_prompt_file(img_prompt_file)
    
    # Print all image prompts
    print("\nImage Prompts:")
    for i, prompt in enumerate(image_prompts):
        print(f"\nPrompt {i+1}:")
        print(f"{prompt[:100]}..." if len(prompt) > 100 else prompt)
        image, text = generate_image(prompt)
        # Uncomment to save image
        if image:
          os.makedirs('images', exist_ok=True)
          output_path = os.path.join('images', f'{i}.png')
          image.save(output_path)
          print(f"Image saved to: {output_path}")
    