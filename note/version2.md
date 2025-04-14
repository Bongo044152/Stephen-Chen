# 網路爬蟲介紹

## 什麼是網路爬蟲?

當我嘗試搜尋這個問題，我意外的發現國際上居然沒有對這個名詞有定義 !? ( 像是 IEEE 754 那樣 )

理由是 Web crawler 和 Web scraper 並不是「底層運算或數據格式」的技術（ 像 float、JSON、TCP/IP 那類 ），它們比較像是實作策略或工程術語，所以目前沒有像 IEEE 或 ISO 這類機構來統一定義。

因此為了後續的討論，我們需要先定義什麼是「網路爬蟲」。

### 名詞定義

**wiki:**
> **Web crawler, sometimes called a spider or spiderbot and often shortened to crawler, is an Internet bot that systematically browses the World Wide Web and that is typically operated by search engines for the purpose of Web indexing (web spidering).**
- https://en.wikipedia.org/wiki/Web_crawler

**劍橋辭典:**
> **[web crawler](https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler) -> [a crawler](https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler): a computer program that automatically searches for information on the internet, usually in order to index (= list) internet content.**
- https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler

**CloudFlare:**
> **網路爬蟲、蜘蛛或搜尋引擎機器人，會下載網際網路上所有的內容並製作相關索引。此類機器人旨在學習網站（幾乎）每個網頁，以便有必要時擷取資訊。稱此應用程式為「網路爬蟲」，是因為「爬行」是用於指代自動存取網站並透過軟體程式取得資料的技術詞彙。**
- https://www.cloudflare.com/zh-tw/learning/bots/what-is-a-web-crawler/

**Akamai:**
> **A web crawler is an automated program or bot that systematically searches websites and indexes the content on them.**
- https://www.akamai.com/glossary/what-is-a-web-crawler

因此，對於網路爬蟲的通俗定義上，就是:「一個自動化的網路程式用來從網路上獲取內容，專注在探索」。

### "web crawer" vs "web spider" vs "web scraper"

對於 "web spider" 來說，其意義等同於 "web crawer"，因為網路爬蟲主要在全球資訊網 ( World Wide Web : www ) 上游走、爬巡，如同蜘蛛在蜘蛛網上爬行一樣。

那麼 "scraping" 是什麼?
> **the activity of taking information from a website or computer screen and putting it into spreadsheet (= an electronic document in which information is arranged in rows and columns and can be used in calculations) on a computer.**
- https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/scraping

對於 "web scraper"，我的解釋會是:「從特定的網站提取特定的資料，並儲存起來 ( 有利於後續的分析 )」。

### 小總結

對於 "web scraper" 而言，他強調的是數據的抓取，與 "web crawer" 最大的不同就是:
- "web crawer" 專注於探索 ( discover ) ，通常用於搜尋引擎，詳細可以跳轉道 [爬蟲的用途與運作方式](##爬蟲的用途與運作方式)。
- "web scraper" 專注於提取資料，通常會儲存以便於後續的分析 ( 非必要 )。

想要了解更多這兩者之間的差異，有興趣你可以參考[此影片](https://www.youtube.com/watch?v=rcaCxMXKysY)，或者[這篇文章](https://soax.com/blog/web-crawling-vs-web-scraping)。

## 爬蟲的用途與運作方式

爬蟲的用途最常見是用於搜集資料方面，在這個科技盛行的時代裡，所創造出的資料量也會越來越龐大，搜尋資料時難免會覺得麻煩。這個時候來使用爬蟲爬取時，只需要做好輸入的指令和目標網頁，就可以爬取到關於目標網頁所有的內容，這就是爬蟲的厲害之處。

運作方式我們可以用種子來當作舉例，假如我今天想在PTT版尋找打工資訊，而網頁的網址就像種子一樣，透過種子網址我們可以取得到網頁資料，爬蟲可以從文章列表中取得到每篇文章的種子，然後我們可以限定在所想要的打工地區，接著再透過種子連接到每篇文章，接著我們一樣可以透過設計的規則來取得像是時薪，而取得到的時薪就是我們這次透過爬蟲所取得到的產物喔～。


## 參考資料
- https://www.reddit.com/r/explainlikeimfive/comments/1cj58cl/eli5_what_are_web_crawlers_and_what_are_they_used/?rdt=49422
- https://research.aimultiple.com/web-crawler/
- https://soax.com/blog/web-crawling-vs-web-scraping
- https://soax.com/blog/web-crawling-vs-web-scraping
- https://www.cloudflare.com/zh-tw/learning/bots/what-is-a-web-crawler/