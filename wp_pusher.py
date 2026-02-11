import os
import json
import requests
from base64 import b64encode

# ⚙️ የ WordPress መረጃዎች ከ Secrets
WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USERNAME')
WP_PASS = os.getenv('WP_PASSWORD')

# 🎯 ፋይሎቹ ያሉበት ትክክለኛ ቦታ
TARGET_PATH = "enterprise_exports/wordpress"

def push_to_wordpress(title, content):
    if not WP_URL or not WP_USER or not WP_PASS:
        print("❌ ስህተት፡ Secrets አልተገኙም!")
        return False

    clean_url = WP_URL.strip('/')
    wp_auth = b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {wp_auth}',
        'Content-Type': 'application/json'
    }
    
    # ጽሁፉን በሚያምር ሁኔታ ለማቅረብ (HTML Formatting)
    formatted_content = f"\n{content}"
    
    post_data = {
        'title': title,
        'content': formatted_content,
        'status': 'publish',
        'categories': [1] # እንደ አስፈላጊነቱ የካቴጎሪ ID መቀየር ትችላለህ
    }
    
    try:
        url = f"{clean_url}/wp-json/wp/v2/posts"
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            print(f"✅ ጋዜጣው በስኬት ተጭኗል: {title}")
            return True
        else:
            print(f"❌ አልተሳካም: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        return False

def start_upload():
    if not os.path.exists(TARGET_PATH):
        print(f"📂 ቦታው አልተገኘም: {TARGET_PATH}")
        return

    files = [f for f in os.listdir(TARGET_PATH) if f.startswith('production_enterprise')]
    print(f"📝 {len(files)} ፋይሎች ተገኝተዋል፣ ትልቁን ጽሁፍ መፈለግ ጀምሬያለሁ...")

    for file_name in files:
        file_path = os.path.join(TARGET_PATH, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # 1. ርዕሱን ሀገር-ተኮር ማድረግ
                country = data.get('target_country', 'Global')
                topic = data.get('topic', 'AI Strategy')
                title = f"{topic} - {country} Edition (2026)"

                # 2. ትልቁን ጽሁፍ ብቻ መለየት (Logic)
                # 'full_content' ወይም 'article_body' ውስጥ ያለውን 14k ቃል ይወስዳል
                main_article = data.get('full_content') or data.get('article_body') or data.get('content')
                
                # ይዘቱ ከ 3000 ቃላት በላይ ከሆነ ብቻ እንዲጭን (አጭር ሪፖርት ከሆነ ይዘለዋል)
                if main_article and len(str(main_article)) > 3000:
                    push_to_wordpress(title, main_article)
                else:
                    print(f"⏭️ {file_name} አጭር ሪፖርት ስለሆነ ተዘሏል።")
                    
            except Exception as e:
                print(f"⚠️ ስህተት በፋይሉ ላይ {file_name}: {str(e)}")

if __name__ == "__main__":
    start_upload()
