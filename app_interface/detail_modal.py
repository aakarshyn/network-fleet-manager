import customtkinter as ctk
import threading
import config

class DetailModal(ctk.CTkToplevel):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.title("System Details")
        self.geometry("600x500")
        self.configure(fg_color=config.BG_DARK)
        self.transient(controller)
        self.grab_set()

        # Audit Log Trigger on Init
        self.controller.log_audit_event("System Details viewed")

        # Top Panel: 2x2 Grid Identity
        self.top_panel = ctk.CTkFrame(self, fg_color=config.CARD_BG, corner_radius=8)
        self.top_panel.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.top_panel, text="Device Identity:\nLocal-Host", text_color=config.TEXT_MAIN).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.top_panel, text="IP Address:\n192.168.1.X", text_color=config.TEXT_MAIN).grid(row=0, column=1, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.top_panel, text="Physical MAC:\nXX:XX:XX:XX:XX:XX", text_color=config.TEXT_MAIN).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkLabel(self.top_panel, text="Operating System:\nWindows 11", text_color=config.TEXT_MAIN).grid(row=1, column=1, padx=20, pady=10, sticky="w")

        # Middle Panel: Hardware Loads
        self.mid_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.mid_panel.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.mid_panel, text="CPU Utilization", text_color=config.TEXT_MUTED).pack(anchor="w")
        self.cpu_bar = ctk.CTkProgressBar(self.mid_panel, fg_color=config.CARD_BG, progress_color=config.ACCENT_GREEN)
        self.cpu_bar.pack(fill="x", pady=(0, 10))
        self.cpu_bar.set(0.45) 

        ctk.CTkLabel(self.mid_panel, text="RAM Memory", text_color=config.TEXT_MUTED).pack(anchor="w")
        self.ram_bar = ctk.CTkProgressBar(self.mid_panel, fg_color=config.CARD_BG, progress_color=config.ACCENT_PINK)
        self.ram_bar.pack(fill="x")
        self.ram_bar.set(0.60) 

        # Bottom Panel: Services Scrollbox
        self.scroll_box = ctk.CTkScrollableFrame(self, height=100, fg_color=config.CARD_BG)
        self.scroll_box.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(self.scroll_box, text="● Active - System.exe", text_color=config.ACCENT_GREEN).pack(anchor="w", padx=10, pady=2)
        ctk.CTkLabel(self.scroll_box, text="● Disabled - Spooler", text_color=config.TEXT_MUTED).pack(anchor="w", padx=10, pady=2)

        # Bottom Anchored Control Panel
        self.control_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.control_panel.pack(fill="x", side="bottom", padx=20, pady=20)

        self.btn_usb = ctk.CTkButton(self.control_panel, text="USB Peripheral List", fg_color=config.ACCENT_BLUE, text_color=config.BG_DARK, command=self.export_usb)
        self.btn_usb.pack(side="left", expand=True, padx=5)

        self.btn_wifi = ctk.CTkButton(self.control_panel, text="Wi-Fi/LAN Details", fg_color=config.ACCENT_BLUE, text_color=config.BG_DARK, command=self.trigger_wifi_subthread)
        self.btn_wifi.pack(side="left", expand=True, padx=5)

        self.btn_logs = ctk.CTkButton(self.control_panel, text="Device Logs", fg_color=config.ACCENT_BLUE, text_color=config.BG_DARK, command=self.export_logs)
        self.btn_logs.pack(side="left", expand=True, padx=5)

    def trigger_wifi_subthread(self):
        self.controller.log_audit_event("Wi-Fi/LAN Details Extraction Initiated")
        thread = threading.Thread(target=self.controller._run_subnet_scanner)
        thread.daemon = True
        thread.start()
        
    def export_usb(self):
        self.controller.log_audit_event("USB Peripheral List Extracted")
        
    def export_logs(self):
        self.controller.log_audit_event("Device Logs Extracted")
