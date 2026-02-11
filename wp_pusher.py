import os
import json
import requests
from base64 import b64encode

# ⚙️ በፎቶው መሰረት ትክክለኛው የ Secret ስሞች
WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USERNAME')
WP_PASS = os.getenv('WP_PASSWORD')

# 🎯 ፋይሎቹ ያሉበት ትክክለኛ ቦታ
TARGET_PATH = "enterprise_exports/wordpress"

def push_to_wordpress(title, content):
    if not WP_URL or not WP_USER or not WP_PASS:
        print("❌ ስህተት፡ WordPress Secrets አልተገኙም! ስሞቹን አረጋግጥ።")
        return False

    clean_url = WP_URL.strip('/')
    wp_auth = b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'application/json'
    }
    
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    
    try:
        url = f"{clean_url}/wp-json/wp/v2/posts"
        print(f"🚀 በመጫን ላይ፡ {url}")
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            print(f"✅ በስኬት ተጭኗል: {title}")
            return True
        else:
            print(f"❌ አልተሳካም {title}: {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        return False

def start_upload():
    if not os.path.exists(TARGET_PATH):
        print(f"📂 ቦታው አልተገኘም: {TARGET_PATH}")
        return

    files = [f for f in os.listdir(TARGET_PATH) if f.startswith('production_enterprise')]
    print(f"📝 {len(files)} ፋይሎች ተገኝተዋል...")

    for file_name in files:
        file_path = os.path.join(TARGET_PATH, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                title = data.get('title') or data.get('target_country') or file_name
                content = data.get('content') or data.get('full_report')
                
                if content:
                    push_to_wordpress(title, content)
            except Exception as e:
                print(f"⚠️ ስህተት በፋይሉ ላይ {file_name}: {str(e)}")

if __name__ == "__main__":
    start_upload()
