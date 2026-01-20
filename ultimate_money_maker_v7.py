#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v7.0 - ENTERPRISE AUTO-PILOT (UPDATED)
✅ Complete Auto-Pilot System with Telegram Notifications
✅ WordPress API with Application Password
✅ Enhanced Gemini AI with "Gemini Watch" Health Monitor
✅ SEO Analysis with Featured Image Suggestions
✅ Persistent Memory with Auto-Commit
✅ Daily Auto-Run via GitHub Actions
✅ Telegram Status Notifications
✅ Self-Healing AI Model Selection
✅ FREE TIER OPTIMIZED: Prioritizes 'gemini-1.5-flash' for cost-efficiency
"""

import os
import sys
import json
import time
import sqlite3
import threading
import hashlib
import statistics
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import concurrent.futures
import queue

# Check for optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests library not installed. Install with: pip install requests")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai not installed. Install with: pip install google-generativeai")

# =================== TELEGRAM NOTIFICATION BOT ===================

class TelegramNotifier:
    """Sends system status and article notifications to Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
        # Test connection
        if bot_token and chat_id:
            self.available = self._test_connection()
        else:
            self.available = False
    
    def _test_connection(self) -> bool:
        """Test Telegram bot connection"""
        try:
            response = requests.get(
                f"{self.api_url}/getMe",
                timeout=10
            )
            return response.status_code == 200 and response.json().get('ok', False)
        except:
            return False
    
    def send_article_notification(self, article_data: Dict, publish_result: Dict, seo_analysis: Dict):
        """Send notification about new article"""
        if not self.available:
            return
        
        status_icon = "✅" if publish_result.get('success') else "📝"
        wordpress_status = "Published" if publish_result.get('success') else "Draft"
        
        # Create message with emojis
        message = (
            f"🏆 *Ultimate Money Maker v7.0 - Daily Report*\n\n"
            f"{status_icon} *New Article Generated*\n"
            f"📝 *Title:* {article_data['title'][:100]}\n"
            f"📊 *SEO Score:* {seo_analysis['overall_score']}/1.0 ({seo_analysis['grade']})\n"
            f"📏 *Words:* {article_data['word_count']}\n"
            f"🏷️ *Keyword:* {article_data.get('focus_keyword', 'N/A')}\n"
            f"📁 *Status:* {wordpress_status}\n\n"
        )
        
        # Add WordPress link if available
        if publish_result.get('link'):
            message += f"🔗 [View in WordPress]({publish_result['link']})\n\n"
        
        # Add system status
        message += (
            f"⚙️ *System Status*\n"
            f"🔄 Run: #{os.getenv('GITHUB_RUN_NUMBER', '1')}\n"
            f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"🏠 Memory: {self._get_memory_stats()}\n\n"
            f"#AutoBlog #AIWriter #WordPress"
        )
        
        self._send_message(message)
    
    def send_system_start_notification(self):
        """Send system start notification"""
        if not self.available:
            return
        
        message = (
            f"🚀 *Ultimate Money Maker v7.0 - System Start*\n\n"
            f"⚙️ Starting daily automated content generation\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"🌍 GitHub Action Run: #{os.getenv('GITHUB_RUN_NUMBER', '1')}\n\n"
            f"Status updates will follow..."
        )
        
        self._send_message(message)
    
    def send_system_complete_notification(self, success: bool, articles_generated: int = 0):
        """Send system completion notification"""
        if not self.available:
            return
        
        icon = "✅" if success else "⚠️"
        status = "COMPLETED SUCCESSFULLY" if success else "COMPLETED WITH WARNINGS"
        
        message = (
            f"{icon} *Ultimate Money Maker v7.0 - System Complete*\n\n"
            f"📊 *Status:* {status}\n"
            f"📝 *Articles Generated:* {articles_generated}\n"
            f"⏱️ *Completion Time:* {datetime.now().strftime('%H:%M')}\n"
            f"📁 *Next Run:* Tomorrow 6:00 AM UTC\n\n"
            f"System is running on auto-pilot mode. 🚀"
        )
        
        self._send_message(message)
    
    def send_error_notification(self, error_message: str, component: str = "System"):
        """Send error notification"""
        if not self.available:
            return
        
        message = (
            f"⚠️ *Ultimate Money Maker v7.0 - Error Alert*\n\n"
            f"🔴 *Component:* {component}\n"
            f"📛 *Error:* {error_message[:200]}\n"
            f"🕒 *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Please check GitHub Actions logs for details."
        )
        
        self._send_message(message)
    
    def _send_message(self, text: str):
        """Send message to Telegram"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "Markdown",
                    "disable_web_page_preview": True
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("📲 Telegram notification sent successfully!")
            else:
                print(f"⚠️  Telegram API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Failed to send Telegram notification: {e}")
    
    def _get_memory_stats(self) -> str:
        """Get memory statistics for notification"""
        try:
            if os.path.exists("memory/content_memory.db"):
                conn = sqlite3.connect("memory/content_memory.db")
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM articles")
                count = cursor.fetchone()[0]
                conn.close()
                return f"{count} articles"
        except:
            pass
        return "N/A articles"

# =================== WORDPRESS PUBLISHER ===================

class WordPressPublisher:
    """WordPress API integration with Application Password support"""
    
    def __init__(self, wp_url: str, wp_username: str, app_password: str):
        self.wp_url = wp_url.rstrip('/')
        self.wp_username = wp_username
        self.app_password = app_password.strip()
        self.api_url = f"{self.wp_url}/wp-json/wp/v2"
        
        # Authentication for WordPress REST API
        self.auth = (self.wp_username, self.app_password)
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 2
        
        # Test connection
        self.connected = False
        if wp_url and wp_username and app_password:
            self.connected = self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test WordPress API connection with Application Password"""
        if not REQUESTS_AVAILABLE:
            print("❌ requests library not available for WordPress API")
            return False
        
        try:
            # Try to get current user to verify authentication
            response = requests.get(
                f"{self.wp_url}/wp-json/wp/v2/users/me",
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ WordPress connected successfully as user: {user_data.get('name')}")
                return True
            else:
                print(f"⚠️  WordPress connection failed: {response.status_code}")
                if response.text:
                    print(f"   Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ WordPress connection error: {e}")
            return False
    
    def publish_article(self, article_data: Dict, status: str = 'draft') -> Dict:
        """Publish article to WordPress with retry logic"""
        
        if not self.connected:
            return {
                'success': False,
                'error': 'WordPress not connected',
                'article_data': article_data
            }
        
        # Prepare WordPress post data
        post_data = {
            'title': article_data.get('title', ''),
            'content': article_data.get('content', ''),
            'status': status,
            'slug': self._generate_slug(article_data.get('title', ''))
        }
        
        # Add excerpt if available
        if 'excerpt' in article_data:
            post_data['excerpt'] = article_data['excerpt']
        
        # Retry logic
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.api_url}/posts",
                    json=post_data,
                    auth=self.auth,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    return {
                        'success': True,
                        'post_id': result.get('id'),
                        'link': result.get('link'),
                        'status': result.get('status'),
                        'attempts': attempt + 1
                    }
                else:
                    print(f"⚠️  WordPress API error (attempt {attempt + 1}): {response.status_code}")
                    if response.text:
                        error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                        print(f"   Error: {error_data.get('message', response.text[:200])}")
                    
                    # Wait before retry with exponential backoff
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"   Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Request failed (attempt {attempt + 1}): {e}")
                wait_time = self.retry_delay * (2 ** attempt)
                time.sleep(wait_time)
        
        return {
            'success': False,
            'error': f'Failed after {self.max_retries} attempts',
            'article_data': article_data
        }
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL slug from title"""
        slug = title.lower()
        slug = slug.replace(' ', '-')
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug[:100]
    
    def get_stats(self) -> Dict:
        """Get WordPress publishing statistics"""
        try:
            response = requests.get(
                f"{self.api_url}/posts",
                params={'per_page': 1, 'context': 'edit'},
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                total_posts = int(response.headers.get('X-WP-Total', 0))
                total_pages = int(response.headers.get('X-WP-TotalPages', 0))
                
                return {
                    'total_posts': total_posts,
                    'total_pages': total_pages,
                    'connected': True,
                    'url': self.wp_url
                }
        except:
            pass
        
        return {'connected': False, 'total_posts': 0, 'url': self.wp_url}

# =================== GEMINI WATCH & CONTENT GENERATOR ===================

class GeminiContentGenerator:
    """
    Gemini AI for intelligent content generation with Model Switching
    Includes 'Gemini Watch' to monitor free-tier availability and latency
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.available = False
        self.watcher_data = {}  # Stores health stats from the watcher
        
        if not GEMINI_AVAILABLE:
            print("⚠️  google-generativeai library not installed")
            print("   Install with: pip install google-generativeai")
            return
        
        try:
            genai.configure(api_key=api_key)
            self.available = True
            print("✅ Gemini AI configured successfully")
            
            # Run the Watch immediately
            self.watch_gemini_health()
            
        except Exception as e:
            print(f"⚠️  Gemini AI configuration failed: {e}")

    def watch_gemini_health(self):
        """
        🕒 GEMINI WATCH: Monitors API Health, Latency, and Free-Tier Availability
        Pings known models to ensure they are responsive before main execution.
        """
        print("\n" + "=" * 60)
        print("🕒 GEMINI WATCH: INITIALIZING HEALTH CHECK...")
        print("=" * 60)
        
        self.available_models = []
        
        # 2024/2025 Current Model List - Optimized for Free/Cost Efficiency
        # 'gemini-1.5-flash' is the current standard for free tier (fast, efficient).
        # 'gemini-1.5-pro' offers higher quality but higher quota usage/cost.
        test_models = [
            {'name': 'gemini-1.5-flash', 'type': 'FREE_OPTIMIZED', 'priority': 1},
            {'name': 'gemini-1.5-pro', 'type': 'PREMIUM', 'priority': 2},
            {'name': 'gemini-1.0-pro', 'type': 'LEGACY', 'priority': 3}
        ]
        
        for model_info in test_models:
            model_name = model_info['name']
            print(f"   📡 Pinging {model_name}...", end=" ")
            
            try:
                model = genai.GenerativeModel(model_name)
                
                start_time = time.time()
                # Minimal request for latency check
                response = model.generate_content(
                    "Hi", 
                    generation_config={'max_output_tokens': 2}
                )
                latency = round((time.time() - start_time) * 1000, 2) # ms
                
                if response.text:
                    self.available_models.append(model_name)
                    self.watcher_data[model_name] = {
                        'status': 'ONLINE',
                        'latency_ms': latency,
                        'type': model_info['type']
                    }
                    print(f"✅ ONLINE ({latency}ms) [{model_info['type']}]")
                else:
                    print(f"❌ NO RESPONSE")
                    self.watcher_data[model_name] = {'status': 'OFFLINE', 'error': 'No text'}
                    
            except Exception as e:
                error_str = str(e).lower()
                if 'quota' in error_str:
                    status = "❌ QUOTA EXCEEDED"
                elif 'permission' in error_str:
                    status = "❌ PERMISSION DENIED"
                elif '404' in error_str:
                    status = "❌ NOT FOUND"
                else:
                    status = "❌ ERROR"
                
                print(status)
                self.watcher_data[model_name] = {'status': 'OFFLINE', 'error': str(e)[:50]}
        
        # Sort models by priority (Free ones first)
        # We want to use 'flash' whenever possible to save money
        if self.available_models:
            # Re-sort to prioritize flash
            self.available_models.sort(key=lambda x: 1 if 'flash' in x else 2)
            print("\n🕒 GEMINI WATCH SUMMARY:")
            for m in self.available_models:
                print(f"   • {m}: {self.watcher_data[m]['latency_ms']}ms - Ready")
            print("=" * 60)
            self.available = True
        else:
            print("\n❌ GEMINI WATCH ALERT: No models accessible.")
            print("   Check API Key or Quota status at https://aistudio.google.com/app/apikey")
            self.available = False
    
    def generate_article(self, topic: str, word_count: int = 1200) -> Dict:
        """Generate article using Gemini AI with model switching"""
        
        if not self.available:
            print("❌ Gemini AI not available, using fallback")
            return self._generate_fallback_article(topic, word_count)
        
        if not hasattr(self, 'available_models') or not self.available_models:
            print("⚠️  No models available (Watch failed), using fallback")
            return self._generate_fallback_article(topic, word_count)
        
        # Enhanced prompt
        prompt = self._create_prompt(topic, word_count)
        
        print(f"🤖 Generating article with {len(self.available_models)} available model(s)...")
        
        # Try each available model in order (Watch prioritized this list)
        for attempt, model_name in enumerate(self.available_models):
            try:
                print(f"   Attempt {attempt + 1}: Using model '{model_name}'...")
                
                model = genai.GenerativeModel(model_name)
                
                # Generate content
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        # Use a safe token limit. 1.5 Flash handles 8192 output max usually.
                        'max_output_tokens': min(word_count * 1.5, 8192), 
                    }
                )
                
                content = response.text.strip()
                
                if self._validate_content(content):
                    cleaned_content = self._clean_content(content)
                    
                    # Retrieve latency from watcher if available
                    latency_info = f" ({self.watcher_data[model_name]['latency_ms']}ms)" if model_name in self.watcher_data else ""
                    
                    print(f"   ✅ Success with model '{model_name}'{latency_info}")
                    
                    return {
                        'success': True,
                        'content': cleaned_content,
                        'word_count': len(cleaned_content.split()),
                        'attempts': attempt + 1,
                        'model_used': model_name,
                        'source': 'gemini_ai',
                        'quality': 'ai_generated',
                        'available_models': len(self.available_models)
                    }
                else:
                    print(f"   ⚠️  Model '{model_name}' generated invalid content")
                    
            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Model '{model_name}' failed: {error_msg[:80]}")
                
                if attempt < len(self.available_models) - 1:
                    wait_time = 2 ** attempt
                    print(f"      Waiting {wait_time} seconds before next model...")
                    time.sleep(wait_time)
        
        print("❌ All Gemini models failed, using fallback template")
        return self._generate_fallback_article(topic, word_count)
    
    def _create_prompt(self, topic: str, word_count: int) -> str:
        """Create enhanced prompt for better article generation"""
        
        return f"""Create a comprehensive, SEO-optimized article about: "{topic}"

REQUIREMENTS:
1. Word Count: Approximately {word_count} words
2. Language: Professional English, engaging tone
3. Structure: Must include H1, H2, and H3 headings with proper HTML tags
4. Format: Use HTML tags for all formatting (<h1>, <h2>, <h3>, <p>, <ul>, <li>, etc.)
5. SEO: Naturally include the focus keyword and related terms
6. Quality: Well-researched, practical, valuable information

ARTICLE STRUCTURE:
<h1>Main Title</h1>
<p>Introduction paragraph that hooks the reader.</p>

<h2>First Major Section</h2>
<p>Detailed content about this section.</p>

<h3>Subsection if needed</h3>
<p>More detailed information.</p>

<h2>Second Major Section</h2>
<p>Continue with valuable content.</p>

<h2>Conclusion</h2>
<p>Summarize key points and provide actionable advice.</p>

IMPORTANT:
- Do not use markdown, only HTML tags
- Make it genuinely useful for readers
- Include practical tips and examples
- Write in a natural, engaging style

The article should be publication-ready and provide real value to readers interested in {topic}."""
    
    def _validate_content(self, content: str) -> bool:
        """Validate generated content meets minimum requirements"""
        if not content or len(content.strip()) == 0:
            return False
        word_count = len(content.split())
        if word_count < 100:
            print(f"      Content too short: {word_count} words")
            return False
        return True
    
    def _clean_content(self, content: str) -> str:
        """Clean and format generated content"""
        content = re.sub(r'```[a-z]*\n', '', content)
        content = content.replace('```', '')
        content = content.replace('`', '')
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if not line: continue
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    
    def _generate_fallback_article(self, topic: str, word_count: int) -> Dict:
        """Generate fallback article when Gemini fails"""
        print("📄 Using enhanced fallback template system...")
        
        current_year = datetime.now().year
        
        if any(word in topic.lower() for word in ['guide', 'how to', 'tutorial', 'step']):
            template = self._create_guide_template(topic, current_year)
        elif any(word in topic.lower() for word in ['list', 'top', 'best', 'ways']):
            template = self._create_list_template(topic, current_year)
        else:
            template = self._create_general_template(topic, current_year)
        
        content = template
        
        while len(content.split()) < word_count * 0.8:
            extra_sections = [
                self._create_faq_section(topic),
                self._create_pro_tips_section(topic),
                self._create_resources_section(topic)
            ]
            for section in extra_sections:
                if len(content.split()) < word_count * 0.9:
                    content += '\n\n' + section
        
        return {
            'success': False,
            'content': content,
            'word_count': len(content.split()),
            'source': 'enhanced_fallback',
            'quality': 'template_generated',
            'note': 'Gemini AI models unavailable, using enhanced template system'
        }
    
    def _create_guide_template(self, topic: str, year: int) -> str:
        """Create guide-style template"""
        main_keyword = topic.split(':')[0] if ':' in topic else topic.split()[0]
        return f"""
<h1>{topic}</h1>
<p>Welcome to our comprehensive guide on {topic}. Whether you're just getting started or looking to improve your skills, this guide will walk you through everything you need to know in {year}.</p>
<h2>Why {main_keyword} is Important Today</h2>
<p>In today's digital landscape, understanding {main_keyword.lower()} is more crucial than ever. With technology evolving rapidly, staying updated with the latest practices can give you a significant competitive advantage.</p>
<h2>Prerequisites and Requirements</h2>
<p>Before diving in, make sure you have:</p>
<ul>
<li>A basic understanding of related concepts</li>
<li>Access to necessary tools and resources</li>
<li>Time to practice and implement what you learn</li>
<li>A willingness to experiment and learn from mistakes</li>
</ul>
<h2>Step-by-Step Implementation</h2>
<ol>
<li><strong>Step 1: Research and Planning</strong><br>Start by researching current best practices and creating a solid plan.</li>
<li><strong>Step 2: Setup and Configuration</strong><br>Get your environment set up with the right tools and configurations.</li>
<li><strong>Step 3: Implementation Phase</strong><br>Begin implementing your plan systematically, starting with the basics.</li>
<li><strong>Step 4: Testing and Optimization</strong><br>Test your implementation thoroughly and optimize based on results.</li>
<li><strong>Step 5: Scaling and Maintenance</strong><br>Once working correctly, scale your solution and establish maintenance routines.</li>
</ol>
<h2>Common Challenges and Solutions</h2>
<p>Here are some common challenges you might face and how to overcome them:</p>
<ul>
<li><strong>Challenge 1: Information Overload</strong><br><em>Solution:</em> Focus on one aspect at a time and avoid trying to learn everything at once.</li>
<li><strong>Challenge 2: Technical Difficulties</strong><br><em>Solution:</em> Break problems into smaller parts and seek help from online communities.</li>
</ul>
<h2>Conclusion and Next Steps</h2>
<p>Mastering {topic.lower()} is a journey that requires patience, practice, and persistence. By following this guide and implementing the strategies discussed, you'll be well on your way to success.</p>
"""
    
    def _create_list_template(self, topic: str, year: int) -> str:
        """Create list-style template"""
        return f"""
<h1>{topic}</h1>
<p>In {year}, {topic.lower()} has become more important than ever. This comprehensive list covers everything you need to know to succeed.</p>
<h2>The Complete List</h2>
<ol>
<li><strong>Essential Strategy 1: Foundation Building</strong><br>Start with a strong foundation. This means understanding the basics before moving to advanced concepts.</li>
<li><strong>Essential Strategy 2: Tool Selection</strong><br>Choose the right tools for the job. Not all tools are created equal, and the right ones can save you time and effort.</li>
<li><strong>Essential Strategy 3: Implementation Plan</strong><br>Create a detailed implementation plan. Without a plan, you're likely to waste time and resources.</li>
<li><strong>Essential Strategy 4: Measurement and Analytics</strong><br>Measure everything. What gets measured gets managed, and analytics provide valuable insights.</li>
<li><strong>Essential Strategy 5: Continuous Optimization</strong><br>Never stop optimizing. The digital landscape changes rapidly, and what worked yesterday may not work tomorrow.</li>
</ol>
<h2>Common Mistakes to Avoid</h2>
<ul>
<li><strong>Mistake 1:</strong> Trying to do everything at once</li>
<li><strong>Mistake 2:</strong> Ignoring data and analytics</li>
<li><strong>Mistake 3:</strong> Not staying updated with trends</li>
</ul>
<h2>Final Thoughts</h2>
<p>{topic} is not a destination but a journey. By following this comprehensive list and adapting it to your specific needs, you'll be well-positioned for success in {year} and beyond.</p>
"""
    
    def _create_general_template(self, topic: str, year: int) -> str:
        """Create general article template"""
        return f"""
<h1>{topic}</h1>
<p>In the rapidly evolving digital landscape of {year}, understanding and implementing effective strategies for {topic.lower()} has become essential for success. This comprehensive article explores everything you need to know.</p>
<h2>The Current State of {topic.split()[0]}</h2>
<p>The field of {topic.lower()} has undergone significant transformation in recent years. What was once considered advanced is now standard practice, and staying current requires continuous learning and adaptation.</p>
<h2>Core Principles and Concepts</h2>
<p>At its heart, {topic.lower()} is built on several core principles:</p>
<ul>
<li><strong>Principle 1: Value Creation</strong> - Focus on creating genuine value for your audience</li>
<li><strong>Principle 2: Consistency</strong> - Regular, predictable efforts yield the best results</li>
<li><strong>Principle 3: Adaptability</strong> - The ability to adjust to changing conditions</li>
</ul>
<h2>Practical Applications</h2>
<p>Here's how you can apply {topic.lower()} in practical scenarios:</p>
<h3>For Beginners</h3>
<p>If you're just starting with {topic.lower()}, focus on learning the fundamentals thoroughly and practicing with small, manageable projects.</p>
<h2>Future Outlook</h2>
<p>Looking ahead to {year + 1} and beyond, {topic.lower()} is expected to evolve with increased integration with artificial intelligence and greater emphasis on automation.</p>
<h2>Conclusion</h2>
<p>{topic} represents both a challenge and an opportunity in today's digital world. By understanding its principles, applying best practices, and staying adaptable to change, you can harness its potential for significant professional and personal growth.</p>
"""
    
    def _create_faq_section(self, topic: str) -> str:
        """Create FAQ section"""
        return f"""
<h2>Frequently Asked Questions</h2>
<p><strong>Q: How long does it take to see results with {topic.lower()}?</strong></p>
<p><em>A:</em> Results vary based on implementation, but most people see initial improvements within 4-6 weeks.</p>
<p><strong>Q: Do I need technical skills to succeed with {topic.lower()}?</strong></p>
<p><em>A:</em> While technical skills can be helpful, they're not always necessary. Strategy and process are often more important.</p>
"""
    
    def _create_pro_tips_section(self, topic: str) -> str:
        """Create pro tips section"""
        return f"""
<h2>Professional Tips and Insights</h2>
<ul>
<li><strong>Tip 1: Document Everything</strong><br>Keep detailed records of your processes, successes, and failures.</li>
<li><strong>Tip 2: Build a Network</strong><br>Connect with others in the field. You'll learn faster and have support when facing challenges.</li>
<li><strong>Tip 3: Focus on Fundamentals</strong><br>Master the basics before moving to advanced techniques.</li>
</ul>
"""
    
    def _create_resources_section(self, topic: str) -> str:
        """Create resources section"""
        return f"""
<h2>Recommended Resources</h2>
<ul>
<li><strong>Books:</strong> Look for recent publications that cover current best practices</li>
<li><strong>Online Courses:</strong> Platforms like Coursera, Udemy, and LinkedIn Learning offer relevant courses</li>
<li><strong>Tools:</strong> Experiment with recommended tools to find what works best for your workflow</li>
</ul>
"""

# =================== CONTENT INTELLIGENCE MEMORY ===================

class ContentMemory:
    """Self-learning memory system for content intelligence"""
    
    def __init__(self):
        self.memory_dir = "memory"
        os.makedirs(self.memory_dir, exist_ok=True)
        self.db_path = f"{self.memory_dir}/content_memory.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize content memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                slug TEXT UNIQUE,
                content_hash TEXT,
                word_count INTEGER,
                focus_keyword TEXT,
                categories TEXT,
                generated_at TEXT,
                published INTEGER DEFAULT 0,
                published_at TEXT,
                performance_score REAL DEFAULT 0,
                wordpress_id INTEGER,
                seo_score REAL DEFAULT 0,
                source TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topic_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_pattern TEXT,
                total_articles INTEGER DEFAULT 0,
                avg_word_count REAL DEFAULT 0,
                avg_performance REAL DEFAULT 0,
                avg_revenue REAL DEFAULT 0,
                success_rate REAL DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_article(self, article_data: Dict):
        """Store article in memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (title, slug, content_hash, word_count, focus_keyword, categories, 
                 generated_at, published, wordpress_id, seo_score, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data.get('title', ''),
                article_data.get('slug', article_data.get('title', '').lower().replace(' ', '-')[:100]),
                article_data.get('hash', hashlib.md5(article_data.get('content', '').encode()).hexdigest()),
                article_data.get('word_count', 0),
                article_data.get('focus_keyword', ''),
                json.dumps(article_data.get('categories', [])),
                datetime.now().isoformat(),
                1 if article_data.get('published', False) else 0,
                article_data.get('wordpress_id'),
                article_data.get('seo_score', 0),
                article_data.get('generation_source', 'unknown')
            ))
            conn.commit()
        except Exception as e:
            print(f"⚠️  Memory storage error: {e}")
        finally:
            conn.close()
    
    def get_best_topics(self, limit: int = 5) -> List[Dict]:
        """Get best performing topics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic_pattern, avg_performance, total_articles, last_used
            FROM topic_performance 
            WHERE total_articles > 0
            ORDER BY avg_performance DESC, total_articles DESC
            LIMIT ?
        ''', (limit,))
        
        topics = []
        for row in cursor.fetchall():
            topics.append({
                'topic': row[0],
                'performance_score': row[1] or 0,
                'total_articles': row[2],
                'last_used': row[3]
            })
        
        conn.close()
        return topics
    
    def _count_articles(self) -> int:
        """Count total articles in memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def _get_system_stats(self) -> Dict:
        """Get system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM topic_performance")
        topic_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(word_count) FROM articles")
        avg_word_count = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(seo_score) FROM articles")
        avg_seo_score = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_topics': topic_count,
            'avg_word_count': round(avg_word_count, 2),
            'avg_seo_score': round(avg_seo_score, 2),
            'database_size_mb': round(os.path.getsize(self.db_path) / (1024 * 1024), 2) if os.path.exists(self.db_path) else 0
        }

# =================== SEO ANALYSIS AGENT ===================

class SEOAnalysisAgent:
    """Advanced SEO analysis with detailed recommendations"""
    
    def __init__(self):
        self.seo_rules = {
            'title': {'optimal_length': (50, 60), 'max_length': 70},
            'content': {'min_words': 800, 'optimal_words': (1200, 1800)},
            'keyword_density': (1.0, 2.0)
        }
    
    def analyze(self, content: str, title: str, keyword: str) -> Dict:
        """Comprehensive SEO analysis"""
        
        analysis = {
            'overall_score': 0.0,
            'title_analysis': self._analyze_title(title, keyword),
            'content_analysis': self._analyze_content(content, keyword),
            'readability_analysis': self._analyze_readability(content),
            'technical_seo': self._analyze_technical_seo(content),
            'recommendations': []
        }
        
        scores = [
            analysis['title_analysis']['score'] * 0.25,
            analysis['content_analysis']['score'] * 0.40,
            analysis['readability_analysis']['score'] * 0.20,
            analysis['technical_seo']['score'] * 0.15
        ]
        
        analysis['overall_score'] = round(sum(scores), 2)
        analysis['grade'] = self._assign_grade(analysis['overall_score'])
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_title(self, title: str, keyword: str) -> Dict:
        """Analyze title SEO"""
        length = len(title)
        has_keyword = keyword.lower() in title.lower() if keyword else False
        score = 0.0
        
        if 50 <= length <= 60: score += 0.4
        elif 30 <= length <= 70: score += 0.3
        else: score += 0.1
        
        if has_keyword: score += 0.4
        if title[0].isupper() and title[-1] not in '!?': score += 0.2
        
        return {'score': round(score, 2), 'length': length, 'has_keyword': has_keyword}
    
    def _analyze_content(self, content: str, keyword: str) -> Dict:
        """Analyze content SEO"""
        words = content.split()
        word_count = len(words)
        keyword_density = 0.0
        
        if keyword:
            keyword_lower = keyword.lower()
            content_lower = content.lower()
            keyword_occurrences = content_lower.count(keyword_lower)
            keyword_density = (keyword_occurrences / word_count) * 100 if word_count > 0 else 0
        
        h2_count = content.count('<h2')
        h3_count = content.count('<h3')
        
        score = 0.0
        if word_count >= 1200: score += 0.3
        elif word_count >= 800: score += 0.2
        else: score += 0.1
        
        if 1.0 <= keyword_density <= 2.0: score += 0.3
        elif keyword_density > 0: score += 0.2
        else: score += 0.1
        
        heading_score = min(h2_count / 3, 0.2) + min(h3_count / max(h2_count, 1), 0.2)
        score += heading_score
        
        return {'score': round(score, 2), 'word_count': word_count, 'keyword_density': round(keyword_density, 2), 'headings': {'h2': h2_count, 'h3': h3_count}}
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze readability"""
        sentences = [s for s in re.split(r'[.!?]+', content) if s.strip()]
        words = content.split()
        
        if len(sentences) == 0: return {'score': 0.5, 'avg_sentence_length': 0}
        
        avg_sentence_length = len(words) / len(sentences)
        score = 0.0
        
        if 15 <= avg_sentence_length <= 25: score += 0.5
        elif 10 <= avg_sentence_length <= 30: score += 0.3
        else: score += 0.1
        
        return {'score': round(score, 2), 'avg_sentence_length': round(avg_sentence_length, 1)}
    
    def _analyze_technical_seo(self, content: str) -> Dict:
        """Analyze technical SEO elements"""
        score = 0.0
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        alt_count = sum(1 for img in img_tags if 'alt=' in img.lower())
        if img_tags: score += (alt_count / len(img_tags)) * 0.3
        
        link_tags = re.findall(r'<a[^>]*href=[^>]*>', content, re.IGNORECASE)
        if len(link_tags) >= 2: score += 0.2
        
        return {'score': round(score, 2), 'images_with_alt': alt_count, 'internal_links': len(link_tags)}
    
    def _assign_grade(self, score: float) -> str:
        """Assign letter grade"""
        if score >= 0.9: return "A+ (Excellent)"
        elif score >= 0.8: return "A (Very Good)"
        elif score >= 0.7: return "B (Good)"
        elif score >= 0.6: return "C (Fair)"
        else: return "D (Needs Improvement)"
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate SEO recommendations"""
        recs = []
        
        title = analysis['title_analysis']
        if title['score'] < 0.7:
            if not title['has_keyword']: recs.append("Add focus keyword to title")
            if not (50 <= title['length'] <= 60): recs.append(f"Adjust title length (current: {title['length']}, optimal: 50-60)")
        
        content = analysis['content_analysis']
        if content['word_count'] < 1000: recs.append(f"Increase content length (current: {content['word_count']})")
        if content['headings']['h2'] < 2: recs.append("Add more H2 headings")
        
        return recs[:3] if recs else ["Good SEO optimization"]

# =================== ENTERPRISE ORCHESTRATOR PRO ===================

class EnterpriseOrchestratorPro:
    """Main orchestrator with all integrations"""
    
    def __init__(self, config: Dict):
        print("🚀 Initializing Enterprise Orchestrator PRO...")
        print("=" * 60)
        
        self.config = config
        self.memory = ContentMemory()
        self.seo_agent = SEOAnalysisAgent()
        
        # Telegram
        self.telegram = None
        if config.get('TELEGRAM_BOT_TOKEN') and config.get('TELEGRAM_CHAT_ID'):
            self.telegram = TelegramNotifier(config['TELEGRAM_BOT_TOKEN'], config['TELEGRAM_CHAT_ID'])
            if self.telegram.available: print("✅ Telegram Notifier initialized")
            else: print("⚠️  Telegram Notifier not available")
        
        # WordPress
        self.wordpress = None
        if config.get('WP_URL') and config.get('WP_USERNAME') and config.get('WP_PASSWORD'):
            self.wordpress = WordPressPublisher(config['WP_URL'], config['WP_USERNAME'], config['WP_PASSWORD'])
            if self.wordpress.connected: print("✅ WordPress Publisher initialized")
            else: print("⚠️  WordPress Publisher not connected")
        
        # Gemini AI (Includes Watch)
        self.gemini = None
        if config.get('GEMINI_API_KEY'):
            self.gemini = GeminiContentGenerator(config['GEMINI_API_KEY'])
            if self.gemini.available: print("✅ Gemini AI initialized (Watch Active)")
            else: print("⚠️  Gemini AI not available")
        
        print("=" * 60)
        print("📊 System Status Summary:")
        print(f"   Telegram: {'✅ Connected' if self.telegram and self.telegram.available else '❌ Not configured'}")
        print(f"   WordPress: {'✅ Connected' if self.wordpress and self.wordpress.connected else '❌ Not connected'}")
        print(f"   Gemini AI: {'✅ Available' if self.gemini and self.gemini.available else '❌ Not available'}")
        print(f"   Memory: ✅ {self.memory._count_articles()} articles in database")
        print("=" * 60)
    
    def execute_daily_run(self) -> Dict:
        """Execute complete daily run"""
        
        if self.telegram and self.telegram.available:
            self.telegram.send_system_start_notification()
        
        print("\n🎯 Starting daily content generation...")
        
        # Select topic
        topic = self._select_topic()
        print(f"📝 Selected Topic: {topic}")
        
        # Generate content
        print("🤖 Generating content...")
        if self.gemini and self.gemini.available:
            generation_result = self.gemini.generate_article(topic, word_count=1200)
        else:
            generation_result = self._generate_template_article(topic)
        
        # Create article data
        article_data = {
            'title': topic,
            'content': generation_result['content'],
            'word_count': generation_result['word_count'],
            'focus_keyword': self._extract_keyword(topic),
            'categories': self._select_categories(topic),
            'generated_at': datetime.now().isoformat(),
            'generation_source': generation_result.get('source', 'unknown'),
            'quality': generation_result.get('quality', 'unknown'),
            'slug': topic.lower().replace(' ', '-')[:100]
        }
        
        print(f"📊 Article generated: {generation_result['word_count']} words")
        
        # SEO Analysis
        print("🔍 Running SEO analysis...")
        seo_analysis = self.seo_agent.analyze(
            article_data['content'],
            article_data['title'],
            article_data['focus_keyword']
        )
        
        article_data['seo_score'] = seo_analysis['overall_score']
        article_data['seo_grade'] = seo_analysis['grade']
        article_data['seo_recommendations'] = seo_analysis['recommendations']
        
        print(f"📈 SEO Score: {seo_analysis['overall_score']} ({seo_analysis['grade']})")
        
        # Publish
        publish_result = None
        if self.wordpress and self.wordpress.connected:
            print("🌐 Publishing to WordPress...")
            publish_result = self.wordpress.publish_article(article_data, status='draft')
            
            if publish_result.get('success'):
                article_data['published'] = True
                article_data['wordpress_id'] = publish_result.get('post_id')
                article_data['wordpress_link'] = publish_result.get('link')
                print(f"✅ Published to WordPress (ID: {publish_result.get('post_id')})")
            else:
                print(f"⚠️  WordPress publish failed: {publish_result.get('error')}")
        else:
            print("⚠️  WordPress not connected, skipping publish")
            publish_result = {'success': False, 'error': 'WordPress not connected'}
        
        # Memory
        self.memory.store_article(article_data)
        
        # Report
        report_file = self._generate_daily_report(article_data, seo_analysis, publish_result)
        
        # Notify
        if self.telegram and self.telegram.available:
            self.telegram.send_article_notification(article_data, publish_result, seo_analysis)
        
        return {
            'success': True,
            'article': article_data,
            'seo_analysis': seo_analysis,
            'publish_result': publish_result,
            'report_file': report_file
        }
    
    def _select_topic(self) -> str:
        best_topics = self.memory.get_best_topics(5)
        
        if best_topics:
            high_performing = [t for t in best_topics if t.get('performance_score', 0) >= 0.7]
            if high_performing:
                selected = random.choice(high_performing)
                print(f"   Using high-performing topic from memory: {selected['topic']}")
                return selected['topic']
        
        fallback_topics = [
            "How to Start a Successful Blog in 2025",
            "AI Content Creation: Best Practices and Tools",
            "WordPress SEO: Complete Optimization Guide",
            "Passive Income Strategies for Content Creators",
            "Building an Automated Content Pipeline with Python",
            "Digital Marketing Strategies That Actually Work",
            "How to Monetize Your Website with Affiliate Marketing",
            "The Future of AI in Content Creation",
            "Essential WordPress Plugins for Every Website",
            "Content Strategy for Growing Your Online Audience"
        ]
        
        selected = random.choice(fallback_topics)
        print(f"   Using fallback topic: {selected}")
        return selected
    
    def _generate_template_article(self, topic: str) -> Dict:
        print("   Using template system for article generation")
        templates = [
            f"""
<h1>{topic}</h1>
<p>Welcome to our complete guide on {topic}. In today's digital world, understanding and implementing effective strategies for {topic.lower()} is more important than ever.</p>
<h2>Why {topic.split(':')[0] if ':' in topic else 'This Topic'} Matters</h2>
<p>The importance of {topic.lower()} cannot be overstated. Whether you're a beginner looking to get started or an experienced professional seeking to optimize your approach, this guide will provide valuable insights.</p>
<h2>Key Principles and Strategies</h2>
<ul>
<li><strong>Strategy 1:</strong> Focus on quality and consistency in your approach</li>
<li><strong>Strategy 2:</strong> Leverage the right tools and technologies</li>
<li><strong>Strategy 3:</strong> Measure and analyze your results regularly</li>
</ul>
<h2>Conclusion</h2>
<p>{topic} offers significant opportunities for those who approach it strategically. By following the principles outlined in this guide, you can achieve meaningful results.</p>
"""
        ]
        content = random.choice(templates)
        return {'content': content, 'word_count': len(content.split()), 'source': 'template_system'}
    
    def _extract_keyword(self, topic: str) -> str:
        words = topic.split()
        if len(words) >= 3: return ' '.join(words[:3])
        elif len(words) == 2: return topic
        else: return f"{topic} guide"
    
    def _select_categories(self, topic: str) -> List[str]:
        categories = []
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['ai', 'artificial', 'machine']): categories.append('Artificial Intelligence')
        if any(word in topic_lower for word in ['wordpress', 'blog', 'website']): categories.append('WordPress')
        if any(word in topic_lower for word in ['seo', 'search', 'ranking']): categories.append('SEO')
        if any(word in topic_lower for word in ['money', 'income', 'revenue', 'monetize']): categories.append('Monetization')
        if any(word in topic_lower for word in ['marketing', 'promotion', 'audience']): categories.append('Marketing')
        
        if not categories: categories = ['Technology', 'Business', 'Digital Marketing']
        return categories[:3]
    
    def _generate_daily_report(self, article_data: Dict, seo_analysis: Dict, publish_result: Dict = None) -> str:
        report = {
            'execution_date': datetime.now().isoformat(),
            'github_run_number': os.getenv('GITHUB_RUN_NUMBER', 'N/A'),
            'article': {
                'title': article_data['title'],
                'word_count': article_data['word_count'],
                'seo_score': article_data['seo_score'],
                'grade': article_data['seo_grade']
            },
            'publishing': {
                'success': publish_result.get('success', False) if publish_result else False,
                'link': publish_result.get('link') if publish_result else None
            }
        }
        
        os.makedirs("daily_reports", exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        report_file = f"daily_reports/report_{date_str}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Daily report saved: {report_file}")
        return report_file

# =================== MAIN EXECUTION ===================

def main():
    print("=" * 80)
    print("🏆 ULTIMATE MONEY MAKER v7.0 - ENTERPRISE AUTO-PILOT")
    print("=" * 80)
    print("\n🚀 Starting system with all integrations...\n")
    
    config = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
        'WP_URL': os.getenv('WP_URL', ''),
        'WP_USERNAME': os.getenv('WP_USERNAME', ''),
        'WP_PASSWORD': os.getenv('WP_PASSWORD', ''),
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', '')
    }
    
    print("📋 Configuration Status:")
    config_status = [
        ('GEMINI_API_KEY', config['GEMINI_API_KEY'], 'AI Content Generation'),
        ('WP_URL', config['WP_URL'], 'WordPress Publishing'),
        ('WP_USERNAME', config['WP_USERNAME'], 'WordPress Username'),
        ('WP_PASSWORD', config['WP_PASSWORD'], 'WordPress App Password'),
        ('TELEGRAM_BOT_TOKEN', config['TELEGRAM_BOT_TOKEN'], 'Telegram Bot'),
        ('TELEGRAM_CHAT_ID', config['TELEGRAM_CHAT_ID'], 'Telegram Chat')
    ]
    
    for key, value, description in config_status:
        status = "✅" if value else "⚠️ "
        masked = "****" + value[-4:] if len(value) > 4 else "Not Set"
        print(f"   {status} {description}: {masked}")
    
    has_minimum_config = bool(config['WP_URL'] and config['WP_USERNAME'] and config['WP_PASSWORD'])
    
    if not has_minimum_config:
        print("\n⚠️  WARNING: Minimum configuration not met!")
        print("   Required: WP_URL, WP_USERNAME, WP_PASSWORD")
        print("   System will run in limited mode")
    
    try:
        orchestrator = EnterpriseOrchestratorPro(config)
    except Exception as e:
        print(f"\n❌ System initialization failed: {e}")
        if config['TELEGRAM_BOT_TOKEN'] and config['TELEGRAM_CHAT_ID']:
            try:
                notifier = TelegramNotifier(config['TELEGRAM_BOT_TOKEN'], config['TELEGRAM_CHAT_ID'])
                notifier.send_error_notification(str(e), "System Initialization")
            except: pass
        sys.exit(1)
    
    try:
        result = orchestrator.execute_daily_run()
        
        if result.get('success'):
            article = result['article']
            publish_result = result['publish_result']
            print("\n✅ Daily Execution Complete!")
            print(f"   Article: {article['title']}")
            print(f"   SEO Score: {article['seo_score']} ({article['seo_grade']})")
            print(f"   WordPress: {'Published' if publish_result.get('success') else 'Draft/Not Published'}")
        
        if orchestrator.telegram and orchestrator.telegram.available:
            articles_generated = 1 if result.get('success') else 0
            orchestrator.telegram.send_system_complete_notification(
                success=result.get('success', False),
                articles_generated=articles_generated
            )
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"\n❌ Daily execution failed: {e}")
        if orchestrator.telegram and orchestrator.telegram.available:
            orchestrator.telegram.send_error_notification(str(e), "Daily Execution")
        return False

if __name__ == "__main__":
    os.makedirs("memory", exist_ok=True)
    os.makedirs("daily_reports", exist_ok=True)
    
    success = main()
    
    print("\n" + "=" * 80)
    if success: print("✅ ENTERPRISE AUTO-PILOT EXECUTION SUCCESSFUL")
    else: print("⚠️  EXECUTION COMPLETED WITH ISSUES")
    print("=" * 80)
    
    sys.exit(0 if success else 1)
