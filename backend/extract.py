from vertexai.preview.language_models import ChatModel
import vertexai
import os
import json
import PyPDF2
import docx
import datetime
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_text_from_file(filepath):
    """Extract text from different file types"""
    if filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    elif filepath.endswith('.pdf'):
        text = ""
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text() + "\n"
        except Exception as e:
            text = f"Error extracting PDF text: {str(e)}"
        return text
    
    elif filepath.endswith('.docx'):
        try:
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return f"Error extracting DOCX text: {str(e)}"
    
    return "Unsupported file type"

from vertexai.generative_models import GenerativeModel

def send_to_gemini(text):
    try:
        # Use service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            'vertexai_key.json'
        )

        # Get project details from .env file
        PROJECT_ID = os.getenv('PROJECT_ID').strip('"').strip()
        LOCATION = os.getenv('LOCATION').strip('"').strip()

        # Initialize Vertex AI
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            credentials=credentials
        )

        # Use Gemini 2.0 Flash model
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""
You are helping a college student understand academic material by converting it into a short educational video.

Below is the raw text extracted from a class document. Your task is to identify and structure the most important concepts clearly so that they can be used to generate visual and audio content for a video.

Please return:
1. A **list of 5–7 core concepts or topics** from the material, written in short and simple language.
2. For each concept, include:
   - A **title** (max 8 words)
   - A **1–2 sentence explanation** (max 30 words)
   - A **visual description** (to guide AI image generation)
   - A **voiceover script** (natural and student-friendly, max 3 sentences)

### Example Output Format:
- **Title:** What is a Graph?
  - **Explanation:** A graph is a way to show how things are connected using points (nodes) and lines (edges).
  - **Visual:** An illustration of 5 dots connected by lines, representing friends in a social network.
  - **Voiceover:** "Imagine your social network. Each person is a dot, and each connection is a line. That's what we call a graph."

Here is the document content:

{text[:5000]}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error with Gemini API: {str(e)}"


def process_uploaded_file(filename):
    """Process the file in uploads directory and save results as JSON"""
    # Construct file path
    uploads_dir = 'uploads'
    filepath = os.path.join(uploads_dir, filename)
    
    # Check if file exists
    if not os.path.exists(filepath):
        return {"error": f"File {filename} not found in uploads directory"}
    
    # Extract text from file
    extracted_text = extract_text_from_file(filepath)
    
    # Process with Gemini
    gemini_response = send_to_gemini(extracted_text)
    
    # Create a summary object
    summary = {
        "filename": filename,
        "processed_time": datetime.datetime.now().isoformat(),
        "extracted_text_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
        "gemini_analysis": gemini_response
    }
    
    # Save as JSON
    json_path = os.path.join('uploads', 'summary.json')
    
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(summary, json_file, indent=2, ensure_ascii=False)
    
    return {
        "message": "File successfully processed",
        "summary_file": json_path,
        "original_file": filepath
    }

if __name__ == "__main__":
    # Get list of files in uploads directory
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Filter out JSON files from processing
    files = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f)) and not f.endswith('.json')]
    
    if not files:
        print("No files found in uploads directory")
    else:
        # Process the most recently added file (based on modification time)
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(uploads_dir, f)))
        print(f"Processing latest file: {latest_file}")
        
        result = process_uploaded_file(latest_file)
        print(json.dumps(result, indent=2))