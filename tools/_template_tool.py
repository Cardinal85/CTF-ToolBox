"""
CTF 工具箱插件开发模板

使用说明：
1. 复制本文件
2. 修改文件名（例如 my_tool.py）
3. 填写 TOOL_INFO
4. 实现 run() 函数
5. 放入 tools/ 目录即可被自动识别
"""

# =========================
# 工具元信息
# =========================
TOOL_INFO = {
    "name": "示例插件",     #工具名称（必填）
    "description": "示例",      #一句话描述这个工具做什么（必填）
    "category": "other",      # crypto / web / pwn / rev / misc
    "author": "songlan",
    "version": "1.0"
}


# =========================
# 工具入口函数（必须）
# =========================
def run():
    """
    工具执行入口

    返回值说明：
    （1）只返回一个值：
        return output

    （2）返回两个值（推荐）：
        return output, input_data
        - output      : 显示给用户的结果（str / 任意可打印）
        - input_data  : dict，用于记录运行参数（会写入数据库）
    """

    # 示例代码（请删除）：

    user_input = input("请输入内容: ").strip()

    # 工具输出内容
    output = f"你输入的是: {user_input}"

    # 建议记录的输入参数（可选）
    input_data = {
        "input": user_input
    }

    return output, input_data
