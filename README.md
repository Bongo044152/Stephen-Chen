# **期中報告**

本項目為期中作業，利用 **爬蟲技術** 從 [亞洲大學資工系官網](https://csie.asia.edu.tw/zh_tw/TeacherIntroduction/Full_time_faculty) 獲取每位教授的專長資訊，並將其存取下來。

## 功能特點

- **HTML 解析**：透過自製 ProfessorParser 模組，自動擷取教授頁面中的關鍵資訊  
- **Email 解碼還原**：支援解析 JavaScript 混淆的email，還原聯絡資訊  
- **模組化架構**：採用清晰的模組劃分（parsers、scrapers、utils 等），便於擴充與維護  
- **內建錯誤分類回報**： 可辨識多種常見錯誤（如 Timeout、HTTPError、RequestException、UnknownError）
- **資料儲存至 SQLite**：以 Python 的 sqlite3 將結構化資料安全儲存至本地資料庫  
- **JSON 標準輸出**：同步輸出為 JSON 格式，利於後續資料分析與整合應用


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
  - 可以透過 [**visualiz_sqlite**](visualiz_sqlite.ipynb) 視覺化

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
  (記得根據 [setting 檔案](config/setting.py) 更改你的資料夾名稱)

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
