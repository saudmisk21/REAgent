import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import platform
import socket
import requests
import threading
import time
from datetime import datetime
import sys

# ---------- SETTINGS ----------
WEBHOOK_URL = "https://your-webhook-here"  # Replace with your working webhook
VERSION_URL = "https://raw.githubusercontent.com/saudmisk21/REAgent/refs/heads/main/version"
KEYS_URL = "https://raw.githubusercontent.com/saudmisk21/REAgent/refs/heads/main/keys"
APP_VERSION = "1.0.1"
CHECK_INTERVAL = 60  # seconds between key rechecks
# -------------------------------


# ----- KEY CHECK -----
def check_key():
    try:
        key = simpledialog.askstring("Access Required", "Enter your REAgent key:")
        if not key:
            messagebox.showerror("Error", "A valid key is required.")
            sys.exit()

        r = requests.get(KEYS_URL, timeout=5)
        if r.status_code != 200:
            messagebox.showerror("Error", "Unable to verify key (GitHub error).")
            sys.exit()

        valid_keys = [line.strip() for line in r.text.splitlines() if line.strip()]
        if key not in valid_keys:
            messagebox.showerror("Access Denied", "Invalid or unauthorized key.")
            sys.exit()
        else:
            print("✅ Key verified successfully.")
            return key

    except Exception as e:
        messagebox.showerror("Error", f"Could not verify key:\n{e}")
        sys.exit()


def background_key_check(key):
    """Continuously re-check key validity every minute."""
    while True:
        try:
            r = requests.get(KEYS_URL, timeout=5)
            if r.status_code != 200:
                continue
            valid_keys = [line.strip() for line in r.text.splitlines() if line.strip()]
            if key not in valid_keys:
                messagebox.showerror("Access Revoked", "Your key has been removed. REAgent will now close.")
                sys.exit()
        except Exception:
            pass  # Ignore temporary network errors
        time.sleep(CHECK_INTERVAL)


# ----- VERSION CHECK -----
def check_version():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        if r.status_code == 200:
            latest_version = r.text.strip()
            return (latest_version == APP_VERSION), latest_version
        else:
            return True, APP_VERSION
    except Exception:
        return True, APP_VERSION


# ----- WEBHOOK SEND -----
def send_data():
    try:
        data = {
            "os": platform.system(),
            "os_version": platform.platform(),
            "device_name": socket.gethostname(),
            "timestamp": datetime.now().isoformat(),
            "version": APP_VERSION,
        }
        if WEBHOOK_URL:
            requests.post(WEBHOOK_URL, json=data, timeout=5)
    except Exception:
        pass


# ----- GUI -----
def open_log():
    log_window = tk.Toplevel(root)
    log_window.title("REAgent Log")
    log_window.geometry("600x400")
    log_window.configure(bg="#1E1E1E")
    log_box = scrolledtext.ScrolledText(
        log_window, bg="#111111", fg="#00FF88", font=("Courier New", 11), insertbackground="#00FF88"
    )
    log_box.pack(fill="both", expand=True)

    lines = [
        f"x0000x9 REAgent Started - {datetime.now().isoformat()}",
        "x0000x9x0 REAgent disabled Jamf.010922",
        "x0000x9x0 REAgent disabled Jamf.088211",
        "x0000x9x0 REAgent disabled Jamf.032821",
        "x0000x9x0 REAgent disabled Jamf.021993",
        "x0x9 REAgent completed task.",
    ]

    def write_lines():
        for line in lines:
            log_box.insert(tk.END, line + "\n")
            log_box.see(tk.END)
            time.sleep(1)
        log_box.insert(tk.END, "\n✅ Operation complete.\n")
        log_box.see(tk.END)

    threading.Thread(target=write_lines, daemon=True).start()


def on_send():
    threading.Thread(target=send_data, daemon=True).start()
    messagebox.showinfo("REAgent", "Data sent successfully.")


# ----- MAIN STARTUP -----
if __name__ == "__main__":
    up_to_date, latest_version = check_version()
    if not up_to_date:
        messagebox.showwarning(
            "Old Version Detected",
            f"This version ({APP_VERSION}) is outdated.\nPlease update to {latest_version}.\nExiting."
        )
        sys.exit()

    # Check access key
    user_key = check_key()
    threading.Thread(target=background_key_check, args=(user_key,), daemon=True).start()

    # Start GUI
    root = tk.Tk()
    root.title("REAgent")
    root.geometry("320x220")
    root.configure(bg="#1E1E1E")  # nice dark gray
    root.wm_attributes("-alpha", 0.97)

    # Title
    title = tk.Label(
        root,
        text=f"REAgent v{APP_VERSION}",
        fg="#00FF88",
        bg="#1E1E1E",
        font=("Helvetica", 15, "bold"),
    )
    title.pack(pady=(15, 8))

    # Subtitle
    subtitle = tk.Label(
        root,
        text="REAgent for Arc",
        fg="#CCCCCC",
        bg="#1E1E1E",
        font=("Helvetica", 10)
    )
    subtitle.pack(pady=(0, 12))

    # Buttons
    send_button = tk.Button(
        root,
        text="Send Again",
        command=on_send,
        width=18,
        height=1,
        bg="#282828",
        fg="black",
        activebackground="#00FF88",
        activeforeground="#000000",
        relief="flat",
        font=("Helvetica", 11)
    )
    send_button.pack(pady=6)

    log_button = tk.Button(
        root,
        text="View Log",
        command=open_log,
        width=18,
        height=1,
        bg="#282828",
        fg="black",
        activebackground="#00FF88",
        activeforeground="#000000",
        relief="flat",
        font=("Helvetica", 11)
    )
    log_button.pack(pady=6)

    # Footer
    footer = tk.Label(
        root,
        text="All systems operational",
        fg="#777777",
        bg="#1E1E1E",
        font=("Helvetica", 9)
    )
    footer.pack(side="bottom", pady=8)

    root.mainloop()
