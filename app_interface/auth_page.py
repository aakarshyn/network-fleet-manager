import customtkinter as ctk
import config

class AuthPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=config.BG_DARK)
        self.controller = controller

        self.card = ctk.CTkFrame(self, width=380, height=420, corner_radius=16, fg_color=config.CARD_BG)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        self.icon_label = ctk.CTkLabel(self.card, text="🔐", font=("Arial", 48))
        self.icon_label.pack(pady=(30, 10))

        self.header = ctk.CTkLabel(self.card, text="CONSOLE LOGIN", font=("Arial", 18, "bold"), text_color=config.TEXT_MAIN)
        self.header.pack(pady=(0, 20))

        self.username = ctk.CTkEntry(self.card, width=280, placeholder_text="Username", fg_color=config.BG_DARK, text_color=config.TEXT_MAIN, border_color=config.TEXT_MUTED)
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self.card, width=280, placeholder_text="Password", show="*", fg_color=config.BG_DARK, text_color=config.TEXT_MAIN, border_color=config.TEXT_MUTED)
        self.password.pack(pady=10)

        self.error_label = ctk.CTkLabel(self.card, text="", text_color=config.ACCENT_PINK, font=("Arial", 12))
        self.error_label.pack(pady=5)

        self.login_btn = ctk.CTkButton(self.card, text="LOGIN", width=280, fg_color=config.ACCENT_BLUE, text_color=config.BG_DARK, font=("Arial", 14, "bold"), command=self.authenticate)
        self.login_btn.pack(pady=20)

    def authenticate(self):
        if self.username.get() == config.AUTH_USER and self.password.get() == config.AUTH_PASS:
            self.error_label.configure(text="")
            self.controller.show_frame("LandingPage")
        else:
            self.error_label.configure(text="❌ INVALID CREDENTIALS")
