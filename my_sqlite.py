#!/usr/bin/env python3
'''
將資料儲存到 sqlite，資料庫名稱: "professor_data.db"

此程式由 GPT 生成，因為我對於 sqlite3 不熟悉，我討厭 SQL! 我覺得 "非關聯資料庫" 比較讚!
'''

import sqlite3

def store(data: list[dict]) -> None:
    """Store a list of professor records into a local SQLite database.

    The function creates (if not already existing) three tables in the
    `professor_data.db` SQLite database:

    - `professor_data`: Stores the professor's basic information.
    - `experience`: Stores the work experience of each professor.
    - `research_field`: Stores the research fields associated with each professor.

    Professors are uniquely identified by their name. If a professor already
    exists in the database, their record will be skipped.

    Args:
        data (list[dict]): A list of dictionaries, each containing information
            about a professor. Expected keys in each dictionary:
            
            - "姓名" (str): Full name of the professor.
            - "職稱" (str): Job title.
            - "學歷" (str): Education background.
            - "經歷" (list[str]): List of work experiences.
            - "研究領域" (list[str]): List of research areas.
            - "email" (str): Email address.
            - "辦公室" (str): Office location.
            - "Office hour" (str): Office hours.

    Returns:
        None
    """
    conn = sqlite3.connect('professor_data.db')
    cursor = conn.cursor()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER,
            experience TEXT,
            FOREIGN KEY (professor_id) REFERENCES professor_data(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_field (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER,
            research_field TEXT,
            FOREIGN KEY (professor_id) REFERENCES professor_data(id)
        )
    ''')

    for professor in data:
        cursor.execute('''
            SELECT COUNT(*) FROM professor_data WHERE name = ?
        ''', (professor['姓名'],))
        count = cursor.fetchone()[0]

        if count != 0:
            continue  # 如果已經有這位教授的資料了

        cursor.execute('''
            INSERT INTO professor_data (name, title, education, email, office, office_hour)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            professor['姓名'], professor['職稱'], professor['學歷'],
            professor['email'], professor['辦公室'], professor['Office hour']
        ))

        professor_id = cursor.lastrowid

        for experience in professor['經歷']:
            cursor.execute('''
                INSERT INTO experience (professor_id, experience)
                VALUES (?, ?)
            ''', (professor_id, experience))

        for field in professor['研究領域']:
            cursor.execute('''
                INSERT INTO research_field (professor_id, research_field)
                VALUES (?, ?)
            ''', (professor_id, field))

    conn.commit()
    conn.close()