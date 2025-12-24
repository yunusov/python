from math import ceil
from itertools import groupby
from string import digits


class RomanArabicConverter:
    @staticmethod
    def roman_to_arabic(roman_number: str) -> int:
        """Преобразует римское число в арабское"""
        roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        prev_num = roman_map.get(roman_number[0])
        result = prev_num
        data = roman_number[1:]
        for s in data:
            current_num = roman_map.get(s)
            result += current_num
            if current_num > prev_num:
                result -= 2 * prev_num
            prev_num = current_num

        return result

    @staticmethod
    def arabic_to_roman(arabic_number: int) -> str:
        """Преобразует арабское число в римское."""
        result = ""
        arabic_map = {"M": 1000, "CM": 900, "D": 500, "CD": 400, "C": 100, "XC": 90,
                      "L": 50, "XL": 40, "X": 10, "IX": 9, "V": 5, "IV": 4, "I": 1}
        remain_part = arabic_number

        for key, value in arabic_map.items():
            int_part = remain_part // value
            if int_part > 0:
                result += key * int_part
                remain_part -= value * int_part

        return result


def chunks_amount(file_size: int, chunk_size: int = 1024) -> tuple:
    return (file_size // chunk_size, file_size % chunk_size)


class RLEAmateur:
    @staticmethod
    def rle_compression(data: str) -> str:
        """Сжимает строку с использованием RLE"""
        list_of_tuples = [(key, sum(1 for _ in group)) for key, group in groupby(data)]
        return "".join(str(item) for tup in list_of_tuples for item in tup)

    @staticmethod
    def rle_uncompression(compression_data: str) -> str:
        """Восстанавливает строку из сжатого представления RLE."""
        list_data = list(compression_data)
        for i, char in enumerate(list_data):
            if char in digits:
                alpha = list_data[i - 1]
                list_data[i] = alpha * (int(char) - 1)
        return "".join(list_data)


def arithmetical_mean(a: str) -> int:
    result = 0
    values = a.split(" ")
    for v in values:
        result += int(v)
    return ceil(result / len(values))


def number_reverse(data: int) -> int:
    return int(str(data)[::-1])


def is_palindrome(data: str) -> bool:
    data = data.lower().replace(" ", "")
    rev_data = data[::-1]
    return data == rev_data


# print(is_palindrome("А роза упала на лапу Азора"))
# print(number_reverse(123)) #321
# print(number_reverse(456000)) #654
# print(number_reverse(10003)) #30001

# print(arithmetical_mean("10 20 30 40")) # 25
# print(arithmetical_mean("100 200 100")) # 134
# print(arithmetical_mean("-100 200 500")) # 200

# amateur_compressed = RLEAmateur.rle_compression("abbcccaabbbc")
# print(amateur_compressed)  # Вывод: a1b2c3a2b3c1

# amateur_uncompressed = RLEAmateur.rle_uncompression("a1b2c3a2b3c1")
# print(amateur_uncompressed)  # Вывод: abbcccaabbbc

# print(chunks_amount(23456, 2056))


# Примеры использования
converter = RomanArabicConverter()

# Преобразование римского числа в арабское
# arabic_number = converter.roman_to_arabic("XXI")
# print(arabic_number)
# arabic_number = converter.roman_to_arabic("XXVI")
# print(arabic_number)
# print(f"{converter.roman_to_arabic("IX") = }")
# print(f"{converter.roman_to_arabic("CDXVII") = }")
# print(f"{converter.roman_to_arabic("XIV") = }")
# print(f"{converter.roman_to_arabic("MMMCDXCIV") = }")
# print(f"{converter.roman_to_arabic("XXIV") = }")
# print(f"{converter.roman_to_arabic("XXIX") = }")

# # Преобразование арабского числа в римское
# roman_number = converter.arabic_to_roman(2222)
# print(roman_number)  # Вывод: MMCCXXII

roman_number = converter.arabic_to_roman(17)
print(roman_number)  # Вывод: XVII
roman_number = converter.arabic_to_roman(2222)
print(roman_number)  # Вывод: MMCCXXII
roman_number = converter.arabic_to_roman(3999)
print(roman_number)  # Вывод: MMMCMXCIX
