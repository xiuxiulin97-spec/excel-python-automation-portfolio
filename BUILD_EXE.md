# Excel Report Tool Windows EXE 打包流程

本文件說明如何使用 PyInstaller 將 Excel Report Tool 打包成 Windows `.exe`。

## 目標

- 使用 PyInstaller 打包
- 產生 `dist/ExcelReportTool.exe`
- 使用 `--windowed`，開啟時不顯示黑色命令視窗
- 不把客戶資料、範例輸出或 `output/` 打包進 exe

## 安裝依賴

請先在專案根目錄安裝必要套件。建議使用本機安裝的 Python，不要使用臨時或內嵌 Python 環境，避免 tkinter 的 Tcl/Tk 檔案不完整。

```powershell
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

如果你的電腦使用 `py` 啟動 Python：

```powershell
py -m pip install -r requirements.txt
py -m pip install pyinstaller
```

## 打包指令

在專案根目錄執行：

```powershell
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ExcelReportTool main.py
```

如果使用 `py`：

```powershell
py -m PyInstaller --noconfirm --clean --onefile --windowed --name ExcelReportTool main.py
```

## tkinter 打包注意事項

如果打包時看到類似訊息：

```text
tkinter installation is broken. It will be excluded from the application
```

代表 PyInstaller 沒有自動把 tkinter / Tcl / Tk 相關檔案包進去。這時請改用完整打包指令。

請先把 `$py` 改成本機 Python 安裝路徑，例如：

```powershell
$py = "C:\Users\你的帳號\AppData\Local\Programs\Python\Python312"
```

本專案這次實測可用的完整打包方式如下：

```powershell
$py = "C:\Users\62516\.cache\codex-runtimes\codex-primary-runtime\dependencies\python"

python -m PyInstaller `
  --noconfirm `
  --clean `
  --onefile `
  --windowed `
  --name ExcelReportTool `
  --hidden-import tkinter `
  --hidden-import _tkinter `
  --runtime-hook ".codex_test_deps\pyi_tkinter_runtime_hook.py" `
  --add-data "$py\Lib\tkinter;tkinter" `
  --add-data "$py\tcl;tcl" `
  --add-data "$py\tcl\tcl8.6;_tcl_data" `
  --add-data "$py\tcl\tk8.6;_tk_data" `
  --add-binary "$py\DLLs\tcl86t.dll;." `
  --add-binary "$py\DLLs\tk86t.dll;." `
  --add-binary "$py\DLLs\_tkinter.pyd;." `
  main.py
```

這組指令的目的，是確保 EXE 可以正常開啟 tkinter GUI。

完成後 exe 會產生在：

```text
dist/ExcelReportTool.exe
```

## 測試 EXE

執行：

```powershell
.\dist\ExcelReportTool.exe
```

確認事項：

- GUI 可以正常開啟
- 不會出現黑色命令視窗
- 可以選擇 Excel 檔案
- 可以產生 `output/result_v2_YYYYMMDD_HHMMSS.xlsx`

## 不打包客戶資料

目前打包指令只加入 tkinter / Tcl / Tk 執行 GUI 所需的程式檔案，不會主動把 Excel 檔案、客戶資料或 `output/` 放進 exe。

請避免在打包時加入以下資料：

- 客戶提供的 Excel / CSV
- `output/`
- 測試產出的報表
- 含有個資或交易資料的檔案

## Git 忽略規則

以下打包產物不應上傳 GitHub：

```text
build/
dist/
*.spec
```

本專案已在 `.gitignore` 排除上述檔案。

## 重新打包

如果修改程式後要重新產生 exe，可以先刪除舊的打包產物，再重新執行 PyInstaller：

```powershell
Remove-Item -Recurse -Force build, dist
Remove-Item -Force *.spec
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ExcelReportTool main.py
```

刪除前請確認 `dist/` 內沒有需要保留的檔案。
