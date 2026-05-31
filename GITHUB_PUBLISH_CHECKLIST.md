# GitHub Publish Checklist

這份清單用於將 Excel Report Tool v1.0 發佈到 GitHub。

## Repository 建議資訊

Repository 名稱建議：

```text
excel-python-automation-portfolio
```

或：

```text
excel-report-tool
```

Repository 簡短描述：

```text
Excel + Python 自動化工具作品集：自動整理 Excel、產生報表，並展示可接案的資料處理工具。
```

Topics 建議：

- `python`
- `excel`
- `pandas`
- `openpyxl`
- `tkinter`
- `automation`
- `data-cleaning`
- `reporting`

## 上傳前檢查清單

- [x] `README.md` 已整理成作品集首頁
- [x] `CHANGELOG.md` 已標記 v1.0
- [x] `RELEASE_NOTES_v1.0.md` 已建立
- [x] `GITHUB_RELEASE.md` 已建立
- [x] `requirements.txt` 已包含必要套件
- [x] `pytest.ini` 已限制測試範圍
- [x] `sample.xlsx` 已建立
- [x] `examples/sample.xlsx` 已建立
- [x] `screenshots/` 已放入 Excel Report Tool 截圖
- [x] `tests/` 已建立
- [x] 自動測試已通過
- [x] 語法檢查已通過
- [ ] GitHub repository 已建立
- [ ] 檔案已上傳 GitHub
- [ ] README 圖片在 GitHub 頁面正常顯示
- [ ] GitHub Release v1.0 已建立

## 建議上傳內容

上傳到 GitHub 時，建議包含：

```text
README.md
CHANGELOG.md
RELEASE_NOTES_v1.0.md
GITHUB_RELEASE.md
GITHUB_PUBLISH_CHECKLIST.md
PORTFOLIO_ROADMAP.md
portfolio_summary.md
main.py
ui.py
cleaner.py
report.py
requirements.txt
pytest.ini
sample.xlsx
examples/
screenshots/
tests/
customer-cleaner/
```

不要上傳：

```text
__pycache__/
.pytest_cache/
.codex_test_deps/
output/
*.pyc
```

這些已由 `.gitignore` 排除。

## GitHub 上傳步驟

### 方式一：使用 GitHub 網頁上傳

1. 登入 GitHub。
2. 建立新的 repository。
3. Repository 名稱可使用 `excel-python-automation-portfolio`。
4. Description 填入：

   ```text
   Excel + Python 自動化工具作品集：自動整理 Excel、產生報表，並展示可接案的資料處理工具。
   ```

5. 選擇 Public，方便作品集展示。
6. 不要勾選自動建立 README，因為本專案已經有 README。
7. 建立 repository。
8. 使用 GitHub 網頁的 Upload files，上傳本資料夾內容。
9. Commit message 建議：

   ```text
   release: publish Excel Report Tool v1.0 portfolio
   ```

10. 打開 GitHub 首頁，確認 README 圖片與文字正常顯示。

### 方式二：使用 Git 指令上傳

如果本機已安裝 Git，可在專案根目錄執行：

```powershell
git init
git add .
git commit -m "release: publish Excel Report Tool v1.0 portfolio"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

請將：

```text
<your-username>
<your-repo-name>
```

換成你的 GitHub 帳號與 repository 名稱。

## 建立 GitHub Release v1.0

1. 進入 GitHub repository。
2. 點選右側或上方的 `Releases`。
3. 點選 `Draft a new release`。
4. Tag version 輸入：

   ```text
   v1.0
   ```

5. Release title 輸入：

   ```text
   Excel Report Tool v1.0
   ```

6. Release description 可貼上 `RELEASE_NOTES_v1.0.md` 的內容。
7. 確認內容後點選 `Publish release`。

## 發佈後檢查

- [ ] GitHub 首頁 README 可正常閱讀
- [ ] 截圖可正常顯示
- [ ] `sample.xlsx` 可下載
- [ ] `requirements.txt` 可看到依賴
- [ ] `tests/` 可看到測試檔
- [ ] Release v1.0 可正常開啟
- [ ] Release Notes 內容完整
