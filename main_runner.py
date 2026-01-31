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
        
        # Initialize Core Engines
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.cultural_engine = CulturalAnthropologistEngine(self.config)
        
        # Initialize Monetization Engines
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)
        self.affiliate_manager = UltraAffiliateManager(user_geo=self.config.default_country)
        self.video_integrator = VideoAffiliateIntegrationEngine(enable_ethical_mode=True)

    def send_to_telegram(self, content_data):
        """መረጃውን ወደ ቴሌግራም ቦት ይልካል"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            logger.warning("⚠️ Telegram credentials missing in Environment Variables!")
            return

        topic = content_data.get('topic', 'N/A')
        message = (
            f"🚀 <b>Profit Master Elite - New Content!</b>\n\n"
            f"📌 <b>Topic:</b> {topic}\n"
            f"✅ <b>Status:</b> Content Generated & Monetized\n"
            f"💰 <b>Predicted Revenue:</b> ${content_data.get('revenue', '0.00')}\n\n"
            f"🔗 <i>Check your WordPress dashboard for the full post.</i>"
        )
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            response = requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
            if response.status_code == 200:
                logger.info("✅ Telegram notification sent successfully!")
            else:
                logger.error(f"❌ Telegram API Error: {response.text}")
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram message: {e}")

    def send_to_wordpress(self, title, content):
        """መረጃውን ወደ ዎርድፕረስ ይልካል"""
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')

        if not all([wp_url, wp_user, wp_pass]):
            logger.warning("⚠️ WordPress credentials missing!")
            return

        auth = (wp_user, wp_pass)
        headers = {'Content-Type': 'application/json'}
        payload = {
            'title': title,
            'content': content,
            'status': 'draft'  # መጀመሪያ ገብተህ እንድታየው በ Draft መልክ ይገባል
        }

        try:
            url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
            response = requests.post(url, json=payload, auth=auth, headers=headers)
            if response.status_code == 201:
                logger.info("✅ Posted to WordPress as Draft!")
            else:
                logger.error(f"❌ WordPress API Error: {response.text}")
        except Exception as e:
            logger.error(f"❌ Failed to post to WordPress: {e}")

    async def run(self, topic, country, language):
        logger.info(f"🚀 Starting process for: {topic} ({country})")
        
        # 1. Generate Content
        content_package = await self.ai_generator.generate_premium_content(topic, language)
        raw_text = content_package.get('content', '')

        # 2. Find Videos
        videos = await self.youtube_hunter.find_relevant_videos(topic, country)
        
        # 3. Monetize
        final_content, report = await self.affiliate_manager.inject_affiliate_links(
            raw_text, topic, user_journey_stage="consideration"
        )
        
        # 4. Integrate Video Ads
        video_campaign = await self.video_integrator.create_video_affiliate_campaign(
            topic, {'name': 'Top Pick', 'link': '#'}, country
        )
        
        # 5. Deployment (መላክ)
        self.send_to_wordpress(f"Premium Guide: {topic}", final_content)
        self.send_to_telegram({
            'topic': topic,
            'revenue': report.get('predicted_revenue', '0.00')
        })

        logger.info("✅ Process Completed Successfully!")
        return {
            'content': final_content,
            'report': report,
            'video_campaign': video_campaign
        }

async def main():
    parser = argparse.ArgumentParser(description='Profit Master Elite Runner')
    parser.add_argument('--topic', type=str, required=True)
    parser.add_argument('--country', type=str, default='US')
    parser.add_argument('--lang', type=str, default='en')
    args = parser.parse_args()
    
    system = UltimateProfitMasterEliteSystem()
    result = await system.run(args.topic, args.country, args.lang)
    
    # Save output for GitHub Artifacts
    with open(f"latest_report.json", "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
