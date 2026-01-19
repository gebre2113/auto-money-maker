#!/usr/bin/env python3
"""
ጀምናይ ሞዴሎች ተገኝነት ሙከራ ስክሪፕት
ይህ ስክሪፕት ለ2026 የተዘመኑ ጎግል ጀምናይ ሞዴሎችን ተገኝነት ይሞክራል
"""

import os
import sys
import time
import json
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# ጎግል ጀነሬቲቭ AI ላይብረሪ አስፈላጊ ነው
try:
    import google.generativeai as genai
    from google.api_core import exceptions, retry
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("ማስጠንቀቂያ: google-generativeai ላይብረሪ አልተጫነም")
    print("እባክዎን ይጫኑት: pip install google-generativeai")

# የሎግ ማዋቀር
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gemini_test.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    """ሞዴል ሁኔታ አይነቶች"""
    AVAILABLE = "ሊጠቀም ይችላል"
    UNAVAILABLE = "አይገኝም"
    LIMITED = "የተገደበ"
    ERROR = "ስህተት"
    RATE_LIMITED = "የፍጥነት ገደብ"

@dataclass
class ModelTestResult:
    """የሞዴል ሙከራ ውጤት"""
    model_name: str
    status: ModelStatus
    response_time: float
    capabilities: Dict[str, bool]
    error_message: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class GeminiModelTester:
    """ጀምናይ ሞዴሎችን የሚሞክር ክፍል"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        ኢኒሻላይዝ ማድረግ
        
        Args:
            api_key: ጎግል AI API ቁልፍ (ባይሰጥ ከተለዋዋጭ አካባቢ ይወሰዳል)
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai ላይብረሪ አልተጫነም")
        
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            logger.error("API ቁልፍ አልተገኘም። GOOGLE_API_KEY አንብበው ያስገቡት።")
            sys.exit(1)
        
        # ጂነራቲቭ AI ኮንፊግ
        genai.configure(api_key=self.api_key)
        
        # ለ2026 የተዘመኑ ሞዴሎች
        self.models_to_test = [
            {
                'name': 'gemini-3-flash',
                'display_name': 'ጀምናይ 3 ፍላሽ',
                'description': 'ፈጣን እና ቀላል ተግባራት ለሚሰሩ ሞዴል',
                'priority': 1
            },
            {
                'name': 'gemini-3-pro',
                'display_name': 'ጀምናይ 3 ፕሮ',
                'description': 'ለአብዛኛዎቹ ስራዎች የተመቻቸ ሞዴል',
                'priority': 2
            },
            {
                'name': 'gemini-3-ultra',
                'display_name': 'ጀምናይ 3 ኡልትራ',
                'description': 'ለሙያዊ እና የምርምር ደረጃ ስራዎች',
                'priority': 3
            },
            {
                'name': 'gemini-3-flash-lite',
                'display_name': 'ጀምናይ 3 ፍላሽ ላይት',
                'description': 'ለሞባይል እና ኃይል ቆጣቢ መሳሪያዎች',
                'priority': 4
            },
            {
                'name': 'gemini-2.5-pro',
                'display_name': 'ጀምናይ 2.5 ፕሮ',
                'description': 'ለተወሰኑ ልዩ ተግባራት',
                'priority': 5
            },
            {
                'name': 'gemini-2.0-flash-exp',
                'display_name': 'ጀምናይ 2.0 ፍላሽ ኤክስፔሪመንታል',
                'description': 'ለሙከራ እና ምርምር',
                'priority': 6
            },
            {
                'name': 'gemini-1.5-flash',
                'display_name': 'ጀምናይ 1.5 ፍላሽ',
                'description': 'መሠረታዊ ፈጣን ሞዴል (መደገፊያ)',
                'priority': 7
            },
            {
                'name': 'gemini-1.5-pro',
                'display_name': 'ጀምናይ 1.5 ፕሮ',
                'description': 'መሠረታዊ ፕሮ ሞዴል (መደገፊያ)',
                'priority': 8
            }
        ]
        
        self.available_models = []
        self.test_results = []
        self.recommended_model = None
        
    def _test_single_model(self, model_name: str, test_prompt: str = "ሰላም። አጭር ምላሽ ስጥ") -> ModelTestResult:
        """
        አንድ ሞዴል ተገኝነት ሙከራ
        
        Args:
            model_name: የሚፈተሽ ሞዴል ስም
            test_prompt: ለሙከራ የሚጠቀም ጥያቄ
        
        Returns:
            ModelTestResult: የሙከራው ውጤት
        """
        start_time = time.time()
        
        try:
            # ሞዴል መፍጠር
            model = genai.GenerativeModel(model_name)
            
            # ቀላል ጥያቄ ላክ
            response = model.generate_content(
                test_prompt,
                generation_config={
                    'max_output_tokens': 50,
                    'temperature': 0.1
                }
            )
            
            response_time = time.time() - start_time
            
            # ችሎታዎችን ማረጋገጫ
            capabilities = {
                'text_generation': bool(response.text),
                'fast_response': response_time < 2.0,
                'reliable': True
            }
            
            return ModelTestResult(
                model_name=model_name,
                status=ModelStatus.AVAILABLE,
                response_time=response_time,
                capabilities=capabilities
            )
            
        except exceptions.NotFound as e:
            logger.warning(f"ሞዴል {model_name} አልተገኘም: {e}")
            return ModelTestResult(
                model_name=model_name,
                status=ModelStatus.UNAVAILABLE,
                response_time=time.time() - start_time,
                capabilities={},
                error_message=str(e)
            )
            
        except exceptions.ResourceExhausted as e:
            logger.warning(f"ሞዴል {model_name} ላይ የፍጥነት ገደብ: {e}")
            return ModelTestResult(
                model_name=model_name,
                status=ModelStatus.RATE_LIMITED,
                response_time=time.time() - start_time,
                capabilities={},
                error_message=str(e)
            )
            
        except Exception as e:
            logger.error(f"ሞዴል {model_name} ላይ ስህተት: {e}")
            return ModelTestResult(
                model_name=model_name,
                status=ModelStatus.ERROR,
                response_time=time.time() - start_time,
                capabilities={},
                error_message=str(e)
            )
    
    @retry.Retry(
        predicate=retry.if_exception_type(
            exceptions.ResourceExhausted,
            exceptions.ServiceUnavailable
        ),
        maximum=3,
        deadline=30
    )
    def test_all_models(self) -> List[ModelTestResult]:
        """
        ሁሉንም ሞዴሎች ይሞክር
        
        Returns:
            የሁሉም ሙከራዎች ውጤት
        """
        logger.info("የጀምናይ ሞዴሎች ተገኝነት ሙከራ እየጀመረ ነው...")
        
        test_results = []
        
        # በቅድሚያ ደረጃ የተደረደሩ ሞዴሎችን መሞከር
        sorted_models = sorted(self.models_to_test, key=lambda x: x['priority'])
        
        for model_info in sorted_models:
            model_name = model_info['name']
            display_name = model_info['display_name']
            
            logger.info(f"ሞዴልን እየፈተሽን ነው: {display_name} ({model_name})")
            
            # ሞዴል ሙከራ
            result = self._test_single_model(model_name)
            test_results.append(result)
            
            # የሚጠቀም ከሆነ ዝርዝር ውስጥ ማኖር
            if result.status == ModelStatus.AVAILABLE:
                self.available_models.append({
                    'name': model_name,
                    'display_name': display_name,
                    'description': model_info['description'],
                    'response_time': result.response_time,
                    'priority': model_info['priority']
                })
            
            # አጭር እረፍት ለመውሰድ
            time.sleep(0.5)
        
        self.test_results = test_results
        self._determine_recommended_model()
        
        return test_results
    
    def _determine_recommended_model(self):
        """ምክረ ሞዴል መወሰን"""
        if not self.available_models:
            self.recommended_model = None
            return
        
        # በፍጥነት እና በቅድሚያ ደረጃ መሠረት መደርደር
        sorted_available = sorted(
            self.available_models,
            key=lambda x: (x['response_time'], x['priority'])
        )
        
        self.recommended_model = sorted_available[0]
    
    def generate_report(self, output_format: str = "text") -> str:
        """
        የሙከራ ሪፖርት ማዘጋጀት
        
        Args:
            output_format: የውጤት ቅርጸት (text, json, html)
        
        Returns:
            የተዘጋጀ ሪፖርት
        """
        if not self.test_results:
            return "ምንም የሙከራ ውጤት የለም። በመጀመሪያ test_all_models() ይጥሩ።"
        
        if output_format == "json":
            return self._generate_json_report()
        elif output_format == "html":
            return self._generate_html_report()
        else:
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """ጽሑፍ ሪፖርት ማዘጋጀት"""
        report_lines = []
        
        # ራእይ መግቢያ
        report_lines.append("=" * 60)
        report_lines.append("የጀምናይ ሞዴሎች ተገኝነት ሙከራ ሪፖርት")
        report_lines.append(f"ጊዜ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # ማጠቃለያ
        available_count = sum(1 for r in self.test_results if r.status == ModelStatus.AVAILABLE)
        total_count = len(self.test_results)
        
        report_lines.append(f"ማጠቃለያ:")
        report_lines.append(f"  - አጠቃላይ የተሞከሩ ሞዴሎች: {total_count}")
        report_lines.append(f"  - የሚጠቀሙ ሞዴሎች: {available_count}")
        report_lines.append(f"  - የማይጠቀሙ ሞዴሎች: {total_count - available_count}")
        report_lines.append("")
        
        # የሚመከር ሞዴል
        if self.recommended_model:
            report_lines.append(f"የሚመከር ሞዴል:")
            report_lines.append(f"  - ስም: {self.recommended_model['display_name']}")
            report_lines.append(f"  - ኮድ: {self.recommended_model['name']}")
            report_lines.append(f"  - የምላሽ ጊዜ: {self.recommended_model['response_time']:.2f} ሰከንድ")
            report_lines.append(f"  - መግለጫ: {self.recommended_model['description']}")
            report_lines.append("")
        
        # ዝርዝር ውጤቶች
        report_lines.append("ዝርዝር ውጤቶች:")
        report_lines.append("-" * 60)
        
        for result in self.test_results:
            status_icon = "✅" if result.status == ModelStatus.AVAILABLE else "❌"
            
            report_lines.append(f"{status_icon} {result.model_name}")
            report_lines.append(f"  ሁኔታ: {result.status.value}")
            
            if result.response_time > 0:
                report_lines.append(f"  የምላሽ ጊዜ: {result.response_time:.2f} ሰከንድ")
            
            if result.error_message:
                report_lines.append(f"  ስህተት: {result.error_message[:100]}...")
            
            report_lines.append("")
        
        # የመጠቀም ምክር
        report_lines.append("=" * 60)
        report_lines.append("የመጠቀም ምክር:")
        
        if self.available_models:
            report_lines.append("1. ለፈጣን ስራዎች: gemini-3-flash ይጠቀሙ")
            report_lines.append("2. ለአጠቃላይ ስራዎች: gemini-3-pro ይጠቀሙ")
            report_lines.append("3. ለሙያዊ ስራዎች: gemini-3-ultra ይጠቀሙ")
            report_lines.append("4. ለሞባይል መተግበሪያዎች: gemini-3-flash-lite ይጠቀሙ")
        else:
            report_lines.append("ምንም የሚጠቀም ሞዴል አልተገኘም።")
            report_lines.append("እባክዎን የAPI ቁልፍዎን ያረጋግጡ።")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def _generate_json_report(self) -> str:
        """JSON ሪፖርት ማዘጋጀት"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tested': len(self.test_results),
                'available': len(self.available_models),
                'unavailable': len(self.test_results) - len(self.available_models)
            },
            'recommended_model': self.recommended_model,
            'available_models': self.available_models,
            'test_results': [asdict(r) for r in self.test_results]
        }
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def _generate_html_report(self) -> str:
        """HTML ሪፖርት ማዘጋጀት"""
        html = f"""
        <!DOCTYPE html>
        <html lang="am">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>የጀምናይ ሞዴሎች ሙከራ ሪፖርት</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; margin: 20px; }}
                .header {{ background-color: #4285f4; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #f1f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .model-card {{ border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin: 10px 0; }}
                .available {{ border-left: 5px solid #34a853; }}
                .unavailable {{ border-left: 5px solid #ea4335; }}
                .recommended {{ background-color: #e8f5e9; border: 2px solid #34a853; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>የጀምናይ ሞዴሎች ተገኝነት ሙከራ ሪፖርት</h1>
                <p>ጊዜ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>ማጠቃለያ</h2>
                <p>አጠቃላይ የተሞከሩ ሞዴሎች: {len(self.test_results)}</p>
                <p>የሚጠቀሙ ሞዴሎች: {len(self.available_models)}</p>
                <p>የማይጠቀሙ ሞዴሎች: {len(self.test_results) - len(self.available_models)}</p>
            </div>
        """
        
        if self.recommended_model:
            html += f"""
            <div class="model-card recommended">
                <h3>🌟 የሚመከር ሞዴል</h3>
                <p><strong>{self.recommended_model['display_name']}</strong> ({self.recommended_model['name']})</p>
                <p>የምላሽ ጊዜ: {self.recommended_model['response_time']:.2f} ሰከንድ</p>
                <p>{self.recommended_model['description']}</p>
            </div>
            """
        
        html += "<h2>የሞዴል ሙከራ ውጤቶች</h2>"
        
        for result in self.test_results:
            status_class = "available" if result.status == ModelStatus.AVAILABLE else "unavailable"
            
            html += f"""
            <div class="model-card {status_class}">
                <h3>{result.model_name}</h3>
                <p><strong>ሁኔታ:</strong> {result.status.value}</p>
                <p><strong>የምላሽ ጊዜ:</strong> {result.response_time:.2f} ሰከንድ</p>
            """
            
            if result.error_message:
                html += f'<p><strong>ስህተት:</strong> {result.error_message[:100]}...</p>'
            
            html += "</div>"
        
        html += """
            <footer>
                <p>© 2026 የጀምናይ ሞዴል ሙከራ መሣሪያ</p>
            </footer>
        </body>
        </html>
        """
        
        return html
    
    def save_report(self, filename: str = "gemini_models_report"):
        """
        ሪፖርት ለማስቀመጥ
        
        Args:
            filename: የፋይል ስም (ቅጥያ አይጨመርም)
        """
        # ጽሑፍ ሪፖርት
        text_report = self.generate_report("text")
        with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        # JSON ሪፖርት
        json_report = self.generate_report("json")
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            f.write(json_report)
        
        # HTML ሪፖርት
        html_report = self.generate_report("html")
        with open(f"{filename}.html", 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        logger.info(f"ሪፖርቶች ተሰብስበዋል: {filename}.txt, {filename}.json, {filename}.html")
    
    def get_available_models(self) -> List[str]:
        """
        የሚጠቀሙ ሞዴሎች ዝርዝር መመለስ
        
        Returns:
            የሚጠቀሙ ሞዴሎች ዝርዝር
        """
        return [model['name'] for model in self.available_models]
    
    def get_best_model(self, use_case: str = "general") -> Optional[str]:
        """
        ለተወሰነ ጥቅም የሚመከር ሞዴል
        
        Args:
            use_case: የመጠቀም አይነት (general, fast, professional, mobile)
        
        Returns:
            የሚመከር ሞዴል ስም
        """
        if not self.available_models:
            return None
        
        use_case_map = {
            'general': ['gemini-3-pro', 'gemini-1.5-pro'],
            'fast': ['gemini-3-flash', 'gemini-1.5-flash'],
            'professional': ['gemini-3-ultra', 'gemini-3-pro'],
            'mobile': ['gemini-3-flash-lite', 'gemini-3-flash'],
            'fallback': ['gemini-1.5-pro', 'gemini-1.5-flash']
        }
        
        preferred_models = use_case_map.get(use_case, use_case_map['general'])
        
        for model_name in preferred_models:
            for available in self.available_models:
                if available['name'] == model_name:
                    return model_name
        
        # ምንም ከተመረጡት ዝርዝር ካልተገኘ የመጀመሪያውን የሚጠቀም ሞዴል መልስ
        return self.available_models[0]['name'] if self.available_models else None


# ቀላል የመጠቀም ምሳሌ
def main():
    """ዋና የመግቢያ ነጥብ"""
    print("የጀምናይ ሞዴሎች ተገኝነት ሙከራ መሣሪያ")
    print("-" * 50)
    
    if not GEMINI_AVAILABLE:
        print("እባክዎን በመጀመሪያ አስፈላጊ ላይብረሪዎችን ይጫኑ:")
        print("pip install google-generativeai")
        return
    
    # API ቁልፍ ማረጋገጫ
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("GOOGLE_API_KEY አልተገኘም።")
        print("እባክዎን እንዲህ ያስገቡት:")
        print("export GOOGLE_API_KEY='your_api_key_here'")
        print("ወይም በቀጥታ ያስገቡ:")
        api_key = input("የጎግል API ቁልፍዎን ያስገቡ: ").strip()
    
    try:
        # ቴስተር መፍጠር
        tester = GeminiModelTester(api_key)
        
        print("ሞዴሎችን እየፈተሽን ነው... እርምት ያድርጉ።")
        print()
        
        # ሁሉንም ሞዴሎች መሞከር
        results = tester.test_all_models()
        
        # ሪፖርት ማሳየት
        report = tester.generate_report("text")
        print(report)
        
        # ሪፖርቶችን ማስቀመጥ
        save_option = input("ሪፖርቶችን ማስቀመጥ ይፈልጋሉ? (አዎ/አይ): ").lower()
        if save_option in ['አዎ', 'y', 'yes', 'ፍሏ', 'ሏ']:
            tester.save_report()
            print("ሪፖርቶች ተሰብስበዋል!")
        
        # የሚጠቀሙ ሞዴሎች ዝርዝር
        available = tester.get_available_models()
        if available:
            print("\nየሚጠቀሙ ሞዴሎች:")
            for model in available:
                print(f"  - {model}")
            
            # ለተለያዩ ዓላማዎች ምክር
            print("\nለተለያዩ ዓላማዎች ምክር:")
            for use_case in ['general', 'fast', 'professional', 'mobile']:
                best_model = tester.get_best_model(use_case)
                if best_model:
                    print(f"  ለ{use_case}: {best_model}")
        
    except Exception as e:
        print(f"ስህተት ተከስቷል: {e}")
        logger.exception("ዋናው ተግባር ላይ ስህተት")


if __name__ == "__main__":
    main()
