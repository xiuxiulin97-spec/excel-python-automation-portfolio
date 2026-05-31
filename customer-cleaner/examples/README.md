# Examples

這個資料夾放 Customer Cleaner 的範例輸入與輸出說明。

## 範例輸入

範例檔案：

```text
sample.xlsx
```

內容：

| 客戶姓名 | 手機 | 電子郵件 | 公司名稱 |
| --- | --- | --- | --- |
| 王小明 | 0912-345-678 | WANG@EXAMPLE.COM | A公司 |
| 王小明 | (0912) 345 678 | wang@example.com | A公司 |
| 陳美華 | 02-2345-6789 | chen@example.com | B公司 |
| 林志強 | 0911-111-111 | bad-email | C公司 |
| 空白 | 0933-333-333 | missing-name@example.com | D公司 |
| 周子安 | 空白 | 空白 | E公司 |

## 範例輸出

執行後會在專案的 `output/` 資料夾產生：

```text
cleaned_customers_YYYYMMDD_HHMMSS.xlsx
```

輸出 Excel 包含三個工作表：

- `原始資料`
- `清理後資料`
- `問題資料`

清理後資料範例：

| 姓名 | 電話 | Email | 公司 |
| --- | --- | --- | --- |
| 王小明 | 0912345678 | wang@example.com | A公司 |
| 陳美華 | 0223456789 | chen@example.com | B公司 |

問題資料範例：

| 姓名 | 電話 | Email | 公司 | 問題 |
| --- | --- | --- | --- | --- |
| 林志強 | 0911111111 | bad-email | C公司 | Email格式錯誤 |
| 空白 | 0933333333 | missing-name@example.com | D公司 | 缺少姓名 |
| 周子安 | 空白 | 空白 | E公司 | 缺少電話或Email |
