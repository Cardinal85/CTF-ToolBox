TOOL_INFO = {
    "name": "XOR 加解密",
    "description": "使用单字节 key 对字符串进行 XOR",
    "category": "crypto",
    "author": "ChatGPT",
    "version": "1.0"
}

def run():
    text = input("请输入字符串: ").strip()
    key = input("请输入 key (单字符): ").strip()

    if len(key) != 1:
        return "key 必须是单个字符"

    key = ord(key)
    result = "".join(chr(ord(c) ^ key) for c in text)

    return result, {
        "text": text,
        "key": chr(key)
    }
