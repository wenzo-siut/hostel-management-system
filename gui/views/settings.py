import customtkinter as ctk
import tkinter as tk
from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_PRIMARY_HOVER, COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY,
    FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE
)
from gui.main_window import DatabaseConfigDialog

class SettingsView(ctk.CTkFrame):
    """View rendering application configuration tools and database status updates."""
    def __init__(self, parent, db_manager, on_reconfigure_callback):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        self.on_reconfigured = on_reconfigure_callback
        
        self.pack_propagate(False)
        self.create_layout()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=15, padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Settings", 
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_breadcrumb.pack(side="left")
        
        profile_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        profile_frame.pack(side="right")
        
        lbl_profile = ctk.CTkLabel(
            profile_frame, 
            text="Registry Officer", 
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_profile.pack(side="left", padx=(0, 10))
        
        badge_circle = ctk.CTkFrame(profile_frame, fg_color=COLOR_BOOTSTRAP_PRIMARY, width=32, height=32, corner_radius=16)
        badge_circle.pack(side="right")
        badge_circle.pack_propagate(False)
        ctk.CTkLabel(badge_circle, text="RO", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)

        # Title block
        lbl_title = ctk.CTkLabel(
            header, 
            text="System Settings & Infrastructure", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Manage database connections, check API endpoints, and view details.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)

        # Settings main card
        card = ctk.CTkFrame(
            self, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        card.pack(fill="both", expand=True, padx=25, pady=(5, 20))
        
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        ctk.CTkLabel(
            card_content, 
            text="Database Configuration", 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        ).pack(anchor="w", pady=(0, 5))
        
        db_type = self.db.db_type.upper()
        details_txt = (
            f"The application is currently running in {db_type} mode.\n\n"
            f"MySQL Host: {self.db.config.get('host')}\n"
            f"MySQL Port: {self.db.config.get('port')}\n"
            f"Database Name: {self.db.config.get('database')}\n"
            f"SQLite Sandbox Path: {self.db.config.get('sqlite_path')}"
        )
        
        lbl_details = ctk.CTkLabel(
            card_content, 
            text=details_txt, 
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            justify="left",
            anchor="w"
        )
        lbl_details.pack(anchor="w", pady=(0, 25))
        
        btn_reconfig = ctk.CTkButton(
            card_content, 
            text="Launch Database Config Center", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.open_db_config,
            height=40,
            width=250
        )
        btn_reconfig.pack(anchor="w")

    def open_db_config(self):
        # Open database setup dialog
        parent_window = self.winfo_toplevel()
        DatabaseConfigDialog(parent_window, self.db, self.on_reconfigured)
