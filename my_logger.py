import logging  # 日誌輸出

# 可以參考 : https://zx7978123.medium.com/python-logging-%E6%97%A5%E8%AA%8C%E7%AE%A1%E7%90%86%E6%95%99%E5%AD%B8-60be0a1a6005
def init_logger(lv: str = 'D') ->'logging.Logger':
    """
    @parms:
        - lv: 日誌輸出等級， 'I' 表示 INFO ， 'D' 表示 DEBUG
    @return:
        - logging.Logger
    @raise:
        - AttributeError : 接收到錯誤的參數
    """

    # 預設
    level = logging.DEBUG

    if lv.upper() == 'D':
        level = logging.DEBUG
    elif lv.upper() == 'I':
        level = logging.INFO
    else:
        raise AttributeError("錯誤的初始化! 只接受 'D' 或 'I' 作為參數")


    my_logger = logging.getLogger('my_logger')
    my_logger.setLevel(level)

    ## basic config
    handler  = logging.StreamHandler() # shell output
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    ## add config
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)

    return my_logger