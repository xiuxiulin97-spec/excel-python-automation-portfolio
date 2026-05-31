# Customer Cleaner v1.0 GitHub 發佈清單

## 發佈前檢查

- [ ] 確認目前位於專案資料夾：`customer-cleaner/`
- [ ] 確認 `README.md` 已包含專案介紹、商業價值、功能特色、安裝方式、執行方式、範例輸入、範例輸出、專案結構、未來規劃
- [ ] 確認 `README.md` 已加入成果展示截圖
- [ ] 確認 `screenshots/` 圖片路徑可正常顯示
- [ ] 確認 `requirements.txt` 包含 `pandas`、`openpyxl`、`pytest`
- [ ] 確認測試可執行：`python -m pytest -q`
- [ ] 確認 `.gitignore` 不會上傳 `output/`、`__pycache__/`、`.pytest_cache/`、`~$*.xlsx`
- [ ] 確認沒有 WPS / Excel 暫存檔被加入 Git

## 應上傳的主要檔案

- [ ] `main.py`
- [ ] `ui.py`
- [ ] `cleaner.py`
- [ ] `validator.py`
- [ ] `exporter.py`
- [ ] `requirements.txt`
- [ ] `pytest.ini`
- [ ] `README.md`
- [ ] `CHANGELOG.md`
- [ ] `RELEASE_NOTES_v1.0.md`
- [ ] `GITHUB_PUBLISH_CHECKLIST.md`
- [ ] `screenshots/main-screen.png`
- [ ] `screenshots/select-file.png`
- [ ] `screenshots/completed.png`
- [ ] `screenshots/output-result.png`
- [ ] `screenshots/issue-data.png`
- [ ] `tests/`

## GitHub 上傳步驟

如果從作品集根目錄上傳：

```powershell
git status
git add .
git commit -m "release: publish Customer Cleaner v1.0"
git push origin main
```

如果只想檢查 Customer Cleaner 相關變更：

```powershell
git status --short customer-cleaner
```

## GitHub Release 發佈步驟

1. 打開 GitHub repository。
2. 進入右側或上方的 `Releases`。
3. 點選 `Draft a new release`。
4. Tag 建議填：`customer-cleaner-v1.0`
5. Release title 填：`Customer Cleaner v1.0`
6. Release description 貼上 `RELEASE_NOTES_v1.0.md` 的內容。
7. 確認不是 prerelease。
8. 點選 `Publish release`。

## 發佈後檢查

- [ ] GitHub 首頁可看到 Customer Cleaner 資料夾
- [ ] `customer-cleaner/README.md` 圖片正常顯示
- [ ] 根目錄作品集 README 的 Customer Cleaner 圖片正常顯示
- [ ] Release 頁面標題與內容正確
- [ ] 測試結果與 v1.0 功能範圍一致

## v1.0 標準

Customer Cleaner v1.0 的目標是成為一個可展示、可執行、可解釋的客戶資料清洗作品。第一版不追求大型系統，而是聚焦中小企業最常見的名單整理問題，展示可交付的自動化工具能力。
