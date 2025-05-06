from itertools import permutations

word = "ЧЕРЕСПОЛОСИЦА"

def count_unique_words(word: str, length: int) -> int:
    unique_words = set()
    for p in permutations(word, length):
        unique_words.add(p)
    return len(unique_words)


result = count_unique_words(word, 6)
print(f"Количество различных 6-буквенных слов: {result}")