def print_histogram(data: list) -> str:
    result = ""
    for i in reversed(data):
        result += "".join(i)
    return result

def get_histogram(input_chars: list, dict_chars: dict) -> list:
    result = [input_chars]
    max_char = max(dict_chars.values())
    len_input_chars = len(input_chars)
    for i in range(max_char):
        result.append([" "] * len_input_chars + ["\n"])
        for j, char in enumerate(input_chars):
            if dict_chars[char] > i:
                result[i + 1][j] = "|"
    return result


def fulfill_dict_chars(input_data: str, dict_data: dict):
    for i in input_data:
        val = dict_data.get(i, 0)
        dict_data[i] = val + 1


def histogram(data: str) -> str:
    # input_data = input("input_data:")
    input_data = data #"ececceaebdadaeae"
    if not input_data:
        print("Ошибка: строка не может быть пустой")
        return
    dict_chars = dict.fromkeys(input_data, 0)
    list_chars = list(dict_chars.keys())
    list_chars.sort()
    fulfill_dict_chars(input_data, dict_chars)
    histogram = get_histogram(list_chars, dict_chars)
    str_histogram = print_histogram(histogram)
    return str_histogram


if __name__ == "__main__":
    print(histogram("abcde"))
    print(histogram("aaaaaa"))
