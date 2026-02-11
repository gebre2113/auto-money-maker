import os
import json
import requests
from base64 import b64encode

# ⚙️ CONFIGURATION
WP_URL = os.getenv('WORDPRESS_URL')
WP_USER = os.getenv('WORDPRESS_USER')
WP_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')

# 🎯 በፎቶው መሰረት ትክክለኛው የፋይሎች መገኛ
TARGET_PATH = "enterprise_exports/wordpress"

def push_to_wordpress(title, content):
    wp_auth = b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
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
        response = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=headers, json=post_data)
        if response.status_code == 201:
            print(f"✅ Successfully uploaded: {title}")
            return True
        else:
            print(f"❌ Failed {title}: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        return False

def start_upload():
    if not os.path.exists(TARGET_PATH):
        print(f"📂 ስህተት: {TARGET_PATH} የሚባለው ቦታ አልተገኘም!")
        # አማራጭ ፍተሻ
        print(f"የአሁኑ ፋይሎች ዝርዝር: {os.listdir('.')}")
        return

    files = [f for f in os.listdir(TARGET_PATH) if f.startswith('production_enterprise')]
    print(f"📝 {len(files)} የሚሆኑ ፋይሎች ተገኝተዋል፣ መጫን እጀምራለሁ...")

    for file_name in files:
        file_path = os.path.join(TARGET_PATH, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # በ TITAN ፋይሎች ውስጥ ርዕሱ 'title' ወይም 'target_country' ውስጥ ሊሆን ይችላል
                title = data.get('title') or data.get('target_country') or file_name
                content = data.get('content') or data.get('full_report')
                
                if content:
                    push_to_wordpress(title, content)
                else:
                    print(f"⚠️ ፋይሉ ባዶ ነው: {file_name}")
            except Exception as e:
                print(f"⚠️ ስህተት በፋይሉ ላይ {file_name}: {str(e)}")

if __name__ == "__main__":
    start_upload()
