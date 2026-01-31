#!/usr/bin/env python3
import asyncio
import os
import requests
import logging
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FullMaster")

class UltimateDiamondSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.yt_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    async def run(self, topic):
        # 1. መጀመሪያ ቪዲዮ መፈለግ
        video_data = await self.yt_hunter.find_relevant_videos(topic, 'US')
        video_html = ""
        if video_data:
            v_id = video_data[0]['video_id']
            video_html = f'<iframe width="100%" height="450" src="https://www.youtube.com/embed/{v_id}" frameborder="0" allowfullscreen style="border-radius:15px; margin-bottom:20px;"></iframe>'

        # 2. ረጅም ጽሁፍ ማመንጨት
        prompt = f"Write a comprehensive 1200-word deep-dive guide on {topic}. Include historical context, step-by-step strategies, and future predictions. Use many headings."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Loading knowledge...")

        # 3. ሙሉ ጽሁፉን የሚያነብ JavaScript (TTS)
        # ይህ ኮድ ድረ-ገጹ ላይ "Read Article" የሚል በተን ይፈጥራል
        audio_script = '''
        <div style="background:#fef3c7; padding:15px; border-radius:10px; margin-bottom:20px; text-align:center; border:2px solid #d97706;">
            <button onclick="readArticle()" style="background:#d97706; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer; font-weight:bold;">🔊 ሙሉውን ጽሁፍ አምብብልኝ (Play Audio)</button>
            <script>
                function readArticle() {
                    const text = document.getElementById('article-content').innerText;
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'en-US';
                    utterance.rate = 0.9;
                    window.speechSynthesis.speak(utterance);
                }
            </script>
        </div>
        '''

        # 4. Vintage Layout + Functional Diamond
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/"
        
        final_layout = f'''
        <div style="background-color: #fdf6e3; padding: 40px; border: 8px double #5d4037; font-family: 'Georgia', serif; color: #2d241e;">
            <h1 style="text-align:center; font-size:38px;">{topic}</h1>
            {video_html}
            {audio_script}
            
            <div id="article-content" style="font-size:20px; line-height:1.8; text-align:justify;">
                {text}
            </div>

            <div style="margin-top:50px; text-align:center; background:#1e293b; padding:30px; border-radius:20px;">
                <h2 style="color:#38bdf8;">💎 እድለኛ ነዎት!</h2>
                <p style="color:white;">ይህንን አልማዝ በመንካት የዛሬውን ትልቅ ቅናሽ ያግኙ።</p>
                <a href="{affiliate_link}" target="_blank" style="font-size:100px; text-decoration:none; display:inline-block; animation: pulse 1.5s infinite;">💎</a>
            </div>
        </div>
        '''

        # 5. WordPress Publish
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {'title': f"Premium Guide: {topic}", 'content': final_layout, 'status': 'publish'}
        
        requests.post(f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts", json=payload, auth=auth)
        logger.info("✅ Full Masterpiece with Video & Audio Published!")

if __name__ == "__main__":
    asyncio.run(UltimateDiamondSystem().run("Artificial Intelligence in Business"))
