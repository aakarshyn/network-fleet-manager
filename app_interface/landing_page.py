import customtkinter as ctk
import config

class LandingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=config.BG_DARK)
        self.controller = controller

        self.header = ctk.CTkLabel(self, text="Network Fleet Manager Dashboard", font=("Arial", 24, "bold"), text_color=config.TEXT_MAIN)
        self.header.pack(pady=(60, 40))

        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(expand=True)

        self.local_btn = ctk.CTkButton(self.grid_frame, text="💻\n\nVIEW THIS SYSTEM DETAILS", width=260, height=160, corner_radius=16, fg_color=config.CARD_BG, text_color=config.ACCENT_BLUE, font=("Arial", 16, "bold"), hover_color=config.BG_DARK, command=self.controller.trigger_local_scan)
        self.local_btn.grid(row=0, column=0, padx=20)

        self.network_btn = ctk.CTkButton(self.grid_frame, text="🌐\n\nSCAN NETWORK", width=260, height=160, corner_radius=16, fg_color=config.CARD_BG, text_color=config.ACCENT_BLUE, font=("Arial", 16, "bold"), hover_color=config.BG_DARK, command=self.controller.trigger_network_sweep)
        self.network_btn.grid(row=0, column=1, padx=20)
        
        self.audit_btn = ctk.CTkButton(self, text="AUDIT REGISTER", fg_color=config.CARD_BG, text_color=config.TEXT_MUTED, hover_color=config.BG_DARK, command=self.controller.prompt_admin_audit_access)
        self.audit_btn.pack(side="bottom", pady=20)
