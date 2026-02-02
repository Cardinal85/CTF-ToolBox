import hashlib

TOOL_INFO = {
    "name": "MD5计算",
    "description": "计算字符串的 MD5 哈希值",
    "category": "crypto",
    "author": "ChatGPT",
    "version": "1.0"
}

def run():
    text = input("请输入字符串: ").strip()
    md5_value = hashlib.md5(text.encode()).hexdigest()

    return md5_value, {"text": text}
