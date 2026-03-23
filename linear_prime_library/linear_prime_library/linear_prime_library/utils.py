"""
Utilities module for LinearPrimeLibrary
وحدة الأدوات المساعدة
"""

from sympy import primerange, isprime
import secrets
from enum import Enum
from typing import Tuple, Optional


class SecurityLevel(Enum):
    """مستويات الأمان"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


def generate_prime_key(min_size: int = 1000, max_size: int = 1000000) -> int:
    """
    توليد مفتاح أولي عشوائي
    
    Args:
        min_size: الحد الأدنى
        max_size: الحد الأقصى
        
    Returns:
        int: عدد أولي عشوائي
    """
    primes = list(primerange(min_size, max_size))
    if not primes:
        # إذا كان النطاق صغيراً، نوسعه
        primes = list(primerange(min_size, max_size * 2))
    
    return secrets.choice(primes)


def get_recommended_equation(security_level: SecurityLevel) -> Tuple[int, int]:
    """
    الحصول على المعادلة الموصى بها حسب مستوى الأمان
    
    Args:
        security_level: مستوى الأمان المطلوب
        
    Returns:
        tuple: (n, m) للمعادلة الموصى بها
    """
    recommendations = {
        SecurityLevel.LOW: (3, 7),     # 8x-7 - سريع
        SecurityLevel.MEDIUM: (3, 1),  # 8x-1 - متوازن
        SecurityLevel.HIGH: (4, 1),    # 16x-1 - تنوع
        SecurityLevel.ULTRA: (5, 1)    # 32x-1 - أقصى أمان
    }
    
    return recommendations[security_level]


def format_path(path: list) -> str:
    """
    تنسيق المسار للعرض
    
    Args:
        path: قائمة الأعداد في المسار
        
    Returns:
        str: المسار المنسق
    """
    if len(path) <= 10:
        return ' → '.join(map(str, path))
    else:
        first_part = ' → '.join(map(str, path[:5]))
        last_part = ' → '.join(map(str, path[-3:]))
        return f"{first_part} → ... → {last_part}"


def calculate_security_strength(path_length: int, convergence_points: int) -> int:
    """
    حساب قوة الأمان بناءً على طول المسار ونقاط الالتقاء
    
    Args:
        path_length: طول المسار
        convergence_points: عدد نقاط الالتقاء
        
    Returns:
        int: قوة الأمان بالبت
    """
    # تقدير بسيط لقوة الأمان
    strength = path_length + (convergence_points / 1000)
    return int(strength)


def validate_parameters(n: int, m: int) -> bool:
    """
    التحقق من صحة المعاملات
    
    Args:
        n: الأس
        m: الثابت
        
    Returns:
        bool: صحة المعاملات
    """
    if n < 1:
        return False
    if m % 2 == 0:
        return False
    return True


def get_equation_string(n: int, m: int) -> str:
    """
    الحصول على النص التعبيري للمعادلة
    
    Args:
        n: الأس
        m: الثابت
        
    Returns:
        str: صيغة المعادلة
    """
    return f"{2**n}x - {m}"
