# Excel Report Tool v2.1 Release Notes

## Release Summary

Excel Report Tool v2.1 是一個通用 Excel / CSV 報表工具，目標是讓使用者不需要固定欄位名稱，也能透過 GUI 選擇資料欄位並產生正式 Excel 報表。

相較於 v1.0 固定使用 `客戶` 與 `金額` 欄位，v2.1 已升級為可分析不同格式表格的工具。使用者可以自行選擇分組欄位、統計欄位與日期欄位，工具會輸出原始資料、清理後資料與統計報表。

v2.1 的重點是讓輸出的 Excel 報表更適合展示與交付客戶，因此加入了自動美化、表格線、欄寬調整、金額格式、日期格式、Top10 排名與摘要區塊。

## Target Users

- 中小企業老闆
- 個人工作室
- 業務團隊
- 行政與財務人員
- 電商賣家
- 需要定期整理 Excel / CSV 的使用者

## Business Value

- 將重複 Excel 整理流程改成按鈕式工具
- 減少資料清理與報表製作時間
- 降低手動複製貼上與公式錯誤
- 讓非技術人員也能自行產生乾淨報表
- 輸出可直接查看、篩選、展示與交付的正式 Excel 報表

## Completed Features

### 通用資料讀取

- 支援 Excel / CSV
- Excel 固定讀取第一個工作表
- 支援 `.xlsx`、`.xlsm`、`.csv`
- 讀取後顯示檔名、列數與欄位數

### 資料清理

- 清除全空白列
- 刪除完全重複資料
- 保留原始資料與清理後資料

### 欄位分析

- 自動分析欄位類型
- 判斷文字欄位
- 判斷數字欄位
- 判斷日期欄位
- GUI 顯示欄位名稱、推測類型、非空筆數與範例值

### 動態報表引擎

- 使用者可自行選擇分組欄位
- 使用者可自行選擇統計欄位
- 日期欄位可選擇「不使用」
- 產生總覽
- 產生分組統計
- 產生月份統計，當使用日期欄位時
- 產生 Top10 排行
- 支援常見金額格式，例如 `元`、`￥`、`NT$`、逗號與空白值

### v2.1 報表美化

- 自動調整欄寬
- 標題列加粗
- 標題列背景色
- 明顯表格線
- 凍結首列
- 加入篩選器
- 金額欄位使用千分位格式
- 日期欄位格式統一為 `yyyy-mm-dd`
- Top10 報表加入排名欄
- 統計報表加入摘要區塊
- 所有工作表使用一致樣式

### GUI

- 使用者可透過 tkinter GUI 選擇 Excel / CSV
- GUI 會顯示欄位分析結果
- GUI 提供分組欄位、統計欄位、日期欄位下拉選單
- 產生完成後顯示輸出路徑

### Windows EXE

- 已可使用 PyInstaller 產生 Windows EXE
- EXE 路徑：

```text
dist/ExcelReportTool.exe
```

- EXE 使用 `--windowed`，開啟時不顯示黑色命令視窗
- 打包時不包含客戶資料、`output/`、`tests/`、`build/`、`dist/` 或原始測試輸出

## Output

工具會輸出：

```text
output/result_v2_YYYYMMDD_HHMMSS.xlsx
```

輸出 Excel 包含三個主要工作表：

- `原始資料`
- `清理後資料`
- `統計報表`

`統計報表` 會依使用者選擇的欄位產生：

- 摘要區塊
- 總覽
- 分組統計
- 月份統計，若有選擇日期欄位
- Top10 排行

## Example Use Cases

### 每月銷售報表整理

使用者匯入銷售 Excel 或 CSV，選擇商品分類、客戶或業務作為分組欄位，再選擇金額欄位進行統計。工具會自動產生清理後資料、分組統計與 Top10 排行。

### 支出與台賬整理

使用者匯入支出或台賬資料，選擇用途、付款人或部門作為分組欄位，再選擇金額欄位進行統計。工具可處理常見金額格式，並輸出可篩選的正式 Excel 報表。

### 業務或代理人統計

使用者匯入代理人、醫院、項目金額或日期資料，選擇代理人作為分組欄位，金額作為統計欄位，日期作為月份統計欄位。工具會產生分組統計、月份統計與 Top10 排行。

## Verification

v2.1 目前已完成以下驗證：

```text
35 passed
```

已確認：

- v2.1 GUI 可啟動
- EXE 可開啟 GUI
- GUI 標題顯示 `Excel Report Tool v2.1 通用表格分析工具`
- README 圖片路徑已檢查
- `dist/ExcelReportTool.exe` 已產生
- v2.1 主畫面截圖已建立
- 測試涵蓋 reader、column analyzer、report builder、excel formatter 與既有 v1.0 功能

## Screenshots

目前已建立：

- `screenshots/excel-report-v21-main-screen.png`

正式發布前建議補齊：

- `excel-report-v21-select-file.png`
- `excel-report-v21-column-analysis.png`
- `excel-report-v21-field-selection.png`
- `excel-report-v21-completed.png`
- `excel-report-v21-cleaned-data.png`
- `excel-report-v21-summary-report.png`
- `excel-report-v21-top10-ranking.png`
- `excel-report-v21-summary-block.png`

## Known Limitations

v2.1 仍有以下限制：

- 尚未支援多工作表合併
- 尚未支援多檔案批次處理
- 尚未支援圖表
- 尚未支援 PDF 匯出
- 尚未支援 AI 摘要
- 尚未支援自動排程
- 原始 Excel 若標題列非常混亂，仍可能需要人工確認欄位選擇
- 日期格式過度混亂時，月份統計結果需要人工檢查
- 客戶正式交付前仍建議使用實際資料再做一次驗收

## Not Included in v2.1

v2.1 不包含以下功能：

- AI 摘要
- PDF 匯出
- 圖表
- 自動排程
- Google Sheets 串接
- 多帳號管理
- CRM 串接
- EXE 安裝器

這些功能可規劃到 v3.0 或後續獨立作品集專案。

## Release Status

目前狀態：**v2.1 Release Candidate**

建議正式 Release 前完成：

- 補齊 v2.1 流程截圖
- 使用 3 份以上真實或接近真實資料驗收
- 建立 GitHub 發佈清單
- 建立客戶交付資料夾
- 最後一次執行 pytest
- 確認 `build/`、`dist/`、`*.spec`、`output/` 沒有被 Git 追蹤
