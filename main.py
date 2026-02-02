import importlib.util
import hashlib
import json
import os
import traceback
import mysql.connector

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from db import get_conn, get_tool_by_key, add_tool, add_run_log,get_tool_by_entry_file,get_all_tool_keys_from_db,delete_tool_by_key
from init_db import init_db

TOOLS_DIR = "tools"

def ensure_db_ready():
    """
    确保初始化数据库
    """
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cur = conn.cursor()

        cur.execute("SHOW DATABASES LIKE %s", (MYSQL_DB,))
        if cur.fetchone() is None:
            raise Exception("数据库不存在")

        cur.close()
        conn.close()


    except Exception:
        print("[!] 数据库未初始化或不完整，正在进行初始化···")
        init_db()
        print("[OK] 数据库初始化成功！")


def generate_tool_key(file_path: str) -> str:
    """
    自动生成唯一tool key
    :param file_path: 文件路径
    :return: 名字和文件hash
    """
    name = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, "rb") as f:
        content = f.read()

    file_hash = hashlib.md5(content).hexdigest()[:8]

    return f"{name}_{file_hash}"


def load_tool_module(file_path: str):
    """
    动态加载工具模块
    :param file_path:模块路径 tools/xxx.py
    :return:moudle
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[!] 工具文件不存在{file_path}")

    module_name = os.path.splitext(os.path.basename(file_path))[0]   # 提取工具名称
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    print(f"[OK] {module_name} 工具加载成功")
    return module


def sync_tool_to_db(tool: dict):
    """
    同步tool工具到数据库
    :param tool:
    :return: tool ID
    """
    db_tool_by_key = get_tool_by_key(tool["tool_key"])
    if db_tool_by_key:
        return db_tool_by_key["id"]


    tool_id = add_tool(
        tool_key=tool["tool_key"],
        name=tool["name"],
        description=tool["description"],
        category=tool["category"],
        author=tool["author"],
        version=tool["version"],
        entry_file=tool["entry_file"],
        enabled=1
    )
    print(f"[OK] 新工具已入库：{tool['name']},(id={tool_id})")
    return tool_id



def get_tools_from_directory():
    tool_keys = set()

    for filename in os.listdir(TOOLS_DIR):
        if filename.endswith(".py") and not filename.startswith("__"):
            tool_key = generate_tool_key(os.path.join(TOOLS_DIR, filename))
            tool_keys.add(tool_key)

    return tool_keys

def remove_tools_not_in_directory():
    # 获取工具文件夹中的工具（tool_key）
    tools_in_directory = get_tools_from_directory()

    # 获取数据库中的所有工具（tool_key）
    tools_in_db = get_all_tool_keys_from_db()

    # 找出多余的工具（数据库中有，但文件夹中没有）
    tools_to_remove = tools_in_db - tools_in_directory

    if tools_to_remove:
        print(f"[OK] 找到 {len(tools_to_remove)} 个不再存在的工具，准备删除...")
        # 删除多余工具
        for tool_key in tools_to_remove:
            delete_tool_by_key(tool_key)
            print(f"[OK] 已删除工具：{tool_key}")
    else:
        print("[OK] 所有工具都在文件夹中存在，暂无需要删除的工具。")


def scan_tools():
    """
    扫描tools/文件夹下的所有工具
    :return:工具列表
    """
    tools = []
    # 检查工作目录
    if not os.path.exists(TOOLS_DIR):
        print(f"[!] 工作目录不存在：{TOOLS_DIR}")
        return tools

    # 加载文件过滤
    for filename in os.listdir(TOOLS_DIR):
        # 跳过非py文件
        if not filename.endswith(".py"):
            continue
        # 跳过__int__.py 等文件
        if filename.startswith("__"):
            continue
        # 拼接文件路径
        file_path = os.path.join(TOOLS_DIR, filename)

        try:
            # 通过路径加载模块
            module = load_tool_module(file_path)

            # 判断是否符合规范
            if not hasattr(module, "TOOL_INFO"):
                continue
            if not hasattr(module, "run"):
                continue

            info = module.TOOL_INFO
            tool_key = generate_tool_key(file_path)

            tool_data = ({
                "tool_key": tool_key,
                "name": info.get("name",tool_key),
                "description": info.get("description", ""),
                "category": info.get("category", "unknown"),
                "author": info.get("author", "unknown"),
                "version": info.get("version", "1.0"),
                "entry_file": file_path,
                "module": module
            })

            tool_id = sync_tool_to_db(tool_data)
            tool_data["tool_id"] = tool_id
            tools.append(tool_data)

        except Exception as e:
            print(f"[!] 加载工具失败：{filename}，错误代码{e}")

    return tools



# 菜单主页
def show_menu(tools):
    print("\n==============================")
    print("          CTF 工具库           ")
    print("==============================")

    for i, t in enumerate(tools,start=1):
        print(f"[{i}] {t['name']} ({t['category']})")
        if t["description"]:
            print(f"     {t['description']}")

    print("\n[0] 退出")
    print("==============================\n")

# 菜单选择界面
def main():
    ensure_db_ready()
    remove_tools_not_in_directory()
    tools = scan_tools()

    if not tools:
        print("[!] tools/ 目录下没有可用工具")
        print("[!] 请放入符合规范的工具脚本，包含 TOOL_INFO 信息 和 run函数")
        return

    while True:
        show_menu(tools)

        choice = input("请选择工具编号: ").strip()

        if choice == "0":
            print("[OK] 您已退出程序")
            print("Bye")
            return

        if not choice.isdigit():
            print("[!] 请输入数字编号")
            continue

        #idx ：输入程序的选项
        idx = int(choice) - 1

        if idx < 0 or idx >= len(tools):
            print("[!] 编号不存在")
            continue

        tool = tools[idx]

        print(f"\n[OK] 运行工具：{tool['name']}")
        print(f"[OK] 工具文件：{tool['entry_file']}\n")

        input_data = {}
        output_data = ""
        status = "success"

        try:
            result = tool["module"].run()

            if isinstance(result, tuple) and len(result) == 2:
                output_data, input_data = result
            else:
                output_data = result

            print("\n====== 工具输出 ======")
            print(output_data)
            print("======================\n")
            input("[!] 按回车键返回菜单...")


        except Exception as e:
            status = "failed"
            output_data = f"{e}\n\n{traceback.format_exc()}"

            print("\n[!] 工具运行失败：")
            print(output_data)
            input("[!] 发生错误，按回车键返回菜单...")

        # 写入 MySQL 日志
        try:
            add_run_log(
                tool_id=tool["tool_id"],
                input_data=json.dumps(input_data, ensure_ascii=False),
                output_data=str(output_data),
                status=status
            )
        except Exception as e:
            print("[!] 写入运行日志失败：", e)


if __name__ == "__main__":
    main()



