from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from cleaner import clean_data
from column_analyzer import DATE, NUMBER, TEXT, analyze_columns
from excel_formatter import format_workbook
from reader import read_table
from report_builder import (
    build_group_report,
    build_monthly_report,
    build_summary,
    build_top10_report,
)


NO_DATE_OPTION = "不使用"
ID_KEYWORDS = ("序号", "序號", "编号", "編號", "流水号", "流水號", "id")
AMOUNT_KEYWORDS = ("金額", "金额", "費用", "费用", "支出", "總額", "总额", "合計", "合计", "成交")


class ReportApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.selected_file: str | None = None
        self.original_df: pd.DataFrame | None = None
        self.cleaned_df: pd.DataFrame | None = None
        self.column_analysis: list[dict[str, object]] = []

        self.file_text = tk.StringVar(value="尚未選擇檔案")
        self.info_text = tk.StringVar(value="列數：-    欄位數：-")
        self.status_text = tk.StringVar(value="等待執行...")
        self.output_text = tk.StringVar(value="尚未產生報表")

        self.group_column = tk.StringVar(value="")
        self.value_column = tk.StringVar(value="")
        self.date_column = tk.StringVar(value=NO_DATE_OPTION)

        self.group_combo: ttk.Combobox | None = None
        self.value_combo: ttk.Combobox | None = None
        self.date_combo: ttk.Combobox | None = None
        self.column_tree: ttk.Treeview | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        self.root.title("Excel Report Tool v2.1 通用表格分析工具")
        self.root.geometry("900x680")
        self.root.minsize(820, 620)

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        title_label = ttk.Label(
            main_frame,
            text="Excel Report Tool v2.1 通用表格分析工具",
            font=("Microsoft JhengHei UI", 18, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 14))

        file_frame = ttk.LabelFrame(main_frame, text="1. 選擇檔案", padding=12)
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        file_frame.columnconfigure(0, weight=1)

        ttk.Label(file_frame, textvariable=self.file_text, wraplength=650).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Button(file_frame, text="選擇 Excel / CSV", command=self.choose_file).grid(
            row=0, column=1, padx=(12, 0), sticky="e"
        )
        ttk.Label(file_frame, textvariable=self.info_text).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

        field_frame = ttk.LabelFrame(main_frame, text="2. 選擇分析欄位", padding=12)
        field_frame.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        for index in range(3):
            field_frame.columnconfigure(index, weight=1)

        ttk.Label(field_frame, text="分組欄位").grid(row=0, column=0, sticky="w")
        self.group_combo = ttk.Combobox(field_frame, textvariable=self.group_column, state="readonly")
        self.group_combo.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(4, 0))

        ttk.Label(field_frame, text="統計欄位").grid(row=0, column=1, sticky="w")
        self.value_combo = ttk.Combobox(field_frame, textvariable=self.value_column, state="readonly")
        self.value_combo.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(4, 0))

        ttk.Label(field_frame, text="日期欄位").grid(row=0, column=2, sticky="w")
        self.date_combo = ttk.Combobox(field_frame, textvariable=self.date_column, state="readonly")
        self.date_combo.grid(row=1, column=2, sticky="ew", pady=(4, 0))

        table_frame = ttk.LabelFrame(main_frame, text="3. 欄位分析結果", padding=12)
        table_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 12))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("name", "type", "count", "samples")
        self.column_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.column_tree.heading("name", text="欄位名稱")
        self.column_tree.heading("type", text="推測類型")
        self.column_tree.heading("count", text="非空筆數")
        self.column_tree.heading("samples", text="範例值")
        self.column_tree.column("name", width=180, anchor="w")
        self.column_tree.column("type", width=90, anchor="center")
        self.column_tree.column("count", width=90, anchor="center")
        self.column_tree.column("samples", width=420, anchor="w")
        self.column_tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.column_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.column_tree.configure(yscrollcommand=scrollbar.set)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, sticky="ew")
        action_frame.columnconfigure(1, weight=1)

        ttk.Button(action_frame, text="產生報表", command=self.generate_report).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(action_frame, textvariable=self.status_text).grid(
            row=0, column=1, sticky="w", padx=(14, 0)
        )
        ttk.Label(main_frame, text="輸出：").grid(row=5, column=0, sticky="w", pady=(14, 4))
        ttk.Label(main_frame, textvariable=self.output_text, wraplength=820).grid(
            row=6, column=0, sticky="w"
        )

    def choose_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="選擇 Excel / CSV 檔案",
            filetypes=[
                ("Excel / CSV files", "*.xlsx *.xlsm *.csv"),
                ("Excel files", "*.xlsx *.xlsm"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        try:
            self.status_text.set("正在讀取資料...")
            self.root.update_idletasks()

            original_df = read_table(file_path)
            cleaned_df = clean_data(original_df)
            analysis = analyze_columns(cleaned_df)

            self.selected_file = file_path
            self.original_df = original_df
            self.cleaned_df = cleaned_df
            self.column_analysis = analysis

            self.file_text.set(Path(file_path).name)
            self.info_text.set(f"列數：{len(original_df)}    欄位數：{len(original_df.columns)}")
            self.output_text.set("尚未產生報表")
            self.status_text.set("欄位分析完成，請選擇分組欄位與統計欄位。")

            self._render_column_analysis()
            self._set_field_options()
        except Exception as exc:
            self._reset_loaded_data()
            self.status_text.set("讀取失敗")
            messagebox.showerror("錯誤", str(exc))

    def generate_report(self) -> None:
        if self.original_df is None or self.cleaned_df is None:
            messagebox.showwarning("提醒", "請先選擇 Excel / CSV 檔案。")
            return

        group_column = self.group_column.get().strip()
        value_column = self.value_column.get().strip()
        date_column = self.date_column.get().strip()

        if not group_column:
            messagebox.showwarning("提醒", "請選擇分組欄位。")
            return

        if not value_column:
            messagebox.showwarning("提醒", "請選擇統計欄位。")
            return

        try:
            self.status_text.set("正在產生報表...")
            self.root.update_idletasks()

            output_path = export_dynamic_report(
                original_df=self.original_df,
                cleaned_df=self.cleaned_df,
                group_column=group_column,
                value_column=value_column,
                date_column=None if date_column == NO_DATE_OPTION else date_column,
            )

            self.output_text.set(output_path)
            self.status_text.set("完成")
            messagebox.showinfo("完成", f"報表已產生：\n{output_path}")
        except Exception as exc:
            self.status_text.set("執行失敗")
            messagebox.showerror("錯誤", str(exc))

    def _render_column_analysis(self) -> None:
        if self.column_tree is None:
            return

        self.column_tree.delete(*self.column_tree.get_children())
        for item in self.column_analysis:
            samples = "、".join(item["sample_values"])  # type: ignore[index]
            self.column_tree.insert(
                "",
                tk.END,
                values=(
                    item["name"],
                    _display_type(str(item["type"])),
                    item["non_null_count"],
                    samples,
                ),
            )

    def _set_field_options(self) -> None:
        text_columns = _columns_by_type(self.column_analysis, TEXT)
        number_columns = _columns_by_type(self.column_analysis, NUMBER)
        value_columns = _value_column_options(number_columns)
        date_columns = _columns_by_type(self.column_analysis, DATE)
        all_columns = [str(item["name"]) for item in self.column_analysis]

        if self.group_combo is not None:
            self.group_combo["values"] = all_columns
        if self.value_combo is not None:
            self.value_combo["values"] = value_columns
        if self.date_combo is not None:
            self.date_combo["values"] = [NO_DATE_OPTION, *date_columns]

        self.group_column.set(text_columns[0] if text_columns else (all_columns[0] if all_columns else ""))
        self.value_column.set(value_columns[0] if value_columns else "")
        self.date_column.set(date_columns[0] if date_columns else NO_DATE_OPTION)

        if not value_columns:
            messagebox.showwarning("提醒", "此檔案沒有可用的數字欄位，無法產生統計報表。")

    def _reset_loaded_data(self) -> None:
        self.selected_file = None
        self.original_df = None
        self.cleaned_df = None
        self.column_analysis = []
        self.file_text.set("尚未選擇檔案")
        self.info_text.set("列數：-    欄位數：-")
        self.output_text.set("尚未產生報表")
        self.group_column.set("")
        self.value_column.set("")
        self.date_column.set(NO_DATE_OPTION)
        if self.column_tree is not None:
            self.column_tree.delete(*self.column_tree.get_children())


def export_dynamic_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    group_column: str,
    value_column: str,
    date_column: str | None = None,
    output_dir: str = "output",
) -> str:
    summary_df = build_summary(cleaned_df, value_column=value_column)
    group_df = build_group_report(cleaned_df, group_column=group_column, value_column=value_column)
    top10_df = build_top10_report(cleaned_df, value_column=value_column)
    monthly_df = (
        build_monthly_report(cleaned_df, date_column=date_column, value_column=value_column)
        if date_column
        else pd.DataFrame()
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_path / f"result_v2_{timestamp}.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        original_df.to_excel(writer, sheet_name="原始資料", index=False)
        cleaned_df.to_excel(writer, sheet_name="清理後資料", index=False)
        _write_statistics_sheet(
            writer=writer,
            summary_df=summary_df,
            group_df=group_df,
            top10_df=top10_df,
            monthly_df=monthly_df,
            include_monthly=date_column is not None,
        )

    format_workbook(report_path)
    return str(report_path)


def _write_statistics_sheet(
    writer: pd.ExcelWriter,
    summary_df: pd.DataFrame,
    group_df: pd.DataFrame,
    top10_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    include_monthly: bool,
) -> None:
    sheet_name = "統計報表"
    start_row = 0

    start_row = _write_section(writer, sheet_name, "總覽", summary_df, start_row)
    start_row = _write_section(writer, sheet_name, "分組統計", group_df, start_row)
    if include_monthly:
        start_row = _write_section(writer, sheet_name, "月份統計", monthly_df, start_row)
    _write_section(writer, sheet_name, "Top10排行", top10_df, start_row)


def _write_section(
    writer: pd.ExcelWriter,
    sheet_name: str,
    title: str,
    df: pd.DataFrame,
    start_row: int,
) -> int:
    pd.DataFrame([[title]]).to_excel(
        writer,
        sheet_name=sheet_name,
        startrow=start_row,
        header=False,
        index=False,
    )
    start_row += 1

    if df.empty:
        pd.DataFrame([{"說明": "沒有資料"}]).to_excel(
            writer,
            sheet_name=sheet_name,
            startrow=start_row,
            index=False,
        )
        return start_row + 4

    df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False)
    return start_row + len(df) + 3


def _columns_by_type(column_analysis: list[dict[str, object]], column_type: str) -> list[str]:
    return [
        str(item["name"])
        for item in column_analysis
        if item.get("type") == column_type
    ]


def _value_column_options(number_columns: list[str]) -> list[str]:
    amount_columns = [column for column in number_columns if _is_amount_like_column(column)]
    other_columns = [
        column
        for column in number_columns
        if column not in amount_columns and not _is_identifier_like_column(column)
    ]
    identifier_columns = [
        column
        for column in number_columns
        if column not in amount_columns and _is_identifier_like_column(column)
    ]
    return [*amount_columns, *other_columns, *identifier_columns]


def _is_identifier_like_column(column: str) -> bool:
    normalized = column.strip().lower()
    return any(keyword.lower() in normalized for keyword in ID_KEYWORDS)


def _is_amount_like_column(column: str) -> bool:
    normalized = column.strip().lower()
    return any(keyword.lower() in normalized for keyword in AMOUNT_KEYWORDS)


def _display_type(column_type: str) -> str:
    labels = {
        TEXT: "文字",
        NUMBER: "數字",
        DATE: "日期",
    }
    return labels.get(column_type, column_type)


def launch_app() -> None:
    root = tk.Tk()
    ReportApp(root)
    root.mainloop()
