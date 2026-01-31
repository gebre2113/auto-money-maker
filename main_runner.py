#!/usr/bin/env python3
import asyncio
import os
import requests
import logging
from profit_core import PremiumConfig, AdvancedAIContentGenerator
from profit_monetization import YouTubeIntelligenceHunterPro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ScrollMaster")

class UltimateVintageSystem:
    def __init__(self):
        self.config = PremiumConfig()
        self.ai_generator = AdvancedAIContentGenerator(self.config)
        self.yt_hunter = YouTubeIntelligenceHunterPro(self.config.__dict__)

    async def run(self, topic):
        logger.info(f"📜 Creating the Great Scroll for: {topic}")
        
        # 1. የቪዲዮ ፍለጋ (Smart Search - ርዕሱን ቀለል አድርጎ በመፈለግ)
        video_html = ""
        try:
            search_query = topic.split(':')[0] # ርዕሱን አሳጥሮ መፈለግ
            video_data = await self.yt_hunter.find_relevant_videos(search_query, 'US')
            if video_data:
                v_id = video_data[0]['video_id']
                video_html = f'''
                <div style="margin: 30px 0; text-align:center;">
                    <iframe width="100%" height="550" src="https://www.youtube.com/embed/{v_id}" 
                    frameborder="0" allowfullscreen 
                    style="border: 10px solid #5d4037; border-radius:15px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);"></iframe>
                </div>'''
        except Exception as e:
            logger.warning(f"Video pull failed: {e}")

        # 2. AI ይዘት ማመንጨት (ረጅም ጽሁፍ)
        prompt = f"Write a 1500-word premium business analysis about {topic}. Use storytelling, subheadings, and bullet points. Make it professional and extensive."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Writing the ancient scrolls...")

        # 3. የጥንታዊ ጥቅልል መጽሐፍ (Full Screen Scroll) ዲዛይን
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/"
        
        final_post = f'''
        <div style="background-color: #2c1e12; padding: 40px 10px; font-family: 'Georgia', serif;">
            <style>
                .scroll-paper {{
                    background: #f4e4bc;
                    background-image: url('https://www.transparenttextures.com/patterns/papyros.png');
                    max-width: 1100px;
                    margin: 0 auto;
                    padding: 80px 50px;
                    border-left: 18px solid #3e2723;
                    border-right: 18px solid #3e2723;
                    box-shadow: 0 0 60px rgba(0,0,0,0.9);
                    border-radius: 5px;
                }}
                .audio-btn {{
                    background: #5d4037; color: #f4e4bc; padding: 20px;
                    border-radius: 50px; text-align: center; cursor: pointer;
                    margin-bottom: 30px; font-weight: bold; border: 2px solid #f4e4bc;
                }}
            </style>

            <div class="scroll-paper">
                <div class="audio-btn" onclick="startReading()">
                    🔊 ሙሉውን ጽሁፍ በድምፅ ያዳምጡ (Play Full Narration)
                </div>

                <h1 style="text-align: center; color: #3e2723; font-size: 45px; border-bottom: 5px double #3e2723; padding-bottom: 20px;">
                    {topic}
                </h1>

                {video_html}

                <div id="readable-content" style="font-size: 22px; color: #2c1e12; line-height: 2; text-align: justify;">
                    {text}
                </div>

                <div style="text-align: center; margin-top: 80px; border-top: 4px solid #3e2723; padding-top: 50px;">
                    <a href="{affiliate_link}" target="_blank" style="font-size: 130px; text-decoration: none; display: inline-block;">💎</a>
                    <h2 style="color: #b91c1c;">"አትንከው - ከነካኸው ግን ትልቅ ቅናሽ አግኝተሃል!"</h2>
                </div>
            </div>

            <script>
                function startReading() {{
                    window.speechSynthesis.cancel();
                    const text = document.getElementById('readable-content').innerText;
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'en-US';
                    utterance.rate = 0.9;
                    window.speechSynthesis.speak(utterance);
                }}
            </script>
        </div>
        '''

        # 4. WordPress Publish (Fixing the payload double braces error)
        wp_url = os.getenv('WP_URL')
        wp_user = os.getenv('WP_USERNAME')
        wp_pass = os.getenv('WP_PASSWORD')
        
        payload = {
            'title': f"✨ The Eternal Guide: {topic}",
            'content': final_post,
            'status': 'publish'
        }
        
        try:
            resp = requests.post(f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts", json=payload, auth=(wp_user, wp_pass))
            if resp.status_code in [200, 201]:
                logger.info("✅ SUCCESS: The masterpiece is live on the site!")
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    asyncio.run(UltimateVintageSystem().run("Artificial Intelligence in Business"))
