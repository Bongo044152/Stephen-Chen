# 指令由 GPT 生成，之後由我手動改寫

$chromeZipUrl = "https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.84/win64/chrome-win64.zip"
$driverZipUrl = "https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.84/win64/chromedriver-win64.zip"
$chromeZipPath = "$PWD\chrome-win64.zip"
$driverZipPath = "$PWD\chromedriver-win64.zip"
$chromeFinalPath = "$PWD\chrome"
$driverFinalPath = "$PWD\chromedriver"

# 下載 Chrome ZIP（如果未安裝）
if (-not (Test-Path "$chromeFinalPath\chrome.exe")) {
    Write-Host "📥 下載 Chrome Test (ZIP) ..."
    Invoke-WebRequest -Uri $chromeZipUrl -OutFile $chromeZipPath
    Write-Host "✅ 下載完成！"

    Write-Host "📦 解壓縮 Chrome Test ..."
    Expand-Archive -Path $chromeZipPath -DestinationPath $PWD -Force
    Rename-Item -Path "$PWD\chrome-win64" -NewName "chrome" -Force
    Write-Host "✅ 解壓縮完成！"
} else {
    Write-Host "🔁 Chrome 已存在，略過下載與解壓縮"
}

# 下載 Chromedriver ZIP（如果未安裝）
if (-not (Test-Path "$driverFinalPath\chromedriver.exe")) {
    Write-Host "📥 下載 Chromedriver (ZIP) ..."
    Invoke-WebRequest -Uri $driverZipUrl -OutFile $driverZipPath
    Write-Host "✅ 下載完成！"

    Write-Host "📦 解壓縮 Chromedriver ..."
    Expand-Archive -Path $driverZipPath -DestinationPath $PWD -Force
    Rename-Item -Path "$PWD\chromedriver-win64" -NewName "chromedriver" -Force
    Write-Host "✅ 解壓縮完成！"
} else {
    Write-Host "🔁 Chromedriver 已存在，略過下載與解壓縮"
}

# 刪除所有 ZIP 檔案（如果存在）
if (Test-Path $chromeZipPath) { Remove-Item $chromeZipPath }
if (Test-Path $driverZipPath) { Remove-Item $driverZipPath }
Write-Host "🗑️ ZIP 檔案已清除"

# 最終提示
Write-Host "`n✅ Chrome 和 Chromedriver 已成功安裝並解壓縮到："
Write-Host "📂 Chrome 路徑： $chromeFinalPath"
Write-Host "📂 Driver 路徑： $driverFinalPath"
