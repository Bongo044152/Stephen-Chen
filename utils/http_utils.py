"""
HTTP 請求工具
"""
import random
import requests
from utils.logger import my_logger
from config.user_agents import USER_AGENTS
from config.setting import TIMEOUT

def get_random_user_agent():
    """
    隨機取得 user_agent
    
    Returns:
        str: 隨機選擇的 User-Agent
    """
    my_logger.debug("獲取隨機的 user_agents")
    return random.choice(USER_AGENTS)

def fetch_page(url, params=None, timeout=TIMEOUT):
    """
    獲取網頁訊息
    
    Args:
        url (str): 網頁的 URL
        params (dict, optional): 請求參數
        timeout (int, optional): 請求超時時間
    
    Returns:
        dict: 包含響應內容或錯誤信息的字典
    """
    my_logger.info(f"開始爬取網站...\n目標網址: {url}, {params}")
    
    headers = {'User-Agent': get_random_user_agent()}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return {'content': response.text}
        
    except requests.exceptions.Timeout:
        my_logger.error(f"請求超時: {url}")
        return {"error": "Timeout", "url": url}
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_map = {
            401: "未經授權",
            403: "禁止訪問",
            404: "頁面未找到",
            500: "伺服器內部錯誤"
        }
        message = error_map.get(status_code, str(e))
        my_logger.error(f"{status_code} 錯誤 - {message}: {url}")
        return {"error": "HTTPError", "message": message, "status_code": status_code, "url": url}
        
    except requests.exceptions.RequestException as e:
        my_logger.error(f"請求錯誤 ({url}): {e}")
        return {"error": "RequestException", "message": str(e), "url": url}
        
    except Exception as e:
        my_logger.error(f"未知錯誤 ({url}): {e}")
        return {"error": "UnknownError", "message": str(e), "url": url}