from loguru_config import logger
from string import ascii_letters as alpha
import itertools

def caesar_cipher(data: str, key: int) -> str:
    result = []
    alpha_len = len(alpha)
    remain_key = key % alpha_len
    for char in data:
        if char in alpha:
            pos = alpha.find(char)
            new_pos = (pos + remain_key) % alpha_len
            result.append(alpha[new_pos])
        else:
            result.append(char)
    return "".join(result)


def caesar_cipher_test():
    logger.info(caesar_cipher("Doggy", 5))
    logger.info(caesar_cipher("Python is the BEST!", 20))  # jSNBIH CM NBy VYmn!
    logger.info(caesar_cipher("abcXYZ", 3))  # Ожидается: defABC
    logger.info(caesar_cipher("Hello, World!", 13))  # Ожидается: Uryyb, Jbeyq!
    logger.info(caesar_cipher("123!@#", 10))  # Ожидается: 123!@# (без изменений)
    logger.info(caesar_cipher("", 5))  # Ожидается: пустая строка
    # Отрицательное смещение
    logger.info(caesar_cipher("defDEF", -3))  # Ожидается: abcABC

    # Смещение больше длины алфавита
    logger.info(caesar_cipher("xyzXYZ", 52))  # Ожидается: xyzXYZ (так как 52 % 52 == 0)
    logger.info(caesar_cipher("abcABC", 55))  # Ожидается: defDEF (55 % 52 == 3)

    # Смешанные символы
    logger.info(
        caesar_cipher("Text with 123 & symbols!", 4)
    )  # Ожидается: Xibx amxl 123 & wcqfsppw!

def demo_takewhile():
    arr = [3, 5, 7, -2, 6]
    logger.info(sum([n for n in itertools.takewhile(lambda x: x >= 0, arr)]))

def main():
    caesar_cipher_test()
    #demo_takewhile()

if __name__ == "__main__":
    main()
