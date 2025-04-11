"""
異步處理工具模組
"""
import asyncio
import functools
from utils.logger import my_logger

def async_request(func):
    """
    A decorator to wrap synchronous functions and make them asynchronous.
    
    This decorator allows synchronous functions to be executed asynchronously 
    by running them in a separate thread pool executor.

    Args:
        func: The synchronous function to be wrapped.
    
    Returns:
        A wrapper function that performs the asynchronous execution of `func`.
    """

    @functools.wraps(func)
    async def wrapper(self, executor, *args, **kwargs) -> None | str:
        loop = asyncio.get_event_loop()
        try:
            res = await loop.run_in_executor(
                executor, 
                lambda: func(self, *args, **kwargs)  # 正確處理 self 參數
            )
        except Exception as e:
            my_logger.error(f"運行錯誤! {e}")
            return None  # 發生異常時返回 None，表示沒有資料
        
        if isinstance(res, dict) and 'error' in res:
            my_logger.info("檢測到錯誤回傳，開始進行錯誤處理")
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
            # HTML 或者 None，但這邊一定是 HTML，因為後者不會發生，這邊是 "防禦性編程"
            return res['content'] if isinstance(res, dict) and 'content' in res else None
            
    return wrapper