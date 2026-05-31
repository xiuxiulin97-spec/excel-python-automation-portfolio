# Customer Cleaner v1.0 發布說明

## 發行摘要

Customer Cleaner v1.0 是一個可執行的客戶資料清洗工具，適合中小企業、個人工作室、活動主辦方與電商賣家整理 Excel / CSV 客戶名單。

使用者可以透過簡單 GUI 選擇客戶資料檔，工具會自動統一欄位名稱、清理電話格式、檢查 Email、刪除重複客戶，並輸出新的 Excel 報表。

## 商業價值

- 減少人工整理客戶名單的時間
- 降低電話與 Email 格式錯誤造成的後續問題
- 協助活動報名、電商名單、業務名單轉成可用資料
- 讓非技術人員也能用按鈕式工具完成資料清洗

## 已完成的功能

- 支援 Excel / CSV 讀取
- 讀取 Excel 第一個工作表
- 清除全空白列
- 統一欄位名稱：`姓名`、`電話`、`Email`、`公司`
- 清理電話格式
- 檢查 Email 格式
- 刪除重複客戶
- 輸出 `output/cleaned_customers_YYYYMMDD_HHMMSS.xlsx`
- 輸出三個工作表：`原始資料`、`清理後資料`、`問題資料`
- tkinter GUI
- 自動時間戳檔名
- pytest 自動測試
- GitHub README 成果展示截圖

## 成果展示

- 主畫面：使用者選擇 Excel / CSV 並開始清洗
- 選擇檔案：支援本機客戶資料檔
- 執行完成：顯示完成狀態與輸出檔案位置
- 輸出結果：產生乾淨名單與問題資料

## 使用方式

```powershell
python -m pip install -r requirements.txt
python main.py
```

如果使用 Windows Python Launcher：

```powershell
py -m pip install -r requirements.txt
py main.py
```

## 測試

```powershell
python -m pytest -q
```

測試涵蓋：

- CSV 讀取
- Excel 讀取
- 欄位名稱統一
- 空白列清理
- 電話格式清理
- 重複客戶刪除
- Email 格式檢查
- 三工作表 Excel 輸出

## 未包含在 v1.0 中

- AI 摘要
- PDF 匯出
- 圖表
- EXE 打包
- Google Sheets 串接
- CRM API 串接
- 批次處理多個檔案

這些功能可作為後續版本或作品集下一階段規劃。
