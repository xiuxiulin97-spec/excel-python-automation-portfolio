# GitHub Release 準備文件

## Release

版本：v1.0

標題建議：

```text
Excel AI 自動報表工具 v1.0
```

## 1. 專案介紹

Excel AI 自動報表工具是一個使用 Python 製作的桌面小工具，目標是協助中小企業、個人工作室或行政人員快速整理 Excel 資料並產生統計報表。

第一版聚焦最常見的 Excel 重複工作：

- 讀取 Excel 檔案
- 清除空白列
- 刪除重複資料
- 依照客戶統計金額
- 產生新的 Excel 報表

這個專案使用：

- pandas：處理資料清理與統計
- openpyxl：讀寫 Excel 檔案
- tkinter：提供簡單 GUI 操作介面

## 2. 功能展示

使用者開啟程式後，可以透過簡單視窗完成報表產生流程：

```text
Excel AI 自動報表工具

檔案：
sales.xlsx

[選擇 Excel]

[開始分析]

狀態：
完成

輸出：
output/result_YYYYMMDD_HHMMSS.xlsx
```

範例輸入資料：

| 客戶 | 金額 |
| --- | ---: |
| A公司 | 1000 |
| A公司 | 3000 |
| B公司 | 2000 |

範例統計結果：

| 客戶 | 金額總和 |
| --- | ---: |
| A公司 | 4000 |
| B公司 | 2000 |

輸出的 Excel 報表包含三個工作表：

- 原始資料
- 清理後資料
- 統計報表

v1.0 已完成：

- Excel讀取
- 第一工作表讀取
- 空白列清理
- 重複資料清理
- 客戶金額統計
- Excel報表輸出
- GUI
- 自動時間戳
- 測試

## 3. 使用方式

安裝套件：

```powershell
python -m pip install -r requirements.txt
```

如果電腦使用 `py` 啟動 Python：

```powershell
py -m pip install -r requirements.txt
```

啟動工具：

```powershell
python main.py
```

或：

```powershell
py main.py
```

操作流程：

1. 按「選擇 Excel」
2. 選擇 `.xlsx` 或 `.xlsm` 檔案
3. 按「開始分析」
4. 等待狀態顯示完成
5. 到 `output/` 資料夾查看報表

輸入 Excel 的第一個工作表必須包含：

- `客戶`
- `金額`

輸出檔案格式：

```text
output/result_YYYYMMDD_HHMMSS.xlsx
```

執行測試：

```powershell
python -m pytest -q
```

目前測試狀態：

```text
8 passed
```

## 4. 商業應用場景

這個工具適合展示給需要經常整理 Excel 的中小企業或個人工作室。

可應用情境：

- 銷售資料整理：將每日或每月銷售明細依客戶統計總金額。
- 訂單報表生成：清理訂單資料中的空白列與重複列，產生乾淨報表。
- 客戶交易分析：快速查看每位客戶的累積消費金額。
- 行政資料整理：把人工整理 Excel 的流程改成按鈕式自動化。
- 接案展示作品：展示 Python + Excel + GUI 的自動化能力。

對客戶的價值：

- 減少手動複製貼上
- 降低人工計算錯誤
- 節省每週重複整理報表的時間
- 讓非技術使用者也能用簡單視窗完成資料處理

## 後續版本方向

v1.0 先完成穩定可執行版本。後續可擴充：

- 選擇工作表
- 多工作表合併
- 圖表
- PDF 匯出
- EXE 打包
- AI 摘要
