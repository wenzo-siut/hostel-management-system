import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_PRIMARY_HOVER, COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY,
    FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE, COLOR_BOOTSTRAP_SIDEBAR
)

class RoomRegistrationDialog(ctk.CTkToplevel):
    """Modern modal dialog to register a new room unit with two-column Slide 4 layout and blue validation notice."""
    def __init__(self, parent, db_manager, on_success_callback):
        super().__init__(parent)
        self.db = db_manager
        self.on_success = on_success_callback
        self.room_types_cache = {}
        
        self.title("HMS - Register Room Unit")
        self.geometry("760x580")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BOOTSTRAP_BG)
        
        # Modal setup
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.refresh_room_types_dropdown()
 
    def create_widgets(self):
        # Header banner frame
        header = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_SIDEBAR, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            header, 
            text="Room Unit Onboarding & Registration (Slide 4)", 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold")
        )
        lbl_title.pack(pady=22, padx=25, anchor="w")
        
        # Main body container
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Two-Column Layout
        body_frame.rowconfigure(0, weight=1)
        body_frame.columnconfigure(0, weight=1) # Left Column: Descriptions & Notice
        body_frame.columnconfigure(1, weight=1) # Right Column: Form fields
        
        # --- Left Column: Info & Alert ---
        left_col = ctk.CTkFrame(body_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        lbl_left_title = ctk.CTkLabel(
            left_col,
            text="Inventory Registration",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_left_title.pack(anchor="w", pady=(5, 5))
        
        lbl_left_desc = ctk.CTkLabel(
            left_col,
            text="Ensure correct classification and total capacity. This allocates specific assets automatically based on selected Tier.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            wraplength=320,
            justify="left"
        )
        lbl_left_desc.pack(anchor="w", pady=(0, 20))
        
        # Dynamic Validation Alert Box (Slide 4 details - light blue alert box)
        alert_box = ctk.CTkFrame(
            left_col,
            fg_color="#eff6ff", # Light Blue bg
            border_color="#3b82f6", # Blue border
            border_width=1,
            corner_radius=8
        )
        alert_box.pack(fill="x", pady=10)
        
        lbl_alert_title = ctk.CTkLabel(
            alert_box,
            text="★ Dynamic Validation Alert",
            font=(FONT_FAMILY, 11, "bold"),
            text_color="#1d4ed8"
        )
        lbl_alert_title.pack(anchor="w", padx=15, pady=(10, 2))
        
        alert_text = (
            "Capacity values cannot exceed the class limit.\n"
            "Unique room identifiers ensure correct tracking inside the Floor Engine maps. "
            "Please review variables before committing changes."
        )
        lbl_alert_body = ctk.CTkLabel(
            alert_box,
            text=alert_text,
            font=(FONT_FAMILY, 10),
            text_color="#1e40af",
            justify="left",
            wraplength=280
        )
        lbl_alert_body.pack(anchor="w", padx=15, pady=(0, 10))
        
        # --- Right Column: Form Card ---
        right_col = ctk.CTkFrame(
            body_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12
        )
        right_col.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        # Form inputs inside right column
        ctk.CTkLabel(right_col, text="Room Identifier (Number):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(15, 2), padx=20)
        self.ent_number = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. 102", width=300)
        self.ent_number.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(right_col, text="Floor Assignment:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2), padx=20)
        self.cmb_floor = ctk.CTkComboBox(
            right_col, 
            values=["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5"], 
            state="readonly",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            width=300
        )
        self.cmb_floor.pack(pady=(0, 10), padx=20)
        self.cmb_floor.set("Floor 1")
        
        ctk.CTkLabel(right_col, text="Layout Tier Class:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2), padx=20)
        self.cmb_type = ctk.CTkComboBox(
            right_col, 
            state="readonly",
            command=self.on_type_selected,
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            width=300
        )
        self.cmb_type.pack(pady=(0, 10), padx=20)
        
        # Pricing feedback subframe
        self.price_frame = ctk.CTkFrame(right_col, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=8, border_color=COLOR_BOOTSTRAP_BORDER, border_width=1)
        self.price_frame.pack(fill="x", pady=(5, 10), padx=20)
        
        self.lbl_tier_price = ctk.CTkLabel(
            self.price_frame, 
            text="Semester Rate: $0.00", 
            font=(FONT_FAMILY, 10, "bold"), 
            text_color=COLOR_BOOTSTRAP_PRIMARY,
            anchor="w"
        )
        self.lbl_tier_price.pack(anchor="w", padx=12, pady=(6, 0))
        
        self.lbl_tier_assets = ctk.CTkLabel(
            self.price_frame, 
            text="Assets: No layout selected", 
            font=(FONT_FAMILY, 9, "italic"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            wraplength=260,
            justify="left",
            anchor="w"
        )
        self.lbl_tier_assets.pack(anchor="w", padx=12, pady=(2, 6))
        
        ctk.CTkLabel(right_col, text="Total Bed Capacity:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2), padx=20)
        self.cmb_capacity = ctk.CTkComboBox(
            right_col, 
            values=["1", "2", "4", "6", "8"], 
            state="readonly",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            width=300
        )
        self.cmb_capacity.pack(pady=(0, 15), padx=20)
        self.cmb_capacity.set("2")

        btn_save = ctk.CTkButton(
            right_col, 
            text="Register Room Unit", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.save_room,
            height=38,
            width=300
        )
        btn_save.pack(pady=(5, 15), padx=20)

    def refresh_room_types_dropdown(self):
        try:
            records = self.db.get_room_types()
            names = []
            self.room_types_cache.clear()
            for r in records:
                names.append(r["type_name"])
                self.room_types_cache[r["type_name"]] = r
                
            self.cmb_type.configure(values=names)
            if names:
                self.cmb_type.set(names[0])
                self.on_type_selected(names[0])
        except Exception as e:
            print(f"Error loading dropdown options: {e}")

    def on_type_selected(self, choice=None):
        selected = self.cmb_type.get()
        r_type = self.room_types_cache.get(selected)
        if r_type:
            price = float(r_type.get("semester_base_price", 0))
            assets = r_type.get("inventory_assets", [])
            self.lbl_tier_price.configure(text=f"Semester Rate: ${price:,.2f}")
            self.lbl_tier_assets.configure(text=f"Assets: {', '.join(assets) or 'None'}")

    def save_room(self):
        number = self.ent_number.get().strip()
        floor = self.cmb_floor.get()
        type_name = self.cmb_type.get()
        capacity_raw = self.cmb_capacity.get()
        
        if not number:
            messagebox.showerror("Validation Error", "Room Identifier Number is required.", parent=self)
            return

        try:
            capacity = int(capacity_raw)
            if capacity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Total capacity must be a positive integer.", parent=self)
            return

        r_type = self.room_types_cache.get(type_name)
        if not r_type:
            messagebox.showerror("Validation Error", "Please register a valid layout class tier first.", parent=self)
            return
            
        type_id = r_type["room_type_id"]

        try:
            self.db.add_room(type_id, number, floor, capacity)
            messagebox.showinfo("Success", f"Dorm Room unit '{number}' successfully created.", parent=self)
            self.on_success()
            self.grab_release()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Write Error", f"Failed to register room record. Verify that Room Number is unique!\n\n{e}", parent=self)


class RoomsView(ctk.CTkFrame):
    """View managing physical room unit registrations, capacity configurations, and layout details."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        
        self.pack_propagate(False)
        self.create_layout()
        self.refresh_rooms_list()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=(15, 5), padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Room Management", 
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
        # Rooms view is "RM" (Room Manager) initials per Slide 2
        ctk.CTkLabel(badge_circle, text="RM", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)
        
        # Title
        lbl_title = ctk.CTkLabel(
            header, 
            text="Room Unit Allocation & Management", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Register individual physical dorm units and map layout classifications.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)

        # Control Actions Frame
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=25, pady=(10, 10))
        
        lbl_table_hdr = ctk.CTkLabel(
            controls, 
            text="Room Inventory Directory", 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_table_hdr.pack(side="left")
        
        btn_add = ctk.CTkButton(
            controls, 
            text="+ Register Room", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.open_registration_dialog,
            height=40,
            corner_radius=20,
            width=180
        )
        btn_add.pack(side="right")

        # Table Listing Card Container
        card_table = ctk.CTkFrame(
            self, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        card_table.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        # Grid Treeview
        cols = ("id", "number", "type", "floor", "occupancy", "status", "assets")
        self.tree = ttk.Treeview(card_table, columns=cols, show="headings")
        
        self.tree.heading("id", text="Room ID")
        self.tree.heading("number", text="Room #")
        self.tree.heading("type", text="Layout Class")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("occupancy", text="Beds Occupied")
        self.tree.heading("status", text="Status Flag")
        self.tree.heading("assets", text="Equipped Assets Checklist")
        
        self.tree.column("id", width=80, minwidth=60, anchor="center")
        self.tree.column("number", width=90, minwidth=80, anchor="center")
        self.tree.column("type", width=160, minwidth=130, anchor="w")
        self.tree.column("floor", width=110, minwidth=90, anchor="center")
        self.tree.column("occupancy", width=120, minwidth=100, anchor="center")
        self.tree.column("status", width=130, minwidth=110, anchor="center")
        self.tree.column("assets", width=220, minwidth=180, anchor="w")
        
        vsb = ttk.Scrollbar(card_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(card_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y", pady=(10, 10))
        self.tree.pack(fill="both", expand=True, padx=(15, 0), pady=(10, 0))
        hsb.pack(fill="x", padx=(15, 15), pady=(0, 10))

    def open_registration_dialog(self):
        parent_window = self.winfo_toplevel()
        RoomRegistrationDialog(parent_window, self.db, self.refresh_rooms_list)

    def refresh_rooms_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        try:
            records = self.db.get_rooms()
            for r in records:
                occ_str = f"{r['current_occupancy']} / {r['total_capacity']}"
                assets_str = ", ".join(r.get("inventory_assets", []))
                
                self.tree.insert("", "end", values=(
                    r["room_id"],
                    r["room_number"],
                    r["type_name"],
                    r["floor_assignment"],
                    occ_str,
                    r["room_status"],
                    assets_str or "None"
                ))
        except Exception as e:
            print(f"Error loading rooms list: {e}")
