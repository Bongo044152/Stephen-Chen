"""
主程序入口: selenium
"""

# config and logger
from config.setting import CHROME_DRIVER_PATH, EXECUTE_CHROME_PATH, TARGET_URL, PAGE_COUNT, OUTPUT_FILE
from utils.logger import my_logger

# selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

# 解析數據工具
from parsers.professor_parser import ProfessorParser

# sqlite
from my_sqlite import store

import time, os, json

# Error
class Error(Exception):
    def __init__(self, message):
        super().__init__(message)

## service
service = Service(executable_path = CHROME_DRIVER_PATH)

## chrome-option
chrome_options = Options()
chrome_options.binary_location = EXECUTE_CHROME_PATH

# https://stackoverflow.com/questions/79330158/python-selenium-error-sandbox-cannot-access-executable
chrome_options.add_argument("--no-sandbox") # 禁用 sandbox

chrome_options.add_argument("--disable-gpu") # 禁用 GPU 加速
chrome_options.add_argument("--log-level=3") # 禁止 ChromeDriver 的錯誤輸出

## driver GET target_url
driver = webdriver.Chrome(service=service, options=chrome_options)

## Wait
wait = WebDriverWait(driver, 15)

def get_data() -> list[str] :
    """
    取得網頁的資料

    Returns:
        list[str]: 很多 html 所組成的 list
    """
    htmls = []
    for i in range(PAGE_COUNT):
        url = TARGET_URL + f"?page_no={i+1}"# 生成 url

        my_logger.info(f"開始獲取: {url}")

        driver.get(url)
        htmls.append(driver.page_source) # 解果儲存
    return htmls

def main():

    # 解析教授數據
    my_logger.info(f"開始獲取數據")
    html_results = get_data()
    all_professors = []

    my_logger.info(f"開始解析資料!!!!!!!")
    for html in html_results:
        if html:
            professors = ProfessorParser.parse_html(html)
            all_professors.extend(professors)

    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        my_logger.info(f"一共找到 {len(all_professors)} 位教授的資訊")
        my_logger.info(f"儲存成 json 格式的資料，位於 {OUTPUT_FILE}")
        json.dump(all_professors, f, indent=4, ensure_ascii=False)

    my_logger.info("將資料儲存至 SQLite 資料庫")
    store(all_professors)
    my_logger.info("資料已成功儲存至 SQLite 資料庫")


if __name__ == '__main__':
    main()