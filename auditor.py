import os
from dotenv import load_dotenv

# Direct import for modern SDK
try:
    from mistralai import Mistral
except ImportError:
    # Fallback for older envs
    try:
        from mistralai.client import MistralClient as Mistral
    except ImportError:
        Mistral = None

load_dotenv()

class SovereignAuditor:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is missing from Render Environment Variables")
        
        if Mistral is None:
            raise ImportError("Mistral SDK failed to load. Ensure requirements.txt includes 'mistralai'.")
            
        self.client = Mistral(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    def analyze_code(self, file_name, content):
        prompt = f"Audit this code for security vulnerabilities: {file_name}\n\n{content}"
        try:
            # Flexible method call for v1.x and v2.x
            method = getattr(self.client.chat, 'complete', self.client.chat)
            response = method(model=self.model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Audit Error: {str(e)}"