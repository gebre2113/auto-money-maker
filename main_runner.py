#!/usr/bin/env python3
import asyncio
import logging
import argparse
import time
import json
import os
import requests

# Import from other modules
from profit_core import PremiumConfig, AdvancedAIContentGenerator, CulturalAnthropologistEngine
from profit_monetization import UltraAffiliateManager, VideoAffiliateIntegrationEngine, YouTubeIntelligenceHunterPro

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProfitMasterElite")

class UltimateProfitMasterEliteSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.cultural_engine = CulturalAnthropologistEngine(self.config)
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)
        self.affiliate_manager = UltraAffiliateManager(user_geo=self.config.default_country)
        self.video_integrator = VideoAffiliateIntegrationEngine(enable_ethical_mode=True)

    def send_to_telegram(self, topic, content, revenue, link):
        """መረጃውን ወደ ቴሌግራም ቦት ይልካል"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id: return

        message = (
            f"🚀 <b>Profit Master Elite - LIVE RUN</b>\n\n"
            f"🎯 <b>ርዕስ:</b> {topic}\n"
            f"💰 <b>የሚጠበቅ ገቢ:</b> ${revenue}\n"
            f"🔗 <b>የሽያጭ ሊንክ:</b> {link}\n\n"
            f"✅ <i>ይዘቱ በ WordPress ላይ ታትሟል።</i>"
        )
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
            logger.info("✅ Telegram notification sent!")
        except Exception as e:
            logger.error(f"❌ Telegram Error: {e}")

    def send_to_wordpress(self, title, content):
        """ይዘቱን ወደ ዎርድፕረስ ይልካል"""
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')

        if not all([wp_url, wp_user, wp_pass]): return

        payload = {'title': title, 'content': content, 'status': 'publish'} # በቀጥታ እንዲወጣ 'publish' አድርጌዋለሁ
        try:
            url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
            requests.post(url, json=payload, auth=(wp_user, wp_pass))
            logger.info("✅ WordPress Post Published!")
        except Exception as e:
            logger.error(f"❌ WP Error: {e}")

    async def run(self, topic, country, language):
        logger.info(f"🚀 Execution Started: {topic}")
        
        # 1. AI Content Generation
        content_package = await self.ai_generator.generate_premium_content(topic, language)
        raw_text = content_package.get('content')
        
        if not raw_text or raw_text == "None":
            raw_text = f"<h2>Strategic Insights: {topic}</h2><p>Exploring the future of business through {topic}.</p>"

        # 2. Affiliate Link Injection (የሙከራ ሊንክ)
        # እዚህ ጋር የምንጠቀመው የሙከራ ሊንክ ነው
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/" 
        monetized_text = raw_text + f'<br><br><div style="padding:20px; background:#f0f9ff; border-radius:10px; border:1px solid #0ea5e9;">' \
                                    f'<h3>🚀 Recommended Tool for {topic}</h3>' \
                                    f'<p>Start your business today with our top-rated platform.</p>' \
                                    f'<a href="{affiliate_link}" style="background:#0ea5e9; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Get Started Now</a>' \
                                    f'</div>'

        # 3. Report Generation
        report = {"predicted_revenue": "65.00"} # ለሙከራ $65 ገቢ ብለነዋል

        # 4. Deployment
        self.send_to_wordpress(f"Master Guide: {topic}", monetized_text)
        self.send_to_telegram(topic, monetized_text, report['predicted_revenue'], affiliate_link)

        return {'content': monetized_text, 'report': report}

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, required=True)
    args = parser.parse_args()
    
    system = UltimateProfitMasterEliteSystem()
    await system.run(args.topic, 'US', 'en')

if __name__ == "__main__":
    asyncio.run(main())
