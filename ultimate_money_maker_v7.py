import os
import requests
from groq import Groq

# መረጃዎችን ከ GitHub Secrets ያነባል
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USERNAME")
WP_APP_PASS = os.getenv("WP_PASSWORD")

# Groq ደንበኛን ያስነሳል
client = Groq(api_key=GROQ_API_KEY)

def generate_article():
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # በጣም ዘመናዊው የ Groq ሞዴል
            messages=[
                {"role": "system", "content": "You are a professional SEO blogger."},
                {"role": "user", "content": "Write a high-quality, SEO-optimized tech article about 'Artificial Intelligence Trends in 2026' in English. Use HTML tags for formatting."}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

def post_to_wordpress(content):
    if not content:
        return
    
    title = "The Future of AI: Top Trends to Watch in 2026"
    # WordPress API Authentication
    # ማሳሰቢያ፡ WP_USER እና WP_APP_PASS በትክክል መኖራቸውን ያረጋግጡ
    data = {
        "title": title,
        "content": content,
        "status": "publish"
    }
    
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=(WP_USER, WP_APP_PASS),
        json=data
    )
    
    if response.status_code == 201:
        print("✅ Article successfully posted to WordPress!")
    else:
        print(f"❌ WordPress Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("🚀 Starting the Auto-Pilot Script...")
    article_content = generate_article()
    post_to_wordpress(article_content)
