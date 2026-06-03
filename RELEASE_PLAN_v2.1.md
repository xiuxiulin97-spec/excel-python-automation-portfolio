# Excel Report Tool v2.1 Release Plan

目標：正式發布 Excel Report Tool v2.1，讓作品可展示、可測試、可打包、可交付客戶。

## 目前狀態

- README 已更新 v2.1 功能與 EXE 狀態。
- `screenshots/excel-report-v21-main-screen.png` 已建立。
- `screenshots/V2.1_SCREENSHOT_CHECKLIST.md` 已建立，列出正式發布前需要補齊的截圖。
- `dist/ExcelReportTool.exe` 已可由 PyInstaller 產生。
- EXE 打包時需要手動包含 tkinter / Tcl / Tk 檔案，詳細指令記錄在 `BUILD_EXE.md`。
- 正式 Release 前仍需補齊流程截圖、真實資料驗收與 GitHub Release Notes。

## 1. Release Candidate 驗收清單

Release Candidate 目標是確認 v2.1 已經具備正式發布條件。

- [ ] GUI 可正常啟動
- [ ] 可選擇 Excel 檔案
- [ ] 可選擇 CSV 檔案
- [ ] Excel 固定讀取第一個工作表
- [ ] 可顯示檔名
- [ ] 可顯示列數與欄位數
- [ ] 可顯示欄位分析結果
- [ ] 可選擇分組欄位
- [ ] 可選擇統計欄位
- [ ] 日期欄位可選擇「不使用」
- [ ] 可正常產生報表
- [ ] 輸出 Excel 包含：
  - [ ] 原始資料
  - [ ] 清理後資料
  - [ ] 統計報表
- [ ] v2.1 美化功能正常：
  - [ ] 表格線
  - [ ] 標題列背景色
  - [ ] 標題列加粗
  - [ ] 自動欄寬
  - [ ] 凍結首列
  - [ ] 篩選器
  - [ ] 金額千分位格式
  - [ ] 日期格式 yyyy-mm-dd
  - [ ] Top10 排名
  - [ ] 統計報表摘要區塊
- [ ] pytest 全部通過

建議測試指令：

```powershell
python -m pytest -q
```

如果本機 Python 沒有 pytest，需先安裝測試依賴。

## 2. 真實資料驗收清單

至少使用 3 份不同格式的真實或接近真實資料測試。

### 測試資料 1：銷售 / 菜單 / 商品資料

- [ ] 可讀取資料
- [ ] 分組欄位可選分類欄位
- [ ] 統計欄位可選價格 / 金額欄位
- [ ] 可產生分類統計
- [ ] 可產生 Top10 排行
- [ ] 輸出表格樣式正常

### 測試資料 2：支出 / 台賬 / 費用資料

- [ ] 可讀取資料
- [ ] 可識別用途 / 付款人等文字欄位
- [ ] 可識別金額欄位
- [ ] 金額欄含 `元`、`￥`、逗號時仍可統計
- [ ] 空白金額不造成整份報表失敗
- [ ] 輸出報表可查看

### 測試資料 3：醫美 / 代理人 / 業務資料

- [ ] 可讀取資料
- [ ] 可選代理人 / 醫院名稱作為分組欄位
- [ ] 可選項目金額作為統計欄位
- [ ] 可選日期欄位產生月份統計
- [ ] 日期格式輸出為 yyyy-mm-dd
- [ ] 報表結果合理

### 真實資料驗收結果

- [ ] 至少 3 份資料成功產生報表
- [ ] 無重大錯誤
- [ ] 錯誤提示可理解
- [ ] 輸出 Excel 可直接交付或展示

## 3. EXE 打包驗收清單

打包工具：PyInstaller。

打包前確認：

- [ ] 測試全部通過
- [ ] README 已更新
- [ ] requirements.txt 完整
- [ ] 不打包 tests/
- [ ] 不打包 output/
- [ ] 不打包 build/
- [ ] 不打包 dist/
- [ ] 不打包 __pycache__/
- [ ] 不打包 .spec
- [ ] 不打包客戶資料

打包指令建議：

```powershell
pyinstaller --onefile --windowed --name ExcelReportTool main.py
```

打包後驗收：

- [ ] `dist/ExcelReportTool.exe` 存在
- [ ] 雙擊 EXE 可開啟 GUI
- [ ] 可選擇 Excel / CSV
- [ ] 可產生報表
- [ ] output/ 可正常建立
- [ ] 報表樣式正常
- [ ] 關閉程式不報錯

## 4. README 更新清單

README 應更新為 v2.1 版本說明。

- [ ] 專案介紹
- [ ] 商業價值
- [ ] v2.1 新增美化功能
- [ ] 安裝方式
- [ ] 執行方式
- [ ] 使用方式
- [ ] 輸入資料格式
- [ ] 輸出結果說明
- [ ] 截圖展示
- [ ] 專案結構
- [ ] 測試方式
- [ ] EXE 使用說明
- [ ] 未來規劃

README 應避免寫得像學習筆記，要像可以展示給客戶或面試主管的作品頁。

## 5. 截圖清單

建議放在 `screenshots/`。

必備截圖：

- [ ] v2.1 主畫面
- [ ] 選擇 Excel / CSV 檔案
- [ ] 欄位分析結果
- [ ] 選擇分組欄位與統計欄位
- [ ] 執行完成訊息
- [ ] 原始資料工作表
- [ ] 清理後資料工作表
- [ ] 統計報表工作表
- [ ] Top10 排名區塊
- [ ] 統計報表摘要區塊

建議命名：

- `excel-report-v21-main-screen.png`
- `excel-report-v21-select-file.png`
- `excel-report-v21-column-analysis.png`
- `excel-report-v21-field-selection.png`
- `excel-report-v21-completed.png`
- `excel-report-v21-original-data.png`
- `excel-report-v21-cleaned-data.png`
- `excel-report-v21-summary-report.png`
- `excel-report-v21-top10-ranking.png`
- `excel-report-v21-summary-block.png`

## 6. GitHub Release 流程

正式發布前：

- [ ] 確認 git status
- [ ] 確認沒有 credentials、token、客戶資料、output 被追蹤
- [ ] 確認 README 已更新
- [ ] 確認 Release Notes 已建立
- [ ] 確認截圖路徑正確
- [ ] 執行 pytest

建議指令：

```powershell
git status
git add .
git commit -m "release: publish Excel Report Tool v2.1"
git push origin main
```

GitHub Release 建議：

- Tag：`excel-report-tool-v2.1`
- Release title：`Excel Report Tool v2.1`
- Release description：使用 `RELEASE_NOTES_v2.1.md`

Release 內容應包含：

- v2.1 新增功能
- 使用方式
- 測試結果
- 截圖
- EXE 下載說明
- 已知限制

## 7. 客戶交付版本流程

建立交付資料夾：

```text
ExcelReportTool_v2.1/
├── ExcelReportTool.exe
├── 使用說明.txt
├── sample.xlsx
├── 範例輸出.xlsx
└── README_客戶版.txt
```

交付版本不要放：

- tests/
- build/
- dist/
- __pycache__/
- .spec
- 原始碼
- credentials.json
- token.json
- 客戶資料
- 開發用 output/

客戶版使用說明需包含：

- 如何開啟程式
- 如何選擇 Excel / CSV
- 如何選擇分組欄位
- 如何選擇統計欄位
- 如何產生報表
- 結果檔在哪裡
- 常見錯誤
- 如何回報問題

交付前最後確認：

- [ ] EXE 可正常開啟
- [ ] sample.xlsx 可正常產生報表
- [ ] 範例輸出.xlsx 已更新為 v2.1 樣式
- [ ] 使用說明清楚
- [ ] 不含敏感資料
- [ ] 資料夾可直接壓縮交付

## 發布建議

建議發布順序：

1. 完成真實資料驗收
2. 更新 README
3. 補齊截圖
4. 建立 Release Notes
5. 打包 EXE
6. 建立客戶交付版本
7. 推送 GitHub
8. 建立 GitHub Release

v2.1 的定位：

Excel Report Tool v2.1 是一個可展示、可測試、可初步交付客戶的通用 Excel 報表工具。
