# Google Sheets Report Sync v1.0

## 專案介紹

Google Sheets Report Sync 是一個 Python 桌面工具，讓使用者可以選擇 Excel / CSV，清理資料、產生客戶金額統計，並同步到指定 Google Sheets。

v1.0 目標是完成可展示、可驗收的第一版流程，適合作為中小企業報表自動化作品集案例。

## 已完成

- 支援 Excel / CSV
- Excel 固定讀取第一個工作表
- 清除全空白列
- 刪除完全重複資料
- 檢查必要欄位：`客戶`、`金額`
- 依照 `客戶` 統計 `金額` 總和
- 使用者輸入 Google Sheet ID
- Google OAuth 本機授權流程
- 寫入 Google Sheets：`清理後資料`
- 寫入 Google Sheets：`統計報表`
- tkinter GUI
- 同步成功與失敗訊息
- README 文件
- 成果截圖
- pytest 測試
- `.gitignore` 排除 `credentials.json` 與 `token.json`

## 成果展示

已補上以下截圖：

- 工具主畫面
- 已選擇檔案畫面
- 同步完成畫面
- Google Sheets 清理後資料
- Google Sheets 統計報表

## 測試

發佈前測試指令：

```powershell
python -m pytest -q
```

驗收重點：

- 資料清理功能正確
- 統計報表正確
- Google Sheets payload 正確
- Google Sheets API 寫入流程可測試
- `credentials.json` 與 `token.json` 不被 Git 追蹤

## 商業應用場景

- 每週銷售資料同步
- 業務報表整理
- Excel / CSV 資料清理後同步雲端
- 小型團隊共享營運報表
- 行政人員定期更新 Google Sheets

## v1.0 不包含

- AI 摘要
- PDF
- 圖表
- 自動排程
- EXE 打包
- 多帳號管理
- CRM 串接

## Release 狀態

Google Sheets Report Sync v1.0 已達發佈前驗收標準，可建立 GitHub Release。
