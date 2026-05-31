# Screenshot Checklist

這份清單用來補拍 GitHub 作品集展示截圖。建議兩個專案都照同一套流程補拍，讓作品集看起來一致、專業。

## Excel 自動報表工具

| 項目 | 建議檔名 | 用途 |
| --- | --- | --- |
| 主畫面 | `excel-report-main-screen.png` | 展示工具有簡單 GUI，讓客戶知道不是只能用命令列操作。 |
| 選擇檔案 | `excel-report-select-file.png` | 展示使用者可以直接選 Excel 檔案，操作門檻低。 |
| 執行中 | `excel-report-running.png` | 展示工具有執行狀態，讓使用者知道目前正在處理資料。 |
| 執行完成 | `excel-report-completed.png` | 展示工具成功產生報表，並顯示輸出路徑。 |
| Excel輸出結果 | `excel-report-output-result.png` | 展示輸出檔包含原始資料、清理後資料、統計報表，證明工具真的有產出成果。 |

## Customer Cleaner

| 項目 | 建議檔名 | 用途 |
| --- | --- | --- |
| 主畫面 | `customer-cleaner-main-screen.png` | 展示 Customer Cleaner 的 GUI 主畫面，讓客戶理解這是可操作工具。 |
| 選擇檔案 | `customer-cleaner-select-file.png` | 展示工具支援選擇 Excel / CSV 客戶資料檔。 |
| 執行中 | `customer-cleaner-running.png` | 展示資料清洗過程有狀態提示。 |
| 執行完成 | `customer-cleaner-completed.png` | 展示工具完成清洗並產生輸出 Excel。 |
| Excel輸出結果 | `customer-cleaner-output-result.png` | 展示輸出 Excel 的三個工作表：原始資料、清理後資料、問題資料。 |

## 補拍建議

- 截圖時盡量使用同一個視窗大小。
- 檔名使用英文小寫與連字號，方便 GitHub 引用。
- 圖片放在本資料夾 `screenshots/`。
- README 中可用相對路徑引用，例如：

```markdown
![Excel 自動報表工具主畫面](screenshots/excel-report-main-screen.png)
```

Customer Cleaner 的截圖也可以統一放在根目錄 `screenshots/`，方便作品集首頁集中展示。
