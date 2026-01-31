#!/usr/bin/env python3
import asyncio
import logging
import os
import requests
import json
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DiamondPremium")

class DiamondPremiumSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    def send_to_telegram(self, topic, link):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if not token or not chat_id: return
        message = f"💎 **New Post Published!**\n🎯 Topic: {topic}\n🔗 Link: {link}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

    async def run(self, topic):
        logger.info(f"🚀 Launching Premium Runner: {topic}")
        
        # 1. AI Content
        prompt = f"Create a viral business guide about {topic}. Use professional subheadings, short paragraphs, and bullet points. Focus on high readability."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Content is being optimized...")

        image_url = "https://images.unsplash.com/photo-1611974717528-587ce9d5d174?auto=format&fit=crop&w=1000"
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" 

        # 2. "አትንከው" Diamond Game
        diamond_game = f'''
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 40px; border-radius: 30px; text-align: center; border: 5px solid #38bdf8; margin: 40px 0;">
            <h2 style="color: #38bdf8; font-size: 32px;">⚠️ አትንከው! (DO NOT TOUCH)</h2>
            <p style="font-size: 20px;">ከነካኸው ግን... ዛሬ እጅግ እድለኛው አንተ ነህ! ትልቅ ቅናሽ ይጠብቅሃል።</p>
            <div style="height: 150px; position: relative; margin-top: 20px; cursor: pointer;" onclick="window.open('{affiliate_link}', '_blank');">
                <div style="font-size: 80px; position: absolute; left: 45%; animation: bounce 2s infinite;">💎</div>
            </div>
            <style>
                @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
            </style>
        </div>
        '''

        # 3. Final HTML Layout
        final_html = f'''
        <div style="background-color: #f8fafc; padding: 30px; border-radius: 20px; color: #334155;">
            <img src="{image_url}" style="width:100%; border-radius:20px; margin-bottom:30px;">
            <div style="max-width: 800px; margin: 0 auto;">
                {text}
                {diamond_game}
            </div>
        </div>
        '''

        # 4. Deployment (Payload Fix)
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')
        
        payload = {
            'title': f"✨ {topic}: Exclusive Guide",
            'content': final_html,
            'status': 'publish'
        }
        
        try:
            resp = requests.post(f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts", json=payload, auth=(wp_user, wp_pass))
            if resp.status_code in [200, 201]:
                logger.info("✅ Published Successfully!")
                self.send_to_telegram(topic, affiliate_link)
        except Exception as e:
            logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(DiamondPremiumSystem().run("Artificial Intelligence in Business"))
