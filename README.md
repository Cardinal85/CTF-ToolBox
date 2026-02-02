# 🧰 CTF ToolBox

一个 **本地化、插件式的 CTF 工具库**，基于 **Python + MySQL**。
 目标是：**让写工具的人只写工具，其它事情交给框架。**

> 把工具丢进 `tools/`，程序会自动识别、注册、记录运行。

------

## ✨ 特性

- 🔌 **插件式工具系统**
- 🧠 **自动扫描 / 自动注册工具**
- 🗃️ **工具与运行日志自动写入 MySQL**
- 🧾 **完整记录每次工具运行**
- 🤝 **社区友好（无需改主程序）**
- 🧪 **适合 CTF / 学习 / 本地工具箱**

------

## 📁 项目结构

```
ctf_toolbox/
├─ main.py              # 主程序入口
├─ config.py            # 数据库配置
├─ db.py                # 数据库操作（CRUD）
├─ init_db.py           # 数据库初始化（首次自动执行）
├─ tools/               # 工具插件目录
│  ├─ __init__.py
│  ├─ _template_tool.py # 工具开发模板（不会被加载）
│  ├─ base64_tool.py
│  ├─ md5_calc.py
│  ├─ md5_crack.py
│  ├─ hex_codec.py
│  └─ xor_tool.py
├─ requirements.txt
└─ README.md
```
------

## 🧩 环境要求

在运行本项目之前，请确保你的环境满足以下条件：

### 🐍 Python

- **Python 3.8 或以上**
- 推荐使用 **Python 3.9 / 3.10**

检查版本：

```
python --version
```

------

### 🗃️ MySQL

- **MySQL 5.7+ 或 MySQL 8.x**
- 需要一个有建库/建表权限的账号
- MySQL 服务需已启动

检查服务状态（示例）：

```
mysql -u root -p
```


------


### 🧠 其他说明

- 不依赖 Docker
- 不依赖 Web 框架
- 不需要虚拟环境（但**推荐使用 venv**）

创建虚拟环境（可选）：

```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

------



## 🚀 快速开始

### 1️⃣ 安装依赖

```
pip install -r requirements.txt
```

或手动：

```
pip install mysql-connector-python
```

------

### 2️⃣ 配置数据库

编辑 `config.py`：

```
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "ctf_toolbox"
```

> ⚠️ 请确保 MySQL 已启动

------

### 3️⃣ 运行程序

```
python main.py
```

程序会自动：

- 初始化数据库（仅第一次）
- 扫描 `tools/` 目录
- 注册新工具
- 显示工具菜单

------

## 🧩 工具开发指南

### ✅ 开发规范

- **一个工具 = 一个 `.py` 文件**
- 放在 `tools/` 目录
- 必须包含：
  - `TOOL_INFO`
  - `run()` 函数

### 示例：`tools/example_tool.py`

```
TOOL_INFO = {
    "name": "示例工具",
    "description": "这是一个示例",
    "category": "misc",
    "author": "community",
    "version": "1.0"
}

def run():
    text = input("请输入内容: ").strip()
    return f"你输入的是: {text}", {"input": text}
```


------

### 🔁 run() 返回值说明

| 返回方式                    | 说明                    |
| --------------------------- | ----------------------- |
| `return output`             | 仅输出结果              |
| `return output, input_data` | 输出 + 运行参数（推荐） |

`input_data` 会被自动写入数据库运行日志。




------

## 🗃️ 数据库说明

### tools 表

- 存储工具元信息
- 自动同步

### run_logs 表

- 记录每次工具运行
- 包含：工具、输入、输出、状态、时间

------

## 🤝 社区贡献方式

1. 复制 `tools/_template_tool.py`
2. 重命名为你的工具名（如 `my_tool.py`）
3. 实现 `run()` 函数
4. 填写 `TOOL_INFO`
5. 放入 `tools/` 即可使用

------

## 📌 开发约定

- `_template_tool.py` 仅作为模板，不会被加载
- 工具应保持 **单一功能**
- 不直接操作数据库
- 不修改主程序逻辑

------

## 📜 License

仅用于 **学习 / CTF / 本地研究**
 请勿用于非法用途。

