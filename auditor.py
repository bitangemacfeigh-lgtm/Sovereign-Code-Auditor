import os
from dotenv import load_dotenv
import mistralai

load_dotenv()

# --- THE FAIL-SAFE RESOLVER ---
def get_mistral_client():
    # 1. Try the most modern way
    try:
        from mistralai import Mistral
        return Mistral
    except ImportError:
        pass

    # 2. Try the sub-module way (Version 2.x)
    try:
        from mistralai.client import MistralClient
        return MistralClient
    except ImportError:
        pass

    # 3. Dynamic Inspection (The "Hunter" method)
    for attr in dir(mistralai):
        if attr.lower() in ["mistral", "mistralclient"]:
            return getattr(mistralai, attr)
            
    return None

MistralClass = get_mistral_client()

if MistralClass is None:
    # If we still fail, we provide the absolute path for debugging
    raise ImportError(f"Mistral library found at {mistralai.__file__} but it contains no client class.")

class SovereignAuditor:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY missing from .env")
        
        # We use the class we 'hunted' above
        self.client = MistralClass(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    def analyze_code(self, file_name, content):
        prompt = f"Audit this code for security vulnerabilities: {file_name}\n\n{content}"
        try:
            # Modern SDKs use .chat.complete(), fallback to .chat()
            chat_engine = getattr(self.client, 'chat', self.client)
            if hasattr(chat_engine, 'complete'):
                response = chat_engine.complete(model=self.model, messages=[{"role": "user", "content": prompt}])
            else:
                response = self.client.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Audit Error: {str(e)}"