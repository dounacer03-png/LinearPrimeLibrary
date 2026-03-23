"""
Core module for LinearPrimeLibrary
"""

from sympy import factorint, primerange
from collections import Counter
import hashlib
import pickle
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class Cycle:
    """تمثيل دورة"""
    elements: List[int]
    
    def __post_init__(self):
        self.length = len(self.elements)
    
    def __repr__(self):
        return f"Cycle({self.elements})"


@dataclass
class EquationInfo:
    """معلومات عن معادلة"""
    n: int
    m: int
    cycles: List[Cycle]
    convergence_points: Dict[int, int]
    avg_path_length: float
    max_path_length: int
    total_primes: int
    unique_nodes: int
    security_bits: int
    equation_type: str
    endpoint_distribution: Dict[int, float]
    
    def get_formula(self) -> str:
        return f"{2**self.n}x - {self.m}"


class EquationAnalyzer:
    """محلل المعادلات الخطية"""
    
    def __init__(self, n: int, m: int, cache_dir: str = "./cache"):
        if m % 2 == 0:
            raise ValueError(f"m يجب أن يكون فردياً")
        
        self.n = n
        self.m = m
        self.coeff = 2 ** n
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.memo = {}
        self.path_cache = {}
    
    def next_prime(self, x: int) -> int:
        if x in self.memo:
            return self.memo[x]
        
        X_next = self.coeff * x - self.m
        factors = factorint(X_next)
        result = max(factors.keys())
        self.memo[x] = result
        return result
    
    def trace_path(self, start: int, max_steps: int = 200):
        cache_key = f"{start}"
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]
        
        path = [start]
        current = start
        visited = {start}
        steps = 0
        
        while steps < max_steps:
            nxt = self.next_prime(current)
            
            if nxt in visited:
                cycle_start = path.index(nxt)
                cycle = path[cycle_start:]
                result = (path, steps, cycle)
                self.path_cache[cache_key] = result
                return result
            
            path.append(nxt)
            visited.add(nxt)
            current = nxt
            steps += 1
        
        result = (path, max_steps, None)
        self.path_cache[cache_key] = result
        return result


class LinearPrimeLibrary:
    """المكتبة الرئيسية"""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        self.equations = {}
        self.analyzers = {}
    
    def analyze_equation(self, n: int, m: int, limit: int = 100000):
        analyzer = self._get_analyzer(n, m)
        
        cache_file = os.path.join(self.cache_dir, f"eq_{n}_{m}.pkl")
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        primes = list(primerange(2, limit))
        total = len(primes)
        
        path_lengths = []
        endpoints = Counter()
        cycles_set = {}
        convergence_points = Counter()
        
        for prime in primes:
            path, steps, cycle = analyzer.trace_path(prime)
            path_lengths.append(steps)
            
            if cycle:
                endpoint = cycle[0]
                endpoints[endpoint] += 1
                cycle_tuple = tuple(sorted(cycle))
                if cycle_tuple not in cycles_set:
                    cycles_set[cycle_tuple] = Cycle(list(cycle_tuple))
                
                for node in path[:-1]:
                    convergence_points[node] += 1
        
        cycles = list(cycles_set.values())
        avg_length = sum(path_lengths) / len(path_lengths)
        max_length = max(path_lengths)
        unique_nodes = len(convergence_points)
        
        # حساب الإنتروبيا
        probs = [c / total for c in endpoints.values()]
        entropy = -sum(p * np.log2(p) for p in probs if p > 0)
        security_bits = int(entropy)
        
        # تحديد النوع
        if avg_length < 5:
            eq_type = "FAST"
        elif max_length > 35:
            eq_type = "DEEP"
        elif len(cycles) > 3:
            eq_type = "DIVERSE"
        else:
            eq_type = "BALANCED"
        
        endpoint_dist = {k: v / total * 100 for k, v in endpoints.most_common(10)}
        
        info = EquationInfo(
            n=n, m=m,
            cycles=cycles,
            convergence_points=dict(convergence_points.most_common(20)),
            avg_path_length=avg_length,
            max_path_length=max_length,
            total_primes=total,
            unique_nodes=unique_nodes,
            security_bits=security_bits,
            equation_type=eq_type,
            endpoint_distribution=endpoint_dist
        )
        
        with open(cache_file, 'wb') as f:
            pickle.dump(info, f)
        
        self.equations[(n, m)] = info
        return info
    
    def _get_analyzer(self, n: int, m: int):
        key = (n, m)
        if key not in self.analyzers:
            self.analyzers[key] = EquationAnalyzer(n, m, self.cache_dir)
        return self.analyzers[key]


class LinearPrimeCrypto:
    """نظام التشفير"""
    
    def __init__(self, library: LinearPrimeLibrary):
        self.library = library
    
    def encrypt(self, message: str, key: int, n: int = 3, m: int = 1) -> str:
        analyzer = self.library._get_analyzer(n, m)
        path = analyzer.trace_path(key)[0]
        
        path_str = '->'.join(map(str, path))
        crypto_key = hashlib.sha256(path_str.encode()).digest()
        
        message_bytes = message.encode()
        key_expanded = crypto_key * (len(message_bytes) // 32 + 1)
        
        encrypted = bytes([b ^ k for b, k in zip(message_bytes, key_expanded)])
        return encrypted.hex()
    
    def decrypt(self, ciphertext: str, key: int, n: int = 3, m: int = 1) -> str:
        analyzer = self.library._get_analyzer(n, m)
        path = analyzer.trace_path(key)[0]
        
        path_str = '->'.join(map(str, path))
        crypto_key = hashlib.sha256(path_str.encode()).digest()
        
        cipher_bytes = bytes.fromhex(ciphertext)
        key_expanded = crypto_key * (len(cipher_bytes) // 32 + 1)
        
        decrypted = bytes([c ^ k for c, k in zip(cipher_bytes, key_expanded)])
        return decrypted.decode()
