# Excel Report Tool v1.0 Release Notes

## Release Summary

Excel Report Tool v1.0 是作品集第一個可展示、可執行的 Excel 自動化工具。使用者可以透過簡單 GUI 選擇 Excel 檔案，工具會自動讀取第一個工作表、清除空白列、刪除重複資料，並依照 `客戶` 欄位統計 `金額` 總和，最後輸出新的 Excel 報表。

## Target Users

- 中小企業老闆
- 個人工作室
- 業務團隊
- 行政與財務人員
- 需要定期整理 Excel 報表的使用者

## Business Value

- 將重複 Excel 整理流程改成按鈕式工具
- 減少資料清理與報表製作時間
- 降低手動複製貼上與公式錯誤
- 讓非技術人員也能自行產生乾淨報表

## Completed Features

- Excel 讀取
- 第一工作表讀取
- 空白列清理
- 重複資料清理
- 客戶金額統計
- Excel 報表輸出
- GUI
- 自動時間戳
- 自動測試
- 範例輸入檔
- GitHub 作品集截圖

## Output

工具會輸出：

```text
output/result_YYYYMMDD_HHMMSS.xlsx
```

輸出 Excel 包含三個工作表：

- `原始資料`
- `清理後資料`
- `統計報表`

## Example

範例輸入：

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

## Verification

Release v1.0 驗證結果：

```text
8 passed
py_compile passed
```

已確認：

- 必要專案檔案存在
- README 已整理成作品集首頁
- CHANGELOG 已標記 v1.0
- screenshots 已放入 Excel Report Tool 截圖
- examples 已放入 sample.xlsx
- 自動測試可執行

## Not Included in v1.0

v1.0 不包含以下功能：

- AI 摘要
- PDF 匯出
- 圖表
- EXE 打包
- Google Sheets 串接
- 多工作表合併

這些功能可作為後續版本或其他作品集專案規劃。
