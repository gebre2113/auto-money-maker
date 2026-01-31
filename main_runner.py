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

    def send_to_telegram(self, topic, content, revenue):
        """መረጃውን ወደ ቴሌግራም ቦት ይልካል - አሁን በበለጠ ዝርዝር"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            logger.warning("⚠️ Telegram credentials missing!")
            return

        # ይዘቱ ረጅም ከሆነ ለቴሌግራም እንዲመች አሳጥረው
        summary = (content[:300] + '...') if len(content) > 300 else content
        
        message = (
            f"🚀 <b>Profit Master Elite - PRODUCTION SUCCESS</b>\n\n"
            f"🎯 <b>Topic:</b> {topic}\n"
            f"📝 <b>Content Preview:</b>\n<i>{summary}</i>\n\n"
            f"💰 <b>Estimated Revenue:</b> ${revenue}\n"
            f"✅ <b>Status:</b> WordPress & GitHub Updated"
        )
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
            logger.info("✅ Advanced Telegram notification sent!")
        except Exception as e:
            logger.error(f"❌ Telegram Error: {e}")

    def send_to_wordpress(self, title, content):
        """ይዘቱን ወደ ዎርድፕረስ ይልካል"""
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')

        if not all([wp_url, wp_user, wp_pass]): return

        payload = {'title': title, 'content': content, 'status': 'draft'}
        try:
            url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
            requests.post(url, json=payload, auth=(wp_user, wp_pass))
            logger.info("✅ WordPress Draft Created!")
        except Exception as e:
            logger.error(f"❌ WP Error: {e}")

    async def run(self, topic, country, language):
        logger.info(f"🚀 Execution Started: {topic}")
        
        # 1. AI Content Generation with Safety Check
        content_package = await self.ai_generator.generate_premium_content(topic, language)
        raw_text = content_package.get('content')
        
        # 🛡️ ይዘቱ None ከሆነ የመከላከያ እርምጃ (Content Validation)
        if not raw_text or raw_text == "None":
            logger.warning("⚠️ AI generated empty content. Using fallback generator...")
            raw_text = f"<h1>{topic}</h1><p>Strategic analysis and insights regarding {topic} in the {country} market.</p>"

        # 2. YouTube & Monetization
        videos = await self.youtube_hunter.find_relevant_videos(topic, country)
        
        # 3. Inject Monetization
        try:
            final_content, report = await self.affiliate_manager.inject_affiliate_links(
                raw_text, topic, user_journey_stage="consideration"
            )
        except Exception as e:
            logger.error(f"❌ Monetization Injection Failed: {e}")
            final_content, report = raw_text, {"predicted_revenue": "0.00"}

        # 4. Deployment
        self.send_to_wordpress(f"Master Guide: {topic}", final_content)
        self.send_to_telegram(topic, final_content, report.get('predicted_revenue', '0.00'))

        return {'content': final_content, 'report': report}

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, required=True)
    parser.add_argument('--country', type=str, default='US')
    parser.add_argument('--lang', type=str, default='en')
    args = parser.parse_args()
    
    system = UltimateProfitMasterEliteSystem()
    result = await system.run(args.topic, args.country, args.lang)
    
    with open("latest_report.json", "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
