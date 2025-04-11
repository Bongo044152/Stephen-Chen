"""
專案設定檔
"""
import os

# 目標網站
TARGET_URL = "https://csie.asia.edu.tw/zh_tw/associate_professors_2"

# 資料儲存配置
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(
    DATA_DIR,
    exist_ok=True # 確保不會拋出 OSError
)
OUTPUT_FILE = os.path.join(DATA_DIR, "professors.json")

# 爬蟲配置
MAX_WORKERS = 5 # 最大異步線程
TIMEOUT = 5     # request 的最大等待時間 (s)
PAGE_COUNT = 2  # 爬取頁數

# selenium 設定
CHROME_DRIVER_PATH = os.path.abspath(r".\chromedriver\chromedriver.exe")
EXECUTE_CHROME_PATH = os.path.abspath(r".\chrome\chrome.exe")