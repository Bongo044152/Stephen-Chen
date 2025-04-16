import sys, os

# system path
dir_c = __file__
for _ in range(3):
    dir_c = os.path.dirname(dir_c)
sys.path.append(dir_c)

from parsers.professor_parser import ProfessorParser  # 導入 ProfessorParser
from config.setting import TARGET_URL, PAGE_COUNT  # 導入設定
import json
from utils.logger import my_logger
from my_sqlite import store

import scrapy

# 構造起始 URL 列表
urls = []  
for i in range(PAGE_COUNT):
    url = TARGET_URL[i]
    urls.append(url)

class MySpider(scrapy.Spider):
    name = 'go'  # 爬蟲名稱
    start_urls = urls  # 設定起始 URL

    def parse(self, response):
        # 獲取 HTML 內容
        html_content = response.text

        # 解析 HTML 內容
        res = ProfessorParser.parse_html(html_content)
        res_string_data = json.dumps(res, indent=4, ensure_ascii=False)
        print(res_string_data)  # 打印解析結果

        my_logger.info("將資料儲存至 SQLite 資料庫")
        store(res)
        my_logger.info("資料已成功儲存至 SQLite 資料庫")