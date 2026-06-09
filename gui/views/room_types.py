import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import json

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_PRIMARY_HOVER, COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY,
    FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE, COLOR_BOOTSTRAP_SIDEBAR
)

class LayoutCategoryDialog(ctk.CTkToplevel):
    """Modern modal dialog to create/register a new room layout category tier."""
    def __init__(self, parent, db_manager, on_success_callback):
        super().__init__(parent)
        self.db = db_manager
        self.on_success = on_success_callback
        
        self.title("HMS - Create Layout Tier")
        self.geometry("450x560")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BOOTSTRAP_BG)
        
        # Modal setup
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()

    def create_widgets(self):
        # Header banner frame
        header = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_SIDEBAR, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            header, 
            text="Create Layout Classification", 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold")
        )
        lbl_title.pack(pady=22, padx=25, anchor="w")
        
        # Form body scrollable frame
        form = ctk.CTkScrollableFrame(self, fg_color=COLOR_BOOTSTRAP_CARD, corner_radius=12, border_color=COLOR_BOOTSTRAP_BORDER, border_width=1)
        form.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Inputs
        ctk.CTkLabel(form, text="Category Class Name:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        self.ent_name = ctk.CTkEntry(form, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. Deluxe Single Suite")
        self.ent_name.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form, text="Semester Base Rate ($):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        self.ent_price = ctk.CTkEntry(form, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. 1500.00")
        self.ent_price.pack(fill="x", pady=(0, 15))
        
        # Inventory Checkbox list
        ctk.CTkLabel(form, text="Assigned Physical Assets:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        
        checklist_frame = ctk.CTkFrame(form, fg_color="transparent")
        checklist_frame.pack(fill="x", pady=(0, 15))
        
        self.assets_list = ["Air Conditioner", "Mini Fridge", "Study Desk", "Pillows", "Fan", "Shared Lockers", "Personal Safe"]
        self.assets_vars = {}
        
        for item in self.assets_list:
            var = tk.BooleanVar()
            chk = ctk.CTkCheckBox(
                checklist_frame, 
                text=item, 
                variable=var, 
                font=(FONT_FAMILY, FONT_BODY_SIZE),
                text_color=COLOR_BOOTSTRAP_TEXT_DARK,
                fg_color=COLOR_BOOTSTRAP_PRIMARY,
                checkbox_height=20,
                checkbox_width=20
            )
            chk.pack(fill="x", pady=4)
            self.assets_vars[item] = var

        # Custom asset entry
        ctk.CTkLabel(form, text="Add Custom Asset:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(5, 2))
        self.ent_custom = ctk.CTkEntry(form, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. Microwave")
        self.ent_custom.pack(fill="x", pady=(0, 15))

        btn_save = ctk.CTkButton(
            form, 
            text="Save Classification Tier", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.save_category,
            height=38
        )
        btn_save.pack(fill="x", pady=(5, 10))

    def save_category(self):
        name = self.ent_name.get().strip()
        price_raw = self.ent_price.get().strip()
        custom_asset = self.ent_custom.get().strip()
        
        if not name or not price_raw:
            messagebox.showerror("Validation Error", "All fields are required. Please input Class Name and Base Price.", parent=self)
            return
            
        try:
            price = float(price_raw)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Semester Base Rate must be a valid positive number.", parent=self)
            return

        # Read checkboxes
        selected_assets = []
        for asset, var in self.assets_vars.items():
            if var.get():
                selected_assets.append(asset)
                
        if custom_asset:
            selected_assets.append(custom_asset)

        try:
            self.db.add_room_type(name, price, selected_assets)
            messagebox.showinfo("Success", f"Category layout '{name}' saved successfully.", parent=self)
            self.on_success()
            self.grab_release()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Write Error", f"Could not create room category record:\n{e}", parent=self)


class RoomTypesView(ctk.CTkFrame):
    """View acting as the parent Analytics container holding the Tabview for Reports, ER Schema, and Layout Categories."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        
        self.pack_propagate(False)
        self.create_layout()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=(15, 5), padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Analytics Center", 
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
        ctk.CTkLabel(badge_circle, text="SA", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)
        
        # Title
        lbl_title = ctk.CTkLabel(
            header, 
            text="Business Intelligence & Analytics Console", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Review system ledger updates, explore relational schematics, and assign inventory layout classes.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)

        # Tabview mapping
        self.tabview = ctk.CTkTabview(
            self,
            fg_color="transparent",
            segmented_button_fg_color=COLOR_BOOTSTRAP_BORDER,
            segmented_button_selected_color=COLOR_BOOTSTRAP_PRIMARY,
            segmented_button_selected_hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            segmented_button_unselected_hover_color=COLOR_BOOTSTRAP_BORDER,
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        self.tabview.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Add tabs
        self.tabview.add("Operational Reports")
        self.tabview.add("Database Schema")
        self.tabview.add("Layout Categories")

        # Load Reports View in Tab 1
        from gui.views.reports import ReportsView
        self.reports_tab = ReportsView(self.tabview.tab("Operational Reports"), self.db)
        self.reports_tab.pack(fill="both", expand=True)

        # Load Database Schema (ER Schema) in Tab 2
        from gui.views.er_schema import ErSchemaView
        self.schema_tab = ErSchemaView(self.tabview.tab("Database Schema"), self.db)
        self.schema_tab.pack(fill="both", expand=True)

        # Load Layout Categories in Tab 3
        self.setup_categories_tab()

    def setup_categories_tab(self):
        tab_frame = self.tabview.tab("Layout Categories")
        
        # Control Actions Frame inside Layout Categories tab
        controls = ctk.CTkFrame(tab_frame, fg_color="transparent")
        controls.pack(fill="x", pady=(10, 10))
        
        lbl_table_hdr = ctk.CTkLabel(
            controls, 
            text="Registered Category Configs", 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_table_hdr.pack(side="left")
        
        btn_add = ctk.CTkButton(
            controls, 
            text="+ Create Layout Tier", 
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
            tab_frame, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        card_table.pack(fill="both", expand=True, pady=(0, 10))
        
        # Grid Treeview Layout
        cols = ("id", "name", "price", "assets")
        self.tree = ttk.Treeview(card_table, columns=cols, show="headings")
        
        self.tree.heading("id", text="Type ID")
        self.tree.heading("name", text="Layout Tier Class Name")
        self.tree.heading("price", text="Base Rate / Semester")
        self.tree.heading("assets", text="Equipped Assets Inventory Checklist")
        
        self.tree.column("id", width=80, minwidth=60, anchor="center")
        self.tree.column("name", width=220, minwidth=180, anchor="w")
        self.tree.column("price", width=140, minwidth=110, anchor="e")
        self.tree.column("assets", width=350, minwidth=280, anchor="w")
        
        # Tree scrollbar pairing
        vsb = ttk.Scrollbar(card_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(card_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Map packing
        vsb.pack(side="right", fill="y", pady=(10, 10))
        self.tree.pack(fill="both", expand=True, padx=(15, 0), pady=(10, 0))
        hsb.pack(fill="x", padx=(15, 15), pady=(0, 10))

        # Initial data load
        self.refresh_list()

    def open_registration_dialog(self):
        parent_window = self.winfo_toplevel()
        LayoutCategoryDialog(parent_window, self.db, self.refresh_list)

    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        try:
            records = self.db.get_room_types()
            for r in records:
                assets_str = ", ".join(r.get("inventory_assets", []))
                price_val = f"${float(r['semester_base_price']):,.2f}"
                
                self.tree.insert("", "end", values=(
                    r["room_type_id"],
                    r["type_name"],
                    price_val,
                    assets_str or "None Selected"
                ))
        except Exception as e:
            print(f"Error loading categories list: {e}")
