import os
import requests
import json

def push_and_cleanup():
    wp_url = os.getenv('WP_URL')
    wp_user = os.getenv('WP_USERNAME')
    wp_pass = os.getenv('WP_PASSWORD')

    # በዋናው ፎልደር ውስጥ ያሉትን JSON ፋይሎች በሙሉ መፈለግ
    files_to_send = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not files_to_send:
        print("📭 የሚላክ አዲስ ፋይል የለም። ሁሉም ተልከው ተወግደዋል!")
        return

    for filename in files_to_send:
        try:
            # 1. ፋይሉን ማንበብ
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            market = data.get('market', 'Unknown')
            print(f"📡 {market}ን ወደ ወርድፕረስ እየላኩ ነው...")

            # 2. ወደ WordPress መላክ
            payload = {
                "title": data.get('title', f"Enterprise AI Strategy 2026 - {market}"),
                "content": data.get('content', ''),
                "status": "publish"
            }

            response = requests.post(
                f"{wp_url}/wp-json/wp/v2/posts",
                auth=(wp_user, wp_pass),
                json=payload
            )

            # 3. ከተላከ በኋላ ፋይሉን ማጥፋት
            if response.status_code == 201:
                print(f"✅ {market} በተሳካ ሁኔታ ተልኳል። አሁን ፋይሉን እያጠፋሁ ነው...")
                os.remove(filename) # ፋይሉን ከ GitHub workspace ላይ ያጠፋዋል
                print(f"🗑️ ፋይሉ {filename} ተወግዷል።")
            else:
                print(f"❌ ስህተት {market}: {response.status_code} - አልተላከም፣ ፋይሉ አልጠፋም።")
                
        except Exception as e:
            print(f"⚠️ ስህተት ተከስቷል {filename}: {str(e)}")

if __name__ == "__main__":
    push_and_cleanup()
