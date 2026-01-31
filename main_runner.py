#!/usr/bin/env python3
import asyncio
import logging
import os
import requests
import json
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UltimateDiamondSystem")

class UltimateDiamondSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    async def run(self, topic):
        logger.info(f"🚀 Starting Diamond Production for: {topic}")
        
        # 1. AI ይዘት እና ምስል ማመንጨት
        content_package = await self.ai_generator.generate_premium_content(topic, 'en')
        text = content_package.get('content', f"Secrets of {topic}")
        image_url = f"https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1000&auto=format&fit=crop" # ቋሚ ጥራት ያለው ምስል
        
        # 2. የዩቲዩብ ቪዲዮ መፈለግ
        video_html = ""
        try:
            videos = await self.youtube_hunter.find_relevant_videos(topic, 'US')
            if videos:
                video_id = videos[0]["video_id"]
                video_html = f'<div style="margin:20px 0;"><iframe width="100%" height="400" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></div>'
        except Exception as e:
            logger.error(f"Video search failed: {e}")

        # 3. የሽያጭ ሊንክ እና "ገዳይ ዳይመንድ" ጨዋታ
        # ማስታወሻ፡ እዚህ ጋር የራስህን እውነተኛ ሊንክ መተካት ትችላለህ
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" 
        
        diamond_game = f'''
        <div style="background:#0f172a; color:#f8fafc; padding:35px; border-radius:25px; text-align:center; border: 4px solid #38bdf8; margin:30px 0; font-family: sans-serif;">
            <h2 style="color:#38bdf8; font-size:28px;">💎 The Hidden Diamond Hunt</h2>
            <p style="font-size:18px;">አስደሳች ዜና! በዚህ ገጽ ላይ የተደበቀውን <b>ሰማያዊ አልማዝ</b> ካገኘህ ልዩ ሽልማት ትቀበላለህ።</p>
            
            <div id="game-area" style="height:180px; position:relative; margin-top:20px;">
                <div onclick="window.open('{affiliate_link}', '_blank');" 
                     style="font-size:70px; position:absolute; left:45%; cursor:pointer; animation: diamond-bounce 2s infinite;">
                     💎
                </div>
            </div>
            
            <style>
                @keyframes diamond-bounce {{
                    0%, 100% {{ transform: translateY(0) scale(1); filter: drop-shadow(0 0 10px #38bdf8); }}
                    50% {{ transform: translateY(-30px) scale(1.2); filter: drop-shadow(0 0 30px #0ea5e9); }}
                }}
            </style>
            
            <p style="color:#94a3b8; font-style:italic;">አልማዙን ተጫንና ድልህን አብስር!</p>
        </div>
        '''

        # 4. ሙሉውን ይዘት ማቀናጀት
        final_post = f"""
        <div style="font-size:18px; line-height:1.8; color:#333;">
            <img src="{image_url}" style="width:100%; border-radius:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom:30px;">
            {text}
            {video_html}
            {diamond_game}
        </div>
        """

        # 5. ወደ WordPress መላክ (Payload ስህተቱ እዚህ ጋር ተስተካክሏል)
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')

        if not all([wp_url, wp_user, wp_pass]):
            logger.error("❌ WordPress Credentials missing!")
            return

        payload = {
            'title': f"🔥 {topic}: The Future is Here",
            'content': final_post,
            'status': 'publish'
        }

        try:
            response = requests.post(
                f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts",
                json=payload,
                auth=(wp_user, wp_pass)
            )
            if response.status_code in [200, 201]:
                logger.info("✅ SUCCESS: The Diamond Masterpiece is Published!")
            else:
                logger.error(f"❌ WP Error: {response.text}")
        except Exception as e:
            logger.error(f"❌ Request failed: {e}")

if __name__ == "__main__":
    # ርዕሱን እዚህ ጋር መቀየር ትችላለህ
    asyncio.run(UltimateDiamondSystem().run("Artificial Intelligence in Business"))
