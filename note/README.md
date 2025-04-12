# **期中報告**

本項目為期中作業，利用 **爬蟲技術** 從 [亞洲大學資工系官網](https://csie.asia.edu.tw/zh_tw/associate_professors_2) 獲取每位教授的專長資訊，並將其存取下來。

# **主要函式庫**

## **Request**
- Python 的 Requests 庫被創建用於使 HTTP 請求更加簡單和人性化。請求複雜性抽象變為簡單的 API，可以專注於與網絡上的服務和數據進行交互。 無論抓取網頁和 REST API 互動，還是向伺服器發送數據，Requests 庫都能提供需求。 
最常見用於 **Python** 的HTTP 請求（GET、POST、PUT、DELETE 等）



## **Scrapy**
- Scrapy是一套開放原始碼框架，它已經定義了完整的爬蟲流程與模組，透過這個框架可以快速、簡單的幫助我們抓取HTML頁面、取得API回傳的資料，甚至於可以撰寫非同步網頁爬蟲。像是從網站中自動擷取結構化資料，如商品資訊、新聞文章、學術資料、社群貼文等等。


| 元件名                    | 功能                                 |
|------------------------|------------------------------------|
| **Spider**             | 撰寫的爬蟲邏輯，告訴 Scrapy 要爬哪些頁面、要抓什麼資料    |
| **Item**               | 結構化資料容器（像是 Python 字典）              |
| **Pipeline**           | 對資料做清洗、驗證、儲存等操作                    |
| **Middleware**         | 請求與回應的中介處理，例如換 IP、換 UA、處理 cookie 等 |






## **Selenium**

- Selenium 是一個開源的自動化測試工具和框架，用於測試 Web 應用系統的功能和 UI 畫面。允許開發者編寫腳本來模擬 User 與 Web Browser 的互動。從自動執行一系列的操作，例如點擊按扭，填寫表單及提交等，來測試 Web 的應用系統功能是否正常。

- 在使用**Selenium**前，需要先從 [Chrome for Testing availability](https://googlechromelabs.github.io/chrome-for-testing/)找尋對應自己設備的driver，而後透過 WebDriver，才可以打開瀏覽器，進行模擬 User 操作等。
 

### Selenium + Python 搭配模組

| 模組 | 用途               |
| --- |------------------|
| **BeautifulSoup** | 用來解析 HTML 結構與內容  |
| **Pandas** | 對爬取資料進行結構化處理     |
| **asyncio** | 搭配異步項目提高效率       |
| **logging** | 管理爬蟲過程中的日誌與錯誤輸出  |
| **SQLite / MySQL** | 儲存資料庫型爬蟲結果       |



# 次要函式庫
### BeautifulSoup 
Beautiful Soup是Python中用來解析HTML、XML標籤文件的模組，並能修復含有未閉合標籤等錯誤的文件（此種文件常被稱為tag soup）；解析後會為這個頁面建立一個BeautifulSoup物件，這個物件中包含了整個頁面的結構樹，透過這個BeautifulSoup物件的結構樹，就可以輕鬆的提取頁面內任何有興趣的資料了。


| 功能                  | 說明                             |
|---------------------|--------------------------------|
| 解析 HTML/XML         | 把一整串原始碼解析成樹狀結構                 |
| 查找標籤（Tag）           | 使用 `.find()`、`.find_all()` 等方法 |
| 選擇器查詢（CSS Selector） | 用 `.select()` 快速鎖定特定元素         |
| 讀取文字與屬性             | 拿到 `.text`、`tag['href']` 等內容   |





## **功能特點**
- **自動化**：爬取 **亞洲大學資工系** 教授的專長資訊，無需手動操作
- **高效能**：使用 **異步處理** 提升爬取速度，減少等待時間
- **可追蹤**：內建 **爬蟲運行日誌**，方便除錯與監控
- **標準輸出**：數據以 **JSON 格式** 儲存，便於後續分析與應用
- **規範化日誌輸出**：使用 **Python 的 logging 模組**，以標準格式輸出日誌至終端機
- **將資料儲存到 SQLite**: 使用 **Python 的 sqlite3**，將資料儲存到簡易的資料庫中

## **儲存的資料格式**
1. 終端機輸出 & json 文件: 資料主要以 json 的格式處存，其架構如下:
```
{
    "姓名": str, "職稱": str,
    "學歷": str, "經歷": list[str],
    "研究領域": list[str], "email": str,
    "辦公室": str, "Office hour": str
}
```
2. 透過 `sqlite3` 創建簡易的 SQL 資料庫，經過妥善的處理後將資料儲存
  - 可以透過 [**visualiz_sqlite**](../visualiz_sqlite.ipynb) 視覺化

## **環境設置**
> **請確保 Python 版本 ≥ 3.9** 

### **1. 克隆此專案**
```bash
git clone git@github.com:Bongo044152/Stephen-Chen.git
cd Stephen-Chen
```

### **2. 建立虛擬環境**
```bash
python -m venv .venv
```

### **3. 啟動虛擬環境**
- **Windows PowerShell**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```
- **MacOS/Linux**
  ```bash
  source .venv/bin/activate
  ```

### **4. 安裝依賴套件**
```bash
pip install -r requirements.txt
```

### **5. selenium 環境架設**
對於開發者而言，版本更新意味著舊的套件或許對於目前的應用不相容，這意味著:
  - 如果電腦的 chrome 被更新，那麼救的 chromedriver 就沒有用處了!

所以，我們需要鎖定 chromedriver 以及 chrome 的版本。

如果你是 windows 10 以上的用戶，開啟你的 powershell，輸入以下指令:
```shell
.\download_chrome.ps1
```
> **注意! 這將會下載 64-bit 的版本**

如果你有額外的需求 ( 例如不同的作業系統 )，可以自行下載: https://googlechromelabs.github.io/chrome-for-testing/
  (記得根據 [setting 檔案](config\setting.py) 更改你的資料夾名稱)

### **6. 執行爬蟲程式**
1. 使用 request 實現:
```bash
python my_request.py
```
2. 使用 selenium 實現:
```bash
python my_selenium.py
```
3. 使用 scrapy 實現:
```bash
scrapy crawl go
```

# 爬蟲介紹
爬蟲是屬於自動化的程式，目的是在抓取網站上的資料。通常爬蟲會模擬用戶的瀏覽行為，通過HTTP請求從網站獲取HTML頁面，並分析其內容以提取有用的信息。

### 常見用途：
搜尋引擎像是 Google、Bing 和 Yahoo 等應該是網絡爬蟲最成功的應用了，它們透過爬蟲在網際網路中收集優質的網站與內容，所以當用戶在搜尋引擎上搜尋關鍵字時，就能夠找出相關的網站資料
除了搜尋引擎的爬蟲，也有其他很多的應用，以下舉例幾個常見的用途
- 爬遍所有飯店與航空公司網站，輕鬆找出最划算的房間與機票
- 定期監測特定商品價格，當有降價時，即時通知價格
- 從股票資訊網站中獲取股價、月報、財報等用來追蹤股價趨勢
- 從基金網站中獲取所有基金資料，用來分析最優質的投資項目
- 每天自動下載各個財金新聞網站的標題與內容，快速掌握最新消息
- 批次下載 YouTube 播放清單影片



# 爬蟲的工作原理

爬蟲的基本流程大致如下：

1. **發送請求**：爬蟲向網站發送HTTP請求。
2. **獲取頁面內容**：接收到HTML頁面或其他格式的資料。
3. **解析頁面**：解析HTML結構，提取目標資料（如圖片、文章、鏈接等）。
4. **儲存數據**：將提取到的資料儲存到本地或數據庫中。
5. **迭代抓取**：如果網站包含多頁內容，爬蟲會進一步訪問其他頁面，直到抓取完所有需要的資料。



# 如何編寫爬蟲？

### 1.安裝必要的工具

要寫爬蟲，首先需要安裝一些常用的Python庫：

```bash
pip install requests beautifulsoup4
```

- **requests**：用來發送HTTP請求。
- **BeautifulSoup**：用來解析HTML頁面。

### 2. 編寫簡單的爬蟲

```python
import requests
from bs4 import BeautifulSoup

# 發送請求
url = "https://example.com"
response = requests.get(url)

# 解析HTML頁面
soup = BeautifulSoup(response.text, 'html.parser')

# 提取資料
title = soup.title.text
print(f"頁面標題: {title}")
```

### 3.頁面解析技巧

在爬蟲中，解析HTML結構是一個關鍵步驟。你可以使用**CSS選擇器**或**XPath**來精確定位和提取你需要的資料。

例如：

```python
# 使用CSS選擇器選擇文章標題
article_title = soup.select('h1.article-title')[0].text
```

### 4. 爬蟲常見挑戰

- **反爬蟲技術**：許多網站會使用反爬蟲措施，如IP封鎖、驗證碼等來防止自動化訪問。
- **法律與道德問題**：在進行網絡爬取時，需要遵循相關法律法規及網站的使用條款，避免侵犯版權或濫用數據。
- **效率問題**：大規模抓取時可能會面臨性能瓶頸，如請求速度過快導致伺服器過載。


### 5. 爬蟲工具與框架

### 5.1 Scrapy

Scrapy 是一個強大的Python爬蟲框架，適合進行大規模數據抓取。

```bash
pip install scrapy
```

Scrapy 提供了更多的功能，如異步請求、數據儲存、數據過濾等。

### 5.2 Selenium

Selenium 是一個自動化測試工具，可以用來操作瀏覽器進行網頁抓取，適用於處理JavaScript渲染的動態網頁。

```bash
pip install selenium
```





# 核心模組說明

## **Request**、**Selenium**


| 模組路徑                              | 功能簡述                                                                              |
|-----------------------------------|-----------------------------------------------------------------------------------|
| `my_request.py` 、`my_selenium.py` | 主執行程式，負責初始化流程與整合各模組                                                               |
| `scrapers/professor_scraper.py`   | 負責資料抓取邏輯，包含多頁處理、URL 發送等                                                           |
| `parsers/professor_parser.py`     | 處理 HTML 結構的解析，將教授資訊轉為字典                                                           |
| `utils/async_utils.py`            | 定義 `@async_request` 裝飾器，讓同步函式支援非同步操作                                              |
| `utils/http_utils.py`             | 封裝 HTTP 請求邏輯，包含 User-Agent 模擬與錯誤分類                                                |
| `utils/logger.py`                 | 日誌模組與`Request`模組的結合可以幫助開發者在發送 HTTP 請求、處理響應過程中，並根據設置的日誌級別進行靈活的日誌管理，從而提升除錯與運行監控的能力。 |
| `config/setting.py`               | 控制爬蟲參數，如網址、頁數、超時、輸出路徑等                                                            |



## **Scrapy**

| 模組路徑                     | 功能簡述                                               |
|--------------------------|----------------------------------------------------|
| `my_spider.py`           | 主執行程式，負責初始化流程與整合各模組                                |
| `scrappp/items.py`       | 定義爬取資料的欄位結構，供 `Spider` 抓取`Pipeline` 儲存時使用。         |
| `scrappp/middlewares.py` | 用來插入自訂邏輯的擴展點，攔截 `request`/`response`，控制資料流程與錯誤處理。  |
| `scrappp/pipelines.py`   | 處理與儲存爬取資料的模組，定義好後透過 `process_item()`執行資料清洗或輸出。     |
| `scrappp/settings.py`    | 控制爬蟲行為、資料流程、效能優化與功能擴展的設定檔，是讓你的爬蟲穩定、安全、高效運行的關鍵配置地。  |


## **SQLite**

| 函數名稱                                   | 功能說明                | 影響資料表                                                   | 額外提醒           |
|----------------------------------------|---------------------|---------------------------------------------------------|----------------|
| `fetch_professor_data(professor_name)` | 查詢特定教授的基本資料、經歷與研究領域 | `professor_data`, `experience`, `research_field`        | 若查無資料會提示       |
| `browse_all_data()`                    | 瀏覽所有教授資料與相關表格內容     | 全部表格 (`professor_data`, `experience`, `research_field`) | 僅查詢、不更動資料      |
| `clear_database()`                     | 刪除所有資料表（清空整個資料庫）    | 全部表格                                                    | 資料刪除後**無法還原**  |






# 資料解析方式

### 1. **功能模組**總結


#### 1.1 **HTTP請求工具 (http_utils.py)**
這個模組的主要功能是發送 HTTP 請求，並處理響應和錯誤：
- `get_random_user_agent()`: 隨機選擇一個 User-Agent 來避免被封鎖。
- `fetch_page()`: 發送 GET 請求到指定 URL，並處理回應。它會記錄錯誤，如超時、HTTP錯誤等。
    - 若請求成功，返回 `{'content': response.text}`。
    - 若請求失敗，根據不同的錯誤類型返回錯誤信息（如 `Timeout`, `HTTPError`, 等）。

#### 1.2 **異步處理工具 (async_utils.py)**
這個模組通過裝飾器將同步函數轉換為異步函數，主要應用於非同步請求的處理：
- `async_request(func)`: 用於將同步函數包裝成異步函數，支持異常處理及錯誤分類。
    - 異常會根據錯誤類型輸出，如 `Timeout`、`HTTPError`、`RequestException` 等。

#### 1.3 **日誌模組 (logger.py)**
這個模組提供了基礎的日誌輸出功能：
- `init_logger(level)`: 根據設定的級別來輸出不同的日誌訊息（如 DEBUG、INFO、ERROR等）。
    - 默認日誌級別為 `INFO`，可以根據需要設定為 `DEBUG`, `ERROR` 等來控制日誌的詳細程度。

#### 1.4 **Scrapy設置與中介層 (scrapy)** 
- `MyprojectItem`: 用來定義在 Scrapy 網絡爬蟲項目中使用的數據模型。
    - 每個 `scrapy.Item` 類似於數據結構，可以包含爬取的網頁數據字段。
- `Spider Middleware` 及 `Downloader Middleware`:
    - 用來處理請求和回應的過程，可以進行錯誤處理、異常捕獲、修改請求或響應等操作。
- `MyprojectPipeline`: 在 Scrapy 中處理從爬蟲返回的數據（例如清理數據、存儲到數據庫等）。



### 2. **程式碼功能與Scrapy的關聯**

#### 2.1 **Scrapy專案結構與設定**
- `settings.py`：配置 Scrapy 爬蟲的各種設置，如 User-Agent、請求延遲、最大並發請求等。
- `spider_middleware` 和 `downloader_middleware`：可以對 Scrapy 的請求/回應處理過程進行干預，如錯誤處理、重試機制等。

#### 2.2 **數據流向與處理**
在 Scrapy 的運行過程中，請求被發送到網站，返回的回應會被 `spider_middleware` 或 `downloader_middleware` 進行處理。這些中介層可以記錄請求過程、檢查異常、改寫請求等。

- **Pipeline**: 當數據從爬蟲返回後，它會進入 `item pipelines`，可以在此處處理數據（例如清理數據、存儲到文件、數據庫等）。

#### 2.3 **日誌在Scrapy中的應用**
- Scrapy 本身已經提供了日誌功能，但 `logger.py` 可以進一步定義和優化日誌輸出，並將其應用於爬蟲、請求過程中。它能輸出不同的錯誤，便於後續分析和除錯。
    - 可以在 Scrapy 配置文件中設定日誌級別，並將日誌輸出到文件或控制台。

#### 2.4 **異步請求**
- `async_request` 裝飾器可以與 Scrapy 一起使用，以提高請求處理效率。由於 Scrapy 是基於 Twisted 框架的非同步模型，它支持非同步請求，異步處理工具可以幫助在 Scrapy 中更好地管理請求。



### 3. **總結**

在程式碼中結合了 **Scrapy** 爬蟲框架的功能和一些自定義的工具模組來增強爬蟲的穩定性、效率與可擴展性：

- **異步處理** (`async_request` 裝飾器) 使得請求的處理更加高效，避免阻塞。
- **HTTP請求工具** (`http_utils.py`) 用於發送請求並處理錯誤，並根據請求結果進行適當的日誌記錄。
- **日誌模組** (`logger.py`) 為程式的運行提供詳細的錯誤、警告、信息記錄，幫助您追蹤和除錯。
- **Scrapy設置與中介層** 提供了對請求和響應的處理機制，並且支持錯誤處理、重試等功能。

這些模組的結合的爬蟲項目在穩定性和效率上都有了很大的提升，同時也方便後期維護和擴展。



# 錯誤處理策略
- 所有爬取請求與處理皆包裝於 `@async_request` 裝飾器中
- 自動偵測錯誤類型，分為：
  - `Timeout`：請求超時
  - `HTTPError`：伺服器錯誤
  - `RequestException`：提供明確的錯誤類別 方便使用者進行錯誤補捉
  - `UnknownError`：未知例外狀況
# 輸出資料結構

爬取結果將儲存為 `.json` 檔案，結構如下：

```json
[
  {
    "姓名": None, "職稱": None,
    "學歷": None, "經歷": list[str],
    "研究領域": list[str], "email": None,
    "辦公室": None, "Office hour": None
  
  }
] 
```

