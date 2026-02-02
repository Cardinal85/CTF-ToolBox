import mysql.connector
from config import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB

# 连接数据库
def get_conn():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        autocommit=False
    )


# 添加工具
def add_tool(tool_key, name, description, category, author, version, entry_file, enabled=1):
    sql = """
    INSERT INTO tools(tool_key, name, description, category, author, version, entry_file, enabled)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (tool_key, name, description, category, author, version, entry_file, enabled))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()



def get_tool_by_entry_file(entry_file: str):
    """
    根据 entry_file 查找工具
    :param entry_file: 工具文件路径
    :return: 工具记录（如果存在），否则 None
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tools WHERE entry_file = %s", (entry_file,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result




def get_all_tool_keys_from_db():
    tool_keys = set()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT tool_key FROM tools")
    rows = cur.fetchall()
    for row in rows:
        tool_keys.add(row[0])
    cur.close()
    conn.close()

    return tool_keys


def delete_tool_by_key(tool_key: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tools WHERE tool_key = %s", (tool_key,))
    conn.commit()
    cur.close()
    conn.close()


# 查询工具列表，并返回工具数据
def list_tools(enabled_only=True):
    if enabled_only:
        sql = "SELECT * FROM tools WHERE enabled=1 ORDER BY id ASC"
    else:
        sql = "SELECT * FROM tools ORDER BY id ASC"

    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

# 根据id搜索工具
def get_tool_by_id(tool_id):
    sql = "SELECT * FROM tools WHERE id=%s LIMIT 1"
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (tool_id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

# 根据key搜索工具
def get_tool_by_key(tool_key):
    sql = "SELECT * FROM tools WHERE tool_key=%s LIMIT 1"
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (tool_key,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

# 启用或关闭工具
def set_tool_enabled(tool_id, enabled: int):
    sql = "UPDATE tools SET enabled=%s WHERE id=%s"
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (enabled, tool_id))
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()


# 添加运行记录
def add_run_log(tool_id, input_data="", output_data="", status="success"):
    sql = """
    INSERT INTO run_logs(tool_id, input_data, output_data, status)
    VALUES (%s, %s, %s, %s)
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (tool_id, input_data, output_data, status))
        conn.commit()
        return cur.lastrowid
    finally:
        cur.close()
        conn.close()