'''
將資料儲存到 sqlite，資料庫名稱: "professor_data.db"

此程式由 GPT 生成，因為我對於 sqlite3 不熟悉，我討厭 SQL! 我覺得 "非關聯資料庫" 比較讚!
'''

import sqlite3

def store(data: list[dict]) -> None:
    """
    儲存教授資料到 SQLite 資料庫。
    Args:
        data (list[dict]): 每個字典包含教授的基本資料，其中 dict 的格式為：
            {
                "姓名": str, "職稱": str,
                "學歷": str, "經歷": list[str],
                "研究領域": list[str], "email": str,
                "辦公室": str, "Office hour": str
            }
    Returns:
        None
    """
    # 連接 SQLite 資料庫（若資料庫不存在，會自動創建）
    conn = sqlite3.connect('professor_data.db')
    cursor = conn.cursor()

    # 創建 professor_data 表格，這是存儲基本資料的表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            title TEXT,
            education TEXT,
            email TEXT,
            office TEXT,
            office_hour TEXT
        )
    ''')

    # 創建 experience 表格，這是存儲經歷的附屬表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER,
            experience TEXT,
            FOREIGN KEY (professor_id) REFERENCES professor_data(id)
        )
    ''')

    # 創建 research_field 表格，這是存儲研究領域的附屬表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_field (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER,
            research_field TEXT,
            FOREIGN KEY (professor_id) REFERENCES professor_data(id)
        )
    ''')

    # 插入資料
    for professor in data:

        # 查詢教授的名字
        cursor.execute('''
            SELECT COUNT(*) FROM professor_data WHERE name = ?
        ''', (professor['姓名'],))
        count = cursor.fetchone()[0]

        if count != 0:
            return # 教授的資料已經存在
        
        # 插入基本資料到 professor_data 表格
        cursor.execute('''
            INSERT INTO professor_data (name, title, education, email, office, office_hour)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (professor['姓名'], professor['職稱'], professor['學歷'], professor['email'], professor['辦公室'], professor['Office hour']))
        
        # 取得 professor 的 id (資料插入後自動生成的 ID)
        professor_id = cursor.lastrowid
        
        # 插入經歷資料到 experience 表格
        for experience in professor['經歷']:
            cursor.execute('''
                INSERT INTO experience (professor_id, experience)
                VALUES (?, ?)
            ''', (professor_id, experience))
        
        # 插入研究領域資料到 research_field 表格
        for field in professor['研究領域']:
            cursor.execute('''
                INSERT INTO research_field (professor_id, research_field)
                VALUES (?, ?)
            ''', (professor_id, field))

    # 提交並關閉連接
    conn.commit()
    conn.close()