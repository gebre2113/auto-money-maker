import os
import requests
from datetime import datetime

# የተላኩ ፖስቶችን መመዝገቢያ (GitHub ላይ አብሮ ይቀመጣል)
LOG_FILE = "published_history.log"

def is_already_published(market, topic):
    """ይህ ፖስት ቀደም ብሎ መላኩን ያረጋግጣል"""
    post_id = f"{market}-{topic}".strip().lower()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            if post_id in f.read().splitlines():
                return True
    return False

def mark_as_published(market, topic):
    """የተላከውን ፖስት በመዝገብ ላይ ያሰፍራል"""
    post_id = f"{market}-{topic}".strip().lower()
    with open(LOG_FILE, "a") as f:
        f.write(post_id + "\n")

def push_to_wordpress(market, topic, content, wp_url, wp_user, wp_app_pass):
    """ጥራት ያለው ይዘት ብቻ ወደ ወርድፕረስ ይልካል"""
    
    # 1. መጀመሪያ ድግግሞሽ መኖሩን አረጋግጥ
    if is_already_published(market, topic):
        print(f"⚠️ ዝለል፡ {market} - {topic} ቀደም ብሎ ተልኳል!")
        return False

    print(f"📡 አዲስ ይዘት ወደ ወርድፕረስ እየተላከ ነው: {market}...")

    # 2. የቪዲዮ እና የዲዛይን ማስተካከያ (ጥራት)
    # ማሳሰቢያ፡ content ውስጥ [VIDEO_HERE] የሚል ቦታ ካለ በቪዲዮ ይተካዋል
    video_code = f'<div class="wp-block-embed is-type-video"><iframe src="https://www.youtube.com/embed?listType=search&list=AI+Wealth+{market}" width="560" height="315" frameborder="0" allowfullscreen></iframe></div>'
    final_content = content.replace("[VIDEO_HERE]", video_code)

    # 3. WordPress API Payload
    payload = {
        "title": f"Enterprise AI Implementation Strategies 2026 for {market}",
        "content": final_content,
        "status": "publish",
        "categories": [1], # እንደፈለግክ ቀይረው
        "format": "standard"
    }

    # 4. መላክ
    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/posts",
        auth=(wp_user, wp_app_pass),
        json=payload
    )

    if response.status_code == 201:
        print(f"✅ በተሳካ ሁኔታ ተለጠፈ፡ {market}")
        mark_as_published(market, topic) # ድጋሚ እንዳይላክ መዝግብ
        return True
    else:
        print(f"❌ ስህተት፡ {response.status_code} - {response.text}")
        return False
