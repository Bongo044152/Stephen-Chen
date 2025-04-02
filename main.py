import requests # 獲取網站
from bs4 import BeautifulSoup      # 解析數據
import json, os # 儲存資料
import random   # 隨機功能
import sys      # 系統控制，這邊是為了強制退出程式

# 日誌
from my_logger import init_logger

# 異步處理
import asyncio
from functools import wraps
from concurrent.futures import ThreadPoolExecutor  # 引入 ThreadPoolExecutor

# email 部分處理
import re
import base64

# 運行時間
import time

# 目標網站
target_url = "https://csie.asia.edu.tw/zh_tw/associate_professors_2"
file_path = "data.json"

# init my log
my_logger = init_logger('I')

# 裝飾器實現異步處理同步函數
def async_request(func) -> None:
    """將同步請求包裝為異步函數"""
    @wraps(func)
    async def wrapper(executor:ThreadPoolExecutor, *args, **kwargs):
        loop = asyncio.get_event_loop()
        # 使用 executor 來執行同步請求
        res = await loop.run_in_executor(executor, func, *args, **kwargs)
        if 'error' in res:
            my_logger.info("心懸是北七!")
            error_mes = res['error']
            if error_mes == 'Timeout':
                my_logger.warning(f"檢測到請求超時，該結果不採用\nurl: {kwargs['url']}")
            elif error_mes == 'HTTPError':
                my_logger.warning(f"{res['message']}! 請確保該錯誤得到合適的處裡")
            elif error_mes == 'RequestException':
                my_logger.warning(f"本地端錯誤!\n{res['message']}")
            elif error_mes == 'UnknownError':
                my_logger.warning(f"未被分類的錯誤!\n{res['message']}")
            else:
                my_logger.critical("未經過妥善處裡的錯誤! 強制暫停程式運行..")
                sys.exit(-1)
        else:
            return res['content']
        return None
    return wrapper

# function defined for request
def get_random_user_agent() -> str:
    """隨機取得 user_agent"""
    my_logger.debug("獲取隨機的 user_agents")

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(user_agents)

# 使用 "異步處裡"，加快速度
@async_request
def fetch_page(url:str, parms:dict = None) -> dict:
    """獲取網頁訊息

    @parms:
        - url: 網頁的 url
        - parms = None: 用來設定 request 的查詢參數，因為學校的網頁有下一頁。
    @return:
        - json格式的資料
    """
    my_logger.info(f"開始爬取網站...\n目標網址: {url}, {parms}")

    headers = { 'User-Agent': get_random_user_agent() }
    response = requests.get(url, headers=headers, params=parms, timeout=3)
    try:
        response.raise_for_status()
        return {'content' : response.text}

    except requests.exceptions.Timeout:
        # 請求超時
        my_logger.error(f"請求超時: {url}")
        return {"error": "Timeout", "url": url}

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 401:
            my_logger.error(f"401 错误 - 未经授权: {url}")
            return {"error": "HTTPError", "message": "未经授权", "status_code": 401, "url": url}
        elif status_code == 403:
            my_logger.error(f"403 错误 - 禁止访问: {url}")
            return {"error": "HTTPError", "message": "禁止访问", "status_code": 403, "url": url}
        elif status_code == 404:
            my_logger.error(f"404 错误 - 未找到页面: {url}")
            return {"error": "HTTPError", "message": "页面未找到", "status_code": 404, "url": url}
        elif status_code == 500:
            my_logger.error(f"500 错误 - 服务器内部错误: {url}")
            return {"error": "HTTPError", "message": "服务器内部错误", "status_code": 500, "url": url}
        else:
            # 处理其他 HTTP 错误
            my_logger.error(f"HTTP 错误 ({status_code}) - {url}: {e}")
            return {"error": "HTTPError", "message": str(e), "status_code": status_code, "url": url}

    except requests.exceptions.RequestException as e:
        # 捕获所有的 requests 库引发的异常 -> AI 建議
        my_logger.error(f"请求错误 ({url}): {e}")
        return {"error": "RequestException", "message": str(e), "url": url}

    except Exception as e:
        my_logger.error(f"未知错误 ({url}): {e}")
        return {"error": "UnknownError", "message": str(e), "url": url}

# 資料清洗
def get_inf(item) -> dict:
    """
    獲取有效訊息，格式如下:
    @return:
        {
            "姓名": str | null,
            "職稱": str | null,
            "學歷": str | null,
            "經歷": list[str],
            "研究領域": list[str],
            "email": str | null,
            "辦公室": str | null,
            "Office hour": str | null
        }
    """
    my_logger.debug("開始清洗資料...")

    # 預設資訊
    res = {
        "姓名": None, "職稱": None,
        "學歷": None, "經歷": [],
        "研究領域": [], "email": None,
        "辦公室": None, "Office hour": None
    }
    # 搜尋的目標資訊
    search = ["姓名", "職稱", "學歷", "辦公室", "經歷", "email", "研究領域", "Office hour"]
    get_content = lambda txt: txt[txt.find(":") + 2:].replace('\xa0', '').strip('\n').strip()
    def get_email(html_string:str):
        """因應網頁設計，這邊專門做個 function 處裡"""
        my_logger.debug("進行 email 解碼..")
        assert type(html_string) == str, "參數錯誤"
        base64_email_pattern = r'atob\("([^"]+)"\)'  # 正規畫表達式 regex: 捕捉 atob() 中的 Base64 字串
        match = re.search(base64_email_pattern, html_string)
        
        if match:
            # 提取 並 解碼
            base64_email = match.group(1)
            decoded_email = base64.b64decode(base64_email).decode('utf-8')
            return decoded_email.strip()
        else:
            return None
    
    # 開始搜尋
    for i in range(len(item)):
        current_li = item[i]  # 現在的 li 元素
        for s in search:
            if s in current_li.text:
                if s == '研究領域':
                    res[s] = get_content(current_li.text).split('、')
                elif s == 'Office hour':
                    office_hour = current_li.select_one('a')['href']
                    res[s] = f"時程表: {office_hour}"
                elif s == '經歷':
                    try:
                        temp = str(current_li.select_one('span:nth-of-type(2)'))
                        text_ls = temp.split("<br/>")
                        text_ls = [re.sub(r'<[^>]+>', '', txt).strip() for txt in text_ls if txt.strip()]
                        res[s] = text_ls
                    except Exception as e:
                        my_logger.warning(f"解析經歷資料時出錯: {e}")
                else:
                    res[s] = get_content(current_li.text)
                break
    # email 格式單獨處理 -> 沒有欄位
    res['email'] = get_email(str(item))

    my_logger.debug(f"{res['姓名']} 執行完畢!")
    return res

async def main():
    time_start = time.time()
    my_logger.info("程式開始運行!")

    # 異步操作
    with ThreadPoolExecutor(max_workers=min(10, os.cpu_count() * 2)) as executor:
        tasks = []
        # 目標網頁頁數，只有兩頁!
        for i in range(1, 3):
            parms = {'page_no': i}
            tasks.append(fetch_page(executor, target_url, parms))  # 增加到待執行的任務列表

        # 等待所有異步任務完成
        results = await asyncio.gather(*tasks)
        my_logger.info("獲取資料完畢!")

    professors_data = []
    for html in results:
        if not html:
            continue

        # 原始網頁資料
        soup = BeautifulSoup(html, features="html.parser")
        self_introductions = soup.select('.i-member-item.col-md-6')

        # 清洗並儲存資料
        my_logger.info("開始清洗資料..")
        for context in self_introductions:
            line = context.select('li')
            professor_info = get_inf(line)
            professors_data.append(professor_info)
            my_logger.debug(professor_info)

    # 寫入硬碟
    with open(file_path, "w", encoding='utf-8') as f:
        my_logger.info(f"一共找到 {len(professors_data)} 位教授的資訊")
        my_logger.info(f"儲存成 json 格式的資料，位於 {os.path.abspath(file_path)}")
        json.dump(professors_data, f, indent=4, ensure_ascii=False)
    my_logger.info(f"運行結束，花費時間 {round(time.time() - time_start, 4)}")


if __name__ == '__main__':
    asyncio.run(main())