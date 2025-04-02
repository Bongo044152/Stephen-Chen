#!/usr/bin/env python3
"""
主程序入口
"""
import asyncio
from scrapers.professor_scraper import ProfessorScraper
from utils.logger import my_logger

async def main():
    """主程序入口"""
    my_logger.info("程式開始運行!")
    
    scraper = ProfessorScraper()
    success = await scraper.scrape()
    
    if success:
        my_logger.info("爬蟲任務成功完成!")
    else:
        my_logger.error("爬蟲任務失敗!")

if __name__ == '__main__':
    asyncio.run(main())