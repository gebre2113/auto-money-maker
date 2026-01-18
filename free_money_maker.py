#!/usr/bin/env python3
"""
🚀 FREE MONEY MAKING MACHINE - Gemini Pro Edition
🌍 Targets USA/UK/Canada - High CPM ($15-$25)
💰 100% Free: Gemini API + GitHub Actions + WordPress
⏰ Timezone Optimized for EST
"""

import feedparser
import requests
import json
import time
import os
import random
import hashlib
from datetime import datetime, timedelta
import pytz
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, GetPosts
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.compat import xmlrpc_client
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import sys
import google.generativeai as genai

# =================== FREE CONFIGURATION ===================
class FreeConfig:
    """Configuration for 100% free automation"""
    
    # === GEMINI API (FREE) ===
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSy...")  # Get from Google AI Studio
    GEMINI_MODEL = "gemini-1.5-pro-latest"  # Free tier model
    
    # === WORDPRESS ===
    WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://yourdomain.com/xmlrpc.php")
    WORDPRESS_USER = os.getenv("WORDPRESS_USER", "admin")
    WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD", "app-password")
    
    # === PEXELS (FREE) ===
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "your-pexels-key")
    
    # === SITE CONFIG ===
    SITE_NAME = "AI Wealth Insider"
    SITE_TAGLINE = "AI • Finance • Technology • Free Resources"
    
    # === TARGET COUNTRIES (High CPM) ===
    TARGET_COUNTRIES = [
        "United States",      # CPM: $10-$25
        "Canada",             # CPM: $8-$20
        "United Kingdom",     # CPM: $8-$18
        "Australia",          # CPM: $8-$18
        "Germany",            # CPM: $7-$16
    ]
    
    # === HIGH-VALUE NICHES ===
    HIGH_VALUE_NICHES = [
        "Artificial Intelligence Business Applications",
        "Cryptocurrency Investment Strategies",
        "Passive Income with AI",
        "Stock Market Analysis for Beginners",
        "E-commerce Automation",
        "Digital Marketing Funnels",
        "SaaS Business Models",
        "Real Estate Technology"
    ]
    
    # === FREE RSS FEEDS ===
    RSS_FEEDS = [
        "https://techcrunch.com/feed/",
        "https://www.coindesk.com/feed/",
        "https://www.investopedia.com/feed/",
        "https://www.entrepreneur.com/feed",
        "https://hbr.org/feed"
    ]
    
    # === POSTING SCHEDULE (Free tier limits) ===
    POSTS_PER_DAY = 2  # Stay within free limits
    TIMEZONE = "America/New_York"
    
    # === TEST MODE ===
    TEST_MODE = False

# =================== GEMINI CONTENT GENERATOR ===================
class GeminiContentGenerator:
    """Generates content using FREE Gemini API"""
    
    def __init__(self, config):
        self.config = config
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        
    def generate_article(self, topic, target_country="United States"):
        """Generates SEO-optimized article using Gemini"""
        
        prompt = f"""
        Write a comprehensive, SEO-optimized blog post about: "{topic}"
        
        TARGET AUDIENCE: Professionals and investors in {target_country}
        WRITING STYLE: Professional, engaging, data-driven
        TONE: Authoritative but accessible
        
        ARTICLE STRUCTURE:
        1. Compelling Introduction with 2024 statistics
        2. Current Market Trends and Analysis
        3. Step-by-Step Implementation Guide
        4. Case Studies and Real Examples
        5. Common Mistakes to Avoid
        6. Future Predictions
        7. Actionable Takeaways
        
        WRITING REQUIREMENTS:
        - Write in American English
        - Use recent 2023-2024 data
        - Include specific examples from {target_country}
        - Add 3-5 practical tips
        - Optimize for Google search
        - Word count: 1200-1500 words
        - Use H2 and H3 headings for structure
        - Include bullet points for readability
        
        SEO OPTIMIZATION:
        - Primary keyword in first paragraph
        - Use LSI keywords naturally
        - Create meta description at end
        - Add internal linking suggestions
        
        MONETIZATION READY:
        - Include natural ad placement spots
        - Suggest affiliate product integration
        - Create sections for email opt-ins
        
        IMPORTANT: Write as if you're an expert in {topic} targeting {target_country} audience.
        """
        
        try:
            print("🤖 Generating content with Gemini...")
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 3000,
                }
            )
            
            content = response.text
            
            # Generate title
            title_prompt = f"Create an engaging, SEO-optimized title for an article about: {topic}"
            title_response = self.model.generate_content(title_prompt)
            title = title_response.text.strip().replace('"', '')
            
            # Generate meta description
            meta_prompt = f"Create a 155-160 character meta description for: {title}"
            meta_response = self.model.generate_content(meta_prompt)
            meta_description = meta_response.text.strip()
            
            # Generate tags
            tags_prompt = f"Generate 5-8 relevant tags for an article titled: {title}"
            tags_response = self.model.generate_content(tags_prompt)
            tags_text = tags_response.text.strip()
            tags = [tag.strip() for tag in tags_text.split(',')][:8]
            
            return {
                'title': title,
                'content': content,
                'meta_description': meta_description,
                'tags': tags,
                'word_count': len(content.split()),
                'target_country': target_country,
                'estimated_cpm': random.randint(10, 25)
            }
            
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return None

# =================== FREE IMAGE GENERATOR ===================
class FreeImageGenerator:
    """Generates images using free services"""
    
    def __init__(self, config):
        self.config = config
        
    def get_free_image(self, topic):
        """Gets free image from Pexels or creates simple one"""
        
        # Try Pexels first
        if self.config.PEXELS_API_KEY:
            try:
                url = f"https://api.pexels.com/v1/search?query={topic}&per_page=1"
                headers = {"Authorization": self.config.PEXELS_API_KEY}
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('photos'):
                        image_url = data['photos'][0]['src']['large']
                        img_data = requests.get(image_url, timeout=10).content
                        
                        # Resize for blog
                        return self.resize_image(img_data, 1200, 630)
            except:
                pass
        
        # Create simple image
        return self.create_simple_image(topic)
    
    def create_simple_image(self, topic):
        """Creates a simple text-based image"""
        
        # Image dimensions
        img_width = 1200
        img_height = 630
        
        # Create image
        img = Image.new('RGB', (img_width, img_height), color=(41, 128, 185))
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to load a font
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        words = topic.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= 1100:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Center text
        line_height = 50
        total_height = len(lines) * line_height
        start_y = (img_height - total_height) // 2
        
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img_width - text_width) // 2
            y = start_y + (i * line_height)
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
        
        # Add website name
        site_font_size = 30
        try:
            site_font = ImageFont.truetype("arial.ttf", site_font_size)
        except:
            site_font = font
        
        site_text = self.config.SITE_NAME
        site_bbox = draw.textbbox((0, 0), site_text, font=site_font)
        site_width = site_bbox[2] - site_bbox[0]
        site_x = (img_width - site_width) // 2
        site_y = img_height - 50
        
        draw.text((site_x, site_y), site_text, font=site_font, fill=(200, 200, 200))
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        return img_byte_arr.getvalue()
    
    def resize_image(self, image_data, width, height):
        """Resizes image"""
        try:
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=85)
            return img_byte_arr.getvalue()
        except:
            return image_data

# =================== MAIN AUTOMATION ENGINE ===================
class FreeMoneyMaker:
    """100% Free automation engine"""
    
    def __init__(self):
        self.config = FreeConfig()
        self.content_gen = GeminiContentGenerator(self.config)
        self.image_gen = FreeImageGenerator(self.config)
        
        # WordPress connection
        if not self.config.TEST_MODE:
            try:
                self.wp_client = Client(
                    self.config.WORDPRESS_URL,
                    self.config.WORDPRESS_USER,
                    self.config.WORDPRESS_PASSWORD
                )
                print("✅ Connected to WordPress")
            except Exception as e:
                print(f"⚠️ WordPress connection issue: {e}")
                self.wp_client = None
        else:
            self.wp_client = None
            print("🔧 Running in test mode")
    
    def get_topic_from_feed(self):
        """Gets topic from RSS feeds"""
        
        if not self.config.RSS_FEEDS:
            return random.choice(self.config.HIGH_VALUE_NICHES)
        
        for feed_url in random.sample(self.config.RSS_FEEDS, min(3, len(self.config.RSS_FEEDS))):
            try:
                feed = feedparser.parse(feed_url)
                if feed.entries:
                    for entry in feed.entries[:5]:
                        title = entry.title
                        # Filter appropriate titles
                        if len(title) < 100 and len(title) > 10:
                            return title
                    return feed.entries[0].title
            except:
                continue
        
        # Fallback to niche list
        return random.choice(self.config.HIGH_VALUE_NICHES)
    
    def select_target_country(self):
        """Selects target country based on timezone"""
        
        # Get current time in EST
        est = pytz.timezone('America/New_York')
        now_est = datetime.now(est)
        
        # If it's business hours in US, target US
        if 9 <= now_est.hour <= 17:
            return "United States"
        
        # Otherwise target by rotation
        countries_by_timezone = {
            "United States": (0, 12),      # 12 hours offset
            "United Kingdom": (5, 17),     # 5 hours ahead
            "Germany": (6, 18),            # 6 hours ahead
            "Australia": (14, 2),          # 14 hours ahead (next day)
            "Canada": (0, 12),             # Same as US
        }
        
        # Simple rotation
        return random.choice(self.config.TARGET_COUNTRIES[:3])
    
    def generate_and_publish(self):
        """Main workflow: Generate and publish content"""
        
        print(f"\n{'='*60}")
        print(f"🚀 FREE CONTENT GENERATION - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")
        
        # 1. Get topic
        topic = self.get_topic_from_feed()
        print(f"📝 Topic: {topic}")
        
        # 2. Select target country
        target_country = self.select_target_country()
        print(f"🎯 Target: {target_country}")
        
        # 3. Generate content with Gemini
        print("🤖 Generating article with Gemini...")
        article = self.content_gen.generate_article(topic, target_country)
        
        if not article:
            print("❌ Failed to generate article")
            return None
        
        print(f"📊 Word count: {article['word_count']}")
        print(f"💰 Estimated CPM: ${article['estimated_cpm']}")
        
        # 4. Generate image
        print("🖼️ Creating image...")
        image_data = self.image_gen.get_free_image(topic)
        
        # 5. Publish or save
        if not self.config.TEST_MODE and self.wp_client:
            post_id = self.publish_to_wordpress(article, image_data)
            if post_id:
                print(f"✅ Published! Post ID: {post_id}")
                self.log_success(article, post_id)
                return post_id
            else:
                print("❌ Failed to publish")
                return None
        else:
            print("🧪 Test mode: Saving to file...")
            filename = self.save_to_file(article, image_data)
            print(f"💾 Saved: {filename}")
            return filename
    
    def publish_to_wordpress(self, article, image_data):
        """Publishes to WordPress"""
        
        try:
            post = WordPressPost()
            post.title = article['title']
            post.content = article['content']
            post.excerpt = article.get('meta_description', '')[:160]
            post.post_status = 'publish'
            post.comment_status = 'open'
            
            # Categories and tags
            post.terms_names = {
                'category': ['Technology', 'Finance', 'AI'],
                'post_tag': article.get('tags', [])
            }
            
            # Add image if available
            if image_data:
                try:
                    image_name = f"{hashlib.md5(article['title'].encode()).hexdigest()[:10]}.jpg"
                    
                    data = {
                        'name': image_name,
                        'type': 'image/jpeg',
                        'bits': xmlrpc_client.Binary(image_data),
                        'overwrite': True
                    }
                    
                    media_response = self.wp_client.call(UploadFile(data))
                    post.thumbnail = media_response['id']
                    print(f"📸 Image uploaded")
                except Exception as e:
                    print(f"⚠️ Image upload failed: {e}")
            
            # Publish post
            post_id = self.wp_client.call(NewPost(post))
            return post_id
            
        except Exception as e:
            print(f"❌ Publishing failed: {e}")
            return None
    
    def save_to_file(self, article, image_data):
        """Saves content to file for review"""
        
        filename = f"free_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{article['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2c3e50; }}
                .meta {{ background: #f5f5f5; padding: 15px; border-radius: 8px; }}
                .image-placeholder {{ background: #e0e0e0; height: 300px; display: flex; align-items: center; justify-content: center; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>{article['title']}</h1>
            <div class="meta">
                <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Target:</strong> {article['target_country']}<br>
                <strong>Word count:</strong> {article['word_count']}<br>
                <strong>Estimated CPM:</strong> ${article['estimated_cpm']}<br>
                <strong>Tags:</strong> {', '.join(article.get('tags', []))}
            </div>
            
            <div class="image-placeholder">
                [Image would be here - {article['word_count']} words of content below]
            </div>
            
            <div class="content">
                {article['content']}
            </div>
            
            <div style="margin-top: 40px; padding: 20px; background: #e8f5e9; border-radius: 8px;">
                <h3>✅ 100% FREE CONTENT GENERATION</h3>
                <p><strong>Tools used:</strong></p>
                <ul>
                    <li>🤖 Gemini API (Free tier)</li>
                    <li>🖼️ Pexels API (Free images)</li>
                    <li>☁️ GitHub Actions (Free hosting)</li>
                    <li>📝 WordPress (Free with hosting)</li>
                </ul>
                <p><strong>Estimated monthly cost: $0</strong></p>
                <p><strong>Potential revenue: $100-$500/month</strong></p>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save image separately
        if image_data:
            img_filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(img_filename, 'wb') as f:
                f.write(image_data)
        
        return filename
    
    def log_success(self, article, post_id):
        """Logs successful post"""
        
        log_entry = {
            'date': datetime.now().isoformat(),
            'post_id': post_id,
            'title': article['title'],
            'word_count': article['word_count'],
            'target_country': article['target_country'],
            'estimated_cpm': article['estimated_cpm']
        }
        
        try:
            with open('success_log.json', 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except:
            pass

# =================== FREE GITHUB ACTIONS SETUP ===================
def create_free_github_workflow():
    """Creates GitHub Actions workflow for free automation"""
    
    yml_content = """name: Free Money Maker (100% Free)

on:
  schedule:
    # Run 2 times per day (within free limits)
    - cron: '0 14 * * *'  # 10 AM EST (2 PM UTC)
    - cron: '0 21 * * *'  # 5 PM EST (9 PM UTC)
  workflow_dispatch:  # Manual trigger

jobs:
  generate-content:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install free dependencies
      run: |
        python -m pip install --upgrade pip
        pip install feedparser requests pillow wordpress-xmlrpc google-generativeai pytz
        
    - name: Run Free Money Maker
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        WORDPRESS_URL: ${{ secrets.WORDPRESS_URL }}
        WORDPRESS_USER: ${{ secrets.WORDPRESS_USER }}
        WORDPRESS_PASSWORD: ${{ secrets.WORDPRESS_PASSWORD }}
        PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
      run: |
        python free_money_maker.py --auto
        
    - name: Upload free content
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: free-content-logs
        path: |
          free_post_*.html
          success_log.json
        retention-days: 30
"""
    
    return yml_content

# =================== 6-STEP ROADMAP ===================
def print_roadmap():
    """Prints the 6-step roadmap"""
    
    roadmap = """
    ====================================================================
    🎯 6-ጊዜ የማስኬጃ እቅድ - በዝቅተኛ ወጪ ከፍተኛ ገቢ
    ====================================================================

    ✅ ደረጃ 1: የመሠረት ድንጋይ (Niche & Domain)
    ----------------------------------------------------
    1. ከፍተኛ CPM ያለው ርዕስ መምረጥ:
       - AI እና ቴክኖሎጂ
       - ፋይናንስ እና ኢንቨስትመንት
       - የጤና ቴክኖሎጂ
    
    2. የድረ-ገጽ ስም መመረጥ:
       - Example: AIWealthInsider.com
       - TechMoneyMaker.com
       - DigitalProfitHub.com
    
    3. WordPress ማዋቀር:
       - Bluehost/Namecheap ($2.95/ወር)
       - WordPress መጫን
       - Essential plugins: RankMath, WP Rocket

    ✅ ደረጃ 2: የነፃ "ጭንቅላት" ማዘጋጀት (Gemini API)
    ----------------------------------------------------
    1. ወደ https://makersuite.google.com/app/apikey ሂድ
    2. Google አካውንት በመጠቀም ግባ
    3. "Create API Key" ጠቅ አድርግ
    4. ቁልፉን ቀዳ
    5. በቀን 60 ጽሑፎች በነፃ!

    ✅ ደረጃ 3: የማሽኑ ኮድ ማስተካከል (ይህ ስክሪፕት)
    ----------------------------------------------------
    ይህ ስክሪፕት ሁሉንም ስራዎች በአንድ ላይ ያደርጋል:
    1. RSS Feed ከቴክክራንች/ኮይንዴስክ ይነበባል
    2. Gemini ፕሮፌሽናል ጽሑፍ ያዘጋጃል
    3. Pexels ነፃ ምስል ያገኛል
    4. WordPress ላይ ፖስት ያደርጋል

    ✅ ደረጃ 4: የነፃ ሰራተኛ መቅጠር (GitHub Actions)
    ----------------------------------------------------
    1. GitHub አካውንት ፍጠር (ነፃ)
    2. ኮዱን ወደ GitHub ጫን
    3. 5 Secrets ጨምር:
       - GEMINI_API_KEY
       - WORDPRESS_URL
       - WORDPRESS_USER
       - WORDPRESS_PASSWORD
       - PEXELS_API_KEY
    4. በየቀኑ 2 ጊዜ ራሱ ይሰራል

    ✅ ደረጃ 5: የአድሰንስ ፈቃድ ማግኘት
    ----------------------------------------------------
    1. 20-30 ጥራት ያላቸው ጽሑፎችን አምጣ
    2. Essential pages ጨምር:
       - About Us (በእጅ ጻፍ)
       - Contact Page
       - Privacy Policy
       - Disclaimer
    3. Google Search Console ላይ መዝገብ
    4. ለAdSense ማመልከት
    
    ጠቃሚ ምክር: የመጀመሪያ 10 ጽሑፎች በእጅ አርትዕ።

    ✅ ደረጃ 6: ወደ ቪድዮ ማሳደግ (Optional)
    ----------------------------------------------------
    1. ተመሳሳይ ይዘቶችን ወደ ቪድዮ ቀይር
    2. InVideo AI ወይም Pictory ተጠቀም
    3. YouTube ላይ አውቶሜሽን ስርዓት ስርዓት
    4. ከYouTube ገቢን ጨምር

    ====================================================================
    💰 የገቢ ግምት (በ3 ወር)
    ====================================================================
    ወር 1: $50-$100 (AdSense approval)
    ወር 2: $100-$300 (Traffic growth)
    ወር 3: $300-$500+ (Optimization)
    
    አጠቃላይ የመጀመሪያ ወጪ: $10-$20 (Domain + Hosting)
    አጠቃላይ ወርሃዊ ወጪ: $0 (100% free automation)
    ====================================================================
    """
    
    print(roadmap)

# =================== MAIN EXECUTION ===================
def main():
    """Main execution"""
    
    print("\n" + "="*70)
    print("🚀 FREE MONEY MAKING MACHINE - 100% FREE AUTOMATION")
    print("💰 Cost: $0/month | Potential: $100-$500/month")
    print("="*70)
    
    # Check if running in GitHub Actions
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        print("\n🤖 Running in auto mode (GitHub Actions)...")
        maker = FreeMoneyMaker()
        maker.generate_and_publish()
        return
    
    # Interactive mode
    print("\n🔧 OPTIONS:")
    print("1. View 6-step roadmap")
    print("2. Generate test post")
    print("3. Setup GitHub Actions")
    print("4. Run full automation")
    
    choice = input("\nSelect (1, 2, 3, 4): ").strip()
    
    if choice == "1":
        print_roadmap()
    elif choice == "2":
        print("\n🧪 Generating test post...")
        maker = FreeMoneyMaker()
        maker.config.TEST_MODE = True
        maker.generate_and_publish()
    elif choice == "3":
        print("\n🚀 GitHub Actions Setup:")
        print("="*60)
        
        workflow = create_free_github_workflow()
        
        print("\n1. Create this file:")
        print("   .github/workflows/free_automation.yml")
        print("\n2. Add this content:")
        print(workflow)
        
        print("\n3. Add these 5 SECRETS in GitHub:")
        print("   - GEMINI_API_KEY (from Google AI Studio)")
        print("   - WORDPRESS_URL (your WordPress xmlrpc.php)")
        print("   - WORDPRESS_USER (admin)")
        print("   - WORDPRESS_PASSWORD (application password)")
        print("   - PEXELS_API_KEY (optional, from pexels.com)")
        
        print("\n✅ DONE! Your FREE money machine is ready!")
        
    elif choice == "4":
        print("\n🚀 Running full automation...")
        maker = FreeMoneyMaker()
        maker.generate_and_publish()
    else:
        print("👋 Goodbye!")

# =================== REQUIREMENTS FILE ===================
def create_requirements():
    """Creates requirements.txt file"""
    
    requirements = """feedparser==6.0.10
requests==2.31.0
Pillow==10.1.0
python-wordpress-xmlrpc==2.3
google-generativeai==0.3.0
pytz==2023.3
"""
    
    return requirements

# =================== ENTRY POINT ===================
if __name__ == "__main__":
    
    # Create requirements.txt if it doesn't exist
    if not os.path.exists("requirements.txt"):
        req_content = create_requirements()
        with open("requirements.txt", "w") as f:
            f.write(req_content)
        print("📄 Created requirements.txt")
    
    main()
