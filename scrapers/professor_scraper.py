"""
教授資訊爬蟲模組
"""
import json
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from utils.logger import my_logger
from utils.async_utils import async_request
from utils.http_utils import fetch_page
from parsers.professor_parser import ProfessorParser
from config.setting import TARGET_URL, OUTPUT_FILE, MAX_WORKERS, PAGE_COUNT

class ProfessorScraper:
    """教授資訊爬蟲類"""
    
    def __init__(self):
        """初始化爬蟲"""
        self.target_url = TARGET_URL
        self.output_file = OUTPUT_FILE
        self.max_workers = MAX_WORKERS
        self.page_count = PAGE_COUNT

    # 這邊我使用了 decorator 的寫法! @async_request 設計上搭配 fetch_page
    @async_request
    def _fetch_page_wrapper(self, url, params=None):
        """
        封裝 fetch_page 函數為可異步調用
        
        Args:
            url (str): 目標 URL
            params (dict, optional): 請求參數
            
        Returns:
            dict: HTTP 響應或錯誤信息
        """
        return fetch_page(url, params)
    
    async def scrape(self):
        """
        執行爬蟲並保存結果
        
        Returns:
            bool: 是否成功
        """
        time_start = time.time()
        
        try:
            # 獲取教授數據
            professors_data = await self._fetch_professors_data()
            
            # 寫入文件
            if professors_data:
                self._save_to_file(professors_data)
                my_logger.info(f"運行結束，花費時間 {round(time.time() - time_start, 3)}")
                return True
            else:
                my_logger.error("未獲取到任何教授資料")
                return False
                
        except Exception as e:
            my_logger.error(f"爬蟲過程中發生錯誤: {e}")
            return False
    
    async def _fetch_professors_data(self):
        """
        獲取所有教授資料
        
        Returns:
            list: 教授資料列表
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = []
            
            # 設置爬取任務
            for i in range(1, self.page_count + 1):
                params = {'page_no': i}
                tasks.append(self._fetch_page_wrapper(executor, self.target_url, params))
            
            # 執行所有任務
            html_results = await asyncio.gather(*tasks)
            my_logger.info("獲取網頁資料完畢!")
        
        # 解析教授數據
        all_professors = []
        for html in html_results:
            if html:
                professors = ProfessorParser.parse_html(html)
                all_professors.extend(professors)
        
        return all_professors
    
    def _save_to_file(self, data):
        """
        保存數據到 JSON 文件
        
        Args:
            data (list): 要保存的數據
        """
        import os
        
        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, "w", encoding='utf-8') as f:
            my_logger.info(f"一共找到 {len(data)} 位教授的資訊")
            my_logger.info(f"儲存成 json 格式的資料，位於 {os.path.abspath(self.output_file)}")
            json.dump(data, f, indent=4, ensure_ascii=False)