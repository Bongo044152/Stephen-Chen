#!/usr/bin/env python3
"""
主程序入口: request
"""
import asyncio
from scrapers.professor_scraper import ProfessorScraper
from utils.logger import my_logger

async def main():
    """Main asynchronous entry point.

    This function initializes the scraper and starts the scraping process.
    Logging is used to indicate success or failure of the task.
    """
    my_logger.info("程式開始運行!")

    scraper = ProfessorScraper()
    success = await scraper.scrape()

    if success:
        my_logger.info("爬蟲任務成功完成!")
    else:
        my_logger.error("爬蟲任務失敗!")


if __name__ == '__main__':
    asyncio.run(main())