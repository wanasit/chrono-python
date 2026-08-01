NUMBER = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}

WEEKDAY_OFFSET = {
    "天": 0,
    "日": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
}


def zh_string_to_number(text: str) -> int:
    number = 0
    for char in text:
        if char == "十":
            number = NUMBER[char] if number == 0 else number * NUMBER[char]
        else:
            number += NUMBER.get(char, 0)
    return number


def zh_string_to_year(text: str) -> int:
    string = ""
    for char in text:
        string += str(NUMBER.get(char, char))
    return int(string)
