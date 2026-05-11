import os
from dotenv import load_dotenv
from google import genai

def test_gemini_connection():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env")
        return

    # SWITCH TO v1beta for Preview models
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})

    try:
        # Match exactly what is in your AI Studio sidebar
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Say 'Morpheus is online' if you can hear me."
        )

        if response.text:
            print("\n✅ CONNECTION SUCCESSFUL!")
            print(f"🤖 Gemini 3 says: {response.text.strip()}")
        else:
            print("\n⚠️  Connected, but no text was returned.")

    except Exception as e:
        print(f"\n❌ CONNECTION FAILED")
        print(f"Error details: {e}")

if __name__ == "__main__":
    test_gemini_connection()
