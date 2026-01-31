#!/usr/bin/env python3
import asyncio
import os
import requests
import logging
import random
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExtremeMaster")

class ExtremeDiamondSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.yt_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    async def run(self, topic):
        logger.info(f"🔥 Generating Extreme Content for: {topic}")
        
        # 1. ቪዲዮ በግድ መጎተት (Advanced Video Puller)
        video_id = "vjVfS9V-4uM" # Fallback video
        try:
            v_data = await self.yt_hunter.find_relevant_videos(topic, 'US')
            if v_data: video_id = v_data[0]['video_id']
        except: pass

        # 2. እጅግ ረጅም ጽሁፍ (3000-5000 ቃላት)
        # ጽሁፉን በ 5 ክፍሎች እንከፍለዋለን (ለጥራት)
        prompt = f"""
        Act as a top business consultant. Write a 4000-word ultimate masterclass on {topic}.
        Structure it with:
        - A massive introduction
        - 10 Detailed Chapters with Subheadings
        - Case studies of major companies
        - Future predictions (2026-2035)
        - Actionable steps
        Use professional, authoritative tone. Include placeholders like [IMAGE] for me to insert photos.
        """
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Gathering deep insights...")

        # 3. ምስሎችን በመሃል ማስገባት
        random_img = "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=800"
        text = text.replace("[IMAGE]", f'<img src="{random_img}" style="width:100%; border-radius:10px; margin:20px 0;">')

        # 4. የጥንታዊ ጥቅልል ዲዛይን (The Full Scroll)
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/"
        
        final_html = f'''
        <div style="background-color: #fdf6e3; padding: 50px 20px; font-family: 'Times New Roman', serif; border: 15px solid #3e2723; line-height: 1.8;">
            
            <div style="max-width: 1000px; margin: 0 auto; background: #fffdf5; padding: 40px; box-shadow: 0 0 30px rgba(0,0,0,0.2);">
                <h1 style="text-align: center; font-size: 50px; color: #3e2723; border-bottom: 5px double #3e2723;">{topic}</h1>
                
                <div style="margin: 40px 0;">
                    <iframe width="100%" height="550" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen style="border: 10px solid #5d4037;"></iframe>
                </div>

                <div style="background: #3e2723; color: #f4e4bc; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 30px;">
                    <button onclick="readFullContent()" style="background:#f4e4bc; border:none; padding:15px 30px; font-weight:bold; cursor:pointer;">🔊 ጀምር: ሙሉውን ጽሁፍ በድምፅ ያዳምጡ</button>
                    <button onclick="window.speechSynthesis.cancel()" style="background:#ff4444; color:white; border:none; padding:15px 30px; margin-left:10px; cursor:pointer;">🛑 አቁም</button>
                </div>

                <div id="main-content" style="font-size: 22px; color: #2c1e12; text-align: justify;">
                    {text}
                </div>

                <div style="text-align: center; margin-top: 100px; padding: 50px; background: #1a1a1a; border-radius: 20px;">
                    <h2 style="color: #ffd700;">💎 ምስጢራዊው አልማዝ</h2>
                    <p style="color: white;">ይህንን በመንካት የዛሬውን ትልቅ ቅናሽ ያግኙ።</p>
                    <a href="{affiliate_link}" target="_blank" style="font-size: 150px; text-decoration: none; display: inline-block;">💎</a>
                </div>
            </div>

            <script>
                function readFullContent() {{
                    window.speechSynthesis.cancel();
                    const text = document.getElementById('main-content').innerText;
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'en-US';
                    utterance.rate = 0.9;
                    window.speechSynthesis.speak(utterance);
                }}
            </script>
        </div>
        '''

        # 5. WordPress መለጠፍ
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {'title': f"The Ultimate Scroll: {topic}", 'content': final_html, 'status': 'publish'}
        
        try:
            requests.post(f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts", json=payload, auth=auth)
            logger.info("✅ Extreme Masterpiece Published!")
        except Exception as e:
            logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(ExtremeDiamondSystem().run("Artificial Intelligence in Business"))
