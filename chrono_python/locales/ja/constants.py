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
        # Check if code point is in the specified character classes:
        # [\uFF01\uFF03-\uFF06\uFF08\uFF09\uFF0C-\uFF19\uFF1C-\uFF1F\uFF21-\uFF3B\uFF3D\uFF3F\uFF41-\uFF5B\uFF5D\uFF5E]
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
