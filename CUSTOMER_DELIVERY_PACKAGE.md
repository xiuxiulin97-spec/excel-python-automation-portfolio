# Excel Report Tool v2.1 客戶交付包

## 交付包位置

```text
ExcelReportTool_v2.1/
```

## 交付包內容

```text
ExcelReportTool_v2.1/
├── ExcelReportTool.exe
├── 使用說明.txt
├── sample.xlsx
└── screenshots/
```

## 內容說明

- `ExcelReportTool.exe`：給一般使用者直接開啟的 Windows 程式。
- `使用說明.txt`：非技術使用者可照著操作的使用說明。
- `sample.xlsx`：範例輸入檔，用於第一次測試工具。
- `screenshots/`：工具畫面與操作展示截圖。

## 不放入交付包的內容

交付包不包含以下內容：

- 原始碼
- tests/
- build/
- dist/
- __pycache__/
- .spec
- output/
- 客戶真實資料
- Git / GitHub 相關設定

## 使用對象

此交付包適合完全不懂 Python 的一般使用者。使用者只需要雙擊 `ExcelReportTool.exe`，選擇 Excel / CSV，並依照畫面選擇分組欄位與統計欄位即可產生報表。

## 交付前檢查

- [ ] `ExcelReportTool.exe` 可正常開啟
- [ ] `sample.xlsx` 可用來產生報表
- [ ] 使用說明清楚
- [ ] screenshots 內有展示截圖
- [ ] 不包含客戶真實資料
- [ ] 不包含原始碼或測試檔案
