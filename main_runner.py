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

    def send_to_telegram(self, topic, revenue, link):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if not token or not chat_id: return
        message = f"💎 **Diamond Content Published!**\n🎯 Topic: {topic}\n💰 Est. Revenue: ${revenue}\n🔗 Link: {link}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

    async def run(self, topic):
        logger.info(f"🚀 Launching Premium Runner: {topic}")
        
        # 1. AI Content - በአጭር ነጥቦች እና ንዑስ ርዕስ እንዲሆን ታዟል
        prompt = f"Create a viral business guide about {topic}. Use professional subheadings, short paragraphs, and bullet points. Focus on high readability."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Content is being optimized...")

        # 2. የጀርባ ቀለም እና የጽሁፍ ዲዛይን (Background & Layout)
        # እዚህ ጋር ለስላሳ ግራጫ/ሰማያዊ የጀርባ ቀለም እንጠቀማለን
        image_url = f"https://images.unsplash.com/photo-1611974717528-587ce9d5d174?q=80&w=1000&auto=format&fit=crop"
        
        # 3. "አትንከው" የሚለው ገዳይ ዳይመንድ
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" # እውነተኛ ሊንክህን እዚህ ቀይረው
        
        diamond_game = f'''
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; padding: 40px; border-radius: 30px; text-align: center; border: 5px solid #38bdf8; margin: 40px 0; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
            <h2 style="color: #38bdf8; font-size: 32px; margin-bottom: 10px;">⚠️ አትንከው! (DO NOT TOUCH)</h2>
            <p style="font-size: 20px; color: #cbd5e1;">ከነካኸው ግን... ዛሬ እጅግ እድለኛው አንተ ነህ! ትልቅ ቅናሽ ይጠብቅሃል።</p>
            
            <div style="height: 200px; position: relative; margin-top: 20px; cursor: pointer;" onclick="window.open('{affiliate_link}', '_blank');">
                <div style="font-size: 80px; position: absolute; left: 42%; animation: diamond-glow 1.5s infinite ease-in-out;">
                     💎
                </div>
            </div>
            
            <style>
                @keyframes diamond-glow {{
                    0% {{ transform: scale(1); filter: drop-shadow(0 0 10px #38bdf8); }}
                    50% {{ transform: scale(1.3); filter: drop-shadow(0 0 40px #0ea5e9); }}
                    100% {{ transform: scale(1); filter: drop-shadow(0 0 10px #38bdf8); }}
                }}
            </style>
            
            <p style="background: #0ea5e9; display: inline-block; padding: 10px 20px; border-radius: 50px; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Limited Time Offer</p>
        </div>
        '''

        # 4. ሙሉውን የድረ-ገጽ ዲዛይን ማዋሃድ (Background Color Included)
        final_html = f'''
        <div style="background-color: #f8fafc; padding: 30px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #334155; border-radius: 20px;">
            <img src="{image_url}" style="width:100%; border-radius:20px; margin-bottom:30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="max-width: 800px; margin: 0 auto;">
                {text}
                <hr style="border: 0; height: 1px; background: #e2e8f0; margin: 40px 0;">
                {diamond_game}
            </div>
        </div>
        '''

        # 5. WordPress እና Telegram Deployment
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {{'title': f"✨ {topic}: The Exclusive Guide", 'content': final_html, 'status': 'publish'}}
        
        try:
            resp = requests.post(f"{{wp_url.rstrip('/')}}/wp-json/wp/v2/posts", json=payload, auth=auth)
            if resp.status_code in [200, 201]:
                logger.info("✅ Published Successfully!")
                self.send_to_telegram(topic, "85.00", affiliate_link)
        except Exception as e:
            logger.error(f"❌ Deployment failed: {{e}}")

if __name__ == "__main__":
    asyncio.run(DiamondPremiumSystem().run("Artificial Intelligence in Business"))
