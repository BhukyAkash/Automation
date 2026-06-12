"""
popup_utils.py
--------------
Reusable popup dialog utilities for Playwright automation scripts.
Displays Tkinter dialogs during automation runs instead of blocking
the terminal with input(). Waits indefinitely until the user responds.

Functions:
    ask_popup(question)              → 'yes' | 'no'
    select_popup(question, options)  → one of the provided option strings
"""

import tkinter as tk
from tkinter import messagebox


def ask_popup(question: str, title: str = "Automation Input") -> str:
    # ── Colours ──────────────────────────────
    BG           = "#FFFFFF"
    DIVIDER      = "#E5E7EB"
    ACCENT       = "#378ADD"
    TEXT_MAIN    = "#111827"
    BTN_FG       = "#FFFFFF"
    BTN_HOVER    = "#2563EB"
    NO_BG        = "#F3F4F6"
    NO_FG        = "#374151"
    NO_HOVER     = "#E5E7EB"
    # ─────────────────────────────────────────

    result = {"value": "no"}

    root = tk.Tk()
    root.title(title)
    root.configure(bg=BG)
    root.attributes("-topmost", True)
    root.resizable(False, False)

    root.update_idletasks()
    win_w, win_h = 300, 180
    x = (root.winfo_screenwidth()  // 2) - (win_w // 2)
    y = (root.winfo_screenheight() // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # ── Question label (Bold) ─────────────────
    tk.Label(
        root,
        text=question,
        bg=BG,
        fg=TEXT_MAIN,
        font=("Segoe UI", 10, "bold"),   # ← bold
        wraplength=260,
        justify="left"
    ).pack(anchor="w", padx=20, pady=(20, 16))

    tk.Frame(root, bg=DIVIDER, height=1).pack(fill="x")

    # ── Yes / No buttons ──────────────────────
    btn_row = tk.Frame(root, bg=BG)
    btn_row.pack(fill="x", padx=16, pady=14)

    def on_yes():
        result["value"] = "yes"
        root.quit()

    def on_no():
        result["value"] = "no"
        root.quit()

    def yes_enter(e): yes_btn.config(bg=BTN_HOVER)
    def yes_leave(e): yes_btn.config(bg=ACCENT)
    def no_enter(e):  no_btn.config(bg=NO_HOVER)
    def no_leave(e):  no_btn.config(bg=NO_BG)

    no_btn = tk.Button(
        btn_row, text="No", command=on_no,
        bg=NO_BG, fg=NO_FG, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground=NO_HOVER, activeforeground=NO_FG,
        bd=0, pady=9
    )
    no_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
    no_btn.bind("<Enter>", no_enter)
    no_btn.bind("<Leave>", no_leave)

    yes_btn = tk.Button(
        btn_row, text="Yes", command=on_yes,
        bg=ACCENT, fg=BTN_FG, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground=BTN_HOVER, activeforeground=BTN_FG,
        bd=0, pady=9
    )
    yes_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))
    yes_btn.bind("<Enter>", yes_enter)
    yes_btn.bind("<Leave>", yes_leave)

    root.mainloop()
    value = result["value"]

    try:
        root.destroy()
    except Exception:
        pass

    return value


def select_popup(question: str, options: list, title: str = "Automation Input") -> str:
    # ── Colours ──────────────────────────────
    BG           = "#FFFFFF"
    DIVIDER      = "#E5E7EB"
    ACCENT       = "#378ADD"
    TEXT_MAIN    = "#111827"
    TEXT_DIM     = "#9CA3AF"
    BTN_FG       = "#FFFFFF"
    BTN_HOVER    = "#2563EB"
    # ─────────────────────────────────────────

    selected = {"value": options[0]}
    option_frames = {}

    root = tk.Tk()
    root.title(title)
    root.configure(bg=BG)
    root.attributes("-topmost", True)
    root.resizable(False, False)

    root.update_idletasks()
    win_w, win_h = 300, 70 + (len(options) * 44) + 60
    x = (root.winfo_screenwidth()  // 2) - (win_w // 2)
    y = (root.winfo_screenheight() // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # ── Question label (Bold) ─────────────────
    tk.Label(
        root,
        text=question,
        bg=BG,
        fg=TEXT_MAIN,
        font=("Segoe UI", 10, "bold"),   # ← bold
        wraplength=260,
        justify="left"
    ).pack(anchor="w", padx=20, pady=(16, 4))

    tk.Frame(root, bg=DIVIDER, height=1).pack(fill="x")

    def select_option(chosen: str):
        selected["value"] = chosen
        for opt, widgets in option_frames.items():
            is_active = (opt == chosen)
            widgets["frame"].config(bg=BG)
            widgets["canvas"].config(bg=BG)
            widgets["label"].config(bg=BG, fg=TEXT_MAIN)
            c = widgets["canvas"]
            c.delete("all")
            c.create_oval(2, 2, 14, 14, outline=ACCENT if is_active else TEXT_DIM, width=2)
            if is_active:
                c.create_oval(5, 5, 11, 11, fill=ACCENT, outline=ACCENT)
            widgets["divider"].config(bg=DIVIDER)

    for i, opt in enumerate(options):
        row = tk.Frame(root, bg=BG, cursor="hand2")
        row.pack(fill="x")

        inner = tk.Frame(row, bg=BG)
        inner.pack(fill="x", padx=20)

        canvas = tk.Canvas(inner, width=16, height=16, bg=BG, highlightthickness=0)
        canvas.pack(side="left", padx=(0, 10), pady=12)

        lbl = tk.Label(inner, text=opt, bg=BG, fg=TEXT_MAIN, font=("Segoe UI", 10), anchor="w")
        lbl.pack(side="left", pady=12)

        divider = tk.Frame(row, bg=DIVIDER, height=1)
        if i < len(options) - 1:
            divider.pack(fill="x")

        option_frames[opt] = {"frame": inner, "canvas": canvas, "label": lbl, "divider": divider}

        for widget in (row, inner, canvas, lbl):
            widget.bind("<Button-1>", lambda e, o=opt: select_option(o))

    tk.Frame(root, bg=DIVIDER, height=1).pack(fill="x")

    def confirm():
        root.quit()

    def on_enter(e): confirm_btn.config(bg=BTN_HOVER)
    def on_leave(e): confirm_btn.config(bg=ACCENT)

    confirm_btn = tk.Button(
        root, text="Confirm", command=confirm,
        bg=ACCENT, fg=BTN_FG, font=("Segoe UI", 10, "bold"),
        relief="flat", cursor="hand2",
        activebackground=BTN_HOVER, activeforeground=BTN_FG,
        bd=0, pady=9
    )
    confirm_btn.pack(fill="x", padx=16, pady=14)
    confirm_btn.bind("<Enter>", on_enter)
    confirm_btn.bind("<Leave>", on_leave)

    select_option(options[0])
    root.mainloop()
    result = selected["value"]

    try:
        root.destroy()
    except Exception:
        pass

    return result
