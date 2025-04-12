from google.cloud import aiplatform
from google.oauth2 import service_account
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import pathlib


credentials = service_account.Credentials.from_service_account_file('vertexai_key.json')

# Define project information
PROJECT_ID = "deep-sphere-456607-s4"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

# Use the generative model (Imagen/Image Generation Model)
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

# Sample prompts
prompts = {
    "graph": "A cartoon-style illustration of a graph data structure, with nodes connected by edges, representing a social network.",
    "stack": "A colorful cartoon of a stack data structure, with blocks labeled A, B, C being pushed and popped in a last-in-first-out order."
}


# Generate and download images
for label, prompt in prompts.items():
    response = imagen_model.generate_images(
        prompt=prompt,
        aspect_ratio='16:9'
    )
    image = response.images[0]
    
    # Display the image (if running in environment with display capability)
    try:
        image.show()
    except:
        print(f"Could not display image for: {label}")
    
    # Save the image
    pathlib.Path(f"{label}.png").write_bytes(image._image_bytes)
    print(f"{label}.png generated!")