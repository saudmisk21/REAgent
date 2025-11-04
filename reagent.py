import tkinter as tk
from tkinter import messagebox
import platform, socket, requests, time, threading
from datetime import datetime

# ---------- Version ----------
APP_VERSION = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/saudmisk21/REAgent/refs/heads/main/version"

def check_version():
    """Check GitHub for latest version and return (is_up_to_date, latest_version)."""
    try:
        response = requests.get(VERSION_URL, timeout=5)
        # Clean up any trailing spaces, newlines, or carriage returns
        latest = response.text.strip().replace('\n', '').replace('\r', '').replace(' ', '')
        print(f"DEBUG: Latest={repr(latest)}, Current={repr(APP_VERSION)}")  # Optional debug
        is_up_to_date = (latest == APP_VERSION)
        if not is_up_to_date:
            messagebox.showwarning(
                "Old Version Detected",
                f"This version ({APP_VERSION}) is outdated.\n\n"
                "Get the latest version from:\n"
                "https://github.com/saudmisk21/REAgent"
            )
        return is_up_to_date, latest
    except Exception as e:
        print("Version check failed:", e)
        # If we can't reach GitHub, assume current version is OK
        return True, APP_VERSION

# Run version check before anything else
UP_TO_DATE, LATEST_VERSION = check_version()

if not UP_TO_DATE:
    # Stop the app if outdated
    exit()

# ---------- System Info Sender ----------
WEBHOOK_URL = "https://7b293d66dbb8777396ffc04f5ac9a12f.m.pipedream.net"

def send_system_info(show_status=False):
    data = {
        "os": platform.system(),
        "os_version": platform.version(),
        "device_name": socket.gethostname(),
        "timestamp": datetime.now().isoformat(),
        "version": APP_VERSION,
        "up_to_date": UP_TO_DATE
    }
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=5)
        if show_status:
            status_label.config(
                text=f"✅ Info sent at {datetime.now().strftime('%H:%M:%S')}")
            animate_log()
    except Exception as e:
        if show_status:
            status_label.config(text=f"❌ Error: {e}")

# ---------- Animated Log Window ----------
def animate_log():
    log_win = tk.Toplevel(root)
    log_win.title("REAgent Log")
    log_win.geometry("500x240")
    log_win.configure(bg="#101010")
    log_win.attributes("-alpha", 0.93)

    log_text = tk.Text(
        log_win, bg="#101010", fg="#00FF7F",
        insertbackground="#00FF7F",
        font=("Courier New", 12),
        relief="flat", wrap="none"
    )
    log_text.pack(expand=True, fill="both", padx=8, pady=8)
    log_text.config(state="disabled")

    lines = [
        f"x0000x9 REAgent Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "x0000x9x0 REAgent disabled Jamf.010922",
        "x0000x9x0 REAgent disabled Jamf.088211",
        "x0000x9x0 REAgent disabled Jamf.032821",
        "x0000x9x0 REAgent disabled Jamf.021993",
        f"x0x9 REAgent completed task. UpToDate={UP_TO_DATE}"
    ]

    def writer():
        for line in lines:
            time.sleep(1)
            log_text.config(state="normal")
            log_text.insert("end", line + "\n")
            log_text.see("end")
            log_text.config(state="disabled")

    threading.Thread(target=writer, daemon=True).start()

# ---------- Main Window ----------
root = tk.Tk()
root.title("REAgent")
root.geometry("360x220")
root.configure(bg="#f2f2f2")
root.attributes("-alpha", 0.95)

tk.Label(root, text="REAgent", font=("Arial", 16, "bold"), bg="#f2f2f2").pack(pady=10)
tk.Label(root, text="REAgent Software for Arc", bg="#f2f2f2").pack(pady=2)
tk.Label(root, text=f"Version {APP_VERSION}", bg="#f2f2f2", font=("Arial", 10, "italic")).pack(pady=2)

btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Send Again",
          command=lambda: send_system_info(show_status=True),
          font=("Arial", 12), width=12).grid(row=0, column=0, padx=8)

tk.Button(btn_frame, text="View Log",
          command=animate_log,
          font=("Arial", 12), width=12).grid(row=0, column=1, padx=8)

status_label = tk.Label(root, text="", fg="green", bg="#f2f2f2")
status_label.pack()

# Silent send on startup
root.after(1000, send_system_info)
root.mainloop()
