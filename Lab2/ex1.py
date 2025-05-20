from itertools import permutations

def count_unique_words(word: str, length: int) -> int:
    unique_words = set()
    for p in permutations(word, length):
        unique_words.add(p)
    return unique_words


if __name__ == "__main__":
    word = "ЧЕРЕСПОЛОСИЦА"
    word_length = 6
    print(f"Количество различных 6-буквенных слов: {len(count_unique_words(word, word_length))}")
    unique = list(count_unique_words(word, word_length))
    for i in range(200):
        print(''.join(unique[i]))