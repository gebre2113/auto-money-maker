import google.generativeai as genai
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# ቁልፎችን ከ GitHub Secrets መውሰድ
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
WP_URL = os.getenv("WORDPRESS_URL")
WP_USER = os.getenv("WORDPRESS_USER")
WP_PASS = os.getenv("WORDPRESS_PASSWORD")

def run_ai_engine():
    # Gemini ማዋቀር
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # ይዘት ማመንጨት
    prompt = "Write a professional 1000-word blog post about 'Top AI Trends in 2026'. Include an introduction, subheadings, and a conclusion."
    response = model.generate_content(prompt)
    
    # WordPress ላይ መለጠፍ
    try:
        wp = Client(WP_URL, WP_USER, WP_PASS)
        post = WordPressPost()
        post.title = "The Future of AI: Top Trends for 2026"
        post.content = response.text
        post.post_status = 'publish'
        
        wp.call(NewPost(post))
        print("በተሳካ ሁኔታ ፖስት ተደርጓል!")
    except Exception as e:
        print(f"ስህተት ተፈጥሯል: {e}")

if __name__ == "__main__":
    run_ai_engine()
  
