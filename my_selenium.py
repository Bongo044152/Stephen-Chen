#!/usr/bin/env python3
"""
主程序入口: selenium
"""

# Configuration and logger
from config.setting import CHROME_DRIVER_PATH, EXECUTE_CHROME_PATH, TARGET_URL, PAGE_COUNT, OUTPUT_FILE
from utils.logger import my_logger

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Custom parser and DB
from parsers.professor_parser import ProfessorParser
from my_sqlite import store

import time
import os
import json


class Error(Exception):
    """Custom base exception for the crawler."""
    def __init__(self, message):
        super().__init__(message)


# Initialize Selenium Chrome driver
service = Service(executable_path=CHROME_DRIVER_PATH)
chrome_options = Options()
chrome_options.binary_location = EXECUTE_CHROME_PATH

# Chrome driver settings
chrome_options.add_argument("--disable-gpu") # 禁用 GPU 加速
chrome_options.add_argument("--log-level=3") # 禁止

# https://stackoverflow.com/questions/79330158/python-selenium-error-sandbox-cannot-access-executable
chrome_options.add_argument("--no-sandbox") # 禁用 sandbox

# Setup driver
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)


def get_data() -> list[str]:
    """Retrieve HTML pages from the target URL.

    This function iterates through the specified number of pages,
    loads each page using Selenium, and collects the HTML content.

    Returns:
        list[str]: A list of raw HTML strings from each page.
    """
    htmls = []
    for i in range(PAGE_COUNT):
        url = TARGET_URL[i]
        my_logger.info(f"開始獲取: {url}")

        driver.get(url)
        htmls.append(driver.page_source)
    return htmls


def main():
    """Main workflow of the scraper.

    - Launches the crawler and collects HTML pages. ( using selenium )
    - Parses professor information from the HTML.
    - Outputs the results as a JSON file.
    - Stores structured data into an SQLite database.
    """
    my_logger.info(f"開始獲取數據")
    html_results = get_data()
    all_professors = []

    my_logger.info(f"開始解析資料!!!!!!!")
    for html in html_results:
        if html:
            professors = ProfessorParser.parse_html(html)
            all_professors.extend(professors)

    # Write to JSON
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        my_logger.info(f"一共找到 {len(all_professors)} 位教授的資訊")
        my_logger.info(f"儲存成 json 格式的資料，位於 {OUTPUT_FILE}")
        json.dump(all_professors, f, indent=4, ensure_ascii=False)

    # Save to SQLite
    my_logger.info("將資料儲存至 SQLite 資料庫")
    store(all_professors)
    my_logger.info("資料已成功儲存至 SQLite 資料庫")



if __name__ == '__main__':
    main()