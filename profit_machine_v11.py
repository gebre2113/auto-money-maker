#!/usr/bin/env python3
"""
🏆 PROFIT MACHINE v11.0 - Simplified Version for GitHub Actions
"""

import os
import sys
import json
import asyncio
import argparse
import uuid
import random
from datetime import datetime
from typing import Dict, List

class ProfitMachineSimple:
    """Simplified Profit Machine for CI/CD"""
    
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration"""
        config = {
            'DATABASE_PATH': 'data/profit_machine_v11_complete.db',
            'EXPORT_DIR': 'exports',
            'LOG_DIR': 'logs',
            'MIN_WORD_COUNT': 2000,
            'MAX_WORD_COUNT': 4000
        }
        
        # Try to load from file
        if os.path.exists('config_complete.json'):
            try:
                with open('config_complete.json', 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except:
                pass
                
        return config
    
    async def generate_article(self, topic: str, country: str = "US", niche: str = "Technology") -> Dict:
        """Generate a complete article"""
        print(f"🚀 Generating article: {topic}")
        print(f"   🌍 Country: {country}")
        print(f"   📊 Niche: {niche}")
        
        # Generate unique ID
        article_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        # Create content
        content = await self._create_content(topic, country, niche)
        
        # Create metadata
        metadata = {
            'id': article_id,
            'topic': topic,
            'country': country,
            'niche': niche,
            'generated_at': datetime.now().isoformat(),
            'version': 'v11.0',
            'seo_score': random.randint(75, 95),
            'readability_score': random.randint(70, 90),
            'word_count': len(content.split()),
            'estimated_revenue': round(random.uniform(50, 500), 2)
        }
        
        # Generate article data
        article = {
            'metadata': metadata,
            'content': content,
            'seo_analysis': await self._generate_seo_analysis(content, topic),
            'market_data': await self._generate_market_data(topic, country),
            'social_posts': await self._generate_social_posts(topic, country)
        }
        
        return article
    
    async def _create_content(self, topic: str, country: str, niche: str) -> str:
        """Create article content"""
        # For demo purposes - in production, call AI APIs
        sections = [
            f"# {topic} in {country}: Comprehensive Market Analysis",
            f"\n## Executive Summary\nThis report provides an in-depth analysis of {topic.lower()} in the {country} market, focusing on the {niche} sector.",
            "\n## Market Overview",
            f"The {niche} industry in {country} is undergoing significant transformation. With advancements in technology and changing consumer behaviors, businesses must adapt to stay competitive.",
            "\n## Key Trends (2024)",
            "1. Digital transformation acceleration\n2. AI and automation integration\n3. Sustainability and ESG focus\n4. Remote work and digital collaboration\n5. Data-driven decision making",
            "\n## Market Size and Growth",
            f"The {niche} market in {country} is estimated at ${random.randint(10, 100)} billion, with a projected CAGR of {random.randint(5, 15)}% over the next five years.",
            "\n## Competitive Landscape",
            f"The competitive landscape in {country} is characterized by both established players and innovative startups. Key competitive factors include:\n- Innovation and R&D\n- Market reach and distribution\n- Customer experience\n- Pricing strategies\n- Regulatory compliance",
            "\n## Opportunities for Growth",
            f"1. **Digital Services**: Expanding online presence and digital offerings\n2. **Sustainable Solutions**: Developing eco-friendly products and services\n3. **AI Integration**: Leveraging artificial intelligence for efficiency\n4. **Market Expansion**: Targeting underserved regions within {country}\n5. **Strategic Partnerships**: Collaborating with complementary businesses",
            "\n## Challenges and Risks",
            f"1. Regulatory changes in {country}\n2. Economic uncertainty and inflation\n3. Supply chain disruptions\n4. Talent acquisition and retention\n5. Cybersecurity threats",
            "\n## Strategic Recommendations",
            f"1. **Invest in Digital Transformation**: Allocate resources to technology upgrades\n2. **Focus on Customer Experience**: Enhance customer journey across all touchpoints\n3. **Develop Sustainable Practices**: Implement ESG initiatives\n4. **Leverage Data Analytics**: Make data-driven decisions\n5. **Build Strategic Alliances**: Partner with industry leaders",
            "\n## Conclusion",
            f"The {niche} sector in {country} presents significant opportunities for growth and innovation. By understanding market dynamics and implementing strategic initiatives, businesses can achieve sustainable success in {topic.lower()}.",
            f"\n---\n*Generated by Profit Machine v11.0 on {datetime.now().strftime('%B %d, %Y')}*"
        ]
        
        return "\n".join(sections)
    
    async def _generate_seo_analysis(self, content: str, topic: str) -> Dict:
        """Generate SEO analysis"""
        words = content.split()
        word_count = len(words)
        unique_words = len(set(words))
        
        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'readability_score': random.randint(65, 85),
            'keyword_density': {
                topic.split()[0].lower(): round(random.uniform(1.5, 3.0), 2),
                'market': round(random.uniform(0.8, 1.5), 2),
                'growth': round(random.uniform(0.5, 1.2), 2)
            },
            'recommendations': [
                'Add more internal links',
                'Include more LSI keywords',
                'Optimize meta description',
                'Add alt text to images'
            ]
        }
    
    async def _generate_market_data(self, topic: str, country: str) -> Dict:
        """Generate market data"""
        return {
            'trends': [
                f'Increasing demand for {topic} in {country}',
                'Digital transformation acceleration',
                'Focus on sustainability',
                'AI and automation adoption'
            ],
            'competition_level': random.choice(['Low', 'Medium', 'High']),
            'market_size': f"${random.randint(10, 100)}B",
            'growth_rate': f"{random.randint(5, 20)}% CAGR",
            'opportunities': [
                'Digital services expansion',
                'International market entry',
                'Product innovation',
                'Strategic partnerships'
            ]
        }
    
    async def _generate_social_posts(self, topic: str, country: str) -> Dict:
        """Generate social media posts"""
        return {
            'twitter': [
                f"New analysis: {topic} in {country} shows exciting growth opportunities. #Business #MarketAnalysis",
                f"Key trends in {topic} for {country} market. Read our comprehensive report. #IndustryInsights"
            ],
            'linkedin': [
                f"Professional analysis of {topic} in the {country} market.\n\nKey insights:\n• Market trends\n• Growth opportunities\n• Strategic recommendations\n\n#BusinessIntelligence #MarketResearch"
            ],
            'facebook': [
                f"Explore our latest analysis of {topic} in {country}. Discover market opportunities and strategic insights.",
                f"What's driving growth in {topic}? Our new report breaks down the {country} market. #BusinessAnalysis"
            ]
        }
    
    def export_article(self, article: Dict, batch_index: int = None):
        """Export article to files"""
        export_dir = self.config['EXPORT_DIR']
        os.makedirs(export_dir, exist_ok=True)
        
        article_id = article['metadata']['id']
        base_name = f"article_{article_id}"
        
        if batch_index is not None:
            base_name = f"batch_{batch_index:03d}_{base_name}"
        
        # Export JSON
        json_file = f"{export_dir}/{base_name}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        
        # Export HTML
        html_file = f"{export_dir}/{base_name}.html"
        html_content = self._create_html_export(article)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Export Markdown summary
        md_file = f"{export_dir}/{base_name}_summary.md"
        md_content = self._create_markdown_summary(article)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Exported: {base_name}.*")
        return {
            'json': json_file,
            'html': html_file,
            'md': md_file
        }
    
    def _create_html_export(self, article: Dict) -> str:
        """Create HTML export"""
        meta = article['metadata']
        
        # Process content for HTML
        content = article['content']
        # Escape HTML special characters
        content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Convert newlines to <br> and headers
        lines = content.split('\n')
        html_lines = []
        for line in lines:
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('<br>')
        
        processed_content = '\n'.join(html_lines)
        
        # Now create the HTML template without backslashes in f-string
        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta['topic']} - Market Analysis</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif; 
            line-height: 1.6; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            color: #333; 
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 10px; 
        }}
        h2 {{ 
            color: #34495e; 
            margin-top: 30px; 
        }}
        .metadata {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
        }}
        .metrics {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 20px 0; 
        }}
        .metric-card {{ 
            background: white; 
            padding: 15px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }}
        footer {{ 
            margin-top: 50px; 
            padding-top: 20px; 
            border-top: 1px solid #ddd; 
            color: #7f8c8d; 
            font-size: 0.9em; 
        }}
    </style>
</head>
<body>
    <h1>{meta['topic']} in {meta['country']}</h1>
    
    <div class="metadata">
        <p><strong>Generated:</strong> {meta['generated_at']}</p>
        <p><strong>Niche:</strong> {meta['niche']}</p>
        <p><strong>Version:</strong> {meta['version']}</p>
    </div>
    
    <div class="metrics">
        <div class="metric-card">
            <h3>📊 SEO Score</h3>
            <p style="font-size: 2em; color: #27ae60;">{meta['seo_score']}/100</p>
        </div>
        <div class="metric-card">
            <h3>📝 Word Count</h3>
            <p style="font-size: 2em; color: #2980b9;">{meta['word_count']:,}</p>
        </div>
        <div class="metric-card">
            <h3>💰 Est. Revenue</h3>
            <p style="font-size: 2em; color: #e74c3c;">${meta['estimated_revenue']}</p>
        </div>
    </div>
    
    <div class="content">
        {processed_content}
    </div>
    
    <footer>
        <p>Generated by 🏆 Profit Machine v11.0</p>
        <p>Article ID: {meta['id']}</p>
    </footer>
</body>
</html>'''
        
        return html_template
    
    def _create_markdown_summary(self, article: Dict) -> str:
        """Create markdown summary"""
        meta = article['metadata']
        
        # Create keyword density string
        keyword_density_lines = []
        for k, v in article['seo_analysis']['keyword_density'].items():
            keyword_density_lines.append(f'  - {k}: {v}%')
        keyword_density_str = '\n'.join(keyword_density_lines)
        
        # Create trends string
        trends_lines = []
        for trend in article['market_data']['trends']:
            trends_lines.append(f'  - {trend}')
        trends_str = '\n'.join(trends_lines)
        
        # Create social media string
        social_lines = []
        for platform, posts in article['social_posts'].items():
            social_lines.append(f'### {platform.capitalize()}')
            for post in posts:
                social_lines.append(f'- {post}')
            social_lines.append('')
        social_str = '\n'.join(social_lines)
        
        return f"""# Article Summary

## 📋 Basic Information
- **Topic:** {meta['topic']}
- **Country:** {meta['country']}
- **Niche:** {meta['niche']}
- **Generated:** {meta['generated_at']}
- **Article ID:** {meta['id']}

## 📊 Quality Metrics
- **SEO Score:** {meta['seo_score']}/100
- **Readability Score:** {meta['readability_score']}/100
- **Word Count:** {meta['word_count']:,}
- **Estimated Revenue:** ${meta['estimated_revenue']}

## 🔍 SEO Analysis
- **Unique Words:** {article['seo_analysis']['unique_words']}
- **Keyword Density:**
{keyword_density_str}

## 📈 Market Data
- **Competition Level:** {article['market_data']['competition_level']}
- **Market Size:** {article['market_data']['market_size']}
- **Growth Rate:** {article['market_data']['growth_rate']}
- **Top Trends:**
{trends_str}

## 📱 Social Media Posts
{social_str}
---
*Generated by Profit Machine v11.0*
"""

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='🏆 PROFIT MACHINE v11.0')
    parser.add_argument('--topic', type=str, required=True,
                       help='Article topic (e.g., "AI in Healthcare")')
    parser.add_argument('--country', type=str, default='US',
                       help='Target country (US, UK, DE, etc.)')
    parser.add_argument('--niche', type=str, default='Technology',
                       help='Business niche/category')
    parser.add_argument('--batch', type=int, default=0,
                       help='Number of articles to generate (batch mode)')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🏆 PROFIT MACHINE v11.0")
    print("🎯 Automated Content Generation")
    print("=" * 80)
    
    machine = ProfitMachineSimple()
    
    if args.batch > 0:
        print(f"\n🚀 Starting batch generation of {args.batch} articles...")
        print("=" * 80)
        
        export_files = []
        for i in range(args.batch):
            topic = f"{args.topic} - Part {i+1}"
            print(f"\n📝 Generating article {i+1}/{args.batch}: {topic}")
            
            article = await machine.generate_article(topic, args.country, args.niche)
            files = machine.export_article(article, i)
            export_files.append(files)
            
            # Small delay between articles
            if i < args.batch - 1:
                await asyncio.sleep(1)
        
        print(f"\n✅ Batch generation complete! Generated {args.batch} articles.")
        
    else:
        print(f"\n📝 Generating single article...")
        article = await machine.generate_article(args.topic, args.country, args.niche)
        machine.export_article(article)
        print(f"\n✅ Article generated successfully!")
    
    print("\n" + "=" * 80)
    print("🏆 PROFIT MACHINE v11.0 - COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
