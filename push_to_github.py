import os
import requests
import json
import base64
from pathlib import Path

# መዝገብ (ድጋሚ እንዳይላክ)
LOG_FILE = "published_history_github.log"

def is_already_published(content_id):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return content_id in f.read().splitlines()
    return False

def mark_as_published(content_id):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content_id + "\n")

def push_to_github():
    print("🚀 ወደ GitHub ዳሽቦርድ በመስቀል ላይ...")
    
    # ከ Environment Variables የ GitHub መረጃዎችን ማምጣት
    github_token = os.getenv('GITHUB_TOKEN')
    github_repo = os.getenv('GITHUB_REPO') # ምሳሌ: "habtamu/auto-money-maker"

    if not github_token or not github_repo:
        print("❌ ስህተት: GITHUB_TOKEN ወይም GITHUB_REPO አልተገኙም። እባክዎ Terminal/Environment ውስጥ ያስገቡ!")
        print("ምሳሌ Linux/Mac: export GITHUB_TOKEN='ghp_your_token_here'")
        return

    # ፋይሎችን 'enterprise_outputs' ፎልደር ውስጥ መፈለግ (የ TITAN ራነር ውጤቶች ያሉበት)
    output_dir = Path('enterprise_outputs')
    
    if not output_dir.exists():
        print("❌ ስህተት: 'enterprise_outputs' የሚባል ፎልደር አልተገኘም። እባክዎ መጀመሪያ ማምረቻ ማሽኑን (TITAN) ያስኪዱ።")
        return

    # ሁሉንም የ JSON ፋይሎች መፈለግ
    files_found = list(output_dir.glob('*.json'))
    
    if not files_found:
        print("❌ ዜሮ (0) የ JSON ፋይል ነው ያገኘሁት።")
        return

    for filepath in files_found:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # TITAN ራነሩ ውጤቱን በ 'country_results' ውስጥ ነው የሚያስቀምጠው
            results = data.get('country_results', [])
            topic_name = data.get('topic', 'Enterprise_AI').replace(' ', '_')

            if not results:
                print(f"⚠️ ፋይል {filepath.name} ውስጥ 'country_results' አልተገኘም፣ ዘለልኩት።")
                continue

            for item in results:
                # ገና ያልተጠናቀቀ ወይም ባዶ ከሆነ ዝለለው
                if not isinstance(item, dict) or item.get('status') != 'completed':
                    continue

                market = item.get('country', 'Global')
                html_content = item.get('content', '')
                
                if not html_content:
                    continue

                content_id = f"{market}-{topic_name}".strip().lower()

                # ድግግሞሽ መቆጣጠሪያ
                if is_already_published(content_id):
                    print(f"⏭️ {market} ቀደም ብሎ ወደ GitHub ተልኳል፣ ዘለልኩት።")
                    continue

                # የፋይል ስም በ GitHub ላይ (ለምሳሌ: US_Enterprise_AI.html)
                file_name = f"{market}_{topic_name[:15]}.html"
                file_path = f"published_pages/{file_name}" # GitHub ላይ የሚቀመጥበት ፎልደር
                
                # 1. ጽሑፉን ወደ Base64 መቀየር (GitHub API ስለሚፈልገው)
                encoded_content = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

                # 2. GitHub API URL
                url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"
                
                headers = {
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }

                payload = {
                    "message": f"🚀 Add {market} HTML presentation for {topic_name}",
                    "content": encoded_content,
                    "branch": "main" # ወይም የፕሮጀክትህ ዋና ብራንች ስም
                }

                # ፋይሉ ቀድሞ ካለ ለማደስ (Update) SHA መጠየቅ ያስፈልጋል
                get_resp = requests.get(url, headers=headers)
                if get_resp.status_code == 200:
                    payload["sha"] = get_resp.json()["sha"]
                    payload["message"] = f"🔄 Update {market} HTML presentation"

                # ወደ GitHub መግፋት (Push)
                response = requests.put(url, headers=headers, json=payload)

                if response.status_code in [200, 201]:
                    # የ GitHub Pages ሊንክን ማሳየት
                    username = github_repo.split('/')[0]
                    repo_name = github_repo.split('/')[1]
                    live_link = f"https://{username}.github.io/{repo_name}/{file_path}"
                    
                    print(f"\n✅ ተሳክቷል፡ {market} ወደ GitHub ተሰቅሏል!")
                    print(f"🔗 ለማየት እዚህ ይጫኑ (Link): {live_link}\n")
                    mark_as_published(content_id)
                else:
                    print(f"❌ ስህተት ለ {market}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ ፋይሉን ማንበብ ወይም መላክ አልተቻለም {filepath.name}: {str(e)}")

if __name__ == "__main__":
    push_to_github()
