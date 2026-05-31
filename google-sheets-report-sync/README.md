# Google Sheets 自動同步報表

目前版本：v1.0 開發中

這是作品集第三個專案，目標是建立一個 Python 桌面工具，讓使用者選擇 Excel / CSV，清理資料、產生統計報表，並同步到指定 Google Sheets。

## 第一階段狀態

目前已先完成本機資料處理基礎：

- 建立專案結構
- 支援 Excel / CSV 讀取
- Excel 固定讀取第一個工作表
- 清除全空白列
- 刪除完全重複資料
- 檢查必要欄位：`客戶`、`金額`
- 依 `客戶` 統計 `金額` 總和
- 建立 Google Sheets batch update payload
- 建立 pytest 測試

Google Sheets OAuth 連線與真正寫入雲端表格會在下一階段加入。

## 商業價值

許多中小企業會先在本機 Excel / CSV 整理資料，再手動複製到 Google Sheets 與團隊共享。這個工具的目標是把清理、統計、同步流程串起來，減少人工貼上、版本混亂與欄位錯誤。

適合場景：

- 每週業務報表同步
- 客戶名單整理後同步到雲端
- 遠端團隊共用營運報表
- 行政或營運人員定期更新 Google Sheets

## v1.0 功能範圍

1. 支援選擇 Excel / CSV
2. Excel 固定讀取第一個工作表
3. 清除全空白列
4. 刪除完全重複資料
5. 檢查必要欄位：`客戶`、`金額`
6. 依 `客戶` 統計 `金額` 總和
7. 使用者輸入 Google Sheet ID
8. 寫入 Google Sheets 兩個工作表：
   - `清理後資料`
   - `統計報表`
9. 建立簡單 tkinter GUI
10. 顯示同步成功或失敗訊息
11. 建立 README、測試、Release Notes

## 專案結構

```text
google-sheets-report-sync/
├── main.py
├── ui.py
├── cleaner.py
├── report.py
├── sheets_client.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
├── examples/
│   └── sample_sales.xlsx
├── screenshots/
│   └── README.md
└── tests/
    ├── test_cleaner.py
    ├── test_report.py
    └── test_sheets_payload.py
```

## 安裝方式

```powershell
python -m pip install -r requirements.txt
```

## 執行方式

第一階段 GUI 只顯示專案狀態，完整同步流程會在下一階段加入。

```powershell
python main.py
```

## 測試

```powershell
python -m pytest -q
```

## Google Sheets 憑證規則

第一版會使用本機 OAuth：

- `credentials.json`
- `token.json`

這兩個檔案包含授權資訊，不能上傳到 GitHub，已在 `.gitignore` 排除。

## v1.0 不包含

- AI 摘要
- PDF
- 圖表
- 自動排程
- EXE 打包
- 多帳號管理
- CRM 串接
