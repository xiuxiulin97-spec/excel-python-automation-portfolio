import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from cleaner import clean_data, read_source_file
from report import build_summary
from sheets_client import write_report_to_google_sheets


class GoogleSheetsReportSyncApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.file_path = tk.StringVar(value="")
        self.sheet_id = tk.StringVar(value="")
        self.status = tk.StringVar(value="等待執行...")

        self.root.title("Google Sheets 自動同步報表")
        self.root.geometry("680x430")
        self.root.minsize(620, 390)

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=24)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="Google Sheets 自動同步報表", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 18))

        ttk.Label(frame, text="檔案：").grid(row=1, column=0, sticky="w", pady=(0, 6))
        ttk.Label(frame, textvariable=self.file_path, wraplength=430).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(0, 8)
        )
        ttk.Button(frame, text="選擇 Excel / CSV", command=self.select_file).grid(
            row=2, column=2, sticky="e", padx=(12, 0), pady=(0, 8)
        )

        ttk.Separator(frame).grid(row=3, column=0, columnspan=3, sticky="ew", pady=14)

        ttk.Label(frame, text="Google Sheet ID：").grid(row=4, column=0, sticky="w", pady=(0, 6))
        sheet_entry = ttk.Entry(frame, textvariable=self.sheet_id)
        sheet_entry.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        ttk.Button(frame, text="開始同步", command=self.sync_report).grid(
            row=6, column=0, sticky="w", pady=(8, 14)
        )

        ttk.Separator(frame).grid(row=7, column=0, columnspan=3, sticky="ew", pady=8)

        ttk.Label(frame, text="狀態：").grid(row=8, column=0, sticky="w", pady=(6, 6))
        ttk.Label(frame, textvariable=self.status, wraplength=590).grid(
            row=9, column=0, columnspan=3, sticky="w"
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)

    def select_file(self) -> None:
        selected_path = filedialog.askopenfilename(
            title="選擇 Excel / CSV 檔案",
            filetypes=[
                ("Excel / CSV files", "*.xlsx *.xlsm *.csv"),
                ("Excel files", "*.xlsx *.xlsm"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )

        if selected_path:
            self.file_path.set(selected_path)
            self.status.set(f"已選擇檔案：{Path(selected_path).name}")

    def sync_report(self) -> None:
        if not self.file_path.get():
            messagebox.showwarning("缺少檔案", "請先選擇 Excel / CSV 檔案")
            return

        spreadsheet_id = self.sheet_id.get().strip()
        if not spreadsheet_id:
            messagebox.showwarning("缺少 Google Sheet ID", "請輸入 Google Sheet ID")
            return

        try:
            self.status.set("正在讀取與清理資料...")
            self.root.update_idletasks()

            original_df = read_source_file(self.file_path.get())
            cleaned_df = clean_data(original_df)
            summary_df = build_summary(cleaned_df)

            self.status.set("正在同步到 Google Sheets，第一次執行可能會開啟瀏覽器授權...")
            self.root.update_idletasks()

            write_report_to_google_sheets(spreadsheet_id, cleaned_df, summary_df)

            message = "同步完成：已寫入「清理後資料」與「統計報表」"
            self.status.set(message)
            messagebox.showinfo("完成", message)
        except Exception as exc:
            error_message = f"同步失敗：{exc}"
            self.status.set(error_message)
            messagebox.showerror("同步失敗", error_message)


def launch_app() -> None:
    root = tk.Tk()
    GoogleSheetsReportSyncApp(root)
    root.mainloop()
