#!/usr/bin/env python3
"""
🚀 ULTIMATE PRODUCTION MAIN RUNNER v5.0 - FINAL PRODUCTION VERSION
🎯 Script A (YouTube Affiliate) + Script B (Profit Master) Full Integration
💎 Enterprise-Grade Orchestration with Zero Data Loss
🔒 Production-Ready with Comprehensive Error Handling & Fallback Systems
📊 Real-Time Monitoring, Logging, and Performance Tracking
"""

import asyncio
import logging
import sys
import os
import json
import time
import hashlib
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
import traceback
import textwrap
import warnings

# Suppress specific warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

# =================== የስክሪፕቶች ግንኙነት (Production-Ready Import System) ===================

class ProductionImportSystem:
    """
    ለምርት ዝግጁ የስክሪፕቶች ግንኙነት ስርዓት
    ሁለቱንም ስክሪፕቶች በሙሉ ይጠቀማል እና የራስን ማሻሻል ይችላል
    """
    
    def __init__(self):
        self.script_a = None
        self.script_b = None
        self.import_errors = []
        self.import_success = False
        self.modules_loaded = {}
        
    def import_scripts_with_fallback(self) -> bool:
        """
        ሁለቱንም ስክሪፕቶች መጫን ከራስን ማሻሻል ስርዓት ጋር
        """
        print("\n🔍 Importing Production Scripts...")
        print("="*70)
        
        # Try to import Script A (YouTube Affiliate System)        print("\n📦 Attempting to import Script A (YouTube Affiliate System)...")
        try:
            # Import from actual script files
            from youtube_affiliate_system import (
                YouTubeIntelligenceHunterPro,
                VideoAffiliateIntegrationEngine,
                UltraAffiliateManager,
                GlobalMonetizationIntelligence
            )
            
            self.script_a = {
                'YouTubeIntelligenceHunterPro': YouTubeIntelligenceHunterPro,
                'VideoAffiliateIntegrationEngine': VideoAffiliateIntegrationEngine,
                'UltraAffiliateManager': UltraAffiliateManager,
                'GlobalMonetizationIntelligence': GlobalMonetizationIntelligence
            }
            
            self.modules_loaded['script_a'] = True
            print("✅ Script A imported successfully!")
            
        except ImportError as e:
            error_msg = f"Script A import failed: {e}"
            self.import_errors.append(error_msg)
            print(f"❌ {error_msg}")
            print("⚠️  Script A will not be available")
            self.modules_loaded['script_a'] = False
        
        # Try to import Script B (Profit Master System)
        print("\n📦 Attempting to import Script B (Profit Master System)...")
        try:
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
            
            self.script_b = {
                'UltimateProfitMasterSystem': UltimateProfitMasterSystem,
                'PremiumConfig': PremiumConfig,
                'AdvancedAIContentGenerator': AdvancedAIContentGenerator,
                'CulturalAnthropologistEngine': CulturalAnthropologistEngine,
                'HyperLocalizedContentProducer': HyperLocalizedContentProducer,
                'PremiumMultimediaEnhancer': PremiumMultimediaEnhancer,
                'ProductionManager': ProductionManager,
                'UserInterface': UserInterface            }
            
            self.modules_loaded['script_b'] = True
            print("✅ Script B imported successfully!")
            
        except ImportError as e:
            error_msg = f"Script B import failed: {e}"
            self.import_errors.append(error_msg)
            print(f"❌ {error_msg}")
            print("⚠️  Script B will not be available")
            self.modules_loaded['script_b'] = False
        
        # Determine overall success
        self.import_success = self.modules_loaded.get('script_b', False)
        
        if self.import_success:
            print("\n✅ Production scripts imported successfully!")
            if not self.modules_loaded.get('script_a', True):
                print("⚠️  Note: Running in limited mode (Script A not available)")
        else:
            print("\n❌ Critical error: Script B (Profit Master) is required!")
            print("   Please ensure profit_master_system.py is in the same directory")
        
        print("="*70)
        return self.import_success
    
    def get_import_status(self) -> Dict:
        """የመጫን ሁኔታ ሪፖርት"""
        return {
            'success': self.import_success,
            'script_a_available': self.modules_loaded.get('script_a', False),
            'script_b_available': self.modules_loaded.get('script_b', False),
            'errors': self.import_errors,
            'timestamp': datetime.now().isoformat()
        }

# =================== የሎጂንግ ስርዓት (Production-Grade Logging) ===================

class ProductionLogger:
    """ለምርት ዝግጁ የሎጂንግ ስርዓት"""
    
    def __init__(self, name: str = "production_runner"):
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # Main logger setup
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplication        self.logger.handlers.clear()
        
        # Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler (DEBUG and above)
        file_handler = logging.FileHandler(
            self.log_dir / f'{name}_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Error file handler (ERROR and above)
        error_handler = logging.FileHandler(
            self.log_dir / f'{name}_errors_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        
        self.logger.info("="*70)
        self.logger.info("🚀 Production Logger Initialized")
        self.logger.info("="*70)
    
    def log_stage(self, stage_num: int, stage_name: str, message: str, 
                 level: str = "INFO", details: str = ""):
        """ደረጃ ሎግ ማድረግ"""
        log_msg = f"STAGE {stage_num}: {stage_name} | {message}"
        if details:
            log_msg += f" | {details}"
        
        getattr(self.logger, level.lower())(log_msg)
        
        # ለአስፈላጊ ደረጃዎች ኮንሶል ላይ ማተም
        if level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
            # እዚህ ጋር ያሉት ክፍተቶች (Spaces) እኩል መሆናቸውን አረጋግጥ
            emoji = "✅" if level == "INFO" else "⚠️" if level == "WARNING" else "❌"
            print(f"\n{emoji} STAGE {stage_num}: {stage_name}")
            print(f"   {message}")
            if details:
                print(f"   Details: {details}")
    
    def log_error(self, error: Exception, context: str = "", stage: str = ""):
        """ስህተት ሎግ ማድረግ"""
        error_msg = f"""
        🚨 ERROR in {stage}
        Context: {context}
        Type: {type(error).__name__}
        Message: {str(error)}
        Traceback:
        {traceback.format_exc()}
        """
        
        self.logger.error(error_msg)
        
        # Also print to console
        print(f"\n❌ Error in {stage}: {type(error).__name__}")
        print(f"   Message: {str(error)}")
        print(f"   Context: {context}")
    
    def log_production_summary(self, production_id: str, summary: Dict):
        """የምርት ማጠቃለያ ሎግ ማድረግ"""
        summary_text = f"""
        {'='*70}
        📊 PRODUCTION SUMMARY - {production_id}
        {'='*70}
        
        Status: {summary.get('status', 'unknown')}
        Total Stages: {summary.get('total_stages', 0)}
        Successful: {summary.get('successful_stages', 0)}
        Failed: {summary.get('failed_stages', 0)}
        Success Rate: {summary.get('success_rate', 0):.1f}%
        Total Duration: {summary.get('total_duration', 0):.2f}s
        
        Content Metrics:
        - Word Count: {summary.get('word_count', 0)}
        - Quality Score: {summary.get('quality_score', 0)}%
        - Affiliate Links: {summary.get('affiliate_links', 0)}
        - Multimedia Assets: {summary.get('multimedia_assets', 0)}
        
        Monetization:
        - Predicted Revenue: ${summary.get('predicted_revenue', 0):.2f}
        - Localized Versions: {summary.get('localized_versions', 0)}
        
        {'='*70}
        """        
        self.logger.info(summary_text)
        print(summary_text)

# =================== የአፈፃፀም ክትትል (Performance & Resource Monitoring) ===================

class PerformanceMonitor:
    """የአፈፃፀም እና የሀብት ክትትል"""
    
    def __init__(self):
        self.stage_times = {}
        self.resource_snapshots = {}
        self.start_time = time.time()
        self.memory_usage = []
        
    def start_stage(self, stage_name: str):
        """ደረጃ መጀመር"""
        timestamp = time.time()
        self.stage_times[stage_name] = {
            'start': timestamp,
            'end': None,
            'duration': None
        }
        
        # Record initial resource usage
        self._snapshot_resources(stage_name, 'start')
    
    def end_stage(self, stage_name: str) -> float:
        """ደረጃ መጨረሻ"""
        end_time = time.time()
        
        if stage_name in self.stage_times:
            self.stage_times[stage_name]['end'] = end_time
            duration = end_time - self.stage_times[stage_name]['start']
            self.stage_times[stage_name]['duration'] = duration
            
            # Record final resource usage
            self._snapshot_resources(stage_name, 'end')
            
            return duration
        
        return 0.0
    
    def _snapshot_resources(self, stage_name: str, point: str):
        """የሀብት አጠቃቀም መመዝገቢያ"""
        try:
            import psutil
            
            process = psutil.Process()
            memory_info = process.memory_info()            
            snapshot = {
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_mb': memory_info.rss / (1024 * 1024),
                'memory_percent': process.memory_percent(),
                'timestamp': datetime.now().isoformat()
            }
            
            key = f"{stage_name}_{point}"
            self.resource_snapshots[key] = snapshot
            self.memory_usage.append(memory_info.rss / (1024 * 1024))
            
        except ImportError:
            self.resource_snapshots[f"{stage_name}_{point}"] = {
                'note': 'Resource monitoring unavailable',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_performance_report(self) -> Dict:
        """የአፈፃፀም ሪፖርት"""
        total_duration = time.time() - self.start_time
        
        completed_durations = [
            data['duration'] for data in self.stage_times.values()
            if data['duration'] is not None
        ]
        
        if completed_durations:
            avg_duration = sum(completed_durations) / len(completed_durations)
            max_duration = max(completed_durations)
            min_duration = min(completed_durations)
        else:
            avg_duration = max_duration = min_duration = 0
        
        return {
            'total_duration': round(total_duration, 2),
            'total_stages': len(self.stage_times),
            'completed_stages': len(completed_durations),
            'average_stage_duration': round(avg_duration, 2),
            'longest_stage': round(max_duration, 2),
            'shortest_stage': round(min_duration, 2),
            'peak_memory_mb': round(max(self.memory_usage), 2) if self.memory_usage else 0,
            'stage_breakdown': {
                stage: round(data['duration'], 2)
                for stage, data in self.stage_times.items()
                if data['duration'] is not None
            }
        }
    
    def print_report(self):
        """የአፈፃፀም ሪፖርት ማተም"""
        report = self.get_performance_report()
        
        print("\n" + "="*70)
        print("📈 PERFORMANCE REPORT")
        print("="*70)
        # የተቀረው የሪፖርት ኮድ እዚህ ይቀጥላል...
        
        print("\n" + "="*70)
        print("📈 PERFORMANCE REPORT")
        print("="*70)
        print(f"⏱️  Total Duration: {report['total_duration']}s")
        print(f"📊 Total Stages: {report['total_stages']}")
        print(f"✅ Completed Stages: {report['completed_stages']}")
        print(f"📈 Average Stage Duration: {report['average_stage_duration']}s")
        print(f"🐌 Longest Stage: {report['longest_stage']}s")
        print(f"⚡ Shortest Stage: {report['shortest_stage']}s")
        print(f"💾 Peak Memory Usage: {report['peak_memory_mb']} MB")
        
        print("\n📋 Stage Breakdown:")
        for stage, duration in report['stage_breakdown'].items():
            print(f"   • {stage}: {duration}s")
        
        print("="*70)

# =================== ዋና ኦርኬስትሬተር (Production Orchestrator) ===================

class ProductionOrchestrator:
    """
    ዋና የምርት ኦርኬስትሬተር
    ሁለቱንም ስክሪፕቶች በሙሉ ይጠቀማል
    """
    
    def __init__(self):
        # Initialize logging
        self.logger = ProductionLogger("orchestrator")
        
        # Initialize performance monitoring
        self.monitor = PerformanceMonitor()
        
        # Import scripts
        self.importer = ProductionImportSystem()
        if not self.importer.import_scripts_with_fallback():
            raise RuntimeError("Critical scripts could not be imported")
        
        # Initialize systems
        self._initialize_systems()
        
        self.logger.logger.info("✅ Production Orchestrator Initialized")
    
    def _initialize_systems(self):
        """ሁሉንም ስርዓቶች መጀመር"""
        
        import_status = self.importer.get_import_status()
        # እዚህ ጋር ለሁለት መስመር መከፈላቸውን አረጋግጥ
        self.script_a_available = import_status['script_a_available']
        self.script_b_available = import_status['script_b_available']
        
        self.logger.logger.info(f"System Status: Script A: {'✅' if self.script_a_available else '❌'}, "
                              f"Script B: {'✅' if self.script_b_available else '❌'}")
        
        # Initialize Script B systems (required)
        if self.script_b_available:
            try:
                PremiumConfig = self.importer.script_b['PremiumConfig']
                self.config = PremiumConfig()
                self.logger.logger.info("✅ Config initialized")
                
                UltimateProfitMasterSystem = self.importer.script_b['UltimateProfitMasterSystem']
                self.content_system = UltimateProfitMasterSystem(self.config)
                self.logger.logger.info("✅ Content system initialized")
                
                ProductionManager = self.importer.script_b['ProductionManager']
                self.production_manager = ProductionManager(self.config)
                self.logger.logger.info("✅ Production manager initialized")
                
            except Exception as e:
                self.logger.log_error(e, "Script B initialization", "SystemInit")
                raise RuntimeError(f"Script B initialization failed: {e}")
        
        # Initialize Script A systems (optional)
        if self.script_a_available:
            try:
                YouTubeIntelligenceHunterPro = self.importer.script_a['YouTubeIntelligenceHunterPro']
                self.youtube_hunter = YouTubeIntelligenceHunterPro()
                self.logger.logger.info("✅ YouTube hunter initialized")
                
                VideoAffiliateIntegrationEngine = self.importer.script_a['VideoAffiliateIntegrationEngine']
                self.video_engine = VideoAffiliateIntegrationEngine(
                    enable_ethical_mode=True,
                    enable_tracking=True
                )
                self.logger.logger.info("✅ Video engine initialized")
                
                UltraAffiliateManager = self.importer.script_a['UltraAffiliateManager']
                self.affiliate_manager = UltraAffiliateManager(
                    user_geo="US",
                    user_segment="premium",
                    ethical_mode=True,
                    enable_ab_testing=True
                )
                self.logger.logger.info("✅ Affiliate manager initialized")
                
            except Exception as e:
                self.logger.log_error(e, "Script A initialization", "SystemInit")
                self.script_a_available = False    
    async def execute_production(self, topic: str, 
                               target_countries: List[str] = None,
                               content_type: str = "blog_post") -> Dict:
        """
        ሙሉ የምርት ፈረቃ አስተናግድ
        """
        
        production_id = f"prod_{hashlib.md5(f'{topic}{datetime.now()}'.encode()).hexdigest()[:12]}"
        self.logger.logger.info(f"\n🚀 Starting Production: {production_id}")
        self.logger.logger.info(f"   Topic: {topic}")
        self.logger.logger.info(f"   Countries: {target_countries or ['US']}")
        self.logger.logger.info(f"   Content Type: {content_type}")
        
        results = {
            'production_id': production_id,
            'topic': topic,
            'target_countries': target_countries or ['US'],
            'content_type': content_type,
            'status': 'processing',
            'stages_completed': [],
            'stages_failed': [],
            'errors': [],
            'metrics': {},
            'timestamps': {
                'start': datetime.now().isoformat(),
                'end': None
            }
        }
        
        try:
            # STAGE 1: YouTube Video Search (Optional)
            if self.script_a_available and hasattr(self, 'youtube_hunter'):
                await self._stage_1_youtube_search(topic, results)
            
            # STAGE 2: Content Generation (Required)
            await self._stage_2_content_generation(topic, target_countries, content_type, results)
            
            # STAGE 3: Affiliate Integration (Optional)
            if self.script_a_available and hasattr(self, 'affiliate_manager'):
                await self._stage_3_affiliate_integration(topic, results)
            
            # STAGE 4: Multimedia Enhancement (Optional)
            if hasattr(self, 'content_system'):
                await self._stage_4_multimedia_enhancement(results)
            
            # STAGE 5: Cultural Localization (Optional)
            if hasattr(self, 'content_system') and target_countries:
                await self._stage_5_cultural_localization(topic, target_countries, results)
                        # STAGE 6: Quality Assurance
            await self._stage_6_quality_assurance(results)
            
            # STAGE 7: Production Report
            await self._stage_7_production_report(results)
            
            # Finalize
            results['status'] = 'completed'
            results['timestamps']['end'] = datetime.now().isoformat()
            
            # Generate summary
            summary = self._generate_summary(results)
            self.logger.log_production_summary(production_id, summary)
            
            self.logger.logger.info(f"✅ Production {production_id} completed successfully")
            
        except Exception as e:
            self.logger.log_error(e, f"Production pipeline for {topic}", "ProductionPipeline")
            results['status'] = 'failed'
            results['error'] = str(e)
            results['error_traceback'] = traceback.format_exc()
            results['timestamps']['end'] = datetime.now().isoformat()
        
        finally:
            # Always save results
            await self._save_results(results)
        
        return results
    
    async def _stage_1_youtube_search(self, topic: str, results: Dict):
        """STAGE 1: YouTube Video Search"""
        self.monitor.start_stage('youtube_search')
        self.logger.log_stage(1, "YouTube Video Search", f"Searching for: {topic}")
        
        try:
            videos = await self.youtube_hunter.find_relevant_videos(
                topic=topic,
                country="US",
                max_results=5
            )
            
            results['youtube_videos'] = videos
            results['stages_completed'].append('youtube_search')
            
            duration = self.monitor.end_stage('youtube_search')
            self.logger.log_stage(1, "YouTube Video Search", 
                                f"Found {len(videos)} videos", "INFO",
                                f"Duration: {duration:.2f}s")
            
            results['metrics']['youtube_videos_found'] = len(videos)            
        except Exception as e:
            self.logger.log_error(e, "YouTube search", "Stage 1")
            results['stages_failed'].append('youtube_search')
            results['errors'].append(str(e))
            self.monitor.end_stage('youtube_search')
    
    async def _stage_2_content_generation(self, topic: str, 
                                         target_countries: List[str],
                                         content_type: str,
                                         results: Dict):
        """STAGE 2: Content Generation"""
        self.monitor.start_stage('content_generation')
        self.logger.log_stage(2, "Content Generation", 
                            f"Topic: {topic} | Type: {content_type}")
        
        try:
            content_result = await self.content_system.full_production_pipeline(
                topic=topic,
                target_countries=target_countries
            )
            
            results['content'] = content_result
            results['stages_completed'].append('content_generation')
            
            duration = self.monitor.end_stage('content_generation')
            self.logger.log_stage(2, "Content Generation",
                                f"Generated {content_result.get('word_count', 0)} words",
                                "INFO", f"Duration: {duration:.2f}s")
            
            # Update metrics
            results['metrics'].update({
                'word_count': content_result.get('word_count', 0),
                'quality_score': content_result.get('quality_report', {}).get('overall_score', 0),
                'generation_time': content_result.get('generation_time', 0),
                'readability': content_result.get('quality_report', {}).get('readability', 0),
                'seo_score': content_result.get('quality_report', {}).get('seo', 0)
            })
            
        except Exception as e:
            self.logger.log_error(e, "Content generation", "Stage 2")
            results['stages_failed'].append('content_generation')
            results['errors'].append(str(e))
            self.monitor.end_stage('content_generation')
            raise  # This is critical, so re-raise
    
    async def _stage_3_affiliate_integration(self, topic: str, results: Dict):
        """STAGE 3: Affiliate Integration"""
        self.monitor.start_stage('affiliate_integration')
        self.logger.log_stage(3, "Affiliate Integration", topic)        
        try:
            content_text = results['content'].get('content', '')
            
            if content_text:
                content_with_affiliates, monetization_report = await self.affiliate_manager.inject_affiliate_links(
                    content=content_text,
                    topic=topic,
                    content_type="article",
                    user_journey_stage="consideration",
                    user_intent="research"
                )
                
                results['content']['content_with_affiliates'] = content_with_affiliates
                results['monetization_report'] = monetization_report
                results['stages_completed'].append('affiliate_integration')
                
                duration = self.monitor.end_stage('affiliate_integration')
                links_count = monetization_report.get('total_injections', 0)
                self.logger.log_stage(3, "Affiliate Integration",
                                    f"Added {links_count} affiliate links",
                                    "INFO", f"Duration: {duration:.2f}s")
                
                results['metrics'].update({
                    'affiliate_links_count': links_count,
                    'predicted_revenue': monetization_report.get('predicted_total_revenue', 0)
                })
            else:
                raise ValueError("No content available for affiliate integration")
                
        except Exception as e:
            self.logger.log_error(e, "Affiliate integration", "Stage 3")
            results['stages_failed'].append('affiliate_integration')
            results['errors'].append(str(e))
            self.monitor.end_stage('affiliate_integration')
    
    async def _stage_4_multimedia_enhancement(self, results: Dict):
        """STAGE 4: Multimedia Enhancement"""
        self.monitor.start_stage('multimedia_enhancement')
        self.logger.log_stage(4, "Multimedia Enhancement", "Adding audio, video, visuals")
        
        try:
            enhancement = await self.content_system.multimedia_enhancer.enhance_content_with_multimedia(
                results['content']
            )
            
            results['content']['multimedia_enhancement'] = enhancement
            results['stages_completed'].append('multimedia_enhancement')
            
            # --- እዚህ ጋር ነው መለያየት ያለባቸው ---
            duration = self.monitor.end_stage('multimedia_enhancement')
            assets_count = len(enhancement.get('enhancements', {}))
            # ------------------------------------
            
            self.logger.log_stage(4, "Multimedia Enhancement",
                                f"Created {assets_count} multimedia assets",
                                "INFO", f"Duration: {duration:.2f}s")
            
            results['metrics'].update({
                'multimedia_assets': assets_count,
                'enhancement_quality': enhancement.get('quality_score', 0)
            })
            
        except Exception as e:
            self.logger.log_error(e, "Multimedia enhancement", "Stage 4")
            results['stages_failed'].append('multimedia_enhancement')
            results['errors'].append(str(e))
            self.monitor.end_stage('multimedia_enhancement') 
            
        except Exception as e:
            self.logger.log_error(e, "Multimedia enhancement", "Stage 4")
            results['stages_failed'].append('multimedia_enhancement')
            results['errors'].append(str(e))
            self.monitor.end_stage('multimedia_enhancement')
    
    async def _stage_5_cultural_localization(self, topic: str, 
                                            target_countries: List[str],
                                            results: Dict):
        """STAGE 5: Cultural Localization"""
        self.monitor.start_stage('cultural_localization')
        self.logger.log_stage(5, "Cultural Localization", 
                            f"Countries: {', '.join(target_countries)}")
        
        try:
            localized_content = await self.content_system.hyper_localizer.produce_geo_optimized_content(
                topic=topic,
                target_countries=target_countries
            )
            
            results['localized_content'] = localized_content
            results['stages_completed'].append('cultural_localization')
            
            duration = self.monitor.end_stage('cultural_localization')
            versions_count = len(localized_content)
            self.logger.log_stage(5, "Cultural Localization",
                                f"Created {versions_count} localized versions",
                                "INFO", f"Duration: {duration:.2f}s")
            
            results['metrics']['localized_versions'] = versions_count
            
        except Exception as e:
            self.logger.log_error(e, "Cultural localization", "Stage 5")
            results['stages_failed'].append('cultural_localization')
            results['errors'].append(str(e))
            self.monitor.end_stage('cultural_localization')
    
    async def _stage_6_quality_assurance(self, results: Dict):
        """STAGE 6: Quality Assurance"""
        # እነዚህ ሁለት መስመሮች የግድ መለየት አለባቸው
        self.monitor.start_stage('quality_assurance')
        self.logger.log_stage(6, "Quality Assurance", "Final quality check")
        
        try:
            # Get final quality score
            final_quality = results['metrics'].get('quality_score', 0)
            
            results['stages_completed'].append('quality_assurance')
            results['metrics']['final_quality_score'] = final_quality
            
            duration = self.monitor.end_stage('quality_assurance')
            self.logger.log_stage(6, "Quality Assurance",
                                f"Quality score: {final_quality}%",
                                "INFO", f"Duration: {duration:.2f}s")
            
        except Exception as e:
            self.logger.log_error(e, "Quality assurance", "Stage 6")
            results['stages_failed'].append('quality_assurance')
            results['errors'].append(str(e))
            self.monitor.end_stage('quality_assurance')

    async def _stage_7_production_report(self, results: Dict):
        """STAGE 7: Production Report"""
        self.monitor.start_stage('production_report')
        self.logger.log_stage(7, "Production Report", "Generating final report")
        
        try:
            report = self._generate_production_report(results)
            results['production_report'] = report
            results['stages_completed'].append('production_report')
            
            duration = self.monitor.end_stage('production_report')
            self.logger.log_stage(7, "Production Report",
                                "Report generated successfully",
                                "INFO", f"Duration: {duration:.2f}s")
            
        except Exception as e:
            self.logger.log_error(e, "Production report", "Stage 7")
            results['stages_failed'].append('production_report')
            results['errors'].append(str(e))
            self.monitor.end_stage('production_report')
    
    def _generate_production_report(self, results: Dict) -> Dict:
        """የምርት ሪፖርት ማመንጨት"""
        
        total_stages = len(results['stages_completed']) + len(results['stages_failed'])
        successful_stages = len(results['stages_completed'])
        success_rate = (successful_stages / total_stages * 100) if total_stages > 0 else 0
        
        performance = self.monitor.get_performance_report()
        
        # return የሚለው ቃል ከ performance ጋር እኩል መሆን አለበት (ትርፍ ስፔስ የለም)
        return {
            'summary': {
                'production_id': results['production_id'],
                'topic': results['topic'],
                'status': results['status'],
                'success_rate': round(success_rate, 2),
                'total_duration_seconds': performance['total_duration'],
                'start_time': results['timestamps']['start'],
                'end_time': results['timestamps']['end']
            },
            'stages': {
                'completed': results['stages_completed'],
                'failed': results['stages_failed'],
                'total': total_stages,
                'successful': successful_stages
            },
            'performance': performance,
            'content_metrics': results['metrics'],
            'monetization': results.get('monetization_report', {}),
            'localization': {
                'countries_targeted': len(results['target_countries']),
                'versions_created': results['metrics'].get('localized_versions', 0)
            }
        }
    
    def _generate_summary(self, results: Dict) -> Dict:
        """ማጠቃለያ ማመንጨት"""
        
        total_stages = len(results['stages_completed']) + len(results['stages_failed'])
        successful_stages = len(results['stages_completed'])
        success_rate = (successful_stages / total_stages * 100) if total_stages > 0 else 0
        
        return {
            'status': results['status'],
            'total_stages': total_stages,
            'successful_stages': successful_stages,
            'failed_stages': len(results['stages_failed']),
            'success_rate': success_rate,
            'total_duration': self.monitor.get_performance_report()['total_duration'],
            'word_count': results['metrics'].get('word_count', 0),
            'quality_score': results['metrics'].get('final_quality_score', 0),
            'affiliate_links': results['metrics'].get('affiliate_links_count', 0),
            'predicted_revenue': results['metrics'].get('predicted_revenue', 0),
            'multimedia_assets': results['metrics'].get('multimedia_assets', 0),
            'localized_versions': results['metrics'].get('localized_versions', 0)
        }
    
    async def _save_results(self, results: Dict):
        """ውጤቶችን ማስቀመጥ"""
        # 'try:' መስመር ከበላዩ ካለው ማብራሪያ ጋር እኩል መስመር ላይ መሆን አለበት
        try:
            output_dir = Path('production_outputs')
            output_dir.mkdir(exist_ok=True)
            
            production_id = results['production_id']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Save full JSON results
            json_file = output_dir / f"production_{production_id}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.logger.info(f"✅ Results saved to: {json_file}")
            
            # Save summary text file
            summary_file = output_dir / f"summary_{production_id}_{timestamp}.txt"
            summary = self._generate_text_summary(results)
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            self.logger.logger.info(f"✅ Summary saved to: {summary_file}")

        except Exception as e:
            self.logger.log_error(e, "Saving results", "SaveResults")
    
    def _generate_text_summary(self, results: Dict) -> str:
        """ጽሑፍ ማጠቃለያ ማመንጨት"""
        
        summary = f"""
{'='*70}
🚀 ULTIMATE PRODUCTION RUNNER - RESULTS SUMMARY
{'='*70}

📋 PRODUCTION DETAILS
   ID: {results.get('production_id')}
   Topic: {results.get('topic')}
   Status: {results.get('status')}
   Start: {results.get('timestamps', {}).get('start')}
   End: {results.get('timestamps', {}).get('end')}

📊 STAGE PERFORMANCE
   Total Stages: {len(results.get('stages_completed', [])) + len(results.get('stages_failed', []))}
   Completed: {len(results.get('stages_completed', []))}
   Failed: {len(results.get('stages_failed', []))}
   Success Rate: {((len(results.get('stages_completed', [])) / (len(results.get('stages_completed', [])) + len(results.get('stages_failed', []))) * 100) if (len(results.get('stages_completed', [])) + len(results.get('stages_failed', []))) > 0 else 0):.1f}%

✅ COMPLETED STAGES:
{chr(10).join([f'   • {stage}' for stage in results.get('stages_completed', [])])}

❌ FAILED STAGES:{chr(10).join([f'   • {stage}' for stage in results.get('stages_failed', [])])}

📈 CONTENT METRICS
   Word Count: {results.get('metrics', {}).get('word_count', 0)}
   Quality Score: {results.get('metrics', {}).get('quality_score', 0)}%
   Final Quality: {results.get('metrics', {}).get('final_quality_score', 0)}%
   Readability: {results.get('metrics', {}).get('readability', 0)}%
   SEO Score: {results.get('metrics', {}).get('seo_score', 0)}%

💰 MONETIZATION
   Affiliate Links: {results.get('metrics', {}).get('affiliate_links_count', 0)}
   Predicted Revenue: ${results.get('metrics', {}).get('predicted_revenue', 0):.2f}

🌍 LOCALIZATION
   Target Countries: {len(results.get('target_countries', []))}
   Localized Versions: {results.get('metrics', {}).get('localized_versions', 0)}

🎬 MULTIMEDIA
   Assets Created: {results.get('metrics', {}).get('multimedia_assets', 0)}

{'='*70}
        """
        
        return summary
    
    def print_system_status(self):
        """የስርዓት ሁኔታ ማሳየት"""
        
        status = f"""
{'='*70}
🔧 SYSTEM STATUS
{'='*70}

📦 IMPORT STATUS
   Script A (YouTube Affiliate): {'✅ Loaded' if self.script_a_available else '❌ Not Available'}
   Script B (Profit Master): {'✅ Loaded' if self.script_b_available else '❌ Not Available'}

🚀 AVAILABLE COMPONENTS:
   • YouTube Intelligence: {'✅' if hasattr(self, 'youtube_hunter') else '❌'}
   • Content Generation: {'✅' if hasattr(self, 'content_system') else '❌'}
   • Affiliate Manager: {'✅' if hasattr(self, 'affiliate_manager') else '❌'}
   • Video Engine: {'✅' if hasattr(self, 'video_engine') else '❌'}
   • Production Manager: {'✅' if hasattr(self, 'production_manager') else '❌'}

📊 PERFORMANCE:
   Monitoring Active: ✅
   Resource Tracking: {'✅' if hasattr(self.monitor, 'memory_usage') else '⚠️ Limited'}

🛠️ OPERATIONAL MODES:
   • Full Integration: {'✅ Ready' if self.script_a_available and self.script_b_available else '⚠️ Limited'}   • Content Only: {'✅ Ready' if self.script_b_available else '❌ Not Available'}
   • Affiliate Only: {'✅ Ready' if self.script_a_available else '❌ Not Available'}

{'='*70}
        """
        
        print(status)

# =================== ዋና አፈፃፀም (Main Execution) ===================

async def main():
    """ዋና አፈፃፀም"""
    
    # Display banner
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  🚀 ULTIMATE PRODUCTION MAIN RUNNER v5.0                            ║
║  🎯 Script A + Script B Full Integration                            ║
║  💎 Enterprise-Grade Orchestration                                  ║
║  🔒 Production-Ready with Zero Data Loss                            ║
║  📊 Real-Time Monitoring & Performance Tracking                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    
    print(banner)
    print(f"🕐 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Initialize orchestrator
    try:
        orchestrator = ProductionOrchestrator()
        orchestrator.print_system_status()
    except Exception as e:
        print(f"\n❌ Failed to initialize orchestrator: {e}")
        return
    
    # Get user input
    print("\n📝 Please provide production details:")
    
    # Topic selection
    topics = [
        "AI-Powered Content Creation Strategies 2026",
        "Digital Marketing Trends for Ethiopian Businesses",
        "Passive Income Streams for Tech Professionals",
        "Building an Online Business from Scratch",
        "Social Media Monetization Techniques",
        "Custom Topic (Enter your own)"
    ]    
    print("\n📚 Available Topics:")
    for i, t in enumerate(topics, 1):
        print(f"   {i}. {t}")
    
    while True:
        choice = input("\nSelect topic number (1-6): ").strip()
        
        if choice == '6':
            topic = input("Enter your custom topic: ").strip()
            if topic:
                break
            else:
                print("❌ Please enter a valid topic")
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            topic = topics[int(choice) - 1]
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-6")
    
    # Target countries
    countries_input = input("\nEnter target countries (comma-separated, default: US): ").strip()
    countries = [c.strip() for c in countries_input.split(',')] if countries_input else ['US']
    
    # Content type
    content_types = ['blog_post', 'product_review', 'how_to_guide', 'general']
    print(f"\n📋 Available Content Types: {', '.join(content_types)}")
    
    content_type = input("Enter content type (default: blog_post): ").strip()
    if not content_type or content_type not in content_types:
        content_type = 'blog_post'
    
    # Summary
    print("\n" + "="*70)
    print("🎯 PRODUCTION CONFIGURATION")
    print("="*70)
    print(f"📝 Topic: {topic}")
    print(f"🌍 Target Countries: {', '.join(countries)}")
    print(f"📋 Content Type: {content_type}")
    print("="*70)
    
    # Confirm
    confirm = input("\nStart production? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', 'yep', 'yeah']:
        print("\n⚠️ Production cancelled by user")
        return
    
    print(f"\n🚀 Starting production pipeline...")
    print("⏳ This may take several minutes. Please wait...")
        try:
        # Execute production
        results = await orchestrator.execute_production(
            topic=topic,
            target_countries=countries,
            content_type=content_type
        )
        
        # Print performance report
        orchestrator.monitor.print_report()
        
        # Final summary
        print("\n" + "="*70)
        print("🎉 PRODUCTION COMPLETE!")
        print("="*70)
        
        if results['status'] == 'completed':
            print(f"✅ Production {results['production_id']} completed successfully!")
            print(f"📊 {len(results['stages_completed'])}/{len(results['stages_completed']) + len(results['stages_failed'])} stages successful")
            
            if results.get('metrics'):
                print(f"📝 Word Count: {results['metrics'].get('word_count', 0)}")
                print(f"💰 Predicted Revenue: ${results['metrics'].get('predicted_revenue', 0):.2f}")
                print(f"🌍 Localized Versions: {results['metrics'].get('localized_versions', 0)}")
            
            print(f"\n💾 Results saved to: production_outputs/")
            
        else:
            print(f"❌ Production failed: {results.get('error', 'Unknown error')}")
            print(f"📋 Check logs for details: logs/")
    
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        traceback.print_exc()

# =================== ፕሮግራሙን መጀመር ===================

if __name__ == "__main__":
    # Handle keyboard interrupt gracefully
    def signal_handler(sig, frame):
        print("\n\n⚠️ Production interrupted by user")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("🚀 Ultimate Production Runner v5.0 - Starting...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:        print("\n\n⚠️ Production interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
