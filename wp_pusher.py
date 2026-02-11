import os
import requests
import json

# 1. መዝገብ (ድጋሚ እንዳይላክ)
LOG_FILE = "published_history.log"

def is_already_published(content_id):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return content_id in f.read().splitlines()
    return False

def mark_as_published(content_id):
    with open(LOG_FILE, "a") as f:
        f.write(content_id + "\n")

def push_to_wordpress():
    wp_url = os.getenv('WP_URL')
    wp_user = os.getenv('WP_USERNAME')
    wp_pass = os.getenv('WP_PASSWORD')

    # ፋይሎችን በዋናው ፎልደር (Root) ውስጥ መፈለግ
    files_found = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not files_found:
        print("❌ ዜሮ (0) የ JSON ፋይል ነው ያገኘሁት። ማምረቻው ማሽን (main.py) ፋይል አልፈጠረም ማለት ነው።")
        return

    for filename in files_found:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            market = data.get('market', 'Global')
            topic = data.get('topic', 'Enterprise AI')
            content_id = f"{market}-{topic}".strip().lower()

            # ድግግሞሽ መቆጣጠሪያ
            if is_already_published(content_id):
                print(f"⏭️ {market} ቀደም ብሎ ተልኳል፣ ዘለልኩት።")
                continue

            # ይዘቱን ወደ WordPress መላክ
            payload = {
                "title": f"Enterprise AI Implementation Strategies 2026 for {market}",
                "content": data.get('content', ''),
                "status": "publish"
            }

            response = requests.post(
                f"{wp_url}/wp-json/wp/v2/posts",
                auth=(wp_user, wp_pass),
                json=payload
            )

            if response.status_code == 201:
                print(f"✅ ተሳክቷል፡ {market} ተልኳል።")
                mark_as_published(content_id)
            else:
                print(f"❌ ስህተት ለ {market}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ ፋይሉን ማንበብ አልተቻለም {filename}: {str(e)}")

if __name__ == "__main__":
    push_to_wordpress()
