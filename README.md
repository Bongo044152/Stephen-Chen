# **期中報告**

本項目為期中作業，利用 **爬蟲技術** 從 [亞洲大學資工系官網](https://csie.asia.edu.tw/zh_tw/associate_professors_2) 獲取每位教授的專長資訊，並將其存取下來。

## **功能特點**
- **自動化**：爬取 **亞洲大學資工系** 教授的專長資訊，無需手動操作
- **高效能**：使用 **異步處理** 提升爬取速度，減少等待時間
- **可追蹤**：內建 **爬蟲運行日誌**，方便除錯與監控
- **標準輸出**：數據以 **JSON 格式** 儲存，便於後續分析與應用
- **規範化日誌輸出**：使用 **Python 的 logging 模組**，以標準格式輸出日誌至終端機

## **環境設置**
> **請確保 Python 版本 ≥ 3.9** 

### **1. 克隆此專案**
```bash
git clone <倉庫網址>
cd <專案資料夾>
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

### **5. 執行爬蟲程式**
```bash
python main.py
```

# 爬蟲介紹