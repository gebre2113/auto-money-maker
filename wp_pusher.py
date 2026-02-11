import os
import json
import requests
from base64 import b64encode

# ⚙️ WordPress Settings
WP_URL = os.getenv('WP_URL')
WP_USER = os.getenv('WP_USERNAME')
WP_PASS = os.getenv('WP_PASSWORD')

# 🔍 ምስሉ ላይ ያየናቸው ትክክለኛ መገኛዎች
SEARCH_DIRS = ["enterprise_outputs", "enterprise_exports"]

def push_to_wordpress(title, content):
    if not WP_URL or not WP_USER or not WP_PASS: return False
    clean_url = WP_URL.strip('/')
    wp_auth = b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
    headers = {'Authorization': f'Basic {wp_auth}', 'Content-Type': 'application/json'}
    post_data = {'title': title, 'content': content, 'status': 'publish'}
    try:
        response = requests.post(f"{clean_url}/wp-json/wp/v2/posts", headers=headers, json=post_data, timeout=60)
        return response.status_code == 201
    except: return False

def aggregate_and_upload():
    print("🚜 የፋይል ክፍሎችን የመሰብሰብ ስራ ተጀምሯል...")
    
    for base_dir in SEARCH_DIRS:
        if not os.path.exists(base_dir): continue
        
        for root, dirs, files in os.walk(base_dir):
            # ፎልደሩ '_content' የሚል ስም ካለው በውስጡ ያሉትን ፋይሎች በሙሉ እናያይዛለን
            if "_content" in root and files:
                print(f"📦 በፎልደር {os.path.basename(root)} ውስጥ ያሉትን ክፍሎች እያያያዝኩ ነው...")
                full_article_parts = []
                
                # ፋይሎቹን በቅደም ተከተል እንዲቀመጡ በስማቸው Sort እናደርጋቸዋለን
                for file_name in sorted(files):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            # ፋይሉ JSON ከሆነ ይዘቱን ይወስዳል፣ ካልሆነ ግን ጥሬ ጽሁፉን ያነባል
                            file_data = f.read()
                            try:
                                json_data = json.loads(file_data)
                                part = json_data.get('content') or json_data.get('full_content') or str(json_data)
                                full_article_parts.append(str(part))
                            except:
                                full_article_parts.append(file_data)
                        except: continue
                
                if full_article_parts:
                    final_content = "\n\n".join(full_article_parts)
                    folder_id = os.path.basename(root).split('_')[1]
                    title = f"Enterprise Strategy Report: {folder_id}"
                    
                    print(f"📤 {len(full_article_parts)} ክፍሎች ተገኝተዋል። በመጫን ላይ...")
                    if push_to_wordpress(title, final_content):
                        print(f"✅ በስኬት ተጭኗል: {title}")
                    else:
                        print(f"❌ መጫን አልተቻለም: {title}")

if __name__ == "__main__":
    aggregate_and_upload()
