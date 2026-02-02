import hashlib
import os

TOOL_INFO = {
    "name": "MD5 字典爆破",
    "description": "使用字典文件爆破 MD5 哈希",
    "category": "crypto",
    "author": "ChatGPT",
    "version": "1.0"
}

def run():
    target = input("请输入 MD5 哈希: ").strip()
    dict_path = input("请输入字典文件路径: ").strip()

    if not os.path.exists(dict_path):
        return "字典文件不存在", {"dict": dict_path}

    with open(dict_path, "r", errors="ignore") as f:
        for line in f:
            pwd = line.strip()
            if hashlib.md5(pwd.encode()).hexdigest() == target:
                return f"[+] 破解成功: {pwd}", {
                    "hash": target,
                    "dict": dict_path
                }

    return "[-] 未在字典中找到", {
        "hash": target,
        "dict": dict_path
    }
