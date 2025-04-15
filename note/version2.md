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
> **[web crawler](https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler) -> [a crawler](https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler): <mark>a computer program that automatically searches for information on the internet</mark>, usually in order to index (= list) internet content.**
- https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/crawler

**CloudFlare:**
> **網路爬蟲、蜘蛛或搜尋引擎機器人，會下載網際網路上所有的內容並製作相關索引。此類機器人旨在學習網站（幾乎）每個網頁，以便有必要時擷取資訊。稱此應用程式為「網路爬蟲」，是因為<mark>「爬行」是用於指代自動存取網站並透過軟體程式取得資料的技術詞彙</mark>。**
- https://www.cloudflare.com/zh-tw/learning/bots/what-is-a-web-crawler/

**Akamai:**
> **<mark>A web crawler is an automated program or bot</mark> that systematically searches websites and indexes the content on them.**
- https://www.akamai.com/glossary/what-is-a-web-crawler

因此，對於網路爬蟲的通俗定義上，就是:**「<mark>一個自動化的網路程式用來從網路上獲取內容，專注在探索</mark>」**。

### web crawer vs web spider vs web scraper

對於 web spider 來說，其意義等同於 web crawer，因為網路爬蟲主要在全球資訊網 ( World Wide Web : www ) 上游走、爬巡，如同蜘蛛在蜘蛛網上爬行一樣。

那麼 scraping 是什麼?
> **<mark>the activity of taking information from a website or computer screen</mark> and <mark>putting it into spreadsheet</mark> (= an electronic document in which information is arranged in rows and columns and can be used in calculations) <mark>on a computer.</mark>**
- https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/scraping

對於 web scraper，我的解釋會是:**「<mark>從特定的網站提取特定的資料，並儲存起來 ( 有利於後續的分析 )</mark>」**。

### 小總結

對於 web scraper 而言，他強調的是數據的抓取，與 web crawer 最大的不同就是:
- web crawer 專注於探索 ( discover ) ，通常用於搜尋引擎，詳細可以跳轉道 [爬蟲的用途與運作方式](##爬蟲的用途與運作方式)。
- web scraper 專注於提取資料，通常會儲存以便於後續的分析 ( 非必要 )。

想要了解更多這兩者之間的差異，有興趣你可以參考[此影片](https://www.youtube.com/watch?v=rcaCxMXKysY)，或者[這篇文章](https://soax.com/blog/web-crawling-vs-web-scraping)。

## 爬蟲的用途與運作方式

剛開始對於"crawler" 的用途，我蠻好奇平常會在生活上麼時候會去使用到？

結果令我蠻震驚的，我們居然每天都會去使用到這些網站：
- Googlebot, the crawler for Google’s search engine
- Bingbot, Microsoft’s search engine crawler
- Amazonbot, the Amazon web crawler
- DuckDuckBot, the crawler for the search engine DuckDuckGo
- YandexBot, the crawler for the Yandex search engine
- Baiduspider, the web crawler for the Chinese search engine Baidu
- Slurp, the web crawler for Yahoo

這些網站都是平時，我們會去使用的到的，一開始會認為說爬蟲聽起來蠻抽象的，但實際去了解，其實他已經存在於你的生活中了


##### 本專案中我以 "web scraper" 為主，而 "scraper" 在抓取時它是如何**運行**的呢？

![scraper運作圖](https://www.promptcloud.com/wp-content/uploads/2023/09/image.png.webp)

首先會向 "scraper" 提供一個統一網址 (URL)，然後 "scraper" 會載入該 URL。 "scraper" 會載入與該頁面相關的所有 HTML 程式碼。對於進階 "web scrapers" 來說，它們可以呈現網站上的所有內容，包括 JavaScript 和層疊樣式表 (CSS) 元素。
然後，"scraper" 會提取資料。它可以被編程來提取網站的所有資料或僅提取想要的資料。在許多情況下，這關乎我們是如何去設定所要的目標資訊，例如價位資訊。
最後一步是 "web scraper" 將蒐集到的資料以使用者可用的方式輸出。這可能在 CSV 檔案中或作為 Excel 電子表格。一些比較進階的 "web scrapers" 可以輸出其他格式，例如 JSON，它可以與應用程式介面 (API) 整合。

- https://www.promptcloud.com/blog/a-complete-guide-to-web-scraping/
- https://www.fortinet.com/resources/cyberglossary/web-scraping
- https://careerfoundry.com/en/blog/data-analytics/web-scraping-guide/#what-is-web-scraping-used-for
- https://www.akamai.com/glossary/what-is-a-web-crawler

## 參考資料

名詞解釋
---
- https://www.reddit.com/r/explainlikeimfive/comments/1cj58cl/eli5_what_are_web_crawlers_and_what_are_they_used/?rdt=49422
- https://research.aimultiple.com/web-crawler/
- https://soax.com/blog/web-crawling-vs-web-scraping
