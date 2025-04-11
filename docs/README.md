# 此文件用於 python 的 sphinx 模組自動生成 html 等文件

參考影片: https://www.youtube.com/watch?v=KKfQnxQBoWE ( 感謝他的無私貢獻! )

## 備忘錄
### **1. 安裝 sphinx**
> **別忘了進入 python 的虛擬環境!**
```shell
pip install sphinx sphinx_rtd_theme
```
> **這裡我選擇 "sphinx_rtd_theme" 這個樣式，詳細可以參考: https://sphinx-themes.org/#themes**

### **2. 掃描專案**
```shell
sphinx-apidoc -o docs/ .
```
- `-o docs/`: 輸出到這!
- `.`: 要搜尋的路徑
> **記得編輯一下: *.ret 檔案**
### **2. 建構**
```shell
cd docs
sphinx-build -b html . _build/html
```
### **3. 開啟 html**
位於 **./docs/_build/html/index.html**


## 注意!
別忘了使用 google 的 python 風格撰寫，參考:
- https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html
- https://medium.com/han-shih/google-python-%E9%A2%A8%E6%A0%BC%E6%8C%87%E5%8D%97-%E4%BA%8C-a7ee27d85cf9 ( 可略 )
