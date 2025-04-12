import json
import os
from datetime import datetime

def generate_prompts(summary_path="uploads/summary.json", output_dir="prompts"):
    # Create prompts directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"{summary_path} not found.")

    with open(summary_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    gemini_text = data.get("gemini_analysis", "")

    # Extract structured data
    concepts = []
    current = {}

    for line in gemini_text.splitlines():
        line = line.strip()
        if line.startswith("- **Title:**"):
            if current:
                concepts.append(current)
            current = {"title": line.replace("- **Title:**", "").strip()}
        elif line.startswith("- **Explanation:**"):
            current["explanation"] = line.replace("- **Explanation:**", "").strip()
        elif line.startswith("- **Visual:**"):
            current["visual"] = line.replace("- **Visual:**", "").strip()
        elif line.startswith("- **Voiceover:**"):
            current["voiceover"] = line.replace("- **Voiceover:**", "").strip()
    if current:
        concepts.append(current)

    # Prompt customization
    image_theme = "Use a simplistic college-educational style with minimal design. Limit the color palette to 2–3 colors: shades of blue, white, and black."

    img_prompts = []
    aud_prompts = []

    for concept in concepts:
        if "visual" in concept:
            img_prompts.append(f"{concept['visual']}. {image_theme}")
        if "voiceover" in concept:
            aud_prompts.append(concept["voiceover"])

    # Output files
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    img_file_path = os.path.join(output_dir, f"img-prompts-{timestamp}.txt")
    aud_file_path = os.path.join(output_dir, f"aud-prompts-{timestamp}.txt")

    with open(img_file_path, "w", encoding="utf-8") as f:
        for prompt in img_prompts:
            f.write(f"{prompt}\n\n")

    with open(aud_file_path, "w", encoding="utf-8") as f:
        for prompt in aud_prompts:
            f.write(f"{prompt}\n\n")

    print(f"Generated {img_file_path} and {aud_file_path}")
    
    return {
        "image_prompts_file": img_file_path,
        "audio_prompts_file": aud_file_path,
        "num_concepts": len(concepts)
    }

# Example usage
if __name__ == "__main__":
    generate_prompts()
