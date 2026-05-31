import tkinter as tk
from tkinter import ttk


def launch_app() -> None:
    root = tk.Tk()
    root.title("Google Sheets 自動同步報表")
    root.geometry("520x260")

    frame = ttk.Frame(root, padding=24)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="Google Sheets 自動同步報表", font=("Arial", 18, "bold"))
    title.pack(anchor="w", pady=(0, 16))

    message = ttk.Label(
        frame,
        text="第一階段已建立本機資料處理與測試。\nGoogle Sheets OAuth 連線會在下一階段加入。",
        justify="left",
    )
    message.pack(anchor="w")

    root.mainloop()
