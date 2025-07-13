# ui.py
import tkinter as tk
from tkinter import ttk
from widgets import create_modern_entry, create_modern_button
from logic import submit

def build_ui(window):
    entries = {}
    payment_type_var = tk.StringVar(value="Bank Transfer")

    # Background and layout
    window.title("Wire Transfer Tool")
    window.configure(bg="black")
    window.geometry("1000x700")

    # Entry section
    form_frame = tk.Frame(window, bg="black")
    form_frame.pack(pady=10)

    fields = [
        "Sender Bank Name", "Sender Account Number", "Sender Routing Number",
        "Receiver Bank Name", "Receiver Account Number", "Receiver Routing Number", "Amount"
    ]

    for field in fields:
        entry = create_modern_entry(form_frame, field)
        entry.pack(pady=5)
        entries[field] = entry

    # Payment Type Dropdown
    dropdown_label = tk.Label(window, text="Payment Type", bg="black", fg="white", font=("Helvetica", 12, "bold"))
    dropdown_label.pack()
    payment_dropdown = ttk.Combobox(window, textvariable=payment_type_var, values=["Bank Transfer", "Card Payment"])
    payment_dropdown.pack(pady=10)

    # Submit Button
    submit_btn = create_modern_button(window, "🚀 Submit Transfer", lambda: submit(entries, payment_type_var, log_listbox), "green", 25)
    submit_btn.pack(pady=20)

    # Log Box
    log_listbox = tk.Listbox(window, bg="white", fg="black", width=100, height=10, font=("Courier", 10))
    log_listbox.pack(pady=20)

    return window
