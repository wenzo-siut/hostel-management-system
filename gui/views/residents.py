import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_PRIMARY_HOVER, COLOR_BOOTSTRAP_DANGER, COLOR_BOOTSTRAP_DANGER_HOVER,
    COLOR_BOOTSTRAP_SUCCESS_BG, COLOR_BOOTSTRAP_SUCCESS_TEXT,
    COLOR_BOOTSTRAP_WARNING_BG, COLOR_BOOTSTRAP_WARNING_TEXT,
    COLOR_BOOTSTRAP_DANGER_BG, COLOR_BOOTSTRAP_DANGER_TEXT,
    COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY, FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE,
    COLOR_BOOTSTRAP_SIDEBAR
)

class ResidentOnboardingDialog(ctk.CTkToplevel):
    """Modern modal dialog to onboard a student resident with a two-column Slide 6 layout and green safety notice."""
    def __init__(self, parent, db_manager, on_success_callback):
        super().__init__(parent)
        self.db = db_manager
        self.on_success = on_success_callback
        self.rooms_cache = {}
        
        self.title("HMS - Onboard Student Resident")
        self.geometry("820x660")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BOOTSTRAP_BG)
        
        # Modal setup
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.refresh_rooms_dropdown()

    def create_widgets(self):
        # Header banner frame
        header = ctk.CTkFrame(self, fg_color=COLOR_BOOTSTRAP_SIDEBAR, height=80, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            header, 
            text="Student Onboarding Registry (Slide 6)", 
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold")
        )
        lbl_title.pack(pady=22, padx=25, anchor="w")
        
        # Main body container
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Two-Column Layout
        body_frame.columnconfigure(0, weight=4) # Left Column: Descriptions & Notice
        body_frame.columnconfigure(1, weight=6) # Right Column: Scrollable Onboarding Form
        
        # --- Left Column: Onboarding Info & Alert Notice ---
        left_col = ctk.CTkFrame(body_frame, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        lbl_left_title = ctk.CTkLabel(
            left_col,
            text="Onboarding Information",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_left_title.pack(anchor="w", pady=(5, 5))
        
        lbl_left_desc = ctk.CTkLabel(
            left_col,
            text="Assign a student resident to an active room unit and track their financial contracts. The tuition debt and deposits will compile inside the ledger database.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            wraplength=310,
            justify="left"
        )
        lbl_left_desc.pack(anchor="w", pady=(0, 20))
        
        # Dynamic Safety Notice Box (Slide 6 details - light green box)
        safety_box = ctk.CTkFrame(
            left_col,
            fg_color="#ecfdf5", # Light Green bg
            border_color="#10b981", # Green border
            border_width=1,
            corner_radius=8
        )
        safety_box.pack(fill="x", pady=10)
        
        lbl_safety_title = ctk.CTkLabel(
            safety_box,
            text="★ Dynamic Safety Notice",
            font=(FONT_FAMILY, 11, "bold"),
            text_color="#047857"
        )
        lbl_safety_title.pack(anchor="w", padx=15, pady=(10, 2))
        
        safety_text = (
            "Verify academic standing before allocation. Academic tuition arrears "
            "will flag the student record automatically inside the registry table.\n\n"
            "Outstanding debts above safety thresholds block access checks."
        )
        lbl_safety_body = ctk.CTkLabel(
            safety_box,
            text=safety_text,
            font=(FONT_FAMILY, 10),
            text_color="#065f46",
            justify="left",
            wraplength=270
        )
        lbl_safety_body.pack(anchor="w", padx=15, pady=(0, 10))
        
        # --- Right Column: Scrollable Form Container ---
        right_col = ctk.CTkScrollableFrame(
            body_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            scrollbar_button_color=COLOR_BOOTSTRAP_BG,
            scrollbar_button_hover_color=COLOR_BOOTSTRAP_BORDER
        )
        right_col.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        # --- Section 1: Personal Records ---
        lbl_sec1 = ctk.CTkLabel(
            right_col,
            text="1. PERSONAL RECORDS",
            font=(FONT_FAMILY, 10, "bold"),
            text_color=COLOR_BOOTSTRAP_PRIMARY
        )
        lbl_sec1.pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(right_col, text="Student ID Number:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_student_id = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. STU-2026-0012", width=340)
        self.ent_student_id.pack(padx=20, pady=(2, 8))
        
        ctk.CTkLabel(right_col, text="Resident Full Name:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_name = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. Alex Mercer", width=340)
        self.ent_name.pack(padx=20, pady=(2, 8))
        
        ctk.CTkLabel(right_col, text="Academic Major / Program:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_major = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), placeholder_text="e.g. Computer Science", width=340)
        self.ent_major.pack(padx=20, pady=(2, 8))
        
        ctk.CTkLabel(right_col, text="Assign Room Unit:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.cmb_room = ctk.CTkComboBox(right_col, state="readonly", command=self.on_room_selected, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.cmb_room.pack(padx=20, pady=(2, 8))
        
        ctk.CTkLabel(right_col, text="Check-In Date (YYYY-MM-DD):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_checkin = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_checkin.pack(padx=20, pady=(2, 8))
        self.ent_checkin.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ctk.CTkLabel(right_col, text="Check-Out Date (YYYY-MM-DD):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_checkout = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_checkout.pack(padx=20, pady=(2, 15))
        self.ent_checkout.insert(0, (datetime.now() + timedelta(days=150)).strftime("%Y-%m-%d"))
        
        # --- Section 2: Dynamic Room Assignment Allocation ---
        lbl_sec2 = ctk.CTkLabel(
            right_col,
            text="2. DYNAMIC ROOM ASSIGNMENT ALLOCATION",
            font=(FONT_FAMILY, 10, "bold"),
            text_color=COLOR_BOOTSTRAP_PRIMARY
        )
        lbl_sec2.pack(anchor="w", padx=20, pady=(10, 10))
        
        ctk.CTkLabel(right_col, text="Security Deposit Paid ($):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_deposit = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_deposit.pack(padx=20, pady=(2, 8))
        self.ent_deposit.insert(0, "200.00")
        
        ctk.CTkLabel(right_col, text="Hostel Tuition Fee ($):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_hostel_fee = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_hostel_fee.pack(padx=20, pady=(2, 8))
        self.ent_hostel_fee.insert(0, "0.00")
        
        ctk.CTkLabel(right_col, text="Academic Tuition Debt ($):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_debt = ctk.CTkEntry(right_col, font=(FONT_FAMILY, FONT_BODY_SIZE), width=340)
        self.ent_debt.pack(padx=20, pady=(2, 8))
        self.ent_debt.insert(0, "0.00")
        
        ctk.CTkLabel(right_col, text="Allocation Ledger Status:", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.cmb_status = ctk.CTkComboBox(
            right_col, 
            values=['Fully Registered', 'Probational Allocation', 'Outstanding Arrears'], 
            state="readonly",
            command=self.toggle_probation_field,
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            width=340
        )
        self.cmb_status.pack(padx=20, pady=(2, 8))
        self.cmb_status.set("Fully Registered")
        
        ctk.CTkLabel(right_col, text="Probation Approval Reason (If Applicable):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=20)
        self.ent_probation = ctk.CTkTextbox(
            right_col, 
            height=60, 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=8,
            width=340
        )
        self.ent_probation.pack(padx=20, pady=(2, 20))
        self.toggle_probation_field()
        
        btn_save = ctk.CTkButton(
            right_col, 
            text="Confirm Registration & Onboard", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.save_resident,
            height=38,
            width=340
        )
        btn_save.pack(padx=20, pady=(5, 20))

    def refresh_rooms_dropdown(self):
        try:
            records = self.db.get_rooms()
            options = []
            self.rooms_cache.clear()
            for r in records:
                label = f"Room {r['room_number']} ({r['type_name']} - {r['current_occupancy']}/{r['total_capacity']} Beds)"
                if r["current_occupancy"] < r["total_capacity"]:
                    options.append(label)
                    self.rooms_cache[label] = r
                else:
                    label_full = f"Room {r['room_number']} (FULL)"
                    options.append(label_full)
                    self.rooms_cache[label_full] = r
                    
            self.cmb_room.configure(values=options)
            if options:
                self.cmb_room.set(options[0])
                self.on_room_selected(options[0])
        except Exception as e:
            print(f"Error loading dropdown options: {e}")

    def on_room_selected(self, choice=None):
        selected = self.cmb_room.get()
        room = self.rooms_cache.get(selected)
        if room:
            base_price = float(room.get("semester_base_price", 0))
            self.ent_hostel_fee.delete(0, tk.END)
            self.ent_hostel_fee.insert(0, f"{base_price:.2f}")

    def toggle_probation_field(self, choice=None):
        status = self.cmb_status.get()
        if status == 'Probational Allocation':
            self.ent_probation.configure(state="normal", fg_color="#ffffff", text_color=COLOR_BOOTSTRAP_TEXT_DARK)
        else:
            self.ent_probation.delete("1.0", tk.END)
            self.ent_probation.configure(state="disabled", fg_color=COLOR_BOOTSTRAP_BG)

    def save_resident(self):
        student_id = self.ent_student_id.get().strip()
        name = self.ent_name.get().strip()
        major = self.ent_major.get().strip()
        room_sel = self.cmb_room.get()
        checkin = self.ent_checkin.get().strip()
        checkout = self.ent_checkout.get().strip()
        deposit_raw = self.ent_deposit.get().strip()
        fee_raw = self.ent_hostel_fee.get().strip()
        debt_raw = self.ent_debt.get().strip()
        status = self.cmb_status.get()
        probation = self.ent_probation.get("1.0", tk.END).strip()

        if not student_id or not name or not major or not checkin or not checkout:
            messagebox.showerror("Validation Error", "All basic personal details and dates must be completed.", parent=self)
            return

        room = self.rooms_cache.get(room_sel)
        if not room:
            messagebox.showerror("Validation Error", "Please select a valid room unit allocation.", parent=self)
            return

        if room["current_occupancy"] >= room["total_capacity"]:
            messagebox.showerror("Validation Error", "Target room is fully booked. Select another unit.", parent=self)
            return

        try:
            deposit = float(deposit_raw)
            fee = float(fee_raw)
            debt = float(debt_raw)
            if deposit < 0 or fee < 0 or debt < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Financial entries (Deposit, Fees, Debt) must be non-negative values.", parent=self)
            return

        try:
            datetime.strptime(checkin, "%Y-%m-%d")
            datetime.strptime(checkout, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Dates must match the format YYYY-MM-DD.", parent=self)
            return

        if status == 'Probational Allocation' and not probation:
            messagebox.showerror("Validation Error", "Probation Allocation requires a clear Approval Reason.", parent=self)
            return

        probation_val = probation if status == 'Probational Allocation' else None

        try:
            self.db.add_resident(
                room_id=room["room_id"],
                student_id=student_id,
                full_name=name,
                academic_major=major,
                check_in_date=checkin,
                check_out_date=checkout,
                deposit_paid=deposit,
                hostel_tuition_fee=fee,
                academic_tuition_debt=debt,
                allocation_status=status,
                probation_reason=probation_val
            )
            messagebox.showinfo("Success", f"Resident '{name}' has been successfully registered.", parent=self)
            self.on_success()
            self.grab_release()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Onboarding Failed", f"Database failed to process registration. Check that Student ID is unique!\n\n{e}", parent=self)


class ResidentsView(ctk.CTkFrame):
    """View managing student registrations, financial contracts, search directory, and dynamic text blocks."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        
        self.pack_propagate(False)
        self.create_layout()
        self.search_residents()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=(15, 5), padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Student Registry Directory", 
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
        # Residents view has initials RO
        ctk.CTkLabel(badge_circle, text="RO", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)
        
        # Title
        lbl_title = ctk.CTkLabel(
            header, 
            text="Student Stays Registry", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Search student directory, audit financial ledgers, and manage housing contracts.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)

        # Control Actions Frame (Search bar & Add Button)
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=25, pady=(10, 10))
        
        self.ent_search = ctk.CTkEntry(
            controls, 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            placeholder_text="🔍 Search student by ID, Name, Major or Room...",
            height=40,
            corner_radius=20,
            border_color=COLOR_BOOTSTRAP_BORDER,
            fg_color=COLOR_BOOTSTRAP_CARD
        )
        self.ent_search.pack(side="left", fill="x", expand=True, padx=(0, 20))
        self.ent_search.bind("<KeyRelease>", self.on_search_key)
        
        btn_add = ctk.CTkButton(
            controls, 
            text="+ Register Student", 
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
        cols = ("student_id", "name", "major", "room", "dates", "deposit", "debt", "status", "options")
        self.tree = ttk.Treeview(card_table, columns=cols, show="headings")
        
        self.tree.heading("student_id", text="Student ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("major", text="Academic Major")
        self.tree.heading("room", text="Assigned Block Room")
        self.tree.heading("dates", text="Check-In Date")
        self.tree.heading("deposit", text="Deposit")
        self.tree.heading("debt", text="Academic Debt")
        self.tree.heading("status", text="Status Badge")
        self.tree.heading("options", text="Options")
        
        self.tree.column("student_id", width=120, minwidth=100, anchor="center")
        self.tree.column("name", width=140, minwidth=120, anchor="w")
        self.tree.column("major", width=160, minwidth=140, anchor="w")
        self.tree.column("room", width=130, minwidth=110, anchor="center")
        self.tree.column("dates", width=110, minwidth=100, anchor="center")
        self.tree.column("deposit", width=90, minwidth=80, anchor="e")
        self.tree.column("debt", width=90, minwidth=80, anchor="e")
        self.tree.column("status", width=150, minwidth=130, anchor="center")
        self.tree.column("options", width=80, minwidth=60, anchor="center")
        
        # Bind option clicks
        self.tree.bind("<ButtonRelease-1>", self.on_table_click)
        
        # Color tags config for rows
        self.tree.tag_configure("Outstanding Arrears", background=COLOR_BOOTSTRAP_DANGER_BG, foreground=COLOR_BOOTSTRAP_DANGER_TEXT)
        self.tree.tag_configure("Probational Allocation", background=COLOR_BOOTSTRAP_WARNING_BG, foreground=COLOR_BOOTSTRAP_WARNING_TEXT)
        self.tree.tag_configure("Fully Registered", background=COLOR_BOOTSTRAP_CARD, foreground=COLOR_BOOTSTRAP_TEXT_DARK)
        
        vsb = ttk.Scrollbar(card_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(card_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y", pady=(10, 10))
        self.tree.pack(fill="both", expand=True, padx=(15, 0), pady=(10, 0))
        hsb.pack(fill="x", padx=(15, 15), pady=(0, 10))

    def open_registration_dialog(self):
        parent_window = self.winfo_toplevel()
        ResidentOnboardingDialog(parent_window, self.db, self.search_residents)

    def on_search_key(self, event):
        self.search_residents()

    def search_residents(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        term = self.ent_search.get().replace("🔍", "").strip()
        try:
            records = self.db.search_residents(term)
            for r in records:
                dates_str = f"{r['check_in_date']}"
                deposit_str = f"${float(r['deposit_paid']):,.2f}"
                debt_str = f"${float(r['academic_tuition_debt']):,.2f}"
                
                self.tree.insert("", "end", values=(
                    r["student_id"],
                    r["full_name"],
                    r["academic_major"],
                    f"{r['room_number']} ({r['type_name']})",
                    dates_str,
                    deposit_str,
                    debt_str,
                    r["allocation_status"],
                    "⋮"
                ), tags=(r["allocation_status"], r["resident_id"]))
        except Exception as e:
            print(f"Error searching directory: {e}")

    def on_table_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#9":
                item = self.tree.identify_row(event.y)
                self.show_options_menu(event, item)

    def show_options_menu(self, event, item):
        self.tree.selection_set(item)
        tags = self.tree.item(item, "tags")
        if not tags or len(tags) < 2:
            return
            
        resident_id = tags[1]
        values = self.tree.item(item, "values")
        student_id = values[0]
        student_name = values[1]
        current_checkout = ""
        
        try:
            res_rec = self.db.fetch_one("SELECT check_out_date FROM Residents WHERE resident_id = %s", (resident_id,))
            if res_rec:
                current_checkout = str(res_rec["check_out_date"])
        except Exception:
            pass

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label=f"Extend Stay for {student_name}", command=lambda: self.show_prolong_dialog(resident_id, student_name, current_checkout))
        menu.add_separator()
        menu.add_command(label=f"Check-Out / Remove {student_name}", command=lambda: self.checkout_resident(resident_id, student_id, student_name))
        
        menu.post(event.x_root, event.y_root)

    def checkout_resident(self, resident_id, student_id, student_name):
        confirm = messagebox.askyesno(
            "Confirm Check-Out", 
            f"Are you sure you want to trigger check-out for student resident {student_name} ({student_id})?\n\nThis will free up their bed allocation.",
            parent=self
        )
        if confirm:
            try:
                self.db.delete_resident(resident_id)
                messagebox.showinfo("Checked Out", f"Resident stays cleared for {student_name}.", parent=self)
                self.search_residents()
            except Exception as e:
                messagebox.showerror("Check-Out Failed", f"Database error during deletion:\n{e}", parent=self)

    def show_prolong_dialog(self, resident_id, name, current_checkout):
        if not current_checkout:
            current_checkout = datetime.now().strftime("%Y-%m-%d")
            
        dialog = ctk.CTkToplevel(self)
        dialog.title("Extend Stay Duration")
        dialog.geometry("380x240")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLOR_BOOTSTRAP_BG)
        dialog.transient(self)
        dialog.grab_set()

        hdr = ctk.CTkFrame(dialog, fg_color=COLOR_BOOTSTRAP_SIDEBAR, height=60, corner_radius=0)
        hdr.pack(fill="x", side="top")
        ctk.CTkLabel(hdr, text=f"Extend Stay: {name}", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold")).pack(pady=15, padx=20, anchor="w")

        body = ctk.CTkFrame(dialog, fg_color="transparent", padx=25, pady=15)
        body.pack(fill="both", expand=True)

        ctk.CTkLabel(body, text=f"Current stay End-Date: {current_checkout}", font=(FONT_FAMILY, FONT_BODY_SIZE), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(body, text="Enter New Check-Out Date (YYYY-MM-DD):", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w")

        try:
            curr_dt = datetime.strptime(current_checkout, "%Y-%m-%d")
        except ValueError:
            curr_dt = datetime.now()
            
        default_future = (curr_dt + timedelta(days=150)).strftime("%Y-%m-%d")
        
        ent_date = ctk.CTkEntry(body, font=(FONT_FAMILY, FONT_BODY_SIZE))
        ent_date.pack(fill="x", pady=(5, 15))
        ent_date.insert(0, default_future)

        def save_extension():
            new_date = ent_date.get().strip()
            try:
                new_dt = datetime.strptime(new_date, "%Y-%m-%d").date()
                if new_dt <= curr_dt.date():
                    messagebox.showerror("Validation Error", "The new stay end-date must fall after the current checked-out date limits.", parent=dialog)
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid date format. Please format as YYYY-MM-DD.", parent=dialog)
                return

            try:
                self.db.update_booking_time(resident_id, new_date)
                messagebox.showinfo("Success", f"Stay extended successfully to {new_date}.", parent=dialog)
                dialog.grab_release()
                dialog.destroy()
                self.search_residents()
            except Exception as e:
                messagebox.showerror("Database Write Error", f"Failed to prolong stay limit:\n{e}", parent=dialog)

        btn_save = ctk.CTkButton(
            body, 
            text="Confirm Extension & Update", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=save_extension,
            height=36
        )
        btn_save.pack(fill="x")
