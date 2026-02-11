import os
import json
import requests
from base64 import b64encode

# ⚙️ CONFIGURATION (ከ GitHub Secrets የሚወሰድ)
WP_URL = os.getenv('WORDPRESS_URL')
WP_USER = os.getenv('WORDPRESS_USER')
WP_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')
OUTPOST_DIR = "outpost"

def push_to_wordpress(title, content):
    """ጽሁፉን ወደ WordPress ይልካል።"""
    wp_auth = b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'application/json'
    }
    
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish'  # ወዲያውኑ እንዲታተም (ወደ 'draft' መቀየር ትችላለህ)
    }
    
    response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=headers, json=post_data)
    
    if response.status_code == 201:
        print(f"✅ Successfully posted: {title}")
        return True
    else:
        print(f"❌ Failed to post {title}: {response.text}")
        return False

def process_outpost():
    """በ outpost ውስጥ ያሉትን JSON ፋይሎች በሙሉ ያነባል"""
    if not os.path.exists(OUTPOST_DIR):
        print("📂 Outpost folder not found!")
        return

    json_files = [f for f in os.listdir(OUTPOST_DIR) if f.endswith('.json')]
    
    if not json_files:
        print("Empty folder. No JSON files to upload.")
        return

    for file_name in json_files:
        file_path = os.path.join(OUTPOST_DIR, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # በ JSON ውስጥ ያሉትን ቁልፎች (Keys) እንደ TITAN v22.0 አወቃቀር እንለይ
                title = data.get('title', file_name.replace('.json', ''))
                content = data.get('content', '') or data.get('full_report', '')
                
                if content:
                    success = push_to_wordpress(title, content)
                    if success:
                        # ከተጫነ በኋላ ፋይሉን ወደ 'uploaded' ፎልደር እናንቀሳቅሳለን
                        os.makedirs('uploaded_archive', exist_ok=True)
                        os.rename(file_path, os.path.join('uploaded_archive', file_name))
            except Exception as e:
                print(f"⚠️ Error processing {file_name}: {str(e)}")

if __name__ == "__main__":
    process_outpost()
