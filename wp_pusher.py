import os
import json
import requests
from base64 import b64encode

# ⚙️ የ WordPress መረጃዎች
WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USERNAME')
WP_PASS = os.getenv('WP_PASSWORD')

# 🔍 እንዲፈተሹ የፈለግካቸው ዋና ዋና ፎልደሮች
ROOT_DIRS = ["enterprise_exports", "enterprise_outputs", "production_backups", "outputs"]

def push_to_wordpress(title, content):
    if not WP_URL or not WP_USER or not WP_PASS:
        return False

    clean_url = WP_URL.strip('/')
    wp_auth = b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
    headers = {'Authorization': f'Basic {wp_auth}', 'Content-Type': 'application/json'}
    
    post_data = {
        'title': title,
        'content': content,
        'status': 'publish'
    }
    
    try:
        url = f"{clean_url}/wp-json/wp/v2/posts"
        response = requests.post(url, headers=headers, json=post_data)
        return response.status_code == 201
    except:
        return False

def scan_and_upload():
    print("🚀 ፎልደሮችን ማሰስ ተጀምሯል...")
    
    for root_folder in ROOT_DIRS:
        if not os.path.exists(root_folder):
            continue
            
        # os.walk በመጠቀም በፎልደሩ ውስጥ ያሉትን ንዑስ ፎልደሮች በሙሉ ይፈትሻል
        for root, dirs, files in os.walk(root_folder):
            print(f"📂 አሁን እዚህ ውስጥ ነኝ: {root}")
            
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            # ትልቁን ጽሁፍ መለየት
                            content = data.get('full_content') or data.get('article_body') or data.get('content')
                            
                            # ይዘቱ ከ 3000 ቃላት በላይ ከሆነ (ዋናው ጋዜጣ ከሆነ) ይጭነዋል
                            if content and len(str(content)) > 3000:
                                country = data.get('target_country', 'Global')
                                topic = data.get('topic', 'AI Update')
                                title = f"{topic} - {country}"
                                
                                if push_to_wordpress(title, content):
                                    print(f"✅ ተሳክቷል: {title}")
                                else:
                                    print(f"❌ አልተሳካም: {title}")
                            else:
                                print(f"⏭️ ተዘሏል (አጭር ነው): {file_name}")
                        except:
                            continue

if __name__ == "__main__":
    scan_and_upload()
