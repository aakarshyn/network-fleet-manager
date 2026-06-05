import customtkinter as ctk
import config

class NetworkMap(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=config.BG_DARK)
        self.controller = controller

        self.nav_bar = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=config.CARD_BG)
        self.nav_bar.pack(fill="x", side="top")

        self.back_btn = ctk.CTkButton(self.nav_bar, text="← BACK TO DASHBOARD", fg_color="transparent", text_color=config.TEXT_MAIN, hover_color=config.BG_DARK, command=lambda: self.controller.show_frame("LandingPage"))
        self.back_btn.pack(side="left", padx=15, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=config.BG_DARK)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.loading_label = ctk.CTkLabel(self.scroll_frame, text="Scanning Network", text_color=config.ACCENT_BLUE, font=("Arial", 16))

    def show_loading(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.loading_label = ctk.CTkLabel(self.scroll_frame, text="Scanning Network", text_color=config.ACCENT_BLUE, font=("Arial", 16))
        self.loading_label.pack(pady=100)

    def populate_devices(self, devices_list):
        self.loading_label.destroy()
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not devices_list:
            ctk.CTkLabel(self.scroll_frame, text="No Devices on Network", text_color=config.TEXT_MUTED).pack(pady=50)
            return

        col_count = 3
        for index, device in enumerate(devices_list):
            row = index // col_count
            col = index % col_count

            card = ctk.CTkFrame(self.scroll_frame, width=200, height=120, corner_radius=8, fg_color=config.CARD_BG)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=device.get("device_name", "UNKNOWN"), font=("Arial", 14, "bold"), text_color=config.TEXT_MAIN).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=device.get("ip_address", "0.0.0.0"), text_color=config.ACCENT_BLUE).pack()
            ctk.CTkLabel(card, text=device.get("mac_address", "00:00:00:00:00:00"), text_color=config.ACCENT_BLUE).pack()
