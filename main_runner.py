#!/usr/bin/env python3
import asyncio
import logging
import os
import requests
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UltimateMasterpiece")

class UltimateDiamondSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    async def run(self, topic):
        # 1. AI ይዘት እና ምስል
        content_package = await self.ai_generator.generate_premium_content(topic, 'en')
        text = content_package.get('content', f"Secrets of {topic}")
        image_url = f"https://source.unsplash.com/800x400/?{topic.replace(' ', '')},tech"
        
        # 2. የዩቲዩብ ቪዲዮ
        videos = await self.youtube_hunter.find_relevant_videos(topic, 'US')
        video_html = ""
        if videos:
            video_html = f'<iframe width="100%" height="400" src="https://www.youtube.com/embed/{videos[0]["video_id"]}" frameborder="0"></iframe>'

        # 3. "ገዳይ ዳይመንድ" እና የጨዋታ ስክሪፕት (HTML/CSS/JS)
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" # እውነተኛ ሊንክህ እዚህ ይገባል
        
        diamond_game = f'''
        <div style="background:#0f172a; color:#f8fafc; padding:30px; border-radius:20px; text-align:center; border: 3px solid #38bdf8; margin:25px 0;">
            <h2 style="color:#38bdf8;">💎 የአልማዝ አደን (The Diamond Hunt)</h2>
            <p>በዚህ ገጽ ላይ የተደበቀውን <b>ሰማያዊ አልማዝ</b> ፈልገህ አግኝ! ገና እንደነካኸው ልዩ ስጦታህን ትቀበላለህ።</p>
            
            <div id="diamond-box" style="height:150px; position:relative; cursor:pointer;">
                <div onclick="window.location.href='{affiliate_link}';" 
                     style="font-size:60px; position:absolute; left:45%; animation: bounce 2s infinite; filter: drop-shadow(0 0 10px #38bdf8);">
                     💎
                </div>
            </div>
            
            <style>
                @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
            </style>
            
            <p style="font-size:14px; color:#94a3b8;">አልማዙን ነክተህ ሽልማትህን ውሰድ!</p>
        </div>
        '''

        # 4. ሙሉውን ማዋሃድ
        final_post = f"""
        <img src="{image_url}" style="width:100%; border-radius:15px; margin-bottom:20px;">
        {text}
        <hr>
        {video_html}
        {diamond_game}
        """

        # 5. WordPress ላይ መለጠፍ
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {{'title': f"🔥 {topic}: The Hidden Secrets", 'content': final_post, 'status': 'publish'}}
        requests.post(f"{{wp_url.rstrip('/')}}/wp-json/wp/v2/posts", json=payload, auth=auth)
        logger.info("✅ The Diamond Masterpiece is LIVE!")

if __name__ == "__main__":
    asyncio.run(UltimateDiamondSystem().run("Artificial Intelligence in Business"))
