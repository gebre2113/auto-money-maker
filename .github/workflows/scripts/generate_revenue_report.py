#!/usr/bin/env python3
"""
የገቢ ሪፖርት ማመንጨት ስክሪፕት
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_revenue_report():
    """የገቢ ሪፖርት አዘጋጅ"""
    
    reports = []
    total_revenue = 0
    
    # የ JSON ፋይሎችን ፈልግ
    for json_file in Path('.').glob('**/*.json'):
        if 'article' in json_file.name.lower():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # የገቢ መረጃ አስመልከት
                revenue = data.get('revenue_report', {}).get('summary', {})
                
                if revenue:
                    reports.append({
                        'file': json_file.name,
                        'monthly': revenue.get('total_monthly', 0),
                        'country': data.get('metadata', {}).get('country', 'Unknown'),
                        'topic': data.get('metadata', {}).get('topic', 'Unknown')
                    })
                    
                    total_revenue += revenue.get('total_monthly', 0)
                    
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
    
    # ሪፖርት ፍጠር
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_articles': len(reports),
        'total_monthly_revenue': total_revenue,
        'average_per_article': total_revenue / len(reports) if reports else 0,
        'articles': reports,
        'by_country': {},
        'by_topic': {}
    }
    
    # በሀገር እና በርዕስ ማጠቃለያ
    for r in reports:
        country = r['country']
        topic = r['topic']
        
        report['by_country'][country] = report['by_country'].get(country, 0) + r['monthly']
        report['by_topic'][topic] = report['by_topic'].get(topic, 0) + r['monthly']
    
    # ወደ ፋይል አስገባ
    with open('revenue-report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    # ማጠቃለያ ፋይል
    with open('REVENUE_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(f"# Revenue Summary - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"Total Articles: {len(reports)}\n")
        f.write(f"Total Monthly Revenue: ${total_revenue:,.2f}\n")
        f.write(f"Average per Article: ${total_revenue/len(reports) if reports else 0:,.2f}\n\n")
        
        f.write("## By Country\n")
        for country, revenue in sorted(report['by_country'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {country}: ${revenue:,.2f}\n")
        
        f.write("\n## By Topic\n")
        for topic, revenue in sorted(report['by_topic'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {topic}: ${revenue:,.2f}\n")
    
    print(f"✅ Revenue report generated: ${total_revenue:,.2f} monthly")

if __name__ == "__main__":
    generate_revenue_report()
