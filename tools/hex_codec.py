TOOL_INFO = {
    "name": "HEX 编码 / 解码",
    "description": "字符串与十六进制互转",
    "category": "misc",
    "author": "ChatGPT",
    "version": "1.0"
}

def run():
    text = input("请输入内容: ").strip()
    mode = input("选择模式 (1=编码 / 2=解码): ").strip()

    if mode == "1":
        result = text.encode().hex()
        return result, {"text": text, "mode": "encode"}

    elif mode == "2":
        try:
            result = bytes.fromhex(text).decode(errors="ignore")
            return result, {"text": text, "mode": "decode"}
        except Exception as e:
            return f"解码失败: {e}"

    else:
        return "模式错误"
