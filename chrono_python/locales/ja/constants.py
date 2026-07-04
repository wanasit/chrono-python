NUMBER = {
    "零": 0,
    "〇": 0,
    "一": 1,
    "二": 2,
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
    "日": 0,
    "月": 1,
    "火": 2,
    "水": 3,
    "木": 4,
    "金": 5,
    "土": 6,
}


def to_hankaku(text: str) -> str:
    """Convert Zenkaku (full-width) alphanumeric characters to Hankaku (half-width).
    
    This matches the behavior of the TS/JS chrono library's toHankaku function.
    """
    if not text:
        return ""
    
    text = text.replace('\u2019', '\u0027')
    text = text.replace('\u201D', '\u0022')
    text = text.replace('\u3000', '\u0020')
    text = text.replace('\uFFE5', '\u00A5')
    
    res = []
    for char in text:
        cp = ord(char)
        if (cp == 0xFF01 or 
            0xFF03 <= cp <= 0xFF06 or 
            cp == 0xFF08 or cp == 0xFF09 or 
            0xFF0C <= cp <= 0xFF19 or 
            0xFF1C <= cp <= 0xFF1F or 
            0xFF21 <= cp <= 0xFF3B or 
            cp == 0xFF3D or cp == 0xFF3F or 
            0xFF41 <= cp <= 0xFF5B or 
            cp == 0xFF5D or cp == 0xFF5E):
            res.append(chr(cp - 65248))
        else:
            res.append(char)
            
    return "".join(res)


def ja_string_to_number(text: str) -> int:
    number = 0
    for char in text:
        if char == "十":
            number = NUMBER[char] if number == 0 else number * NUMBER[char]
        else:
            number += NUMBER.get(char, 0)
    return number
