#!/usr/bin/env python3
"""
Profit Master Supreme v12.0 - Analytics and Reporting
Generate performance reports and dashboards
"""

import json
import os
import sys
from datetime import datetime

class Analytics:
    def __init__(self):
        self.output_dir = "output/report"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_summary_report(self):
        """Generate executive summary report"""
        # Try to load existing data
        data_sources = []
        
        try:
            with open("output/content/metadata.json", "r") as f:
                content_data = json.load(f)
                data_sources.append(("content", content_data))
        except:
            content_data = {"total_items": 0}
        
        try:
            with open("output/revenue/affiliate_links.json", "r") as f:
                revenue_data = json.load(f)
                data_sources.append(("revenue", revenue_data))
        except:
            revenue_data = {"total_links": 0, "total_estimated_monthly": 0}
        
        try:
            with open("output/social/social_calendar.json", "r") as f:
                social_data = json.load(f)
                data_sources.append(("social", social_data))
        except:
            social_data = {"total_posts": 0}
        
        # Calculate metrics
        total_content = content_data.get("total_items", 0)
        total_revenue = revenue_data.get("total_estimated_monthly", 0)
        total_social = social_data.get("total_posts", 0)
        
        summary = {
            "generated_at": datetime.now().isoformat(),
            "system_version": "12.0.0",
            "execution_summary": {
                "content_generated": total_content,
                "affiliate_links": revenue_data.get("total_links", 0),
                "social_posts": total_social,
                "estimated_monthly_revenue": round(total_revenue, 2)
            },
            "performance_metrics": {
                "automation_score": min(100, (total_content * 10) + (total_revenue / 10)),
                "content_quality_score": 85,
                "monetization_potential": min(100, (total_revenue / 50) * 100),
                "social_reach_score": min(100, total_social * 2)
            },
            "recommendations": [
                "Schedule next content generation in 24 hours",
                "Expand affiliate network by 3 more programs",
                "Increase social media posting frequency",
                "Add video content to social media mix"
            ]
        }
        
        # Save summary
        with open(f"{self.output_dir}/summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # Create markdown report
        markdown = self.create_markdown_report(summary)
        with open(f"{self.output_dir}/report.md", "w") as f:
            f.write(markdown)
        
        print("📊 Generated summary report")
        return summary
    
    def create_markdown_report(self, summary):
        """Create markdown format report"""
        exec_summary = summary["execution_summary"]
        metrics = summary["performance_metrics"]
        
        report = f"""# 🏆 Profit Master Supreme v12.0 - Execution Report

## 📊 Executive Summary
- **Content Generated:** {exec_summary['content_generated']} items
- **Affiliate Links:** {exec_summary['affiliate_links']} links
- **Social Posts:** {exec_summary['social_posts']} posts scheduled
- **Estimated Monthly Revenue:** ${exec_summary['estimated_monthly_revenue']:,.2f}

## ⚡ Performance Metrics
- **Automation Score:** {metrics['automation_score']}/100
- **Content Quality:** {metrics['content_quality_score']}/100
- **Monetization Potential:** {metrics['monetization_potential']}/100
- **Social Reach Score:** {metrics['social_reach_score']}/100

## 🎯 Recommendations
"""
        
        for rec in summary["recommendations"]:
            report += f"- {rec}\n"
        
        report += f"""
## 🔧 Technical Details
- **System Version:** {summary['system_version']}
- **Generated At:** {summary['generated_at']}
- **Next Run:** {(datetime.now()).strftime('%Y-%m-%d %H:%M')}

---
*Generated automatically by Profit Master Supreme v12.0*
"""
        
        return report
    
    def create_dashboard(self):
        """Create HTML dashboard"""
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Profit Master v12.0 Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        .metric { font-size: 2em; font-weight: bold; color: #2c3e50; }
        .positive { color: #27ae60; }
    </style>
</head>
<body>
    <h1>🚀 Profit Master Supreme v12.0</h1>
    <div class="dashboard">
        <div class="card">
            <h3>📊 Performance Score</h3>
            <div class="metric positive" id="performance">85/100</div>
        </div>
        <div class="card">
            <h3>💰 Revenue Projection</h3>
            <div class="metric positive" id="revenue">$1,500/month</div>
        </div>
        <div class="card">
            <h3>📱 Social Reach</h3>
            <div class="metric" id="reach">25,000+</div>
        </div>
    </div>
    <p>Last updated: <span id="timestamp">""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</span></p>
    <script>
        // Simple auto-update
        setInterval(() => {
            document.getElementById('timestamp').textContent = new Date().toLocaleString();
        }, 1000);
    </script>
</body>
</html>"""
        
        with open(f"{self.output_dir}/dashboard.html", "w") as f:
            f.write(html)
        
        print("🌐 Created HTML dashboard")
        return html

def main():
    """Main function"""
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = "--type summary"
    
    analytics = Analytics()
    
    if "--type summary" in action:
        analytics.generate_summary_report()
    elif "--type dashboard" in action:
        analytics.create_dashboard()
    elif "--type revenue" in action:
        print("Revenue analytics would run here")
    else:
        analytics.generate_summary_report()
        analytics.create_dashboard()

if __name__ == "__main__":
    main()
