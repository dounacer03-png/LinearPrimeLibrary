"""
مثال أساسي لاستخدام المكتبة
Basic usage example for LinearPrimeLibrary
"""

from linear_prime_library import LinearPrimeLibrary, LinearPrimeCrypto
from linear_prime_library.utils import generate_prime_key, get_recommended_equation, SecurityLevel


def main():
    """المثال الرئيسي"""
    
    print("=" * 60)
    print("LinearPrimeLibrary - مثال أساسي")
    print("=" * 60)
    
    # 1. إنشاء المكتبة
    print("\n1. إنشاء المكتبة...")
    lib = LinearPrimeLibrary()
    
    # 2. تحليل معادلة 8x-1
    print("\n2. تحليل معادلة 8x-1...")
    info = lib.analyze_equation(3, 1, limit=50000)
    print(f"   الصيغة: {info.get_formula()}")
    print(f"   متوسط طول المسار: {info.avg_path_length:.2f}")
    print(f"   أطول مسار: {info.max_path_length}")
    print(f"   عدد الدورات: {len(info.cycles)}")
    print(f"   نقاط النهاية المهيمنة: {list(info.endpoint_distribution.keys())[:3]}")
    
    # 3. تحليل معادلة 16x-1
    print("\n3. تحليل معادلة 16x-1...")
    info2 = lib.analyze_equation(4, 1, limit=50000)
    print(f"   الصيغة: {info2.get_formula()}")
    print(f"   متوسط طول المسار: {info2.avg_path_length:.2f}")
    print(f"   أطول مسار: {info2.max_path_length}")
    print(f"   عدد الدورات: {len(info2.cycles)}")
    
    # 4. تشفير رسالة
    print("\n4. تشفير رسالة...")
    crypto = LinearPrimeCrypto(lib)
    
    # توليد مفتاح
    key = generate_prime_key(10000, 100000)
    print(f"   المفتاح المستخدم: {key}")
    
    # الرسالة
    message = "رسالة سرية للغاية"
    print(f"   الرسالة الأصلية: {message}")
    
    # تشفير
    encrypted = crypto.encrypt(message, key, n=3, m=1)
    print(f"   النص المشفر: {encrypted[:50]}...")
    
    # فك تشفير
    decrypted = crypto.decrypt(encrypted, key, n=3, m=1)
    print(f"   النص المفكوك: {decrypted}")
    
    # 5. التوصيات
    print("\n5. توصيات حسب مستوى الأمان:")
    for level in [SecurityLevel.LOW, SecurityLevel.MEDIUM, SecurityLevel.HIGH]:
        n, m = get_recommended_equation(level)
        print(f"   {level.value}: {2**n}x - {m}")
    
    print("\n" + "=" * 60)
    print("✅ اكتمل المثال بنجاح!")
    print("=" * 60)


if __name__ == "__main__":
    main()
