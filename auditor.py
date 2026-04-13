import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class SovereignAuditor:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is missing from environment variables.")
        
        # In v2.x, Mistral is the primary class
        try:
            self.client = Mistral(api_key=api_key)
        except Exception as e:
            raise ImportError(f"Failed to initialize Mistral client: {e}")
            
        self.model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    def analyze_code(self, file_name, content):
        prompt = f"Audit this code for security vulnerabilities: {file_name}\n\n{content}"
        try:
            # v2.x uses the .chat.complete interface
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Audit Error: {str(e)}"