import os
import json
import requests
from base64 import b64encode

# ⚙️ WordPress Configuration
WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USERNAME')
WP_PASS = os.getenv('WP_PASSWORD')

# 🔍 በምስሉ ላይ ያየናቸው ዋና ዋና መገኛዎች
SEARCH_DIRS = ["enterprise_outputs", "enterprise_exports", "outputs"]

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
        response = requests.post(url, headers=headers, json=post_data, timeout=30)
        return response.status_code == 201
    except:
        return False

def deep_scan_and_upload():
    print("🔎 ረጃጅም ፋይሎችን ፍለጋ ተጀምሯል...")
    found_count = 0

    for base_dir in SEARCH_DIRS:
        if not os.path.exists(base_dir):
            continue
        
        # os.walk ሁሉንም ንዑስ ፎልደሮች (ምስሉ ላይ እንዳሉት) ያሰሳል
        for root, dirs, files in os.walk(base_dir):
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            # ትልቁን ጽሁፍ መለየት (full_content, body, or segments)
                            content = data.get('full_content') or data.get('content') or data.get('article_body')
                            
                            # ይዘቱ ትልቅ መሆኑን ማረጋገጫ (ከ 3000 ቁምፊ በላይ)
                            if content and len(str(content)) > 3000:
                                country = data.get('target_country', 'Global')
                                topic = data.get('topic', 'AI Analysis')
                                title = f"{topic} - {country} (Exclusive)"
                                
                                print(f"📤 በመጫን ላይ: {title} ({len(str(content))} characters)")
                                if push_to_wordpress(title, content):
                                    print(f"✅ ተሳክቷል: {title}")
                                    found_count += 1
                                else:
                                    print(f"❌ አልተሳካም: {title}")
                        except:
                            continue

    if found_count == 0:
        print("❗ ምንም አይነት ረጅም ፋይል አልተገኘም። ፋይሎቹ በሌላ ስም ተቀምጠው ይሆን?")
    else:
        print(f"🏁 ስራው ተጠናቋል። በድምሩ {found_count} ጋዜጣዎች ተጭነዋል።")

if __name__ == "__main__":
    deep_scan_and_upload()
