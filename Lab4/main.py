from xmlrpc.client import MAXINT
import math
from typing import Any, Literal

class Node:
    def __init__(self, key : int, value : str) -> None:
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __eq__(self, other) -> bool:
        return (self.key == other.key and self.value == other.value and self.left == other.left and self.right == other.right)


def get_codes_pre_order(node, codes : list, code = "") -> None:
    if node.left:
        get_codes_pre_order(node.left,codes, code + "0")
    if node.right:
        get_codes_pre_order(node.right,codes, code + "1")
    if not node.left and not node.right:
        codes.append([node.value,code])


def haffmancode(symbolchance) -> list:
    nodesarr = list()
    for i in symbolchance:
        nodesarr.append(Node(i[1],i[0]))

    while(len(nodesarr) > 1):
        min1 = Node(MAXINT,"NotASymbol")
        min2 = Node(MAXINT,"NotASymbol")
        for i in nodesarr:
            if i.key < min1.key:
                min1, min2 = i, min1
            elif i.key < min2.key and i.value != min1.value:
                min2 = i

        tmp = Node(min1.key + min2.key,min1.value + min2.value)
        tmp.left = min1
        tmp.right = min2

        nodesarr.remove(min1)
        nodesarr.remove(min2)

        nodesarr.append(tmp)

    #print(nodesarr[0].value)
    codes = list()
    get_codes_pre_order(nodesarr[0],codes)
    return codes


def gettext(filepath: str) -> str:
    with open(filepath, "r") as file:
        text = file.read()
    text = text.lower()

    return text


def sortbysecond(arr : list) -> list:
    dlist = arr.copy()
    for i in range(len(dlist)-1):
        for j in range(len(dlist)-1-i):
            if(dlist[j][1] < dlist[j+1][1]):
                dlist[j],dlist[j+1] = dlist[j+1],dlist[j]
    return dlist


def frequency(text : str, a : str) -> int:
    return text.count(a)


def encodetext(text : str, codes : list) -> str:
    for i in codes:
        text = text.replace(i[0], i[1])
    return text


def decodetext(encoded_text : str, codes : list) -> Any | Literal['']:
    decryptedtext = ""
    current_code = ""

    for bit in encoded_text:
        current_code += bit
        for code in codes:
            if current_code == code[1]:
                decryptedtext += code[0]
                current_code = ""
                break

    return decryptedtext


def calculate_shannon_entropy(frequencies,text_len) -> Any | Literal[0]:

    entropy = 0
    for freq in frequencies:
        entropy -= (freq[1]/text_len) * math.log2(freq[1]/text_len)
    return entropy


def lzw_encode(text) -> list:
    # Инициализация словаря всеми возможными символами
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    p = ""
    encoded_data = []

    for c in text:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            encoded_data.append(dictionary[p])
            dictionary[pc] = dict_size
            dict_size += 1
            p = c

    if p:
        encoded_data.append(dictionary[p])

    return encoded_data


def lzw_decode(encoded_data) -> str:
    # Инициализация словаря всеми возможными символами
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    p = chr(encoded_data.pop(0))
    decoded_text = p

    for code in encoded_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = p + p[0]
        else:
            raise ValueError("Некорректный код")

        decoded_text += entry

        dictionary[dict_size] = p + entry[0]
        dict_size += 1

        p = entry

    return decoded_text


def calculate_lzw_length(encoded_data, bits_per_code=12) -> int:
    # Вычисляем длину закодированного текста в битах
    return len(encoded_data) * bits_per_code


def main() -> None:
    text = gettext("Lab4/text.txt")

    #1 Статистический анализ
    allsymbols = set(text)
    symbolchance = list()
    for i in allsymbols:
        symbolchance.append([i,frequency(text,i)])

    alltwos = set()
    for i in range(len(text)-1):
        alltwos.add(text[i]+text[i+1])

    twoschance = list()
    for i in alltwos:
        twoschance.append([i,frequency(text,i)])

    symbolchance = sortbysecond(symbolchance)
    twoschance = sortbysecond(twoschance)

    print("\033[32m Исходный текст:\033[0m",text)

    print("\033[32m Частотность символов:\033[0m",symbolchance)
    print("\033[32m Частотность пар:\033[0m",twoschance)
    print("\033[32m Работаем с отдельными символами:\033[0m")
    #по символам
    #2.1 Построение кодов Хаффмана
    codes = haffmancode(symbolchance)
    print("\033[32m Коды Хаффмана:\033[0m",codes)

    #2.2 Кодированние текста
    Haffmantext = encodetext(text,codes)
    print("\033[32m Закодированный с помощью кодов Хаффмана текст:\033[0m",Haffmantext)

    print("\033[32m Длина текста, закодированного с помощью кодов Хаффмана:\033[0m",len(Haffmantext))
    print("\033[32m Длина исходного текста, закодированного 5 битными кодами:\033[0m",len(text)*5)

    #2.3 Раскодирование текста
    decryptedtext = decodetext(Haffmantext,codes)
    print("\033[32m Раскодированный текст:\033[0m",decryptedtext)
    print("\033[32m Его длина:\033[0m",len(decryptedtext))

    print("\033[32m Работаем с парами символов:\033[0m")
    #по парам:
    #3.1 Построение кодов Хаффмана
    twoscodes = haffmancode(twoschance)
    #twoscodes = sortbysecond(twoscodes)
    print("\033[32m Коды Хаффмана:\033[0m", twoscodes)

    #3.2 Кодированние текста
    twosHaffmantext = encodetext(text, twoscodes)
    print("\033[32m Закодированный с помощью кодов Хаффмана текст\033[0m:", twosHaffmantext)

    print("\033[32m Длина текста, закодированного с помощью кодов Хаффмана:\033[0m", len(twosHaffmantext))
    print("\033[32m Длина исходного текста, закодированного 5 битными кодами:\033[0m", len(text) * 5)

    #3.4 Вычисление количества информации по формуле Шенона
    print("\033[32m Энтропия Шенона\033[0m:", calculate_shannon_entropy(symbolchance, len(text)))
    print("\033[32m Количество бит на символ в случае с кодами Хаффмана для непар:\033[0m", len(Haffmantext) / len(text))
    print("\033[32m Количество бит на символ в случае с кодами Хаффмана для пар:\033[0m", len(twosHaffmantext) / len(text))
    print("\033[32m Количество бит на символ в случае с 5 битовыми кодами: 5")

    #4.1 Kодирование текста с помощью LZW
    lzw_encoded_data = lzw_encode(text)
    tmp = ''
    for i in lzw_encoded_data:
        tmp += bin(i)[2:]
    print("\033[32m Закодированный с помощью LZW текст:\033[0m", tmp)

    #4.2 Раскодирование текста с помощью LZW
    lzw_decoded_text = lzw_decode(lzw_encoded_data)
    print("\033[32m Раскодированный текст с помощью LZW:\033[0m", lzw_decoded_text)

    lzw_encoded_length = calculate_lzw_length(lzw_encoded_data)
    print("\033[32m Длина текста, закодированного с помощью LZW (в битах):\033[0m",lzw_encoded_length)

    if text == decryptedtext: print("Исходный текст совпадает с раскодированным\033[0m")
    else: print("\033[32m Исходный текст не совпадает с раскодированным\033[0m")

    print("\033[32m Длина словаря Хаффмана для непар:\033[0m", len(symbolchance),"; \033[32m Что примерно в битах:\033[0m",len(symbolchance)*(8+10))
    print("\033[32m Длина словаря Хаффмана для пар:\033[0m", len(twoschance)//2,"; \033[32m Что примерно в битах:\033[0m",len(twoschance)*(16+10)//2)



if __name__ == "__main__":
    main()