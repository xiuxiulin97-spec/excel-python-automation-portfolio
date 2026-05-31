# Google Sheets 自動同步報表 v1.0 發布說明

> 狀態：草稿。正式 Release 會在 Google Sheets OAuth 連線與同步流程完成後發布。

## 目標

建立一個 Python 桌面工具，讓使用者可以選擇 Excel / CSV，清理資料、產生統計報表，並同步到指定 Google Sheets。

## v1.0 預計完成

- Excel / CSV 讀取
- Excel 第一工作表讀取
- 空白列清理
- 完全重複資料清理
- `客戶`、`金額` 欄位檢查
- 依 `客戶` 統計 `金額` 總和
- Google Sheets OAuth 本機授權
- 寫入 `清理後資料` 與 `統計報表`
- tkinter GUI
- pytest 測試
- README 與截圖

## 第一階段已完成

- 本機資料清理
- 統計報表建立
- Google Sheets payload 格式建立
- 自動測試

## v1.0 不包含

- AI 摘要
- PDF
- 圖表
- 自動排程
- EXE 打包
- 多帳號管理
- CRM 串接
