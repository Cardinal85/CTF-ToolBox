import mysql.connector
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


def init_db():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,

    )

    cur = conn.cursor()

    # 创建数据库
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} DEFAULT CHARSET utf8mb4")
    cur.execute(f"USE {MYSQL_DB}")

    # 创建表 tools
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tools (
        id INT PRIMARY KEY AUTO_INCREMENT,
        tool_key VARCHAR(64) NOT NULL UNIQUE,
        name VARCHAR(128) NOT NULL,
        description TEXT ,
        category VARCHAR(64) DEFAULT 'unknown',
        author VARCHAR(64) DEFAULT 'unknown',
        version VARCHAR(32) DEFAULT '1.0',
        entry_file VARCHAR(255) NOT NULL UNIQUE ,
        enabled TINYINT(1) DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 创建表 run_logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS run_logs (
        id INT PRIMARY KEY AUTO_INCREMENT,
        tool_id INT NOT NULL,
        run_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        input_data TEXT,
        output_data TEXT,
        status VARCHAR(16) DEFAULT 'success',
        FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)


    conn.commit()
    cur.close()
    conn.close()

    print("[OK] 初始化完成：数据库与数据表已创建")


if __name__ == "__main__":
    init_db()
