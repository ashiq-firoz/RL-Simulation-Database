
import os
import random

# Try importing google.genai, handle failure gracefully
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

CLIENT = None

def init_llm():
    global CLIENT
    api_key = os.getenv("GEMINI_API_KEY")
    if HAS_GENAI and api_key:
        try:
            CLIENT = genai.Client(api_key=api_key)
            print("LLM Client Initialized.")
            return True
        except Exception as e:
            print(f"Failed to init LLM: {e}")
            return False
    return False

def generate_text_content(prompt, fallback_type="task_description"):
    """
    Generates text using LLM if available, otherwise returns fallback.
    """
    global CLIENT
    
    # Fallbacks
    fallbacks = {
        "task_name": ["Fix login bug", "Update homepage hero", "Draft Q3 Report", "Client Meeting Prep"],
        "task_description": ["Please review the attached docs.", "Customer reported this issue on Monday.", "Need this by EOD."],
        "comment": ["Looks good to me!", "Can you clarify this?", "Blocked on dependency.", "Done."]
    }

    if CLIENT:
        try:
            response = CLIENT.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=100,
                    temperature=0.7
                )
            )
            return response.text.strip()
        except Exception as e:
            # print(f"LLM Generation Error: {e}") # Suppress to avoid spam
            pass
            
    return random.choice(fallbacks.get(fallback_type, ["Content"]))
