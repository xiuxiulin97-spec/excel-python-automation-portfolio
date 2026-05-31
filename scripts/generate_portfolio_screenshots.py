from __future__ import annotations

import sys
import time
import tkinter as tk
from pathlib import Path

from PIL import ImageGrab


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "screenshots"


def capture_window(root: tk.Tk, output_path: Path) -> None:
    root.update()
    root.update_idletasks()
    time.sleep(0.2)

    x = root.winfo_rootx()
    y = root.winfo_rooty()
    width = root.winfo_width()
    height = root.winfo_height()

    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    image.save(output_path)


def capture_excel_report_gui() -> None:
    clear_project_modules()
    sys.path.insert(0, str(ROOT))
    from ui import ReportApp

    root = tk.Tk()
    root.geometry("560x360+80+80")
    app = ReportApp(root)
    capture_window(root, SCREENSHOTS / "excel-report-main-screen.png")

    app.selected_file = str(ROOT / "sample.xlsx")
    app.file_text.set("sample.xlsx")
    app.status_text.set("已選擇檔案，等待執行...")
    app.output_text.set("尚未產生報表")
    capture_window(root, SCREENSHOTS / "excel-report-select-file.png")

    app.status_text.set("讀取 Excel 中...")
    capture_window(root, SCREENSHOTS / "excel-report-running.png")

    latest_output = latest_file(ROOT / "output", "result_*.xlsx")
    app.status_text.set("完成")
    app.output_text.set(str(latest_output))
    capture_window(root, SCREENSHOTS / "excel-report-completed.png")

    root.destroy()
    sys.path.remove(str(ROOT))


def capture_customer_cleaner_gui() -> None:
    customer_root = ROOT / "customer-cleaner"
    clear_project_modules()
    sys.path.insert(0, str(customer_root))
    from ui import CustomerCleanerApp

    root = tk.Tk()
    root.geometry("600x380+120+120")
    app = CustomerCleanerApp(root)
    capture_window(root, SCREENSHOTS / "customer-cleaner-main-screen.png")

    app.selected_file = str(customer_root / "sample_customers.xlsx")
    app.file_text.set("sample_customers.xlsx")
    app.status_text.set("已選擇檔案，等待執行...")
    app.output_text.set("尚未產生報表")
    capture_window(root, SCREENSHOTS / "customer-cleaner-select-file.png")

    app.status_text.set("清洗客戶資料中...")
    capture_window(root, SCREENSHOTS / "customer-cleaner-running.png")

    latest_output = latest_file(customer_root / "output", "cleaned_customers_*.xlsx")
    app.status_text.set("完成")
    app.output_text.set(str(latest_output))
    capture_window(root, SCREENSHOTS / "customer-cleaner-completed.png")

    root.destroy()
    sys.path.remove(str(customer_root))
    clear_project_modules()


def clear_project_modules() -> None:
    for module_name in ["ui", "cleaner", "report", "validator", "exporter", "main"]:
        sys.modules.pop(module_name, None)


def latest_file(folder: Path, pattern: str) -> Path:
    files = sorted(folder.glob(pattern), key=lambda path: path.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No file found for {folder / pattern}")
    return files[-1]


def main() -> None:
    SCREENSHOTS.mkdir(exist_ok=True)
    capture_excel_report_gui()
    capture_customer_cleaner_gui()


if __name__ == "__main__":
    main()
