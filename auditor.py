import os
from dotenv import load_dotenv

# Try importing the modern Mistral class
try:
    from mistralai import Mistral
except ImportError:
    # Fallback for specific environment path issues
    try:
        from mistralai.client import Mistral
    except ImportError:
        Mistral = None

load_dotenv()

class SovereignAuditor:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is missing from environment variables.")
        
        if Mistral is None:
            raise ImportError("Mistral SDK failed to load correctly. Check Python version compatibility.")
            
        self.client = Mistral(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    def analyze_code(self, file_name, content):
        prompt = f"Audit this code for security vulnerabilities: {file_name}\n\n{content}"
        try:
            # Modern v2 SDK uses .chat.complete
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Audit Error: {str(e)}"