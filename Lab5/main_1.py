import numpy as np
from typing import Any, Literal
 
 
class CyclicCode:
    def __init__(self, n, k, generator_poly) -> None:
        self.n = n
        self.k = k
        self.r = n - k
        self.generator_poly = generator_poly
        self.g = np.array([int(bit) for bit in generator_poly], dtype=np.uint8)
        self.g_degree = len(self.g) - 1
        self.G = self.build_systematic_generator_matrix()
        self.codewords = self.generate_all_codewords()
        self.d_min = self.calculate_min_distance()
        self.syndrome_table = self.build_syndrome_table()
 
    def poly_div(self, dividend, divisor) -> Any:
        dividend = np.trim_zeros(dividend, 'f')
        divisor = np.trim_zeros(divisor, 'f')
 
        if len(dividend) < len(divisor):
            return dividend.copy()
 
        remainder = dividend.copy()
        len_divisor = len(divisor)
        for i in range(len(dividend) - len_divisor + 1):
            if remainder[i]:
                remainder[i:i + len_divisor] ^= divisor
 
        return np.trim_zeros(remainder, 'f')
 
    def build_systematic_generator_matrix(self) -> np.ndarray[Any, np.dtype[np.unsignedinteger]]:
        I_k = np.eye(self.k, dtype=np.uint8)
        C = np.zeros((self.k, self.r), dtype=np.uint8)
 
        for i in range(self.k):
            poly = np.zeros(self.n, dtype=np.uint8)
            poly[i] = 1
            remainder = self.poly_div(poly, self.g)
            if len(remainder) < self.r:
                padded_remainder = np.pad(remainder, (self.r - len(remainder), 0), 'constant')
                C[i] = padded_remainder[-self.r:]
 
        return np.hstack([I_k, C])
 
    def encode(self, message):
        if len(message) != self.k:
            raise ValueError(f"Длина сообщения должна быть {self.k} бит")
 
        message_padded = np.concatenate([message, np.zeros(self.r, dtype=np.uint8)])
        remainder = self.poly_div(message_padded, self.g)
        if len(remainder) < self.r:
            remainder = np.pad(remainder, (self.r - len(remainder), 0), 'constant')
        return np.concatenate([message, remainder])
 
    def generate_all_codewords(self) -> np.ndarray[Any, np.dtype[np.unsignedinteger]]:
        codewords = np.zeros((2 ** self.k, self.n), dtype=np.uint8)
        for i in range(2 ** self.k):
            message = np.array([int(bit) for bit in f"{i:0{self.k}b}"], dtype=np.uint8)
            codewords[i] = self.encode(message)
        return codewords
 
    def calculate_min_distance(self) -> Any | Any:
        nonzero_codewords = [c for c in self.codewords if np.any(c)]
        if not nonzero_codewords:
            return self.n
 
        min_distance = min(np.sum(c) for c in nonzero_codewords)
        return min_distance
 
    def build_syndrome_table(self) -> dict:
        syndrome_table = {}
        for i in range(self.n):
            error_pattern = np.zeros(self.n, dtype=np.uint8)
            error_pattern[i] = 1
            syndrome = self.poly_div(error_pattern, self.g)
            syndrome_key = tuple(syndrome)
            syndrome_table[syndrome_key] = error_pattern
        return syndrome_table
 
    def decode(self, received) -> tuple[Literal[False], None, Any] | tuple[Literal[True], Any, Any]:
        if len(received) != self.n:
            raise ValueError(f"Длина принятого слова должна быть {self.n} бит")
 
        syndrome = self.poly_div(received, self.g)
        error_detected = np.any(syndrome)
 
        if not error_detected:
            return False, None, received  # Нет ошибки

        # print("Таблица палиндромов: ", self.syndrome_table)
        
        print()
        print()
        print("Синдром: ", syndrome)

        syndrome_key = tuple(syndrome)
        if syndrome_key in self.syndrome_table:
            error_pattern = self.syndrome_table[syndrome_key]
            corrected = (received + error_pattern) % 2
            # print("Паттерн ошибки: ", error_pattern)
            # print("Скорректировано: ", corrected)
            return True, error_pattern, corrected
        else:
            return True, None, received  # Ошибка обнаружена, но не может быть исправлена
 
    def get_capabilities(self) -> tuple[Any, Any]:
        detect = self.d_min - 1
        correct = (self.d_min - 1) // 2
        return detect, correct
 
    def generate_error_examples(self) -> np.ndarray[Any, np.dtype[np.unsignedinteger]]:
        message = np.zeros(self.k, dtype=np.uint8)
        message[0] = 1
        codeword = self.encode(message)
 
        print("\n3. Примеры, иллюстрирующие свойства кода:")
 
        # Пример 1: Обнаружение и исправление одиночной ошибки
        error1 = np.zeros(self.n, dtype=np.uint8)
        error1[5] = 1
        received1 = (codeword + error1) % 2
        detected1, error_pattern1, corrected1 = self.decode(received1)
        print(f"\nПример 1: Обнаружение и исправление одиночной ошибки")
        print(f"Кодовое слово: {codeword}")
        print(f"Внедряем ошибку в эти биты: {error1}")
        print(f"Принятое слово: {received1}")
        print(f"Ошибка обнаружена: {detected1}")
        if error_pattern1 is not None:
            print(f"Вычисленный вектор ошибки: {error_pattern1}")
            print(f"Исправленное слово: {corrected1}")
            print("Проверка:", np.array_equal(corrected1, codeword))
        else:
            print("Ошибка не может быть исправлена")
 
        # Пример 2: Обнаружение двух ошибок
        error2 = np.zeros(self.n, dtype=np.uint8)
        error2[5] = 1
        error2[10] = 1
        received2 = (codeword + error2) % 2
        detected2, error_pattern2, corrected2 = self.decode(received2)
        print(f"\nПример 2: Обнаружение двух ошибок")
        print(f"Кодовое слово: {codeword}")
        print(f"Внедряем ошибку в эти биты: {error2}")
        print(f"Принятое слово: {received2}")
        print(f"Ошибка обнаружена: {detected2}")
        if error_pattern2 is not None:
            print(f"Вычисленный вектор ошибки: {error_pattern2}")
            print(f"Исправленное слово: {corrected2}")
            print("Проверка:", np.array_equal(corrected2, codeword))
        else:
            print("Ошибка не может быть исправлена (код может только обнаружить две ошибки)")
 
        # Пример 3: Ошибка, которую можно обнаружить, но не исправить
        t = (self.d_min - 1) // 2
        error3 = np.zeros(self.n, dtype=np.uint8)
        error3[::2][:t + 2] = 1  # t+2 ошибки (больше чем может исправить)
        received3 = (codeword + error3) % 2
        detected3, error_pattern3, corrected3 = self.decode(received3)
        print(f"\nПример 3: Ошибка, которую можно обнаружить, но не исправить")
        print(f"Кодовое слово: {codeword}")
        print(f"Внедряем ошибку в эти биты: {error3}")
        print(f"Принятое слово: {received3}")
        print(f"Ошибка обнаружена: {detected3}")
        if error_pattern3 is not None:
            print(f"Вычисленный вектор ошибки: {error_pattern3}")
            print(f"Исправленное слово: {corrected3}")
            print("Проверка:", np.array_equal(corrected3, codeword))
        else:
            print("Ошибка не может быть исправлена (количество ошибок превышает корректирующую способность кода)")
 
        return error3
 
 
n = 23
m = 12
generator_poly = '101011100011'
code = CyclicCode(n, m, generator_poly)
 
print("1. Порождающая матрица G:")
print(code.G)
 
print("\nФрагмент множества кодовых слов (первые 5):")
for i in range(min(5, len(code.codewords))):
    print(f"Сообщение {i}: {code.codewords[i]}")
 
d_min = code.d_min
detect, correct = code.get_capabilities()
print(f"\n2. Характеристики кода:")
print(f"Минимальное расстояние кода: d_min = {d_min}")
print(f"Кратность гарантированно обнаруживаемых ошибок: {detect}")
print(f"Кратность гарантированно исправляемых ошибок: {correct}")

 
error_example = code.generate_error_examples()
 
print("\n4. Конкретный вектор ошибки, который код может обнаружить, но не может исправить:")
print(error_example)