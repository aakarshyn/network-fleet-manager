import customtkinter as ctk
import threading
import datetime
import os

from app_interface.auth_page import AuthPage
from app_interface.landing_page import LandingPage
from app_interface.network_map import NetworkMap
from app_interface.detail_modal import DetailModal
import config

class NetworkFleetManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Network Fleet Manager")
        self.geometry("860x580")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=config.BG_DARK)

        self.container = ctk.CTkFrame(self, fg_color=config.BG_DARK)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.frames["AuthPage"] = AuthPage(self.container, self)
        self.frames["LandingPage"] = LandingPage(self.container, self)
        self.frames["NetworkMap"] = NetworkMap(self.container, self)

        self.show_frame("AuthPage")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[page_name].pack(fill="both", expand=True)

    def trigger_local_scan(self):
        self.log_audit_event("Local System Details Viewed")
        DetailModal(self)

    def trigger_network_sweep(self):
        self.show_frame("NetworkMap")
        self.frames["NetworkMap"].show_loading()
        thread = threading.Thread(target=self._run_subnet_scanner)
        thread.daemon = True
        thread.start()

    def _run_subnet_scanner(self):
        self.log_audit_event("Network Subnet Sweep Initiated")
        mapped_devices = [] 
        self.after(0, lambda: self.frames["NetworkMap"].populate_devices(mapped_devices))

    def log_audit_event(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] ACTION: {action} | IP: 127.0.0.1 | MAC: XX:XX:XX:XX:XX:XX | USER: LocalAdmin\n"
        try:
            with open("Internal_Application_Log.txt", "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Audit Log Error: {e}")

    def prompt_admin_audit_access(self):
        auth_popup = ctk.CTkToplevel(self)
        auth_popup.title("Audit Authorization")
        auth_popup.geometry("300x200")
        auth_popup.configure(fg_color=config.BG_DARK)
        auth_popup.transient(self)
        auth_popup.grab_set()

        ctk.CTkLabel(auth_popup, text="Enter Admin Credentials", text_color=config.TEXT_MAIN).pack(pady=(20, 10))
        
        user_entry = ctk.CTkEntry(auth_popup, placeholder_text="Username", fg_color=config.CARD_BG, text_color=config.TEXT_MAIN)
        user_entry.pack(pady=5)
        
        pass_entry = ctk.CTkEntry(auth_popup, placeholder_text="Password", show="*", fg_color=config.CARD_BG, text_color=config.TEXT_MAIN)
        pass_entry.pack(pady=5)

        error_label = ctk.CTkLabel(auth_popup, text="", text_color=config.ACCENT_PINK)
        error_label.pack()

        def validate():
            if user_entry.get() == "Admin" and pass_entry.get() == "Admin123":
                auth_popup.destroy()
                self.open_audit_log()
            else:
                error_label.configure(text="❌ ACCESS DENIED")

        ctk.CTkButton(auth_popup, text="UNLOCK LEDGER", fg_color=config.ACCENT_BLUE, text_color=config.BG_DARK, command=validate).pack(pady=10)

    def open_audit_log(self):
        if os.path.exists("Internal_Application_Log.txt"):
            os.startfile("Internal_Application_Log.txt")

if __name__ == "__main__":
    app = NetworkFleetManager()
    app.mainloop()
