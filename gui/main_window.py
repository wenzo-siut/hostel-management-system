import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import json

from database import DatabaseManager, DatabaseConnectionError, MYSQL_AVAILABLE
from gui.theme import (
    setup_treeview_style, COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_SIDEBAR,
    COLOR_BOOTSTRAP_SIDEBAR_ACTIVE, COLOR_BOOTSTRAP_BORDER, COLOR_BOOTSTRAP_TEXT_WHITE, COLOR_BOOTSTRAP_TEXT_MUTED,
    COLOR_BOOTSTRAP_PRIMARY, COLOR_BOOTSTRAP_PRIMARY_HOVER, FONT_FAMILY, FONT_TITLE_SIZE,
    FONT_SUBTITLE_SIZE, FONT_BODY_SIZE, COLOR_BOOTSTRAP_TEXT_DARK
)

class DatabaseConfigDialog(ctk.CTkToplevel):
    """Modern CustomTkinter database setup dialog supporting MySQL or local SQLite testing configurations."""
    def __init__(self, parent, db_manager, on_success_callback):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.on_success = on_success_callback
        
        self.title("HMS - Database Configuration")
        self.geometry("460x650")
        self.resizable(True, True)
        
        # Style setup
        self.configure(fg_color=COLOR_BOOTSTRAP_BG)
        
        # Modal configuration
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.load_current_values()

    def create_widgets(self):
        # Header banner frame
        header = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_SIDEBAR, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            header, 
            text="Database Setup Center", 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold")
        )
        lbl_title.pack(pady=22, padx=25, anchor="w")
        
        # Main form panel
        form = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_CARD, corner_radius=12, border_color=COLOR_BOOTSTRAP_BORDER, border_width=1)
        form.pack(fill="both", expand=True, padx=25, pady=20)
        
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        
        # Row 0: Engine Choice
        lbl_engine = ctk.CTkLabel(form, text="Connection Engine:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        lbl_engine.grid(row=0, column=0, sticky="w", padx=20, pady=8)
        
        self.var_engine = tk.StringVar(value="sqlite")
        self.cmb_engine = ctk.CTkComboBox(
            form, 
            values=["sqlite", "mysql"], 
            variable=self.var_engine, 
            command=self.toggle_fields,
            width=180,
            font=(FONT_FAMILY, FONT_BODY_SIZE)
        )
        self.cmb_engine.grid(row=0, column=1, sticky="e", padx=20, pady=8)
        
        # Row 1: Host
        self.lbl_host = ctk.CTkLabel(form, text="MySQL Host Name:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_host.grid(row=1, column=0, sticky="w", padx=20, pady=8)
        self.ent_host = ctk.CTkEntry(form, width=180, font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_host.grid(row=1, column=1, sticky="e", padx=20, pady=8)
        
        # Row 2: Port
        self.lbl_port = ctk.CTkLabel(form, text="MySQL Port:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_port.grid(row=2, column=0, sticky="w", padx=20, pady=8)
        self.ent_port = ctk.CTkEntry(form, width=180, font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_port.grid(row=2, column=1, sticky="e", padx=20, pady=8)
        
        # Row 3: Username
        self.lbl_user = ctk.CTkLabel(form, text="Username:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_user.grid(row=3, column=0, sticky="w", padx=20, pady=8)
        self.ent_user = ctk.CTkEntry(form, width=180, font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_user.grid(row=3, column=1, sticky="e", padx=20, pady=8)
        
        # Row 4: Password
        self.lbl_pass = ctk.CTkLabel(form, text="Password:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_pass.grid(row=4, column=0, sticky="w", padx=20, pady=8)
        self.ent_pass = ctk.CTkEntry(form, width=180, show="*", font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_pass.grid(row=4, column=1, sticky="e", padx=20, pady=8)
        
        # Row 5: Database
        self.lbl_db = ctk.CTkLabel(form, text="Database Name:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_db.grid(row=5, column=0, sticky="w", padx=20, pady=8)
        self.ent_db = ctk.CTkEntry(form, width=180, font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_db.grid(row=5, column=1, sticky="e", padx=20, pady=8)
        
        # Row 6: SQLite File
        self.lbl_sqlite = ctk.CTkLabel(form, text="SQLite File Path:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"))
        self.lbl_sqlite.grid(row=6, column=0, sticky="w", padx=20, pady=8)
        self.ent_sqlite = ctk.CTkEntry(form, width=180, font=(FONT_FAMILY, FONT_BODY_SIZE))
        self.ent_sqlite.grid(row=6, column=1, sticky="e", padx=20, pady=8)
        
        # Row 7: Visual Warning Label
        self.lbl_warning = ctk.CTkLabel(
            form, 
            text="MySQL connectivity status audit.", 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED, 
            font=(FONT_FAMILY, 10, "italic"),
            wraplength=380,
            justify="center"
        )
        self.lbl_warning.grid(row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        
        # Row 8: Action Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=8, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 20))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        btn_test = ctk.CTkButton(
            btn_frame, 
            text="Test Connection", 
            fg_color="transparent", 
            border_color=COLOR_BOOTSTRAP_PRIMARY, 
            border_width=1, 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            hover_color=COLOR_BOOTSTRAP_BORDER,
            command=self.test_connection,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            height=36
        )
        btn_test.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        btn_save = ctk.CTkButton(
            btn_frame, 
            text="Save & Connect", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            command=self.save_and_connect,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            height=36
        )
        btn_save.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    def load_current_values(self):
        cfg = self.db_manager.config
        self.var_engine.set(cfg.get("db_type", "sqlite"))
        
        self.ent_host.insert(0, cfg.get("host", "localhost"))
        self.ent_port.insert(0, str(cfg.get("port", 3306)))
        self.ent_user.insert(0, cfg.get("user", "root"))
        self.ent_pass.insert(0, cfg.get("password", ""))
        self.ent_db.insert(0, cfg.get("database", "hostel_management"))
        self.ent_sqlite.insert(0, cfg.get("sqlite_path", "hostel_sandbox.db"))
        
        self.toggle_fields()

    def toggle_fields(self, choice=None):
        engine = self.var_engine.get()
        if engine == "mysql":
            self.ent_host.configure(state="normal")
            self.ent_port.configure(state="normal")
            self.ent_user.configure(state="normal")
            self.ent_pass.configure(state="normal")
            self.ent_db.configure(state="normal")
            self.ent_sqlite.configure(state="disabled")
            
            if not MYSQL_AVAILABLE:
                self.lbl_warning.configure(text="MySQL status: Missing driver! Run 'pip install pymysql' or toggle SQLite Sandbox to run instantly.", text_color="#f87171")
            else:
                self.lbl_warning.configure(text="MySQL driver status: Ready. Ready to test connection parameters.", text_color="#4ade80")
        else:
            self.ent_host.configure(state="disabled")
            self.ent_port.configure(state="disabled")
            self.ent_user.configure(state="disabled")
            self.ent_pass.configure(state="disabled")
            self.ent_db.configure(state="disabled")
            self.ent_sqlite.configure(state="normal")
            self.lbl_warning.configure(text="SQLite Sandbox active. Local file data stores with zero-configuration.", text_color="#60a5fa")

    def test_connection(self):
        temp_config = self.get_fields_as_config()
        test_mgr = DatabaseManager()
        test_mgr.config.update(temp_config)
        test_mgr.db_type = temp_config["db_type"]
        
        try:
            test_mgr.connect()
            test_mgr.initialize_schema()
            messagebox.showinfo("Success", f"Successfully connected to the {temp_config['db_type'].upper()} database!", parent=self)
            return True
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Unable to establish database connection:\n\n{e}", parent=self)
            return False

    def get_fields_as_config(self):
        return {
            "db_type": self.var_engine.get(),
            "host": self.ent_host.get().strip(),
            "port": int(self.ent_port.get().strip() or 3306),
            "user": self.ent_user.get().strip(),
            "password": self.ent_pass.get(),
            "database": self.ent_db.get().strip(),
            "sqlite_path": self.ent_sqlite.get().strip()
        }

    def save_and_connect(self):
        if self.test_connection():
            config = self.get_fields_as_config()
            self.db_manager.save_config(config)
            self.db_manager.connect()
            self.db_manager.initialize_schema()
            self.db_manager.insert_seed_data_if_empty()
            
            self.grab_release()
            self.destroy()
            self.on_success()


class MainWindow(ctk.CTk):
    """Central shell managing modern navigation bar, tab bindings, and system themes."""
    def __init__(self):
        super().__init__()
        self.title("Hostel Management System (HMS) - Enterprise Dashboard")
        self.geometry("1150x720")
        self.minsize(1000, 640)
        
        # Setup visual aesthetics
        self.configure(fg_color=COLOR_BOOTSTRAP_BG)
        setup_treeview_style()
        
        self.db = DatabaseManager()
        
        self.sidebar_frame = None
        self.content_frame = None
        self.active_button = None
        self.active_view = None
        self.nav_buttons = {}

        # Show administrative Sign-In view first
        self.login_view = None
        self.show_login_screen()

    def show_login_screen(self):
        """Builds a beautiful, full-screen sign-in screen matching Slide 1 design."""
        self.login_view = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.login_view.pack(fill="both", expand=True)

        # 2-Column Layout
        self.login_view.rowconfigure(0, weight=1)
        self.login_view.columnconfigure(0, weight=6) # Left Column: Sign-in Card
        self.login_view.columnconfigure(1, weight=4) # Right Column: Branding Panel

        # --- Left Column: Sign-In Box ---
        left_col = ctk.CTkFrame(self.login_view, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew")

        # Center card container
        card_outer = ctk.CTkFrame(left_col, fg_color="transparent")
        card_outer.place(relx=0.5, rely=0.5, anchor="center")

        lbl_signin_title = ctk.CTkLabel(
            card_outer,
            text="Administrative Sign In",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_signin_title.pack(anchor="w", pady=(0, 5))

        lbl_signin_sub = ctk.CTkLabel(
            card_outer,
            text="Provide security parameters to establish secure workstation connection.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_signin_sub.pack(anchor="w", pady=(0, 25))

        # Sign-in Card Form Box
        form_box = ctk.CTkFrame(
            card_outer,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            width=380,
            height=280
        )
        form_box.pack()
        form_box.pack_propagate(False)

        ctk.CTkLabel(
            form_box,
            text="Username / Student ID:",
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )  # Construct first, then place to avoid constructor pad error
        lbl_user = ctk.CTkLabel(form_box, text="Username / Student ID:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK)
        lbl_user.pack(anchor="w", padx=20, pady=(20, 2))

        self.ent_login_user = ctk.CTkEntry(form_box, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_login_user.pack(padx=20, pady=(0, 15))
        self.ent_login_user.insert(0, "admin_hms") # Default presentation placeholder

        lbl_pass = ctk.CTkLabel(form_box, text="System Access Key:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK)
        lbl_pass.pack(anchor="w", padx=20, pady=(0, 2))

        self.ent_login_pass = ctk.CTkEntry(form_box, font=(FONT_FAMILY, FONT_BODY_SIZE), show="*", width=340)
        self.ent_login_pass.pack(padx=20, pady=(0, 12))
        
        self.chk_remember = ctk.CTkCheckBox(
            form_box, 
            text="Remember session on this workstation", 
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            fg_color=COLOR_BOOTSTRAP_PRIMARY,
            checkbox_height=18,
            checkbox_width=18
        )
        self.chk_remember.pack(anchor="w", padx=20, pady=5)
        self.chk_remember.select()

        # Connect button
        btn_connect = ctk.CTkButton(
            card_outer,
            text="Establish Secure Connection",
            fg_color=COLOR_BOOTSTRAP_PRIMARY,
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.attempt_sign_in,
            height=40,
            width=380,
            corner_radius=8
        )
        btn_connect.pack(pady=20)

        # --- Right Column: Branding Panel ---
        right_col = ctk.CTkFrame(self.login_view, fg_color="#1a233a", corner_radius=0) # Slide 1 branding bg
        right_col.grid(row=0, column=1, sticky="nsew")

        # Sleek glowing dome/arch design on a Canvas
        brand_container = ctk.CTkFrame(right_col, fg_color="#1a233a")
        brand_container.place(relx=0.5, rely=0.5, anchor="center")

        dome_canvas = tk.Canvas(
            brand_container,
            bg="#1a233a",
            bd=0,
            highlightthickness=0,
            width=280,
            height=200
        )
        dome_canvas.pack(pady=(0, 20))

        # Draw beautiful glowing vector dome/arch
        dome_canvas.create_arc(40, 60, 240, 260, start=0, extent=180, outline="#3b82f6", width=3, style="arc")
        dome_canvas.create_arc(60, 80, 220, 240, start=0, extent=180, outline="#1d4ed8", width=1.5, style="arc")
        dome_canvas.create_arc(80, 100, 200, 220, start=0, extent=180, outline="#60a5fa", width=1, style="arc")
        # Grid lines inside the arch
        for angle in range(30, 180, 30):
            import math
            rad = math.radians(angle)
            x1 = 140 + 100 * math.cos(rad)
            y1 = 160 - 100 * math.sin(rad)
            x2 = 140 + 60 * math.cos(rad)
            y2 = 160 - 60 * math.sin(rad)
            dome_canvas.create_line(x1, y1, x2, y2, fill="#1e40af", width=1)
        dome_canvas.create_line(40, 160, 240, 160, fill="#3b82f6", width=2)

        lbl_brand_title = ctk.CTkLabel(
            brand_container,
            text="HMS Desktop Portal",
            font=(FONT_FAMILY, 22, "bold"),
            text_color="#ffffff"
        )
        lbl_brand_title.pack(anchor="center", pady=(0, 8))

        lbl_brand_desc = ctk.CTkLabel(
            brand_container,
            text="Securing campus accommodations, monitoring real-time occupancy, and processing student allocations seamlessly.",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE),
            text_color="#94a3b8",
            wraplength=280,
            justify="center"
        )
        lbl_brand_desc.pack(anchor="center")

    def attempt_sign_in(self):
        username = self.ent_login_user.get().strip()
        password = self.ent_login_pass.get()

        if username == "admin_hms" and password == "admin":
            # Credentials pass! Now connect to the database.
            self.check_database_and_start()
        else:
            messagebox.showerror("Access Denied", "Invalid administrative username or system access key credentials.", parent=self)

    def check_database_and_start(self):
        """Validates database connection, triggers config setup if failed, otherwise launches dashboard."""
        try:
            self.db.connect()
            self.db.initialize_schema()
            self.db.insert_seed_data_if_empty()
            self.on_success_signin()
        except DatabaseConnectionError:
            # Show configuration topLevel dialog
            DatabaseConfigDialog(self, self.db, self.on_database_configured)

    def on_database_configured(self):
        """Callback when database setup successfully completes."""
        self.on_success_signin()

    def on_success_signin(self):
        """Clear login screen and build HMS desktop layout shell."""
        if self.login_view:
            self.login_view.destroy()
            self.login_view = None
        self.build_layout()

    def build_layout(self):
        # Sidebar Frame Navigation Pane
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_SIDEBAR, width=230, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        # Dynamic Viewport Container
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.switch_view("dashboard")

    def build_sidebar(self):
        # Brand Logo Header with Blue Rounded 'H' Icon Badge (Slide 2 alignment)
        logo_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", height=80, corner_radius=0)
        logo_container.pack(fill="x", side="top")
        logo_container.pack_propagate(False)
        
        badge = ctk.CTkFrame(logo_container, fg_color=COLOR_BOOTSTRAP_PRIMARY, width=32, height=32, corner_radius=8)
        badge.pack(side="left", padx=(20, 10), pady=24)
        badge.pack_propagate(False)
        lbl_badge = ctk.CTkLabel(badge, text="H", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 16, "bold"))
        lbl_badge.pack(expand=True)
        
        lbl_logo = ctk.CTkLabel(
            logo_container, 
            text="H HMS Admin", 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold")
        )
        lbl_logo.pack(side="left", pady=24)
        
        # Navbar views
        menu_items = [
            ("dashboard", "Dashboard"),
            ("rooms", "Rooms"),
            ("residents", "Residents"),
            ("floor_engine", "Occupancy Map"),
            ("room_types", "Analytics"),
            ("settings", "Settings")
        ]
        
        btn_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        btn_container.pack(fill="both", expand=True)
        
        for view_key, label in menu_items:
            btn = ctk.CTkButton(
                btn_container, 
                text=label, 
                fg_color="transparent",
                text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
                hover_color=COLOR_BOOTSTRAP_SIDEBAR_ACTIVE,
                anchor="w",
                font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
                height=42,
                corner_radius=8,
                command=lambda vk=view_key: self.switch_view(vk)
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.nav_buttons[view_key] = btn

        # Admin Session details stacked in the footer (Slide 2 details)
        status_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent", height=80, corner_radius=0)
        status_container.pack(fill="x", side="bottom")
        status_container.pack_propagate(False)
        
        lbl_conn = ctk.CTkLabel(
            status_container, 
            text="Connection: Secure", 
            text_color="#4ade80", # Green text for secure status
            font=(FONT_FAMILY, 10, "bold")
        )
        lbl_conn.pack(pady=(10, 2), padx=20, anchor="w")

        lbl_version = ctk.CTkLabel(
            status_container, 
            text="Version v1.4.2 | Server: Live", 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            font=(FONT_FAMILY, 9, "normal")
        )
        lbl_version.pack(pady=(0, 10), padx=20, anchor="w")

    def on_reconfigured(self):
        for child in self.content_frame.winfo_children():
            child.destroy()
        # Clean sidebar
        for child in self.sidebar_frame.winfo_children():
            child.destroy()
        self.active_button = None
        self.active_view = None
        self.nav_buttons = {}
        self.build_sidebar()
        self.switch_view("dashboard")

    def switch_view(self, view_key):
        """Fires view changes, visually updating navbar tags and swapping viewport frames."""
        # Unselect previous menu tab
        if self.active_button:
            try:
                if self.active_button.winfo_exists():
                    self.active_button.configure(
                        fg_color="transparent", 
                        text_color=COLOR_BOOTSTRAP_TEXT_MUTED
                    )
            except Exception:
                pass
        
        btn = self.nav_buttons.get(view_key)
        if btn:
            try:
                if btn.winfo_exists():
                    btn.configure(
                        fg_color=COLOR_BOOTSTRAP_PRIMARY, 
                        text_color=COLOR_BOOTSTRAP_TEXT_WHITE
                    )
            except Exception:
                pass
            self.active_button = btn

        # Empty active viewport
        if self.active_view:
            try:
                if self.active_view.winfo_exists():
                    self.active_view.destroy()
            except Exception:
                pass

        # Compile and map target viewport class
        try:
            if view_key == "dashboard":
                from gui.views.dashboard import DashboardView
                self.active_view = DashboardView(self.content_frame, self.db)
            elif view_key == "room_types":
                from gui.views.room_types import RoomTypesView
                self.active_view = RoomTypesView(self.content_frame, self.db)
            elif view_key == "rooms":
                from gui.views.rooms import RoomsView
                self.active_view = RoomsView(self.content_frame, self.db)
            elif view_key == "residents":
                from gui.views.residents import ResidentsView
                self.active_view = ResidentsView(self.content_frame, self.db)
            elif view_key == "floor_engine":
                from gui.views.floor_engine import FloorEngineView
                self.active_view = FloorEngineView(self.content_frame, self.db)
            elif view_key == "settings":
                from gui.views.settings import SettingsView
                self.active_view = SettingsView(self.content_frame, self.db, self.on_reconfigured)
            
            self.active_view.pack(fill="both", expand=True)
        except Exception as e:
            err_frame = ctk.CTkFrame(self.content_frame, fg_color=COLOR_BOOTSTRAP_BG)
            err_frame.pack(fill="both", expand=True)
            ctk.CTkLabel(err_frame, text="View Loading Error", font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), text_color="#ef4444").pack(pady=40)
            ctk.CTkLabel(err_frame, text=f"Unable to load view '{view_key}':\n{e}", font=(FONT_FAMILY, FONT_BODY_SIZE), text_color=COLOR_BOOTSTRAP_TEXT_WHITE).pack(pady=10)
            print(f"Viewport Swapping Exception: {e}")
