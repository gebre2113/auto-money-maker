import os
import json
import requests
from base64 import b64encode

# ⚙️ CONFIGURATION
WP_URL = os.getenv('WORDPRESS_URL')
WP_USER = os.getenv('WORDPRESS_USER')
WP_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')

# ፎቶው ላይ ያየናቸው ዋና ዋና ፎልደሮች ዝርዝር
POSSIBLE_DIRS = ["enterprise_outputs", "enterprise_exports", "outputs", "outpost"]

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
            print(f"✅ በስኬት ተጭኗል: {title}")
            return True
        else:
            print(f"❌ ስህተት ተፈጥሯል {title}: {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        return False

def process_all_folders():
    found_any = False
    for folder in POSSIBLE_DIRS:
        if os.path.exists(folder):
            print(f"📂 አሁን እዚህ ፎልደር ውስጥ እየፈለግኩ ነው: {folder}")
            json_files = [f for f in os.listdir(folder) if f.endswith('.json')]
            
            for file_name in json_files:
                found_any = True
                file_path = os.path.join(folder, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        # የፋይሉን ይዘት መለየት
                        title = data.get('title') or data.get('target_country') or file_name
                        content = data.get('content') or data.get('full_report') or data.get('html_content')
                        
                        if content:
                            if push_to_wordpress(title, content):
                                # ከተጫነ በኋላ ፋይሉን ለማስታወሻነት ስም መቀየር
                                print(f"--- {file_name} ተጠናቀቀ ---")
                    except Exception as e:
                        print(f"⚠️ ፋይሉን ማንበብ አልተቻለም {file_name}: {str(e)}")
        else:
            print(f"🔍 {folder} የሚባል ፎልደር አልተገኘም፣ ወደ ቀጣዩ እሄዳለሁ...")

    if not found_any:
        print("❗ ምንም አይነት የ JSON ፋይል በየትኛውም ፎልደር ውስጥ አልተገኘም!")

if __name__ == "__main__":
    process_all_folders()
