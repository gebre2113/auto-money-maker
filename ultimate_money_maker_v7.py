import os
import requests
from groq import Groq

# መረጃዎችን ከ GitHub Secrets ያነባል
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASS = os.getenv("WP_APP_PASS")

client = Groq(api_key=GROQ_API_KEY)

def generate_article():
    # ጽሑፍ እንዲያመነጭ ለ Groq ትዕዛዝ መስጠት
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a professional SEO blogger."},
            {"role": "user", "content": "Write a detailed, SEO-friendly tech article about 'The Future of AI in 2026' in English. Use HTML tags for formatting."}
        ],
        temperature=0.7,
        max_tokens=2048
    )
    return completion.choices[0].message.content

def post_to_wordpress(content):
    title = "The Future of AI in 2026: What to Expect"
    auth = (WP_USER, WP_APP_PASS)
    data = {
        "title": title,
        "content": content,
        "status": "publish"
    }
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", auth=auth, json=data)
    if response.status_status_code == 201:
        print("Article successfully posted to WordPress!")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    article_content = generate_article()
    post_to_wordpress(article_content)
