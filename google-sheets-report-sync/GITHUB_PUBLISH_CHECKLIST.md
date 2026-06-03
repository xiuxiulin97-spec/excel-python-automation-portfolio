# Google Sheets Report Sync GitHub 發佈檢查清單

## 1. 發佈前檢查

- [ ] README 已包含專案介紹
- [ ] README 已包含商業價值
- [ ] README 已包含使用案例
- [ ] README 已包含成果展示截圖
- [ ] README 已包含安裝方式
- [ ] README 已包含執行方式
- [ ] README 已包含 Google Sheets API 設定方式
- [ ] README 已包含測試方式
- [ ] README 已包含專案結構
- [ ] README 圖片路徑可正常顯示
- [ ] `RELEASE_NOTES_v1.0.md` 已建立
- [ ] `.gitignore` 已排除敏感檔案

## 2. 安全檢查

確認以下檔案沒有被 Git 追蹤：

- [ ] `google-sheets-report-sync/credentials.json`
- [ ] `google-sheets-report-sync/token.json`
- [ ] `google-sheets-report-sync/output/`
- [ ] `__pycache__/`
- [ ] `.pytest_cache/`

建議檢查指令：

```powershell
git ls-files | Select-String -Pattern "google-sheets-report-sync/(credentials|token)\.json"
```

如果沒有輸出，代表沒有被 Git 追蹤。

## 3. 測試檢查

在專案資料夾執行：

```powershell
python -m pytest -q
```

確認測試全部通過後再發佈。

## 4. Git Commit

```powershell
git status
git add google-sheets-report-sync
git commit -m "release: prepare Google Sheets Report Sync v1.0"
```

## 5. Push 到 GitHub

```powershell
git push origin main
```

如果目前 branch 不是 `main`，請先用以下指令確認：

```powershell
git branch --show-current
```

## 6. 建立 GitHub Release

建議 Release tag：

```text
google-sheets-report-sync-v1.0
```

Release title：

```text
Google Sheets Report Sync v1.0
```

Release description：

請使用 `google-sheets-report-sync/RELEASE_NOTES_v1.0.md` 的內容。

## 7. GitHub 頁面人工驗收

- [ ] GitHub 上可以看到 `google-sheets-report-sync/README.md`
- [ ] README 圖片正常顯示
- [ ] `main.py`、`ui.py`、`cleaner.py`、`report.py`、`sheets_client.py` 存在
- [ ] `requirements.txt` 存在
- [ ] `tests/` 存在
- [ ] `credentials.json` 沒有出現在 GitHub
- [ ] `token.json` 沒有出現在 GitHub
- [ ] Release Notes 內容正確
- [ ] GitHub Release 建立成功
