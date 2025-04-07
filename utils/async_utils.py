"""
異步處理工具模組
"""
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from utils.logger import my_logger
from config.setting import MAX_WORKERS

def async_request(func):
    """
    將同步請求包裝為異步函數的裝飾器
    
    Args:
        func: 要包裝的同步函數
    
    Returns:
        裝飾後的異步函數
    """

    @functools.wraps(func)
    async def wrapper(self, executor, *args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            res = await loop.run_in_executor(
                executor, 
                lambda: func(self, *args, **kwargs)  # 正確處理 self 參數
            )
        except Exception as e:
            my_logger.error(f"運行錯誤! {e}")
            return None  # 發生異常時返回 None
        
        if isinstance(res, dict) and 'error' in res:
            my_logger.info("檢測到錯誤回傳，開始進行錯誤處理邏輯!")
            error_mes = res['error']
            
            if error_mes == 'Timeout':
                my_logger.warning(f"檢測到請求超時，該結果不採用\nurl: {kwargs.get('url', '未知URL')}")
            elif error_mes == 'HTTPError':
                my_logger.warning(f"{res['message']}! 請確保該錯誤得到合適的處理")
            elif error_mes == 'RequestException':
                my_logger.warning(f"本地端錯誤!\n{res['message']}")
            elif error_mes == 'UnknownError':
                my_logger.warning(f"未被分類的錯誤!\n{res['message']}")
            else:
                my_logger.critical("未經過妥善處理的錯誤! 強制暫停程式運行..")
                import sys
                sys.exit(-1)
            return None
        else:
            return res['content'] if isinstance(res, dict) and 'content' in res else res
            
    return wrapper