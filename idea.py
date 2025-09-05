from google import genai
from google.genai import types

API_KEY = "AIzaSyAAsF1Q6vFVxuWbsKWjToLigZc0Zi_f-5o"

def quote():
    try:
        client = genai.Client(api_key=API_KEY)
        prompt = ('Give a quote of creation and innovation')
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.5, max_output_tokens=50)
        )
        return(response.text.strip())
    except Exception as e:
        return f"❌ Error: {e}"
    
print(quote())
