import base64

TOOL_INFO = {
    "name": "Base64 编码 / 解码",
    "description": "对字符串进行 Base64 编码或解码",
    "category": "crypto",
    "author": "ChatGPT1",
    "version": "1.0"
}

def run():
    text = input("请输入字符串: ").strip()
    mode = input("选择模式\n 1=编码 \t 2=解码\t \n").strip()

    if mode == "1":
        result = base64.b64encode(text.encode()).decode()
        return result, {"text": text, "mode": "encode"}

    elif mode == "2":
        try:
            result = base64.b64decode(text.encode()).decode(errors="ignore")
            return result, {"text": text, "mode": "decode"}
        except Exception as e:
            return f"解码失败: {e}", {"text": text}

    else:
        return "模式选择错误"
