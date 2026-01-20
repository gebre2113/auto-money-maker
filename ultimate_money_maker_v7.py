import os
import json
import time
from datetime import datetime
import requests
from google import genai
from google.genai import types

class UltimateMoneyMaker:
    def __init__(self):
        print("="*80)
        print("🏆 ULTIMATE MONEY MAKER v7.0 - ENTERPRISE AUTO-PILOT (REPAIRED)")
        print("="*80)
        
        # Configuration from Environment Variables
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.wp_url = os.getenv('WP_URL', '').rstrip('/')
        self.wp_user = os.getenv('WP_USERNAME')
        self.wp_password = os.getenv('WP_PASSWORD')
        self.tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.tg_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        self.available_models = []
        self.client = None
        self.initialize_systems()

    def initialize_systems(self):
        """Initialize all integrations"""
        print("\n🚀 Initializing Enterprise Orchestrator PRO...")
        
        # 1. Initialize Gemini Client (New 2026 SDK)
        try:
            if self.api_key:
                self.client = genai.Client(api_key=self.api_key)
                print("✅ Gemini AI Client initialized")
                self._test_model_availability()
            else:
                print("❌ Gemini API Key missing")
        except Exception as e:
            print(f"⚠️ Gemini Init Failed: {e}")

        # 2. WordPress Check
        if self.wp_url and self.wp_password:
            print("✅ WordPress configuration detected")
        else:
            print("❌ WordPress configuration missing")

    def _test_model_availability(self):
        """Test which Gemini models are available"""
        test_models = ['gemini-2.0-flash-exp', 'gemini-1.5-flash']
        for model_name in test_models:
            try:
                # New SDK syntax for 2026
                response = self.client.models.generate_content(
                    model=model_name, 
                    contents="Hi"
                )
                if response:
                    self.available_models.append(model_name)
                    print(f"✅ {model_name}: Available")
                    break
            except Exception as e:
                print(f"❌ {model_name} failed: {str(e)[:50]}")

    def generate_content(self, topic):
        """Generate high-quality SEO article"""
        if not self.available_models:
            return self._get_fallback_content(topic)
            
        prompt = f"""
        Write a professional, high-quality SEO blog post about: {topic}.
        Include:
        - Engaging Title
        - Introduction
        - 4-5 Detailed Subheadings
        - Conclusion
        - Keywords: {topic}, automation, 2026 trends.
        Write in English, at least 800 words.
        """
        
        try:
            print(f"🤖 Generating content using {self.available_models[0]}...")
            response = self.client.models.generate_content(
                model=self.available_models[0],
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return self._get_fallback_content(topic)

    def publish_to_wordpress(self, title, content):
        """Publish post to WordPress via REST API"""
        if not all([self.wp_url, self.wp_user, self.wp_password]):
            print("⚠️ WordPress credentials missing, skipping publish.")
            return False

        endpoint = f"{self.wp_url}/wp-json/wp/v2/posts"
        
        # WordPress Auth (using App Password)
        import base64
        auth_string = f"{self.wp_user}:{self.wp_password}"
        token = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json'
        }
        
        post_data = {
            'title': title,
            'content': content,
            'status': 'publish' # 'draft' for testing
        }

        for attempt in range(3):
            try:
                response = requests.post(endpoint, json=post_data, headers=headers)
                if response.status_code == 201:
                    print(f"🌐 Successfully published to WordPress: {title}")
                    return True
                else:
                    print(f"⚠️ WordPress API error ({response.status_code}): {response.text}")
                    time.sleep(2)
            except Exception as e:
                print(f"❌ WordPress Connection Error: {e}")
        return False

    def _get_fallback_content(self, topic):
        return f"<h1>{topic}</h1><p>Automatic content generation is currently in maintenance mode.</p>"

    def run_daily_cycle(self):
        topic = "The Future of AI and Automation in 2026"
        print(f"\n🎯 Starting Daily Task: {topic}")
        
        # 1. Generate
        content = self.generate_content(topic)
        
        # 2. Publish
        published = self.publish_to_wordpress(topic, content)
        
        # 3. Final Report
        print("\n" + "="*40)
        print(f"📊 Status: {'SUCCESS' if published else 'PARTIAL SUCCESS'}")
        print(f"📝 Model Used: {self.available_models[0] if self.available_models else 'None'}")
        print("="*40)

if __name__ == "__main__":
    bot = UltimateMoneyMaker()
    bot.run_daily_cycle()
