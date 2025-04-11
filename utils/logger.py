"""
日誌模組，配置並提供日誌功能
如果要新增日誌功能，會建議專門弄一個 logger 資料夾，但是現在沒必要
"""
import logging
import os
from datetime import datetime

def init_logger(level: str = 'I') -> logging.Logger:
    """
    Initializes and configures the logger.

    Args:
        level (str): The logging level (default is 'I' for INFO).
                    Accepted values:
                    'D' = DEBUG
                    'I' = INFO
                    'W' = WARNING
                    'E' = ERROR
                    'C' = CRITICAL

    Returns:
        logging.Logger: A configured logger instance.
    
    Raises:
        AttributeError: If an invalid logging level is provided.
    """

    # 統一大寫
    level = level.upper()

    # 日誌等級映射
    level_map = {
        'D': logging.DEBUG,
        'I': logging.INFO,
        'W': logging.WARNING,
        'E': logging.ERROR,
        'C': logging.CRITICAL
    }
    if level not in level_map:
        raise AttributeError("參數錯誤! 預期接受:\n'D'=DEBUG, 'I'=INFO, 'W'=WARNING, 'E'=ERROR, 'C'=CRITICAL")
    log_level = level_map.get(level, logging.INFO) # 再次確保不會出現異常
    
    my_logger = logging.getLogger('my_logger')
    my_logger.setLevel(log_level)

    ## basic config
    handler  = logging.StreamHandler() # shell output
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    ## add config
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    return my_logger

my_logger = init_logger('I')