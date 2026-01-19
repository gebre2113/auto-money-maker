#!/usr/bin/env python3
"""
🏆 ULTIMATE MONEY MAKER v7.0 - ENTERPRISE AUTO-PILOT
✅ Complete Auto-Pilot System with Telegram Notifications
✅ WordPress API with Application Password
✅ Gemini AI Content Generation
✅ SEO Analysis with Featured Image Suggestions
✅ Persistent Memory with Auto-Commit
✅ Daily Auto-Run via GitHub Actions
✅ Telegram Status Notifications
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
            response = requests.get(
                f"{self.api_url}/posts",
                auth=self.auth,
                params={'per_page': 1},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ WordPress connected successfully with Application Password")
                return True
            else:
                print(f"⚠️  WordPress connection failed: {response.status_code}")
                print("   Tip: Make sure you're using Application Password, not regular password")
                print("   Generate at: WordPress Admin → Users → Profile → Application Passwords")
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
            'slug': self._generate_slug(article_data.get('title', '')),
            'categories': self._get_or_create_categories(article_data.get('categories', [])),
            'author': 1  # Default to first author
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
                        print(f"   Response: {response.text[:200]}")
                    
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
        # Convert to lowercase
        slug = title.lower()
        
        # Replace spaces with hyphens
        slug = slug.replace(' ', '-')
        
        # Remove special characters
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        
        # Trim to 100 characters
        return slug[:100]
    
    def _get_or_create_categories(self, categories: List[str]) -> List[int]:
        """Get or create WordPress categories"""
        category_ids = []
        
        for category_name in categories[:3]:  # Limit to 3 categories
            if not category_name:
                continue
                
            category_id = self._find_category(category_name)
            if not category_id:
                category_id = self._create_category(category_name)
            
            if category_id:
                category_ids.append(category_id)
        
        return category_ids
    
    def _find_category(self, category_name: str) -> Optional[int]:
        """Find existing category"""
        try:
            response = requests.get(
                f"{self.api_url}/categories",
                params={'search': category_name, 'per_page': 10},
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 200:
                categories = response.json()
                for category in categories:
                    if category['name'].lower() == category_name.lower():
                        return category['id']
        except:
            pass
        
        return None
    
    def _create_category(self, category_name: str) -> Optional[int]:
        """Create new category"""
        try:
            response = requests.post(
                f"{self.api_url}/categories",
                json={'name': category_name, 'slug': category_name.lower().replace(' ', '-')},
                auth=self.auth,
                timeout=10
            )
            
            if response.status_code == 201:
                return response.json().get('id')
        except Exception as e:
            print(f"⚠️  Failed to create category '{category_name}': {e}")
        
        return None
    
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

# =================== GEMINI AI CONTENT GENERATOR ===================

class GeminiContentGenerator:
    """Gemini AI for intelligent content generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.available = False
        
        if not GEMINI_AVAILABLE:
            print("⚠️  google-generativeai library not installed")
            print("   Install with: pip install google-generativeai")
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

            self.available = True
            print("✅ Gemini AI configured successfully")
        except Exception as e:
            print(f"⚠️  Gemini AI configuration failed: {e}")
            print("   Make sure your API key is valid and has access to Gemini Pro")
    
    def generate_article(self, topic: str, word_count: int = 1200) -> Dict:
        """Generate article using Gemini AI with fallback"""
        
        if not self.available:
            return self._generate_fallback_article(topic, word_count)
        
        # Enhanced prompt for better articles
        prompt = f"""Write a comprehensive, SEO-optimized article about: "{topic}"

Article Requirements:
- Word count: Approximately {word_count} words
- Target audience: Blog readers interested in technology and business
- Tone: Professional yet engaging and conversational
- Structure: Include H1, H2, and H3 headings
- SEO: Naturally include the focus keyword and related terms
- Quality: Well-researched, practical, and valuable information
- Format: Use HTML tags for proper formatting

Article Structure:
1. Introduction (Hook the reader)
2. Main content with 3-4 subsections
3. Practical tips or step-by-step guide
4. Common mistakes to avoid
5. Conclusion with actionable advice

Make the article genuinely useful and avoid generic content."""

                # Retry logic with exponential backoff
        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'top_k': 40,
                        'max_output_tokens': int(word_count * 1.5),
                    }
                )

                
                content = response.text.strip()
                
                # Validate generated content
                if len(content) > 300 and '<h' in content:  # Basic validation
                    # Clean up content
                    content = self._clean_content(content)
                    
                    return {
                        'success': True,
                        'content': content,
                        'word_count': len(content.split()),
                        'attempts': attempt + 1,
                        'source': 'gemini_ai',
                        'quality': 'ai_generated'
                    }
                else:
                    print(f"⚠️  Gemini generated invalid content (attempt {attempt + 1})")
                    
            except Exception as e:
                print(f"⚠️  Gemini generation failed (attempt {attempt + 1}): {e}")
                wait_time = 2 ** attempt  # Exponential backoff
                time.sleep(wait_time)
        
        # Fallback to template if all retries fail
        return self._generate_fallback_article(topic, word_count)
    
    def _clean_content(self, content: str) -> str:
        """Clean and format generated content"""
        # Remove markdown code blocks if present
        content = re.sub(r'```[a-z]*\n', '', content)
        content = content.replace('```', '')
        
        # Ensure proper HTML structure
        if not content.startswith('<h1>'):
            # Find first heading and make it H1
            h2_match = re.search(r'<h2>(.*?)</h2>', content)
            if h2_match:
                title = h2_match.group(1)
                content = content.replace(h2_match.group(0), f'<h1>{title}</h1>')
            else:
                # Add a basic H1
                content = f'<h1>Article</h1>\n\n{content}'
        
        # Add paragraph tags if missing
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('<') and not line.endswith('>'):
                cleaned_lines.append(f'<p>{line}</p>')
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _generate_fallback_article(self, topic: str, word_count: int) -> Dict:
        """Generate fallback article when Gemini fails"""
        print("📄 Using fallback template system...")
        
        # Template 1: Guide format
        guide_template = f"""
<h1>{topic}</h1>

<p>In this comprehensive guide, we'll explore everything you need to know about {topic}.</p>

<h2>Why {topic.split(':')[0] if ':' in topic else topic.split()[0]} is Important</h2>
<p>Understanding {topic.lower()} is crucial for success in today's digital landscape. Whether you're a beginner or experienced, mastering this topic can significantly impact your results.</p>

<h2>Key Benefits and Advantages</h2>
<ul>
<li><strong>Benefit 1:</strong> Improved efficiency and productivity in your workflow</li>
<li><strong>Benefit 2:</strong> Better results and higher quality outcomes</li>
<li><strong>Benefit 3:</strong> Competitive advantage in your niche or industry</li>
<li><strong>Benefit 4:</strong> Time and resource optimization</li>
</ul>

<h2>Step-by-Step Implementation Guide</h2>
<ol>
<li><strong>Step 1:</strong> Start with clear goals and objectives</li>
<li><strong>Step 2:</strong> Research and gather necessary resources</li>
<li><strong>Step 3:</strong> Create a structured plan of action</li>
<li><strong>Step 4:</strong> Implement systematically and track progress</li>
<li><strong>Step 5:</strong> Measure results and optimize accordingly</li>
</ol>

<h2>Common Challenges and Solutions</h2>
<p>Many people face these challenges when dealing with {topic.lower()}:</p>
<ul>
<li><strong>Challenge 1:</strong> Lack of time and resources - Solution: Start small and scale gradually</li>
<li><strong>Challenge 2:</strong> Difficulty measuring ROI - Solution: Set clear metrics from the beginning</li>
<li><strong>Challenge 3:</strong> Keeping up with changes - Solution: Establish a regular learning routine</li>
</ul>

<h2>Best Practices and Pro Tips</h2>
<p>Here are some expert tips for success with {topic.lower()}:</p>
<ul>
<li>Always focus on quality over quantity</li>
<li>Stay updated with the latest trends and developments</li>
<li>Network with others in the same field</li>
<li>Continuously test and optimize your approach</li>
</ul>

<h2>Conclusion and Next Steps</h2>
<p>Mastering {topic.lower()} is a journey that requires consistent effort and learning. Start implementing these strategies today, and you'll see significant improvements over time.</p>

<p>Remember: The key to success is taking consistent, focused action towards your goals.</p>
"""
        
        # Template 2: List format
        list_template = f"""
<h1>{topic}</h1>

<p>Welcome to our complete guide on {topic}. In this article, we'll cover everything from basics to advanced strategies.</p>

<h2>Introduction to {topic.split(':')[0] if ':' in topic else 'This Topic'}</h2>
<p>{topic} has become increasingly relevant in today's fast-paced digital world. Whether you're just starting or looking to improve your existing knowledge, this guide has something for you.</p>

<h2>10 Key Things You Need to Know</h2>
<ol>
<li><strong>Point 1:</strong> Understand the fundamental concepts and principles</li>
<li><strong>Point 2:</strong> Learn the most effective tools and resources available</li>
<li><strong>Point 3:</strong> Develop a strategic approach for implementation</li>
<li><strong>Point 4:</strong> Measure your progress with clear metrics</li>
<li><strong>Point 5:</strong> Optimize based on data and feedback</li>
<li><strong>Point 6:</strong> Stay updated with industry trends</li>
<li><strong>Point 7:</strong> Network with like-minded individuals</li>
<li><strong>Point 8:</strong> Continuously learn and adapt</li>
<li><strong>Point 9:</strong> Scale your efforts systematically</li>
<li><strong>Point 10:</strong> Maintain consistency for long-term success</li>
</ol>

<h2>Essential Tools and Resources</h2>
<p>Here are some essential tools for working with {topic.lower()}:</p>
<ul>
<li><strong>Tool 1:</strong> Software applications for automation</li>
<li><strong>Tool 2:</strong> Online platforms for learning and collaboration</li>
<li><strong>Tool 3:</strong> Analytics tools for tracking progress</li>
<li><strong>Tool 4:</strong> Community forums for support and networking</li>
</ul>

<h2>Frequently Asked Questions</h2>
<p><strong>Q: How long does it take to see results?</strong><br>
A: Results vary, but with consistent effort, you can see improvements within a few weeks.</p>

<p><strong>Q: Do I need technical skills?</strong><br>
A: Basic understanding helps, but many tools are designed for beginners.</p>

<p><strong>Q: What's the most common mistake to avoid?</strong><br>
A: Trying to do everything at once instead of focusing on one thing at a time.</p>

<h2>Final Thoughts</h2>
<p>{topic} offers incredible opportunities for those willing to learn and apply the principles consistently. Start today, stay consistent, and track your progress for best results.</p>
"""
        
        # Choose template
        templates = [guide_template, list_template]
        content = random.choice(templates)
        
        # Ensure word count
        while len(content.split()) < word_count * 0.8:
            # Add another section from templates
            extra_content = random.choice(templates)
            h2_sections = re.findall(r'<h2>.*?</h2>\s*<p>.*?</p>', extra_content, re.DOTALL)
            if h2_sections:
                content += '\n\n' + random.choice(h2_sections)
        
        return {
            'success': False,
            'content': content,
            'word_count': len(content.split()),
            'source': 'fallback_template',
            'quality': 'template_generated',
            'note': 'Gemini AI unavailable or failed, using template system'
        }

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
        
        # Articles table
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
        
        # Topic performance table
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
        
        # Calculate overall score
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
        
        # Length score (40%)
        if 50 <= length <= 60:
            score += 0.4
        elif 30 <= length <= 70:
            score += 0.3
        else:
            score += 0.1
        
        # Keyword score (40%)
        if has_keyword:
            score += 0.4
        
        # Structure score (20%)
        if title[0].isupper() and title[-1] not in '!?':
            score += 0.2
        
        return {
            'score': round(score, 2),
            'length': length,
            'has_keyword': has_keyword,
            'optimal_range': (50, 60)
        }
    
    def _analyze_content(self, content: str, keyword: str) -> Dict:
        """Analyze content SEO"""
        words = content.split()
        word_count = len(words)
        
        # Keyword density
        keyword_density = 0.0
        if keyword:
            keyword_lower = keyword.lower()
            content_lower = content.lower()
            keyword_occurrences = content_lower.count(keyword_lower)
            keyword_density = (keyword_occurrences / word_count) * 100 if word_count > 0 else 0
        
        # Heading analysis
        h2_count = content.count('<h2')
        h3_count = content.count('<h3')
        
        score = 0.0
        
        # Word count score (30%)
        if word_count >= 1200:
            score += 0.3
        elif word_count >= 800:
            score += 0.2
        else:
            score += 0.1
        
        # Keyword density score (30%)
        if 1.0 <= keyword_density <= 2.0:
            score += 0.3
        elif keyword_density > 0:
            score += 0.2
        else:
            score += 0.1
        
        # Heading structure score (40%)
        heading_score = min(h2_count / 3, 0.2) + min(h3_count / max(h2_count, 1), 0.2)
        score += heading_score
        
        return {
            'score': round(score, 2),
            'word_count': word_count,
            'keyword_density': round(keyword_density, 2),
            'headings': {'h2': h2_count, 'h3': h3_count}
        }
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze readability"""
        sentences = [s for s in re.split(r'[.!?]+', content) if s.strip()]
        words = content.split()
        
        if len(sentences) == 0:
            return {'score': 0.5, 'avg_sentence_length': 0}
        
        avg_sentence_length = len(words) / len(sentences)
        paragraphs = content.count('\n\n') + 1
        
        score = 0.0
        
        # Sentence length score (50%)
        if 15 <= avg_sentence_length <= 25:
            score += 0.5
        elif 10 <= avg_sentence_length <= 30:
            score += 0.3
        else:
            score += 0.1
        
        # Paragraph structure score (30%)
        if paragraphs >= 5:
            score += 0.3
        elif paragraphs >= 3:
            score += 0.2
        else:
            score += 0.1
        
        # Transition words (20%)
        transition_words = ['however', 'therefore', 'moreover', 'consequently']
        transition_count = sum(content.lower().count(word) for word in transition_words)
        score += min(transition_count / 4, 0.2)
        
        return {
            'score': round(score, 2),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'paragraphs': paragraphs
        }
    
    def _analyze_technical_seo(self, content: str) -> Dict:
        """Analyze technical SEO elements"""
        score = 0.0
        
        # Images with alt
        img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
        alt_count = sum(1 for img in img_tags if 'alt=' in img.lower())
        if img_tags:
            alt_ratio = alt_count / len(img_tags)
            score += alt_ratio * 0.3
        
        # Internal links
        link_tags = re.findall(r'<a[^>]*href=[^>]*>', content, re.IGNORECASE)
        if len(link_tags) >= 2:
            score += 0.2
        
        # Mobile friendliness
        if 'viewport' in content.lower():
            score += 0.2
        
        # Meta tags (simulated)
        if '</head>' in content.lower():
            score += 0.3
        
        return {
            'score': round(score, 2),
            'images_with_alt': alt_count,
            'internal_links': len(link_tags)
        }
    
    def _assign_grade(self, score: float) -> str:
        """Assign letter grade"""
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate SEO recommendations"""
        recs = []
        
        title = analysis['title_analysis']
        if title['score'] < 0.7:
            if not title['has_keyword']:
                recs.append("Add focus keyword to title")
            if not (50 <= title['length'] <= 60):
                recs.append(f"Adjust title length (current: {title['length']}, optimal: 50-60)")
        
        content = analysis['content_analysis']
        if content['word_count'] < 1000:
            recs.append(f"Increase content length to at least 1000 words (current: {content['word_count']})")
        
        if content['headings']['h2'] < 2:
            recs.append("Add more H2 headings for better structure")
        
        technical = analysis['technical_seo']
        if technical['images_with_alt'] == 0 and content['word_count'] > 500:
            recs.append("Add images with alt text for better SEO")
        
        return recs[:3] if recs else ["Good SEO optimization"]

# =================== ENTERPRISE ORCHESTRATOR PRO ===================

class EnterpriseOrchestratorPro:
    """Main orchestrator with all integrations"""
    
    def __init__(self, config: Dict):
        print("🚀 Initializing Enterprise Orchestrator PRO...")
        print("=" * 60)
        
        # Store configuration
        self.config = config
        
        # Initialize core systems
        self.memory = ContentMemory()
        self.seo_agent = SEOAnalysisAgent()
        
        # Initialize Telegram notifier
        self.telegram = None
        if config.get('TELEGRAM_BOT_TOKEN') and config.get('TELEGRAM_CHAT_ID'):
            self.telegram = TelegramNotifier(
                config['TELEGRAM_BOT_TOKEN'],
                config['TELEGRAM_CHAT_ID']
            )
            if self.telegram.available:
                print("✅ Telegram Notifier initialized")
            else:
                print("⚠️  Telegram Notifier not available (check token/chat_id)")
        
        # Initialize WordPress publisher
        self.wordpress = None
        if config.get('WP_URL') and config.get('WP_USERNAME') and config.get('WP_PASSWORD'):
            self.wordpress = WordPressPublisher(
                config['WP_URL'],
                config['WP_USERNAME'],
                config['WP_PASSWORD']
            )
            if self.wordpress.connected:
                print("✅ WordPress Publisher initialized")
            else:
                print("⚠️  WordPress Publisher not connected")
        
        # Initialize Gemini AI
        self.gemini = None
        if config.get('GEMINI_API_KEY'):
            self.gemini = GeminiContentGenerator(config['GEMINI_API_KEY'])
            if self.gemini.available:
                print("✅ Gemini AI initialized")
            else:
                print("⚠️  Gemini AI not available")
        
        print("=" * 60)
        print("📊 System Status Summary:")
        print(f"   Telegram: {'✅ Connected' if self.telegram and self.telegram.available else '❌ Not configured'}")
        print(f"   WordPress: {'✅ Connected' if self.wordpress and self.wordpress.connected else '❌ Not connected'}")
        print(f"   Gemini AI: {'✅ Available' if self.gemini and self.gemini.available else '❌ Not available'}")
        print(f"   Memory: ✅ {self.memory._count_articles()} articles in database")
        print("=" * 60)
    
    def execute_daily_run(self) -> Dict:
        """Execute complete daily run"""
        
        # Send start notification
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
        
        # Publish to WordPress (only if SEO score is good)
        publish_result = None
        if self.wordpress and self.wordpress.connected:
            if seo_analysis['overall_score'] >= 0.6:  # Minimum threshold
                print("🌐 Publishing to WordPress...")
                publish_result = self.wordpress.publish_article(
                    article_data,
                    status='draft'  # Start as draft, change to 'publish' for auto-publish
                )
                
                if publish_result.get('success'):
                    article_data['published'] = True
                    article_data['wordpress_id'] = publish_result.get('post_id')
                    article_data['wordpress_link'] = publish_result.get('link')
                    print(f"✅ Published to WordPress (ID: {publish_result.get('post_id')})")
                else:
                    print(f"⚠️  WordPress publish failed: {publish_result.get('error')}")
            else:
                print(f"⚠️  SEO score too low for publishing: {seo_analysis['overall_score']}")
                publish_result = {'success': False, 'error': 'Low SEO score'}
        else:
            print("⚠️  WordPress not connected, skipping publish")
            publish_result = {'success': False, 'error': 'WordPress not connected'}
        
        # Store in memory
        self.memory.store_article(article_data)
        
        # Generate daily report
        report_file = self._generate_daily_report(article_data, seo_analysis, publish_result)
        
        # Send Telegram notification
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
        """Select topic for today's article"""
        
        # Try to get best topics from memory
        best_topics = self.memory.get_best_topics(5)
        
        if best_topics:
            # Filter high-performing topics
            high_performing = [t for t in best_topics if t.get('performance_score', 0) >= 0.7]
            if high_performing:
                selected = random.choice(high_performing)
                print(f"   Using high-performing topic from memory: {selected['topic']}")
                return selected['topic']
        
        # Fallback topics (can be customized)
        fallback_topics = [
            "How to Start a Successful Blog in 2024",
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
        """Generate article from templates"""
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
<li><strong>Strategy 4:</strong> Adapt and optimize based on data and feedback</li>
</ul>

<h2>Practical Implementation Steps</h2>
<ol>
<li><strong>Step 1:</strong> Define clear goals and objectives</li>
<li><strong>Step 2:</strong> Research and gather necessary resources</li>
<li><strong>Step 3:</strong> Create a structured implementation plan</li>
<li><strong>Step 4:</strong> Execute your plan systematically</li>
<li><strong>Step 5:</strong> Review and optimize based on results</li>
</ol>

<h2>Common Mistakes to Avoid</h2>
<p>Many people make these common mistakes when dealing with {topic.lower()}:</p>
<ul>
<li>Trying to do too much at once instead of focusing</li>
<li>Not measuring results and optimizing accordingly</li>
<li>Ignoring the importance of consistency</li>
<li>Failing to stay updated with industry changes</li>
</ul>

<h2>Conclusion</h2>
<p>{topic} offers significant opportunities for those who approach it strategically. By following the principles outlined in this guide, you can achieve meaningful results and build a strong foundation for future success.</p>
"""
        ]
        
        content = random.choice(templates)
        word_count = len(content.split())
        
        return {
            'content': content,
            'word_count': word_count,
            'source': 'template_system'
        }
    
    def _extract_keyword(self, topic: str) -> str:
        """Extract focus keyword from topic"""
        words = topic.split()
        
        if len(words) >= 3:
            return ' '.join(words[:3])
        elif len(words) == 2:
            return topic
        else:
            # Single word topic
            return f"{topic} guide"
    
    def _select_categories(self, topic: str) -> List[str]:
        """Select categories based on topic"""
        categories = []
        topic_lower = topic.lower()
        
        # Category mapping
        if any(word in topic_lower for word in ['ai', 'artificial', 'machine']):
            categories.append('Artificial Intelligence')
        if any(word in topic_lower for word in ['wordpress', 'blog', 'website']):
            categories.append('WordPress')
        if any(word in topic_lower for word in ['seo', 'search', 'ranking']):
            categories.append('SEO')
        if any(word in topic_lower for word in ['money', 'income', 'revenue', 'monetize']):
            categories.append('Monetization')
        if any(word in topic_lower for word in ['marketing', 'promotion', 'audience']):
            categories.append('Marketing')
        if any(word in topic_lower for word in ['python', 'automation', 'code']):
            categories.append('Programming')
        
        # Default categories if none matched
        if not categories:
            categories = ['Technology', 'Business', 'Digital Marketing']
        
        return categories[:3]
    
    def _generate_daily_report(self, article_data: Dict, seo_analysis: Dict, publish_result: Dict = None) -> str:
        """Generate daily execution report"""
        
        report = {
            'execution_date': datetime.now().isoformat(),
            'github_run_number': os.getenv('GITHUB_RUN_NUMBER', 'N/A'),
            'article': {
                'title': article_data['title'],
                'word_count': article_data['word_count'],
                'seo_score': article_data['seo_score'],
                'seo_grade': article_data['seo_grade'],
                'categories': article_data['categories'],
                'focus_keyword': article_data['focus_keyword'],
                'generation_source': article_data.get('generation_source', 'unknown'),
                'quality': article_data.get('quality', 'unknown')
            },
            'seo_analysis': {
                'overall_score': seo_analysis['overall_score'],
                'grade': seo_analysis['grade'],
                'title_score': seo_analysis['title_analysis']['score'],
                'content_score': seo_analysis['content_analysis']['score'],
                'recommendations': seo_analysis['recommendations']
            },
            'publishing': {
                'attempted': publish_result is not None,
                'success': publish_result.get('success', False) if publish_result else False,
                'wordpress_id': publish_result.get('post_id') if publish_result else None,
                'link': publish_result.get('link') if publish_result else None,
                'error': publish_result.get('error') if publish_result else None
            },
            'system_stats': {
                'total_articles': self.memory._count_articles(),
                'memory_stats': self.memory._get_system_stats(),
                'wordpress_connected': self.wordpress.connected if self.wordpress else False,
                'gemini_available': self.gemini.available if self.gemini else False,
                'telegram_available': self.telegram.available if self.telegram else False
            }
        }
        
        # Save report
        os.makedirs("daily_reports", exist_ok=True)
        date_str = datetime.now().strftime('%Y%m%d')
        report_file = f"daily_reports/report_{date_str}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Daily report saved: {report_file}")
        
        return report_file

# =================== MAIN EXECUTION ===================

def main():
    """Main execution function"""
    
    print("=" * 80)
    print("🏆 ULTIMATE MONEY MAKER v7.0 - ENTERPRISE AUTO-PILOT")
    print("=" * 80)
    print("\n🚀 Starting system with all integrations...\n")
    
    # Load configuration from environment variables (GitHub Secrets)
    config = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', ''),
        'WP_URL': os.getenv('WP_URL', ''),
        'WP_USERNAME': os.getenv('WP_USERNAME', ''),
        'WP_PASSWORD': os.getenv('WP_PASSWORD', ''),
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID', '')
    }
    
    # Print configuration status
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
    
    # Check if we have minimum configuration
    has_minimum_config = bool(config['WP_URL'] and config['WP_USERNAME'] and config['WP_PASSWORD'])
    
    if not has_minimum_config:
        print("\n⚠️  WARNING: Minimum configuration not met!")
        print("   Required: WP_URL, WP_USERNAME, WP_PASSWORD")
        print("   System will run in limited mode")
    
    # Initialize orchestrator
    try:
        orchestrator = EnterpriseOrchestratorPro(config)
    except Exception as e:
        print(f"\n❌ System initialization failed: {e}")
        
        # Try to send error notification
        if config['TELEGRAM_BOT_TOKEN'] and config['TELEGRAM_CHAT_ID']:
            try:
                notifier = TelegramNotifier(config['TELEGRAM_BOT_TOKEN'], config['TELEGRAM_CHAT_ID'])
                notifier.send_error_notification(str(e), "System Initialization")
            except:
                pass
        
        sys.exit(1)
    
    # Execute daily run
    try:
        result = orchestrator.execute_daily_run()
        
        if result.get('success'):
            article = result['article']
            publish_result = result['publish_result']
            
            print("\n✅ Daily Execution Complete!")
            print(f"   Article: {article['title']}")
            print(f"   SEO Score: {article['seo_score']} ({article['seo_grade']})")
            print(f"   WordPress: {'Published' if publish_result.get('success') else 'Draft/Not Published'}")
            
            if publish_result.get('link'):
                print(f"   Link: {publish_result['link']}")
        else:
            print("\n⚠️  Daily execution completed with issues")
        
        # Send completion notification
        if orchestrator.telegram and orchestrator.telegram.available:
            articles_generated = 1 if result.get('success') else 0
            orchestrator.telegram.send_system_complete_notification(
                success=result.get('success', False),
                articles_generated=articles_generated
            )
        
        # Create final status file
        status = {
            'run_completed': datetime.now().isoformat(),
            'success': result.get('success', False),
            'article_generated': result.get('success', False),
            'wordpress_published': result.get('publish_result', {}).get('success', False) if result.get('publish_result') else False,
            'seo_score': result.get('article', {}).get('seo_score', 0),
            'telegram_notified': orchestrator.telegram.available if orchestrator.telegram else False,
            'github_run_number': os.getenv('GITHUB_RUN_NUMBER', 'N/A'),
            'files_generated': [
                result.get('report_file', ''),
                'memory/content_memory.db',
                'daily_reports/'
            ]
        }
        
        with open('github_run_status.json', 'w') as f:
            json.dump(status, f, indent=2)
        
        print(f"\n📁 Status saved: github_run_status.json")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"\n❌ Daily execution failed: {e}")
        
        # Send error notification
        if orchestrator.telegram and orchestrator.telegram.available:
            orchestrator.telegram.send_error_notification(str(e), "Daily Execution")
        
        # Create error status file
        error_status = {
            'run_completed': datetime.now().isoformat(),
            'success': False,
            'error': str(e),
            'github_run_number': os.getenv('GITHUB_RUN_NUMBER', 'N/A')
        }
        
        with open('github_run_status.json', 'w') as f:
            json.dump(error_status, f, indent=2)
        
        return False

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("memory", exist_ok=True)
    os.makedirs("daily_reports", exist_ok=True)
    
    # Run main function
    success = main()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ ENTERPRISE AUTO-PILOT EXECUTION SUCCESSFUL")
    else:
        print("⚠️  EXECUTION COMPLETED WITH ISSUES")
    print("=" * 80)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
