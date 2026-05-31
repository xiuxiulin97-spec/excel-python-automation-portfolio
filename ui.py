from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from cleaner import clean_data, read_excel
from report import export_report


class ReportApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.selected_file: str | None = None

        self.file_text = tk.StringVar(value="尚未選擇檔案")
        self.status_text = tk.StringVar(value="等待執行...")
        self.output_text = tk.StringVar(value="尚未產生報表")

        self._build_ui()

    def _build_ui(self) -> None:
        self.root.title("Excel AI 自動報表工具")
        self.root.geometry("560x360")
        self.root.minsize(480, 320)

        main_frame = tk.Frame(self.root, padx=24, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame,
            text="Excel AI 自動報表工具",
            font=("Microsoft JhengHei UI", 18, "bold"),
        )
        title_label.pack(anchor="w")

        separator_1 = tk.Frame(main_frame, height=1, bg="#d9d9d9")
        separator_1.pack(fill=tk.X, pady=14)

        tk.Label(main_frame, text="檔案：", font=("Microsoft JhengHei UI", 11)).pack(anchor="w")
        tk.Label(
            main_frame,
            textvariable=self.file_text,
            anchor="w",
            justify="left",
            wraplength=500,
            fg="#333333",
        ).pack(fill=tk.X, pady=(4, 10))

        tk.Button(main_frame, text="選擇 Excel", command=self.choose_file, width=16).pack(anchor="w")

        separator_2 = tk.Frame(main_frame, height=1, bg="#d9d9d9")
        separator_2.pack(fill=tk.X, pady=14)

        tk.Button(main_frame, text="開始分析", command=self.run_analysis, width=16).pack(anchor="w")
        tk.Label(main_frame, text="狀態：", font=("Microsoft JhengHei UI", 11)).pack(
            anchor="w", pady=(12, 0)
        )
        tk.Label(main_frame, textvariable=self.status_text, anchor="w", fg="#333333").pack(
            fill=tk.X, pady=(4, 0)
        )

        separator_3 = tk.Frame(main_frame, height=1, bg="#d9d9d9")
        separator_3.pack(fill=tk.X, pady=14)

        tk.Label(main_frame, text="輸出：", font=("Microsoft JhengHei UI", 11)).pack(anchor="w")
        tk.Label(
            main_frame,
            textvariable=self.output_text,
            anchor="w",
            justify="left",
            wraplength=500,
            fg="#333333",
        ).pack(fill=tk.X, pady=(4, 0))

    def choose_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="選擇 Excel 檔案",
            filetypes=[
                ("Excel files", "*.xlsx *.xlsm"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        self.selected_file = file_path
        self.file_text.set(Path(file_path).name)
        self.status_text.set("已選擇檔案，等待執行...")
        self.output_text.set("尚未產生報表")

    def run_analysis(self) -> None:
        if not self.selected_file:
            messagebox.showwarning("提醒", "請先選擇 Excel 檔案。")
            return

        try:
            self.status_text.set("讀取 Excel 中...")
            self.root.update_idletasks()

            original_df = read_excel(self.selected_file)

            self.status_text.set("清理資料中...")
            self.root.update_idletasks()

            cleaned_df = clean_data(original_df)

            self.status_text.set("產生統計報表中...")
            self.root.update_idletasks()

            output_path = export_report(original_df, cleaned_df)
            self.output_text.set(output_path)
            self.status_text.set("完成")
            messagebox.showinfo("完成", f"報表已產生：\n{output_path}")
        except Exception as exc:
            self.status_text.set("執行失敗")
            messagebox.showerror("錯誤", str(exc))


def launch_app() -> None:
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()
