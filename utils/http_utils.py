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
    Returns a randomly selected User-Agent string from the predefined list.

    This function is used to help prevent the scraper from being blocked by rotating
    User-Agent headers.

    Returns:
        str: A randomly chosen User-Agent string.
    """
    my_logger.debug("獲取隨機的 user_agents")
    return random.choice(USER_AGENTS)

def fetch_page(url:str, params:dict=None, timeout:int=TIMEOUT):
    """
    Fetches the content of a web page by sending an HTTP GET request.

    Args:
        url (str): The URL of the web page to scrape.
        params (dict, optional): A dictionary of query parameters to be sent in the request. Defaults to None.
        timeout (int, optional): The timeout period for the request in seconds. Defaults to the `TIMEOUT` constant.

    Returns:
        dict: A dictionary containing either the page content or error information.
            The dictionary has the following keys:
            - 'content': The HTML content of the page (if request is successful).
            - 'error': An error message (if any error occurs during the request).
            - 'message': A detailed error message (for specific HTTP errors).
            - 'status_code': The HTTP status code (for HTTP errors).
            - 'url': The URL that was requested.
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