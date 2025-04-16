# 網路爬蟲介紹

隨著網際網路的迅速發展，網路上的資料量呈指數型成長。許多有價值的資訊往往分散在不同的網站上，若以人工方式收集這些資訊，不僅耗時耗力，也不具有效率。因此，透過自動化的 **Web Crawler** 技術來擷取特定網頁中的資料，已成為現代資料蒐集與分析中不可或缺的一環。

## 什麼是網路爬蟲?

當我嘗試搜尋這個問題，我意外的發現國際標準組織（如制定 IEEE 754 標準的機構）似乎並未對「網路爬蟲」這個術語提供一個如同底層技術標準般的統一定義。

這可能是因為 Web crawler 和 Web scraper 比較偏向應用層面的實作策略或工程術語，而非像浮點數 (float)、JSON 或 TCP/IP 這類屬於基礎運算或數據格式的技術，因此缺乏如 IEEE 或 ISO 等標準組織的官方定義。

因此，為了讓後續討論更加清晰，我們先參考幾個權威來源來理解「網路爬蟲」的普遍定義。

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

### web crawler vs web spider vs web scraper

對於 web spider 來說，其意義等同於 web crawer，因為網路爬蟲主要在全球資訊網 ( World Wide Web : www ) 上游走、爬巡，如同蜘蛛在蜘蛛網上爬行一樣。

那麼 scraping 是什麼?
> **<mark>the activity of taking information from a website or computer screen</mark> and <mark>putting it into spreadsheet</mark> (= an electronic document in which information is arranged in rows and columns and can be used in calculations) <mark>on a computer.</mark>**
- https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/scraping

對於 web scraper，我的解釋會是:**「<mark>從特定的網站提取特定的資料，並儲存起來 ( 有利於後續的分析 )</mark>」**。

### 小總結

對於 web scraper 而言，他強調的是數據的抓取，與 web crawler 最大的不同就是:
- web crawler 專注於探索 ( discover ) ，通常用於搜尋引擎，詳細可以跳轉道 [爬蟲的用途與運作方式](##爬蟲的用途與運作方式)。
- web scraper 專注於提取資料，通常會儲存以便於後續的分析。

想要了解更多這兩者之間的差異，有興趣你可以參考[此影片](https://www.youtube.com/watch?v=rcaCxMXKysY)，或者[這篇文章](https://soax.com/blog/web-crawling-vs-web-scraping)。

## 爬蟲的用途與運作方式

在理解了 Web crawler 與 Web scraper 的基本區別後，接下來我們將聚焦探討 Web crawler 的主要用途及其運作方式。

## Web Crawler

> **你知道嗎？**
> 
> 其實我們每天都在使用由爬蟲所提供的服務，只是你可能沒發現
>
> - Google 搜尋結果（Googlebot）
> - Amazon 商品推薦（Amazonbot）
> - DuckDuckGo 搜尋（DuckDuckBot）
> - Yahoo、Baidu、Yandex⋯⋯
>
> 這些網站都是平時，我們會去使用的到的，一開始會認為說爬蟲聽起來蠻抽象的，但實際去了解，其實他已經存在於你的生活中了

Web Crawler 的核心在於「探索 (Discover)」，最典型的應用就是搜尋引擎。我們將以 Google 的爬蟲 Googlebot 為例，來探討下面的兩個問題：
1. Web Crawler 如何「探索 (Discover)」或發現新的網站?
2. GoogleBot 是如何運作的?

### 什麼是 GoogleBot

Googlebot 正是 Web crawler 的一個典型實例。根據 Google 官方文件：
> **<mark>Googlebot is the generic name for two types of web crawlers used by Google Search:</mark><ul><li>Googlebot Smartphone: a mobile crawler that simulates a user on a mobile device.<li>Googlebot Desktop: a desktop crawler that simulates a user on desktop.</ul>**
- https://developers.google.com/search/docs/crawling-indexing/googlebot

>**<mark>The program that does the fetching is called Googlebot (also known as a crawler, robot, bot, or spider).</mark> Googlebot uses an algorithmic process to determine which sites to crawl, how often, and how many pages to fetch from each site. Google's crawlers are also programmed such that they try not to crawl the site too fast to avoid overloading it. This mechanism is based on the responses of the site (for example, HTTP 500 errors mean "slow down").**
- https://developers.google.com/search/docs/fundamentals/how-search-works

> **<mark>The Googlebot crawler is a tool used by Google to discover and index web pages across the internet.</mark> It systematically scans websites, following links from one page to another, and gathers information about the content on each page. This information is then stored in Google’s index, making it accessible for search queries.**
- https://www.americaneagle.com/insights/blog/post/what-is-googlebot-crawler---how-does-it-work

總的來說，Googlebot 的主要目的是：
1.  **探索 (Discover) / 發現新內容:** 發現網路上新的或更新的內容。
2.  **建立索引 (Indexing):** 對抓取到的網頁內容進行分析、整理，並儲存到 Google 巨大的索引資料庫中，以便使用者搜尋時能快速匹配相關結果。
3.  **監測網站變化：** 定期重新訪問已知網頁，檢查內容是否有更新或頁面是否仍然存在。

### Web Crawler 的運作方式 (以 Googlebot 為例)

以下是一張簡化的 Googlebot 運作流程圖：
![googlebot_work_map](https://resources.americaneagle.com/aecom-blobs/images/default-source/blog-images/how-does-the-googlebot-crawler-work.png?sfvrsn=ce204b57_1)
- [圖片來源](https://www.americaneagle.com/insights/blog/post/what-is-googlebot-crawler---how-does-it-work)

#### Crawling Web Pages
1. **發現 URL (URL Discovery):**
> **Google must constantly look for new and updated pages and add them to its list of known pages. This process is called "URL discovery".** ( 節錄自[官方文件](https://developers.google.com/search/docs/fundamentals/how-search-works) )

從已知的 URL 出發，透過掃描的方式獲取該網頁中存在的新的 URL ( 如果網站有更新之類的.. )。
GoogleBot 會掃描頁面上的所有**連結 (Links)**，將找到的新 URL 添加到一個待訪問的清單（稱為「抓取佇列」）。

註記: 我有好奇過第一個網頁是誰提供的? 經過與 ai 的討論，第一個網頁提交道 google 是以 site map 的形式，類似直接跟 google 說我提供了這些服務/可訪問頁面 之類的..。

2. **請求與抓取 (Request & Crawling):**
首先! 該網頁必須是可訪問的，有些 後端 ( 或稱伺服器 ) 會要求登入；後端實作登入在我的背景知識中一共有3種方式來確定你的訪問是許可的: **(1) jwt驗證**、**(2) session key驗證**、**(3) 第三方驗證--OAuth 2.0**。

有些網站不想要被爬蟲騷擾，或撰寫 `robots.txt` 文件，這是一個後台提供的規則檔案，告知爬蟲哪些頁面可以訪問，哪些不可以，並沒有法規強制規定依定要遵守 `robots.txt`，沒錯你可以無視它!
當然 GoogleBot 肯定是會遵守的。 ( 延伸閱讀: [如何避免被 GoogleBot 騷擾?](https://developers.google.com/search/docs/crawling-indexing/googlebot#blocking-googlebot-from-visiting-your-site) )


#### Analyze Page Content
1. **處理與渲染 (Processing & Rendering):**
就像我們平常使用瀏覽器瀏覽網頁那樣，如果你不知道網頁是如何被渲染到你的瀏覽器的? 有興趣可以翻閱[MDN - Parsing](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work#parsing) 與 [MDN - Render](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work#render)。

> **<mark>During the crawl, Google renders the page and runs any JavaScript it finds using a recent version of Chrome, similar to how your browser renders pages you visit.</mark> Rendering is important because websites often rely on JavaScript to bring content to the page, and without rendering Google might not see that content.** ( 節錄自[官方文件](https://developers.google.com/search/docs/fundamentals/how-search-works) )

#### Store in the Index
1. **索引 (Indexing):**
> **<mark>After a page is crawled, Google tries to understand what the page is about. This stage is called indexing and it includes processing and analyzing the textual content and key content tags and attributes, such as \<title> elements and alt attributes, images, videos, and more.</mark>** ( 節錄自[官方文件](https://developers.google.com/search/docs/fundamentals/how-search-works#indexing) )

正如[官方文件](https://developers.google.com/search/docs/fundamentals/how-search-works#indexing)所述， GoogleBot 沒辦法知道這個網頁是什麼? 因此他會開始分析:

1. 首先 Google 會解析 HTML 並且嘗試性的修復它遇到的問題 ( 對於 HTML，可能是語法錯誤 )
2. 會檢查這個東西是否重複存在過
3. 儲存到 Google 龐大的**索引資料庫**中，使得 Google 能夠在毫秒之間從數萬億個網頁中找到與用戶搜尋查詢最相關的結果。 ( 具體存了什麼我也不知道! )

#### Ranking Algorithms

> **真正的魔法就發生在這一步。搜尋引擎演算法分析索引的網頁以確定其與特定搜尋查詢的相關性和價值。關鍵字使用、內容品質、反向連結和用戶參與度等因素在決定頁面在搜尋結果中的排名方面起著至關重要的作用。** ( 引用自[Understanding the search engines](https://medium.com/@anupama.pathirage/understanding-the-search-engines-88fbef0f0ba6) )

想了解更多細節，參考[官方資訊](https://developers.google.com/search/docs/fundamentals/how-search-works)或者[官方影片](https://www.youtube.com/playlist?list=PLKoqnv2vTMUN83JWBNM6MoBuBcyqhFNY3)。

### 延伸考論：SEO 最佳化

了解爬蟲的運作方式，對於網站管理者進行「搜尋引擎優化 (Search Engine Optimization, SEO)」至關重要。
透過優化網站結構、內容品質、載入速度和技術細節 (如正確使用 robots.txt、提交 Sitemap)，可以幫助爬蟲更有效地發現、抓取和索引頁面，進而可能提升網站在搜尋結果中的自然排名。

## Web Scraper

Web Scraper 的核心在於「擷取（Retrieve）」，最典型的應用就是分析資料。

主要用於包括電子商務智慧、品牌監控和市場研究....，通常會存取資料，以便於日後分析、比較。

本專案目標是要去亞大資工的網頁爬取教授的資料，符合 Web Scraper 的主要特徵，也就是「擷取（Retrieve）」。

### **Scraper** 它是如何**運行**的呢？

![scraper運作圖](https://www.promptcloud.com/wp-content/uploads/2023/09/image.png.webp)
- [圖片來源](https://www.promptcloud.com/blog/a-complete-guide-to-web-scraping/)

#### 1&2&3. 獲取 URL: 使用 pyhton 的 request 等工具，可以向網頁發起 HTTP 請求，以獲取網頁 ( HTML )

我們向目標網址: https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Full_time_faculty 發起網路 http 的 GET 請求。

註記: 我們不需要網路代理，直接發起請求即可。
#### 4. 使用 BeautifulSoup 去定位 HTML 元素，並且解析訊息 
( 這個步驟相當於 Scraper 重混亂訊息中，或許可利用的訊息可以是教授的資料、演唱會門票價格、圖書館營業時間等等 )

在我們的專案中，先是使用
`<ul class="i-member-profile-list" data-list="profile_data" data-level="3">`
來定位每個教授，再逐一過濾 `<li>` 標籤。

#### 5. 將獲取的資料進行清洗
如果是字串的話，可以進行依些訊息優化，例如演唱會門票的是`$1000`，可以去掉`$`，只保留`1000`。

<!-- 例如我們去除了 "姓名:" -->

#### 6. 將資料進行彙整
以演唱會為例，其資料可以整理成json格式:

```json
{
    "prize": 1000,
    "date": "2025.4.16",
    "singer":"周杰倫"
}
```

在本專案中，我們將資訊整理成如下格式，方便後續整理:

```json
{
    "姓名": str, "職稱": str,
    "學歷": str, "經歷": list[str],
    "研究領域": list[str], "email": str,
    "辦公室": str, "Office hour": str
}
```

#### 7. 將資訊儲存於電腦中

最後，我們將教授的資料以 json 檔案儲存於電腦中；此外還使用了 python 提供的 sqlite3 ( 一種輕量級的 SQL 資料庫 )，以關聯式資料庫的形式儲存 ( 可以理解為表格 )。

<!-- 首先會向 "scraper" 提供一個網址 (URL)，提出請求訪問，然後 "scraper" 會載入該 URL。 "scraper" 會載入與該頁面相關的所有 HTML 程式碼。對於進階 "web scrapers" 來說，它們可以呈現網站上的所有內容，包括 JavaScript 和層疊樣式表 (CSS) 元素。
然後，"scraper" 會提取資料。它可以被編程來提取網站的所有資料或僅提取想要的資料。在許多情況下，這關乎我們是如何去設定所要的目標資訊，例如價位資訊。
最後一步是 "web scraper" 將蒐集到的資料以使用者可用的方式輸出。這可能在 CSV 檔案中或作為 Excel 電子表格。一些比較進階的 "web scrapers" 可以輸出其他格式，例如 JSON，它可以與應用程式介面 (API) 整合。 -->

<!-- ### 而什麼是進階的 "web scrapers" 呢？

就好比說專案中有使用的 "Selenium"、 "Requests"、 "Scrapy" 就都是屬於進階的爬蟲，它們最主要的三大共通點是：

- 動態內容抓取工具：這些工具可以抓取由 JavaScript 驅動的內容的網站。他們使用無頭瀏覽器或 Selenium 等自動化工具與網頁互動並提取資料。
- API 抓取工具：這些工具直接與 Web API 互動以擷取結構化資料。許多網站提供 API 來以結構化格式存取其資料
- 以及可以根據需求自定義爬取邏輯、處理函數、條件篩選等 -->

### Python 如何幫助我們爬取網頁

#### **Requests**
Python 的 **Requests** 庫是一個用來簡化 HTTP 請求的工具，它將複雜的請求操作抽象成直覺易懂的 API，讓開發者能更專注於與網路上的資料與服務進行互動。不論是抓取網頁、存取 REST API，或是向伺服器提交資料，Requests 都能輕鬆處理。  
常用於發送 HTTP 請求，例如：**GET**、**POST**、**PUT**、**DELETE** 等。

#### **Selenium**
**Selenium** 是一款開源的自動化測試工具與框架，主要用於模擬使用者與網頁之間的互動。它允許開發者透過程式碼自動操作瀏覽器，像是真人使用者一樣執行點擊按鈕、填寫表單、提交資料等操作，廣泛應用於 Web 功能測試與動態資料擷取。

在使用 Selenium 前，需先從 [Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/) 下載對應版本的 Chrome 瀏覽器與驅動程式（ChromeDriver），確保兩者版本相容，以避免執行錯誤。

#### **Scrapy**
**Scrapy** 是一套強大且高效的開源爬蟲框架，內建完整的爬蟲流程與模組，能夠協助開發者快速構建結構化的資料抓取流程。不僅可用於擷取靜態的 HTML 頁面，也支援 API 資料的擷取與非同步請求。適用於大量抓取像是商品資訊、新聞文章、學術資源或社群媒體內容等。

#### **BeautifulSoup**
**BeautifulSoup** 是 Python 中用來解析 HTML 和 XML 的工具，特別擅長處理格式不完整或有錯誤的網頁原始碼（俗稱 tag soup）。透過建立網頁的結構樹（DOM Tree），使用者可以用直觀的方式擷取頁面中任何感興趣的資料。它常與 Requests 搭配使用，成為資料清洗與抽取的利器。

# 專案概述

本專案使用 **Python** 作為撰寫爬蟲的程式語言，並利用 **Requests** 模組發送 HTTP 請求來獲取網頁原始碼。接著，使用 **BeautifulSoup** 解析 HTML 結構，提取所需的資料。擷取到的資料經過整理和格式化後，將以 **JSON** 格式儲存，同時也會存入 **SQLite** 資料庫中，以便後續查詢與分析。

此外，為了處理動態載入的網頁內容，本專案也使用了 **Selenium** 模擬瀏覽器操作，確保動態資料能夠被有效抓取。對於更大規模的爬蟲需求，專案中還採用了 **Scrapy** 框架，進一步提升爬取效能並支援多線程處理。

### 工具和技術

- **requests**  
    用來發送 HTTP 請求，並從網頁伺服器獲取 HTML 內容。它簡單易用，適合抓取靜態網頁。

- **BeautifulSoup (bs4)**  
    用於解析和篩選 HTML 內容。`BeautifulSoup` 可以輕鬆從 HTML 結構中提取出需要的資料（如標題、鏈接等），並將其轉換成結構化資料。

- **Selenium**  
    用於處理動態載入的網頁，尤其是當網站使用 JavaScript 動態生成內容時。`Selenium` 可以模擬瀏覽器操作，讓爬蟲能夠「讀取」這些動態資料。

- **Scrapy**  
    是一個功能強大的爬蟲框架，適用於複雜的爬蟲需求，支援多線程和分佈式爬取。適合用於大規模資料擷取和高效的資料處理。
  
- **SQLite**  
    用來儲存爬取到的資料。`SQLite` 是一個輕量級的資料庫，適合在本地端存儲結構化資料。它提供簡單的查詢介面，便於後續查詢與分析。
 
這是我本專案中的 docs ( 使用工具自動生成 ): https://stephen-chen.vercel.app/index.html

# 總結

在這日新月異的時代裡，網際網路成為了每日最不可或缺的必備品，它既帶來便利性與知識性，而在網際網路中搜尋引擎的背後，所支撐著是網路爬蟲。可以在有如無底洞般的資料庫裡，不斷地搜索，並收集與整理所得到的資料。而在這份專案中可以理解關於爬蟲的基本理念與定義，以及各種爬蟲的差別，還有如何去運作與執行的（如 Googlebot 的探索、建立索引、監測網站變化），不僅更了解網站的爬取方式，也能從中學習到網站的架構方式。隨著網路技術的更新，在未來的每一天當中都會有新的知識與科技，在更新與進步，而我們在這最重要的事情就是，如何去學習它們，以及增進自己。讓自己不在只是跟隨而已。


## 參考資料

名詞解釋
---
- https://www.reddit.com/r/explainlikeimfive/comments/1cj58cl/eli5_what_are_web_crawlers_and_what_are_they_used/?rdt=49422
- https://research.aimultiple.com/web-crawler/
- https://soax.com/blog/web-crawling-vs-web-scraping

爬蟲的用途與運作方式
---
- https://www.promptcloud.com/blog/a-complete-guide-to-web-scraping/
- https://www.fortinet.com/resources/cyberglossary/web-scraping
- https://careerfoundry.com/en/blog/data-analytics/web-scraping-guide/#what-is-web-scraping-used-for
- https://www.akamai.com/glossary/what-is-a-web-crawler
- https://www.pluralsight.com/resources/blog/guides/advanced-web-scraping-tactics-python-playbook
- https://kanhasoft.com/blog/advanced-web-scraping-techniques-for-complex-websites/
- https://soax.com/glossary/web-scraping
- https://medium.com/@anupama.pathirage/understanding-the-search-engines-88fbef0f0ba6
- https://www.americaneagle.com/insights/blog/post/what-is-googlebot-crawler---how-does-it-work
- https://developers.google.com/search/docs/crawling-indexing/googlebot
- https://developers.google.com/search/docs/fundamentals/how-search-works
- https://www.youtube.com/playlist?list=PLKoqnv2vTMUN83JWBNM6MoBuBcyqhFNY3
