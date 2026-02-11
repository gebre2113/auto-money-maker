import os
import requests
import json

# 1. አድራሻዎች እና መዝገቦች
LOG_FILE = "published_history.log"
JSON_DIR = "generated_content" # AI ያመረታቸው ፋይሎች የሚቀመጡበት

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

    # በፎልደሩ ውስጥ ያሉትን ሁሉንም JSON ፋይሎች መፈተሽ
    if not os.path.exists(JSON_DIR):
        print("❌ ምንም የሚላክ ፋይል (JSON) አልተገኘም!")
        return

    for filename in os.listdir(JSON_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(JSON_DIR, filename)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            market = data.get('market', 'Global')
            topic = data.get('topic', 'Enterprise AI')
            content_id = f"{market}-{topic}".strip().lower()

            # ድግግሞሽ መቆጣጠሪያ
            if is_already_published(content_id):
                print(f"⏭️ ተዘልሏል፡ {market} ቀደም ብሎ ተልኳል።")
                continue

            # ቪዲዮ መጨመሪያ (ጥራት)
            video_embed = f'<div class="wp-video"><iframe src="https://www.youtube.com/embed?listType=search&list=AI+Wealth+{market}" width="100%" height="400"></iframe></div>'
            full_content = video_embed + data.get('content', '')

            payload = {
                "title": f"Enterprise AI Strategy 2026: {market} Edition",
                "content": full_content,
                "status": "publish"
            }

            response = requests.post(
                f"{wp_url}/wp-json/wp/v2/posts",
                auth=(wp_user, wp_pass),
                json=payload
            )

            if response.status_code == 201:
                print(f"✅ ተሳክቷል፡ {market} ወደ WordPress ተልኳል።")
                mark_as_published(content_id)
            else:
                print(f"❌ ስህተት ለ {market}: {response.status_code}")

if __name__ == "__main__":
    push_to_wordpress()
