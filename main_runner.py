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
        
        # 1. የቪዲዮ ፍለጋ (Force Video Pull)
        video_html = ""
        try:
            video_data = await self.yt_hunter.find_relevant_videos(topic, 'US')
            if video_data:
                v_id = video_data[0]['video_id']
                video_html = f'''
                <div style="margin: 30px 0; text-align:center;">
                    <iframe width="100%" height="500" src="https://www.youtube.com/embed/{v_id}?rel=0" 
                    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen 
                    style="border: 5px solid #5d4037; border-radius:15px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);"></iframe>
                </div>'''
        except:
            video_html = ""

        # 2. የጥንታዊ ጥቅልል መጽሐፍ (Scroll Animation) እና ሙሉ ስክሪን ዲዛይን
        affiliate_link = "https://www.bluehost.com/track/habtamu_test/"
        
        full_page_html = f'''
        <div class="vintage-body" style="background-color: #2c1e12; padding: 20px; font-family: 'Georgia', serif;">
            
            <style>
                @keyframes unroll {{
                    from {{ height: 0; opacity: 0; }}
                    to {{ height: auto; opacity: 1; }}
                }}
                .scroll-container {{
                    background: #f4e4bc;
                    background-image: url('https://www.transparenttextures.com/patterns/papyros.png');
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 60px;
                    border-left: 15px solid #3e2723;
                    border-right: 15px solid #3e2723;
                    box-shadow: 0 0 50px rgba(0,0,0,0.8);
                    position: relative;
                    animation: unroll 2s ease-out;
                }}
                .audio-nav {{
                    position: sticky; top: 10px; z-index: 100;
                    background: #5d4037; color: white; padding: 15px;
                    border-radius: 50px; text-align: center; cursor: pointer;
                    margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                }}
            </style>

            <div class="scroll-container">
                <div class="audio-nav" onclick="speakAll()">
                    🔊 ሙሉውን ጽሁፍ በድምፅ ያዳምጡ (Play Full Audio)
                </div>

                <h1 style="text-align: center; color: #3e2723; font-size: 50px; text-transform: uppercase; border-bottom: 4px double #3e2723;">
                    {topic}
                </h1>

                {video_html}

                <div id="full-article" style="font-size: 22px; color: #2c1e12; line-height: 1.9; text-align: justify;">
                    [AI_CONTENT_HERE]
                </div>

                <div style="text-align: center; margin-top: 60px; border-top: 3px solid #3e2723; padding-top: 40px;">
                    <p style="font-style: italic;">ምስጢራዊው የአልማዝ ስጦታ</p>
                    <a href="{affiliate_link}" target="_blank" style="font-size: 120px; text-decoration: none; display: inline-block; animation: pulse 2s infinite;">💎</a>
                    <p style="font-weight: bold; color: #b91c1c;">"አትንከው - ከነካኸው ግን እድለኛ ነህ!"</p>
                </div>
            </div>

            <script>
                function speakAll() {{
                    window.speechSynthesis.cancel();
                    const text = document.getElementById('full-article').innerText;
                    const chunks = text.match(/.{{1,200}}/g); // ጽሁፉን በትንንሽ በመከፋፈል እንዳይቋረጥ ማድረግ
                    chunks.forEach(chunk => {{
                        const utterance = new SpeechSynthesisUtterance(chunk);
                        utterance.lang = 'en-US';
                        utterance.rate = 0.85;
                        window.speechSynthesis.speak(utterance);
                    }});
                }}
            </script>
        </div>
        '''

        # 3. AI ይዘት ማመንጨት (ረጅም ጽሁፍ)
        prompt = f"Generate a deep-dive, 1500-word historical and strategic analysis of {topic}. Use professional tone, detailed chapters, and expert insights."
        content_package = await self.ai_generator.generate_premium_content(prompt, 'en')
        text = content_package.get('content', "Writing the ancient scrolls...")
        
        # ይዘቱን ወደ ዲዛይኑ ማስገባት
        final_post = full_page_html.replace("[AI_CONTENT_HERE]", text)

        # 4. መለጠፍ
        wp_url = os.getenv('WP_URL')
        auth = (os.getenv('WP_USERNAME'), os.getenv('WP_PASSWORD'))
        payload = {{'title': f"The Eternal Guide: {topic}", 'content': final_post, 'status': 'publish'}}
        
        requests.post(f"{{wp_url.rstrip('/')}}/wp-json/wp/v2/posts", json=payload, auth=auth)
        logger.info("✅ The masterpiece is published in Full Screen Scroll format!")

if __name__ == "__main__":
    asyncio.run(UltimateVintageSystem().run("Artificial Intelligence in Business"))
