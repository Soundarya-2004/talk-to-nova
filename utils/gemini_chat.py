import google.generativeai as genai

def ask_nova(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(f"You are Nova the Owl, a friendly guide for teens:\n{prompt}")
        return response.text.strip()
    except Exception as e:
        return f"Nova is unavailable right now. Error: {e}"
