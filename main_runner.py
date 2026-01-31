#!/usr/bin/env python3
import asyncio
import os
import requests
import logging
from profit_core import PremiumConfig, AdvancedAIContentGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VintageMaster")

class VintageDiamondSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)

    async def run(self, topic):
        logger.info(f"📜 Creating Vintage Masterpiece: {topic}")
        
        # 1. ረጅም እና ጥልቅ ይዘት (In-depth Content)
        prompt = f"Write an extensive, 1000-word historical and future guide about {topic}. Use storytelling, many subheadings, and detailed analysis. Make it look like a classic long-form essay."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Generating the scrolls...")

        # 2. እውነተኛ የድምፅ ማጫወቻ (Google TTS Link)
        # ጽሁፉን ወደ ድምፅ ለመቀየር የሚረዳ (ለአሁኑ በሊንክ መልክ)
        audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={topic[:50]}&tl=en&client=tw-ob"
        
        audio_html = f'''
        <div style="background:#e5e7eb; padding:20px; border: 2px solid #374151; border-radius:5px; margin-bottom:30px;">
            <p style="margin:0; font-family: 'Georgia', serif; font-weight:bold; color:#1f2937;">🎧 Listen to the Audio Version:</p>
            <audio controls style="width:100%; margin-top:10px;">
                <source src="{audio_url}" type="audio/mpeg">
            </audio>
        </div>
        '''

        # 3. የጥንታዊ (Vintage) ዲዛይን እና ዳይመንድ
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" # የእርስዎ ሊንክ
        
        classic_layout = f'''
        <div style="background-color: #fdf6e3; padding: 50px; border: 10px double #5d4037; font-family: 'Georgia', serif; color: #2d241e; line-height: 1.8; text-align: justify;">
            <h1 style="text-align: center; color: #5d4037; font-size: 36px; border-bottom: 2px solid #5d4037; padding-bottom: 10px;">{topic}</h1>
            
            {audio_html}
            
            <div style="font-size: 19px; first-letter: font-size: 50px; float: left; line-height: 1;">
                {text}
            </div>

            <div style="clear: both; margin-top: 50px; text-align: center; border-top: 2px solid #5d4037; padding-top: 30px;">
                <h3 style="color: #b91c1c;">✨ የጥንቱ ምስጢራዊ አልማዝ</h3>
                <p>ይህንን ዳይመንድ በመንካት የዛሬውን ትልቅ ቅናሽ ያግኙ። እድለኛው እርስዎ ነዎት!</p>
                <a href="{affiliate_link}" target="_blank" style="text-decoration: none; display: inline-block; font-size: 80px; animation: pulse 2s infinite;">💎</a>
            </div>
            
            <style>
                @keyframes pulse {{
                    0% {{ transform: scale(1); opacity: 0.8; }}
                    50% {{ transform: scale(1.2); opacity: 1; }}
                    100% {{ transform: scale(1); opacity: 0.8; }}
                }}
            </style>
        </div>
        '''

        # 4. WordPress ላይ መለጠፍ
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {
            'title': f"The Definitive Guide: {topic}",
            'content': classic_layout,
            'status': 'publish'
        }
        
        try:
            requests.post(f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts", json=payload, auth=auth)
            logger.info("✅ The scroll has been published!")
        except Exception as e:
            logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(VintageDiamondSystem().run("Artificial Intelligence in Business"))
