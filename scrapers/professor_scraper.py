"""
教授資訊爬蟲模組
"""
import json
import time
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.logger import my_logger
from utils.async_utils import async_request
from utils.http_utils import fetch_page
from parsers.professor_parser import ProfessorParser
from config.setting import TARGET_URL, OUTPUT_FILE, MAX_WORKERS, PAGE_COUNT

from my_sqlite import store

class ProfessorScraper:
    """Professor Scraper class for scraping professor data."""

    def __init__(self):
        """Initializes the scraper with configuration settings."""
        self.target_url = TARGET_URL
        self.output_file = OUTPUT_FILE
        self.max_workers = MAX_WORKERS
        self.page_count = PAGE_COUNT

    @async_request
    def fetch_page_wrapper(self, url:str, params:dict=None) -> None | str:
        """
        Asynchronously calls the `fetch_page` function to retrieve data.
        
        Args:
            url (str): The target URL to scrape.
            params (dict, optional): Additional parameters for the request.
        
        Returns:
            None | str: The HTML content (str) if data is successfully retrieved.
                        If no data is available or if an error occurs, returns `None`.
        """
        return fetch_page(url, params)

    async def scrape(self) -> bool:
        """
        Executes the scraping process and saves the results.
        
        This function fetches professor data, processes it, 
        and stores the results into a JSON file and an SQLite database.
        
        Returns:
            bool: Returns True if the scraping was successful, False otherwise.
        """
        time_start = time.time()
        
        try:
            # Fetch professor data
            professors_data = await self.fetch_professors_data()
            
            # Save data to a file if available
            if professors_data:
                self.save_to_file(professors_data)
                my_logger.info(f"運行結束，花費時間 {round(time.time() - time_start, 3)}")
                return True
            else:
                my_logger.error("未獲取到任何教授資料")
                return False
                
        except Exception as e:
            my_logger.error(f"爬蟲過程中發生錯誤: {e}")
            return False

    async def fetch_professors_data(self) -> list[dict]:
        """
        Fetches data for all professors asynchronously.

        This function creates asynchronous tasks to fetch multiple pages,
        then parses the HTML content to extract professor information.
        
        Args:
            None
        
        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains
                        data for one professor.
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = []

            # Set up scraping tasks for each page
            for i in range(1, self.page_count + 1):
                tasks.append(self.fetch_page_wrapper(executor, self.target_url[i-1]))
            
            # Execute all tasks and gather results
            html_results = await asyncio.gather(*tasks)
            my_logger.info("獲取網頁資料完畢!")
        
        # Parse professor data from the HTML
        all_professors = []
        for html in html_results:
            if html:
                professors = ProfessorParser.parse_html(html)
                all_professors.extend(professors)
        
        return all_professors

    def save_to_file(self, data: list[dict]) -> None:
        """
        Saves the professor data to a JSON file and stores it in the SQLite database.
        
        Args:
            data (list[dict]): A list of dictionaries containing professor information.
        
        Returns:
            None: This function does not return any value.
        """
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Save the data to a JSON file
        with open(self.output_file, "w", encoding='utf-8') as f:
            my_logger.info(f"一共找到 {len(data)} 位教授的資訊")
            my_logger.info(f"儲存成 json 格式的資料，位於 {os.path.abspath(self.output_file)}")
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Store the data into the SQLite database
        my_logger.info("將資料儲存至 SQLite 資料庫")
        store(data)
        my_logger.info("資料已成功儲存至 SQLite 資料庫")
