#!/usr/bin/env python3
"""
የጥራት ቁጥጥር ስክሪፕት ለ GitHub Actions
"""

import os
import json
import sys
from pathlib import Path

def check_quality():
    """የይዘት ጥራት ክትትል"""
    
    quality_issues = []
    warnings = []
    
    # የጽሁፍ ፋይሎችን ፈልግ
    export_dir = Path('exports')
    
    if not export_dir.exists():
        print("❌ No exports directory found")
        return {"status": "failed", "issues": ["No content generated"]}
    
    # እያንዳንዱን የ JSON ፋይል አስመልከት
    for json_file in export_dir.glob('**/*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                article = json.load(f)
            
            # ጥራት መለኪያዎች
            quality_score = article.get('quality_metrics', {}).get('seo_score', 0)
            readability = article.get('quality_metrics', {}).get('readability_score', 0)
            word_count = article.get('content', {}).get('word_count', 0)
            
            # ጥራት ማረጋገጫ
            if quality_score < 70:
                quality_issues.append(f"Low SEO score ({quality_score}) in {json_file.name}")
            
            if readability < 60:
                quality_issues.append(f"Low readability ({readability}) in {json_file.name}")
            
            if word_count < 1500:
                quality_issues.append(f"Short article ({word_count} words) in {json_file.name}")
            
        except Exception as e:
            warnings.append(f"Error processing {json_file.name}: {str(e)}")
    
    # ውጤት
    if quality_issues:
        print("⚠️ Quality issues found:")
        for issue in quality_issues:
            print(f"  • {issue}")
        
        return {
            "status": "warning",
            "issues": quality_issues,
            "warnings": warnings
        }
    else:
        print("✅ All quality checks passed")
        return {
            "status": "success",
            "issues": [],
            "warnings": warnings
        }

if __name__ == "__main__":
    result = check_quality()
    
    # Exit code based on status
    if result["status"] == "failed":
        sys.exit(1)
    elif result["status"] == "warning":
        sys.exit(2)
    else:
        sys.exit(0)
