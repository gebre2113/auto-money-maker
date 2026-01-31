#!/usr/bin/env python3
import asyncio
import logging
import argparse
import time
import json
import os
import requests

# Import from other modules
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import UltraAffiliateManager, YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProfitMasterElite")

class UltimateProfitMasterEliteSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.youtube_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)
        self.affiliate_manager = UltraAffiliateManager(user_geo='US')

    def send_to_wordpress(self, title, content):
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')
        if not all([wp_url, wp_user, wp_pass]): return
        
        payload = {'title': title, 'content': content, 'status': 'publish'}
        try:
            url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
            requests.post(url, json=payload, auth=(wp_user, wp_pass))
            logger.info("✅ WordPress Post with Video Published!")
        except Exception as e:
            logger.error(f"❌ WP Error: {e}")

    async def run(self, topic, country):
        logger.info(f"🚀 Running Multimedia Engine for: {topic}")
        
        # 1. AI Content
        content_package = await self.ai_generator.generate_premium_content(topic, 'en')
        raw_text = content_package.get('content', f"Analysis on {topic}")

        # 2. YouTube Video Hunter (ቪዲዮ መፈለጊያ)
        videos = await self.youtube_hunter.find_relevant_videos(topic, country)
        video_embed = ""
        if videos and len(videos) > 0:
            video_id = videos[0].get('video_id')
            video_embed = f'<br><br><div class="video-container"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe></div><br>'
            logger.info(f"✅ Found Video ID: {video_id}")

        # 3. Monetization Link
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/"
        cta_box = f'''<div style="padding:20px; background:#f0f9ff; border:2px solid #0ea5e9; border-radius:15px; margin:20px 0;">
                        <h3>🚀 Expert Recommended for {topic}</h3>
                        <p>Get started with the best tools to scale your business.</p>
                        <a href="{affiliate_link}" style="background:#0ea5e9; color:white; padding:12px 25px; text-decoration:none; border-radius:8px; display:inline-block; font-weight:bold;">Get Started Now</a>
                     </div>'''

        # ጽሁፉን፣ ቪዲዮውን እና ሊንኩን ማዋሃድ
        final_html = f"{raw_text}{video_embed}{cta_box}"

        # 4. Deployment
        self.send_to_wordpress(f"Elite Guide: {topic}", final_html)
        
        return {"status": "Success", "video_found": bool(video_embed)}

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, required=True)
    args = parser.parse_args()
    system = UltimateProfitMasterEliteSystem()
    await system.run(args.topic, 'US')

if __name__ == "__main__":
    asyncio.run(main())
