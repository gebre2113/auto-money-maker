#!/usr/bin/env python3
"""
🚀 ULTIMATE PRODUCTION MAIN RUNNER v3.0
🎯 ሁለቱንም ግዙፍ ስክሪፕቶች በሙሉ የሚያዝዝ የምርት ዝግጁ ራነር
💎 Script A (YouTube Affiliate) + Script B (Profit Master) Integration
🔒 Enterprise-Grade Orchestration with Zero Data Loss
"""

import asyncio
import logging
import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import traceback

# =================== የስክሪፕቶች ግንኙነት (Smart Import System) ===================

class SmartImportSystem:
    """እነዚያን ሁለት ስክሪፕቶች በጥንቃቄ የሚያስገባ ስርዓት"""
    
    @staticmethod
    def import_script_a():
        """Script A (YouTube Affiliate System) መጫን"""
        try:
            # የYouTube አፊሊዬት ስርዓት
            from youtube_affiliate_system import (
                YouTubeIntelligenceHunterPro,
                VideoAffiliateIntegrationEngine,
                UltraAffiliateManager,
                GlobalMonetizationIntelligence
            )
            return {
                'YouTubeIntelligenceHunterPro': YouTubeIntelligenceHunterPro,
                'VideoAffiliateIntegrationEngine': VideoAffiliateIntegrationEngine,
                'UltraAffiliateManager': UltraAffiliateManager,
                'GlobalMonetizationIntelligence': GlobalMonetizationIntelligence
            }
        except ImportError as e:
            logging.error(f"❌ Script A import failed: {e}")
            return None
    
    @staticmethod
    def import_script_b():
        """Script B (Profit Master Mega-System) መጫን"""
        try:
            # የፕሮፊት ማስተር ስርዓት (ይህ መስመር ለብቻው መሆን አለበት)
            from profit_master_system import (
                UltimateProfitMasterSystem,
                PremiumConfig,
                AdvancedAIContentGenerator,
                CulturalAnthropologistEngine,
                HyperLocalizedContentProducer,
                PremiumMultimediaEnhancer,
                ProductionManager,
                UserInterface
            )
            return {
                'UltimateProfitMasterSystem': UltimateProfitMasterSystem,
                'PremiumConfig': PremiumConfig,
                'AdvancedAIContentGenerator': AdvancedAIContentGenerator,
                'CulturalAnthropologistEngine': CulturalAnthropologistEngine,
                'HyperLocalizedContentProducer': HyperLocalizedContentProducer,
                'PremiumMultimediaEnhancer': PremiumMultimediaEnhancer,
                'ProductionManager': ProductionManager,
                'UserInterface': UserInterface
            }
        except ImportError as e:
            import logging
            logging.error(f"❌ Script B import failed: {e}")
            return None

        except ImportError as e:
            logging.error(f"❌ Script B import failed: {e}")
            return None

# =================== የሎጂንግ ስርዓት (Production-Grade Logging) ===================

class ProductionLogger:
    """ለምርት ዝግጁ የሎጂንግ ስርዓት"""
    
    def __init__(self):
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # ዋና ሎግ ፋይል
        main_log = self.log_dir / 'production_main.log'
        
        # የስህተት ሎግ ፋይል
        error_log = self.log_dir / 'production_errors.log'
        
        # የምርት ሪፖርት ፋይል
        report_log = self.log_dir / 'production_reports.log'
        
        # ሎጂንግ ኮንፊግሬሽን
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | [%(levelname)s] | %(name)s | %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(main_log, encoding='utf-8'),
                logging.FileHandler(error_log, encoding='utf-8'),                logging.FileHandler(report_log, encoding='utf-8')
            ]
        )
        
        self.logger = logging.getLogger("ProductionRunner")
        self.logger.info("✅ Production Logger Initialized")
    
    def log_stage(self, stage_name: str, message: str, level: str = "INFO"):
        """የተወሰነ ደረጃ ሎግ ማድረግ"""
        log_msg = f"{'='*20} {stage_name} {'='*20}\n{message}\n{'='*50}"
        getattr(self.logger, level.lower())(log_msg)
    
    def log_error(self, error: Exception, context: str = ""):
        """ስህተት ሎግ ማድረግ"""
        error_msg = f"""
        🚨 CRITICAL ERROR
        Context: {context}
        Error Type: {type(error).__name__}
        Error Message: {str(error)}
        Traceback:
        {traceback.format_exc()}
        """
        self.logger.error(error_msg)

# =================== ዋና ኦርኬስትሬተር (Master Orchestrator) ===================

class UltimateProductionOrchestrator:
    """
    🎯 ሁለቱንም ስክሪፕቶች የሚያዝዝ ዋና ኦርኬስትሬተር
    Script A + Script B Integration with Full Production Pipeline
    """
    
    def __init__(self):
        self.logger = ProductionLogger().logger
        self.start_time = datetime.now()
        
        # ስክሪፕቶችን መጫን
        self.script_a_modules = SmartImportSystem.import_script_a()
        self.script_b_modules = SmartImportSystem.import_script_b()
        
        # ስርዓቶችን መጀመር
        self._initialize_systems()
        
        self.logger.info("🚀 Ultimate Production Orchestrator Initialized")
    
    def _initialize_systems(self):
        """ሁሉንም ስርዓቶች መጀመር"""
        
        # Script B ስርዓቶች (በመጀመሪያ ምክንያቱም የመሰረት ነገሮች አሉት)
        if self.script_b_modules:            self.config = self.script_b_modules['PremiumConfig']()
            self.content_system = self.script_b_modules['UltimateProfitMasterSystem'](self.config)
            self.production_manager = self.script_b_modules['ProductionManager'](self.config)
            self.logger.info("✅ Script B Systems Initialized")
        else:
            raise RuntimeError("Script B failed to initialize!")
        
        # Script A ስርዓቶች
        if self.script_a_modules:
            self.youtube_hunter = self.script_b_modules['AdvancedAIContentGenerator'](self.config)
            self.video_engine = self.script_a_modules['VideoAffiliateIntegrationEngine'](
                enable_ethical_mode=True,
                enable_tracking=True
            )
            self.affiliate_manager = self.script_a_modules['UltraAffiliateManager'](
                user_geo="US",
                user_segment="premium",
                ethical_mode=True,
                enable_ab_testing=True
            )
            self.logger.info("✅ Script A Systems Initialized")
        else:
            self.logger.warning("⚠️ Script A not available - continuing with Script B only")
            self.youtube_hunter = None
            self.video_engine = None
            self.affiliate_manager = None
    
    async def execute_full_production_pipeline(self, topic: str, 
                                              target_countries: List[str] = None,
                                              content_type: str = "blog_post") -> Dict[str, Any]:
        """
        🎬 ሙሉ የምርት ፈረቃ አስተናግድ
        Script A + Script B Integration with Maximum Efficiency
        """
        
        production_id = f"prod_{hashlib.md5(f'{topic}{datetime.now()}'.encode()).hexdigest()[:12]}"
        self.logger.info(f"🔥 Production Started | ID: {production_id} | Topic: {topic}")
        
        results = {
            'production_id': production_id,
            'topic': topic,
            'status': 'processing',
            'stages_completed': [],
            'errors': [],
            'metrics': {}
        }
        
        try:
            # =================== ደረጃ 1: የዩቲዩብ ቪዲዮ መፈለግ (Script A) ===================
            if self.youtube_hunter and self.video_engine:                await self._stage_1_youtube_video_search(topic, results)
            
            # =================== ደረጃ 2: የፕሬሚየም ይዘት ማመንጨት (Script B) ===================
            await self._stage_2_content_generation(topic, target_countries, content_type, results)
            
            # =================== ደረጃ 3: የአፊሊዬት ኢንትግሬሽን (Script A) ===================
            if self.affiliate_manager:
                await self._stage_3_affiliate_integration(topic, results)
            
            # =================== ደረጃ 4: የሙልቲሚዲያ ማሻሻያ (Script B) ===================
            await self._stage_4_multimedia_enhancement(results)
            
            # =================== ደረጃ 5: የባህል ሎካላይዜሽን (Script B) ===================
            if target_countries:
                await self._stage_5_cultural_localization(topic, target_countries, results)
            
            # =================== ደረጃ 6: የጥራት ፈተሻ እና ማረጋገጫ (Both Scripts) ===================
            await self._stage_6_quality_assurance(results)
            
            # =================== ደረጃ 7: የምርት ሪፖርት ማመንጨት (Both Scripts) ===================
            await self._stage_7_production_report(results)
            
            results['status'] = 'completed'
            results['completion_time'] = datetime.now().isoformat()
            results['total_duration_seconds'] = (datetime.now() - self.start_time).total_seconds()
            
            self.logger.info(f"✅ Production Completed Successfully | ID: {production_id}")
            
        except Exception as e:
            error_msg = f"💥 Production Failed: {str(e)}"
            self.logger.error(error_msg)
            ProductionLogger().log_error(e, f"Production Pipeline for {topic}")
            
            results['status'] = 'failed'
            results['error'] = str(e)
            results['error_traceback'] = traceback.format_exc()
        
        return results
    
    async def _stage_1_youtube_video_search(self, topic: str, results: Dict):
        """ደረጃ 1: የዩቲዩብ ቪዲዮ መፈለግ"""
        
        self.logger.info("🎬 STAGE 1: YouTube Video Intelligence Gathering")
        
        try:
            # የዩቲዩብ ቪዲዮዎችን መፈለግ
            videos = await self.youtube_hunter.find_relevant_videos(
                topic=topic,
                country="US",
                max_results=5            )
            
            results['youtube_videos'] = videos
            results['stages_completed'].append('youtube_video_search')
            
            self.logger.info(f"✅ Found {len(videos)} relevant YouTube videos")
            
        except Exception as e:
            self.logger.warning(f"⚠️ YouTube search failed (continuing): {e}")
            results['youtube_videos'] = []
    
    async def _stage_2_content_generation(self, topic: str, 
                                         target_countries: List[str],
                                         content_type: str,
                                         results: Dict):
        """ደረጃ 2: የፕሬሚየም ይዘት ማመንጨት"""
        
        self.logger.info("📝 STAGE 2: Premium Content Generation")
        
        try:
            # የፕሬሚየም ይዘት ማመንጨት
            content_result = await self.content_system.full_production_pipeline(
                topic=topic,
                target_countries=target_countries
            )
            
            results['content'] = content_result
            results['stages_completed'].append('content_generation')
            
            # መለኪያዎችን መዝግብ
            results['metrics']['word_count'] = content_result.get('word_count', 0)
            results['metrics']['quality_score'] = content_result.get('quality_report', {}).get('overall_score', 0)
            results['metrics']['generation_time'] = content_result.get('generation_time', 0)
            
            self.logger.info(f"✅ Content Generated | Words: {results['metrics']['word_count']} | Quality: {results['metrics']['quality_score']}%")
            
        except Exception as e:
            raise RuntimeError(f"Content generation failed: {e}")
    
    async def _stage_3_affiliate_integration(self, topic: str, results: Dict):
        """ደረጃ 3: የአፊሊዬት ኢንትግሬሽን"""
        
        self.logger.info("💰 STAGE 3: Affiliate Link Integration")
        
        try:
            # የአፊሊዬት አገናኞችን መጨመር
            content_with_affiliates, monetization_report = await self.affiliate_manager.inject_affiliate_links(
                content=results['content']['content'],
                topic=topic,
                content_type="article",                user_journey_stage="consideration",
                user_intent="research"
            )
            
            results['content']['content_with_affiliates'] = content_with_affiliates
            results['monetization_report'] = monetization_report
            results['stages_completed'].append('affiliate_integration')
            
            # የገቢ መለኪያዎች
            results['metrics']['predicted_revenue'] = monetization_report.get('predicted_total_revenue', 0)
            results['metrics']['affiliate_links_count'] = monetization_report.get('total_injections', 0)
            
            self.logger.info(f"✅ Affiliate Integration Complete | Links: {results['metrics']['affiliate_links_count']} | Predicted Revenue: ${results['metrics']['predicted_revenue']:.2f}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Affiliate integration failed (continuing): {e}")
    
    async def _stage_4_multimedia_enhancement(self, results: Dict):
        """ደረጃ 4: የሙልቲሚዲያ ማሻሻያ"""
        
        self.logger.info("🎨 STAGE 4: Multimedia Enhancement")
        
        try:
            # የሙልቲሚዲያ ማሻሻያ
            enhancement = await self.content_system.multimedia_enhancer.enhance_content_with_multimedia(
                results['content']
            )
            
            results['content']['multimedia_enhancement'] = enhancement
            results['stages_completed'].append('multimedia_enhancement')
            
            # የሙልቲሚዲያ መለኪያዎች
            results['metrics']['multimedia_assets'] = len(enhancement.get('enhancements', {}))
            results['metrics']['enhancement_quality'] = enhancement.get('quality_score', 0)
            
            self.logger.info(f"✅ Multimedia Enhancement Complete | Assets: {results['metrics']['multimedia_assets']} | Quality: {results['metrics']['enhancement_quality']}%")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Multimedia enhancement failed (continuing): {e}")
    
    async def _stage_5_cultural_localization(self, topic: str, 
                                            target_countries: List[str],
                                            results: Dict):
        """ደረጃ 5: የባህል ሎካላይዜሽን"""
        
        self.logger.info(f"🌍 STAGE 5: Cultural Localization for {', '.join(target_countries)}")
        
        try:
            # ለእያንዳንዱ ሀገር የተለየ ይዘት ማመንጨት
            localized_content = await self.content_system.hyper_localizer.produce_geo_optimized_content(                topic=topic,
                target_countries=target_countries
            )
            
            results['localized_content'] = localized_content
            results['stages_completed'].append('cultural_localization')
            
            # የሎካላይዜሽን መለኪያዎች
            results['metrics']['localized_versions'] = len(localized_content)
            
            self.logger.info(f"✅ Cultural Localization Complete | Versions: {results['metrics']['localized_versions']}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Cultural localization failed (continuing): {e}")
    
    async def _stage_6_quality_assurance(self, results: Dict):
        """ደረጃ 6: የጥራት ፈተሻ እና ማረጋገጫ"""
        
        self.logger.info("🔍 STAGE 6: Quality Assurance & Validation")
        
        try:
            # የጥራት ፈተሻ
            quality_check = self.content_system.content_generator.quality_checker.comprehensive_check(
                results['content']['content']
            )
            
            results['quality_assurance'] = quality_check
            results['stages_completed'].append('quality_assurance')
            
            # የጥራት መለኪያዎች
            results['metrics']['final_quality_score'] = quality_check.get('overall_score', 0)
            results['metrics']['readability'] = quality_check.get('readability', 0)
            results['metrics']['seo_score'] = quality_check.get('seo', 0)
            
            self.logger.info(f"✅ Quality Assurance Complete | Final Score: {results['metrics']['final_quality_score']}%")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Quality assurance failed (continuing): {e}")
    
    async def _stage_7_production_report(self, results: Dict):
        """ደረጃ 7: የምርት ሪፖርት ማመንጨት"""
        
        self.logger.info("📊 STAGE 7: Production Report Generation")
        
        try:
            # የሙሉ ሪፖርት ማመንጨት
            production_report = {
                'production_id': results['production_id'],
                'topic': results['topic'],
                'status': results['status'],                'completion_time': results.get('completion_time'),
                'total_duration_seconds': results.get('total_duration_seconds', 0),
                'stages_completed': results['stages_completed'],
                'metrics': results['metrics'],
                'quality_scores': {
                    'content_quality': results['metrics'].get('quality_score', 0),
                    'final_quality': results['metrics'].get('final_quality_score', 0),
                    'readability': results['metrics'].get('readability', 0),
                    'seo': results['metrics'].get('seo_score', 0)
                },
                'monetization': {
                    'affiliate_links': results['metrics'].get('affiliate_links_count', 0),
                    'predicted_revenue': results['metrics'].get('predicted_revenue', 0),
                    'multimedia_assets': results['metrics'].get('multimedia_assets', 0)
                },
                'localization': {
                    'target_countries': len(results.get('localized_content', {})),
                    'versions_created': results['metrics'].get('localized_versions', 0)
                }
            }
            
            results['production_report'] = production_report
            results['stages_completed'].append('production_report')
            
            # ሪፖርቱን ማተም
            self._print_production_summary(production_report)
            
            self.logger.info("✅ Production Report Generated")
            
        except Exception as e:
            self.logger.error(f"⚠️ Production report generation failed: {e}")
    
    def _print_production_summary(self, report: Dict):
        """የምርት ማጠቃለያ ማተም"""
        
        summary = f"""
{'='*70}
🚀 ULTIMATE PRODUCTION COMPLETE
{'='*70}

📊 PRODUCTION SUMMARY
   • Production ID: {report['production_id']}
   • Topic: {report['topic']}
   • Status: {report['status']}
   • Completion Time: {report.get('completion_time', 'N/A')}
   • Total Duration: {report.get('total_duration_seconds', 0):.2f} seconds

📈 QUALITY METRICS
   • Content Quality: {report['quality_scores']['content_quality']}%
   • Final Quality: {report['quality_scores']['final_quality']}%   • Readability: {report['quality_scores']['readability']}%
   • SEO Score: {report['quality_scores']['seo']}%

💰 MONETIZATION METRICS
   • Affiliate Links: {report['monetization']['affiliate_links']}
   • Predicted Revenue: ${report['monetization']['predicted_revenue']:.2f}
   • Multimedia Assets: {report['monetization']['multimedia_assets']}

🌍 LOCALIZATION METRICS
   • Target Countries: {report['localization']['target_countries']}
   • Versions Created: {report['localization']['versions_created']}

✅ STAGES COMPLETED: {len(report.get('stages_completed', []))}
   {chr(10).join([f'   • {stage}' for stage in report.get('stages_completed', [])])}

{'='*70}
        """
        
        print(summary)
        self.logger.info("Production Summary Printed")

# =================== ዋና አፈፃፀም (Main Execution) ===================

async def main():
    """ዋና አፈፃፀም ፋንክሽን"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  🚀 ULTIMATE PRODUCTION MAIN RUNNER v3.0                            ║
║  🎯 Script A + Script B Full Integration                            ║
║  💎 Enterprise-Grade Orchestration                                  ║
║  🔒 Zero Data Loss Production Pipeline                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # ከተጠቃሚ ወይም ከኮማንድ መስመር ውሂብ መውሰድ
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        countries = sys.argv[2].split(',') if len(sys.argv) > 2 else ['US']
        content_type = sys.argv[3] if len(sys.argv) > 3 else 'blog_post'
    else:
        # የነባር ርዕሶች
        topics = [
            "AI-Powered Content Creation Strategies 2026",
            "Digital Marketing Trends for Ethiopian Businesses",
            "Passive Income Streams for Tech Professionals",
            "Building an Online Business from Scratch",
            "Social Media Monetization Techniques"        ]
        
        print("\n📚 Available Topics:")
        for i, t in enumerate(topics, 1):
            print(f"   {i}. {t}")
        
        choice = input("\nSelect topic number (1-5) or enter custom topic: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= 5:
            topic = topics[int(choice) - 1]
        else:
            topic = choice if choice else topics[0]
        
        countries_input = input("Enter target countries (comma-separated, default: US): ").strip()
        countries = [c.strip() for c in countries_input.split(',')] if countries_input else ['US']
        
        content_type = input("Enter content type (blog_post/product_review/how_to_guide): ").strip() or 'blog_post'
    
    print(f"\n🎯 Starting Production for: {topic}")
    print(f"🌍 Target Countries: {', '.join(countries)}")
    print(f"📝 Content Type: {content_type}")
    print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ኦርኬስትሬተሩን መጀመር
    orchestrator = UltimateProductionOrchestrator()
    
    # ሙሉ የምርት ፈረቃ አስተናግድ
    results = await orchestrator.execute_full_production_pipeline(
        topic=topic,
        target_countries=countries,
        content_type=content_type
    )
    
    # ውጤቱን ማስቀመጥ
    output_file = f"production_{results['production_id']}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Production results saved to: {output_file}")
    
    # የስህተት ሪፖርት ካለ ማሳየት
    if results['status'] == 'failed':
        print(f"\n❌ Production Failed!")
        print(f"Error: {results.get('error', 'Unknown error')}")
        print(f"\nCheck logs for detailed error information.")
    
    print(f"\n{'='*70}")
    print(f"🕐 End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
# =================== ፕሮግራሙን መጀመር ===================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Production interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Critical Error: {e}")
        traceback.print_exc()
        sys.exit(1)
