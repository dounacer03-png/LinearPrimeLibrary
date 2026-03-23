"""
Analyzer module for LinearPrimeLibrary
وحدة التحليل المتقدم للمعادلات
"""

from sympy import primerange
from collections import Counter
import numpy as np
from typing import Dict, List, Tuple
from .core import LinearPrimeLibrary, EquationInfo, Cycle


class StatisticalAnalyzer:
    """محلل إحصائي متقدم"""
    
    def __init__(self, library: LinearPrimeLibrary):
        self.library = library
    
    def analyze_path_distribution(self, n: int, m: int, limit: int = 100000) -> Dict:
        """
        تحليل توزيع أطوال المسارات
        
        Returns:
            dict: إحصائيات توزيع الأطوال
        """
        info = self.library.analyze_equation(n, m, limit)
        
        # محاكاة لتوزيع الأطوال (في الإصدار الكامل ستكون بيانات حقيقية)
        return {
            'avg_length': info.avg_path_length,
            'max_length': info.max_path_length,
            'min_length': 1,
            'std_dev': info.avg_path_length * 0.5,  # تقدير
            'distribution': {
                'short_10': info.total_primes * 0.3,
                'medium_20': info.total_primes * 0.5,
                'long_30': info.total_primes * 0.2
            }
        }
    
    def compare_equations(self, eq1: Tuple[int, int], eq2: Tuple[int, int], limit: int = 100000) -> Dict:
        """
        مقارنة معادلتين
        
        Args:
            eq1: (n1, m1)
            eq2: (n2, m2)
            limit: الحد الأعلى للتحليل
            
        Returns:
            dict: نتائج المقارنة
        """
        info1 = self.library.analyze_equation(eq1[0], eq1[1], limit)
        info2 = self.library.analyze_equation(eq2[0], eq2[1], limit)
        
        return {
            'eq1': {
                'formula': info1.get_formula(),
                'avg_length': info1.avg_path_length,
                'max_length': info1.max_path_length,
                'cycles_count': len(info1.cycles),
                'security_bits': info1.security_bits
            },
            'eq2': {
                'formula': info2.get_formula(),
                'avg_length': info2.avg_path_length,
                'max_length': info2.max_path_length,
                'cycles_count': len(info2.cycles),
                'security_bits': info2.security_bits
            },
            'difference': {
                'avg_length': info1.avg_path_length - info2.avg_path_length,
                'max_length': info1.max_path_length - info2.max_path_length,
                'cycles': len(info1.cycles) - len(info2.cycles)
            }
        }
    
    def get_security_recommendation(self, required_bits: int = 128) -> List[Tuple[int, int]]:
        """
        الحصول على توصيات للمعادلات المناسبة حسب مستوى الأمان المطلوب
        
        Args:
            required_bits: مستوى الأمان المطلوب بالبت
            
        Returns:
            list: قائمة بالمعادلات الموصى بها
        """
        # المعادلات المعروفة بمستويات أمانها
        known_equations = [
            (3, 1),   # 8x-1 - 74 بت
            (3, 7),   # 8x-7 - 60 بت
            (4, 1),   # 16x-1 - 70 بت
        ]
        
        recommendations = []
        for n, m in known_equations:
            info = self.library.analyze_equation(n, m, limit=50000)
            if info.security_bits >= required_bits:
                recommendations.append((n, m))
        
        return recommendations


class CycleAnalyzer:
    """محلل الدورات"""
    
    def __init__(self, library: LinearPrimeLibrary):
        self.library = library
    
    def get_cycle_info(self, n: int, m: int, limit: int = 100000) -> Dict:
        """
        الحصول على معلومات مفصلة عن دورات معادلة
        
        Returns:
            dict: معلومات عن الدورات
        """
        info = self.library.analyze_equation(n, m, limit)
        
        cycles_info = []
        for cycle in info.cycles:
            cycles_info.append({
                'elements': cycle.elements,
                'length': cycle.length,
                'max_element': max(cycle.elements),
                'min_element': min(cycle.elements),
                'avg_element': sum(cycle.elements) / len(cycle.elements)
            })
        
        return {
            'formula': info.get_formula(),
            'total_cycles': len(info.cycles),
            'cycles': cycles_info,
            'dominant_endpoint': list(info.endpoint_distribution.keys())[0] if info.endpoint_distribution else None,
            'dominant_percentage': list(info.endpoint_distribution.values())[0] if info.endpoint_distribution else 0
        }
    
    def find_longest_cycle(self, max_n: int = 4, max_m: int = 31, limit: int = 100000) -> Dict:
        """
        البحث عن أطول دورة بين المعادلات
        
        Returns:
            dict: معلومات عن أطول دورة
        """
        longest_cycle = None
        max_length = 0
        best_equation = None
        
        for n in range(1, max_n + 1):
            for m in range(1, max_m + 1, 2):  # m فردي فقط
                try:
                    info = self.library.analyze_equation(n, m, limit)
                    for cycle in info.cycles:
                        if cycle.length > max_length:
                            max_length = cycle.length
                            longest_cycle = cycle
                            best_equation = (n, m)
                except:
                    continue
        
        return {
            'equation': f"{2**best_equation[0]}x - {best_equation[1]}" if best_equation else None,
            'cycle_length': max_length,
            'cycle_elements': longest_cycle.elements if longest_cycle else None
        }
