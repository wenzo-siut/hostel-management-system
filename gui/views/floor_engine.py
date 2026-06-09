import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_PRIMARY_HOVER, COLOR_BOOTSTRAP_SUCCESS, COLOR_BOOTSTRAP_SUCCESS_HOVER,
    COLOR_BOOTSTRAP_WARNING, COLOR_BOOTSTRAP_WARNING_HOVER, COLOR_BOOTSTRAP_DANGER,
    COLOR_BOOTSTRAP_DANGER_HOVER, COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY,
    FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE, COLOR_BOOTSTRAP_SIDEBAR
)

class FloorEngineView(ctk.CTkFrame):
    """View rendering Slide 7 visual floor tab maps, card grids with status top borders, and stay auditing tools."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        self.selected_room = None
        self.room_cards = {}
        
        self.pack_propagate(False)
        self.create_layout()
        self.load_floor_map()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=(15, 5), padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Occupancy Map Explorer", 
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
        # Floor Map view initials is FS (Floor Specialist) per Slide 2
        ctk.CTkLabel(badge_circle, text="FS", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)
        
        # Title
        lbl_title = ctk.CTkLabel(
            header, 
            text="Reactive Floor Engine Map & Stay Auditing", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Visual floor map explorer, batch stay audits, automated check-outs, and booking extensions (Slide 7).", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)

        # Operational Panel (Top Automation Actions)
        action_bar = ctk.CTkFrame(
            self, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        action_bar.pack(fill="x", padx=25, pady=(5, 10))
        
        lbl_desc = ctk.CTkLabel(
            action_bar, 
            text="★ Automated Cron Hook: Scan stay contracts and clear expired occupancy allocations instantly.", 
            font=(FONT_FAMILY, 11, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_desc.pack(side="left", padx=20, pady=12)
        
        btn_audit = ctk.CTkButton(
            action_bar, 
            text="Execute Batch Stay Audit", 
            fg_color=COLOR_BOOTSTRAP_PRIMARY, 
            hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            text_color=COLOR_BOOTSTRAP_TEXT_WHITE,
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.run_stay_audit,
            height=36,
            corner_radius=18
        )
        btn_audit.pack(side="right", padx=20, pady=12)

        # Two-Section Workspace Split
        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        # Left Workspace: Floor Map Grid
        left_panel = ctk.CTkFrame(workspace, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        card_grid_container = ctk.CTkFrame(
            left_panel, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        card_grid_container.pack(fill="both", expand=True)
        
        lbl_grid_hdr = ctk.CTkLabel(
            card_grid_container, 
            text="Physical Room Allocations", 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_grid_hdr.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Legend (Vacant & Ready, Partial Occupancy, Fully Occupied)
        legend = ctk.CTkFrame(card_grid_container, fg_color="transparent")
        legend.pack(fill="x", padx=20, pady=(0, 10))
        self.create_legend_item(legend, "Vacant & Ready", COLOR_BOOTSTRAP_SUCCESS).pack(side="left", padx=(0, 15))
        self.create_legend_item(legend, "Partial Occupancy", COLOR_BOOTSTRAP_WARNING).pack(side="left", padx=(0, 15))
        self.create_legend_item(legend, "Fully Occupied", COLOR_BOOTSTRAP_DANGER).pack(side="left")

        # Floor Tabview matching Ground, 1st, 2nd floors (Slide 7)
        self.tabview = ctk.CTkTabview(
            card_grid_container,
            fg_color="transparent",
            segmented_button_fg_color=COLOR_BOOTSTRAP_BORDER,
            segmented_button_selected_color=COLOR_BOOTSTRAP_PRIMARY,
            segmented_button_selected_hover_color=COLOR_BOOTSTRAP_PRIMARY_HOVER,
            segmented_button_unselected_hover_color=COLOR_BOOTSTRAP_BORDER,
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.tabview.add("Ground Floor (A)")
        self.tabview.add("1st Floor (B)")
        self.tabview.add("2nd Floor (C)")

        # Scrollable frames inside tabs
        self.scroll_ground = ctk.CTkScrollableFrame(self.tabview.tab("Ground Floor (A)"), fg_color="transparent")
        self.scroll_ground.pack(fill="both", expand=True)
        
        self.scroll_1st = ctk.CTkScrollableFrame(self.tabview.tab("1st Floor (B)"), fg_color="transparent")
        self.scroll_1st.pack(fill="both", expand=True)
        
        self.scroll_2nd = ctk.CTkScrollableFrame(self.tabview.tab("2nd Floor (C)"), fg_color="transparent")
        self.scroll_2nd.pack(fill="both", expand=True)

        # Right Workspace: Detail Inspector Panel
        self.right_panel = ctk.CTkFrame(workspace, fg_color="transparent", width=340)
        self.right_panel.pack(side="right", fill="y")
        self.right_panel.pack_propagate(False)
        
        self.card_details = ctk.CTkFrame(
            self.right_panel, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        self.card_details.pack(fill="both", expand=True)
        
        self.lbl_details_hdr = ctk.CTkLabel(
            self.card_details, 
            text="Inspection Details", 
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        self.lbl_details_hdr.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Detail body fields
        self.detail_body = ctk.CTkFrame(self.card_details, fg_color="transparent")
        self.detail_body.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.lbl_empty_state = ctk.CTkLabel(
            self.detail_body, 
            text="Select a room card in the physical map to inspect allocations, review residents, or extend contract stay limits.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            wraplength=280, 
            justify="left"
        )
        self.lbl_empty_state.pack(pady=40)

    def create_legend_item(self, parent, text, color):
        item = ctk.CTkFrame(parent, fg_color="transparent")
        box = ctk.CTkFrame(item, fg_color=color, width=15, height=15, corner_radius=3)
        box.pack(side="left", padx=(0, 6))
        lbl = ctk.CTkLabel(item, text=text, font=(FONT_FAMILY, FONT_BODY_SIZE), text_color=COLOR_BOOTSTRAP_TEXT_MUTED)
        lbl.pack(side="left")
        return item

    def load_floor_map(self):
        """Loads rooms and groups them under the mapped Ground, 1st, and 2nd Floor tab grids."""
        # Clear previous widgets
        for tab_scroll in [self.scroll_ground, self.scroll_1st, self.scroll_2nd]:
            for child in tab_scroll.winfo_children():
                child.destroy()
        self.room_cards.clear()
        
        try:
            rooms = self.db.get_rooms()
            
            # Grouping dictionary mapping rooms to scroll containers
            ground_rooms = []
            first_rooms = []
            second_rooms = []
            other_rooms = []

            for r in rooms:
                fl = r.get("floor_assignment", "").lower()
                if "1" in fl or "ground" in fl:
                    ground_rooms.append(r)
                elif "2" in fl or "1st" in fl or "first" in fl:
                    first_rooms.append(r)
                elif "3" in fl or "2nd" in fl or "second" in fl:
                    second_rooms.append(r)
                else:
                    other_rooms.append(r) # Fallback to ground if undefined

            # Render grids
            self.render_room_grid(self.scroll_ground, ground_rooms)
            self.render_room_grid(self.scroll_1st, first_rooms)
            self.render_room_grid(self.scroll_2nd, second_rooms)
        except Exception as e:
            print(f"Error drawing floor map: {e}")

    def render_room_grid(self, parent_scroll, rooms_list):
        if not rooms_list:
            lbl_empty = ctk.CTkLabel(
                parent_scroll,
                text="No room units registered on this floor.",
                font=(FONT_FAMILY, FONT_BODY_SIZE),
                text_color=COLOR_BOOTSTRAP_TEXT_MUTED
            )
            lbl_empty.pack(pady=20)
            return

        # Build grid tiles layout (3 columns)
        grid_frame = ctk.CTkFrame(parent_scroll, fg_color="transparent")
        grid_frame.pack(fill="x", anchor="nw")
        grid_frame.columnconfigure((0, 1, 2), weight=1)

        for idx, r in enumerate(rooms_list):
            row_idx = idx // 3
            col_idx = idx % 3

            status = r["room_status"]
            if status == "Vacant & Ready":
                status_color = COLOR_BOOTSTRAP_SUCCESS
            elif status == "Partial Occupancy":
                status_color = COLOR_BOOTSTRAP_WARNING
            else:
                status_color = COLOR_BOOTSTRAP_DANGER

            # Create visual card box frame (Slide 7 cards)
            card = ctk.CTkFrame(
                grid_frame,
                fg_color=COLOR_BOOTSTRAP_CARD,
                border_color=COLOR_BOOTSTRAP_BORDER,
                border_width=1,
                corner_radius=10,
                height=120
            )
            card.grid(row=row_idx, column=col_idx, padx=6, pady=6, sticky="ew")
            card.pack_propagate(False)

            # Top colored border line representing status
            top_border = ctk.CTkFrame(card, fg_color=status_color, height=4, corner_radius=0)
            top_border.pack(fill="x", side="top")

            # Room number label
            lbl_num = ctk.CTkLabel(
                card,
                text=f"Room {r['room_number']}",
                font=(FONT_FAMILY, FONT_BODY_SIZE + 1, "bold"),
                text_color=COLOR_BOOTSTRAP_TEXT_DARK
            )
            lbl_num.pack(anchor="w", padx=12, pady=(10, 2))

            # Status dot & text block
            status_block = ctk.CTkFrame(card, fg_color="transparent")
            status_block.pack(anchor="w", padx=12, pady=2)
            
            dot = ctk.CTkFrame(status_block, fg_color=status_color, width=8, height=8, corner_radius=4)
            dot.pack(side="left", padx=(0, 6))
            
            lbl_status = ctk.CTkLabel(
                status_block,
                text=status,
                font=(FONT_FAMILY, 9, "bold"),
                text_color=COLOR_BOOTSTRAP_TEXT_MUTED
            )
            lbl_status.pack(side="left")

            # Bed count
            lbl_beds = ctk.CTkLabel(
                card,
                text=f"Allocated: {r['current_occupancy']} / {r['total_capacity']} Beds",
                font=(FONT_FAMILY, 10),
                text_color=COLOR_BOOTSTRAP_TEXT_MUTED
            )
            lbl_beds.pack(anchor="w", padx=12, pady=(2, 10))

            # Bind mouse clicks on card elements to load inspection details
            # Create a transparent button covering the card for easy select
            btn_cover = ctk.CTkButton(
                card,
                text="",
                fg_color="transparent",
                hover_color="#f1f5f9",
                command=lambda room=r: self.inspect_room(room)
            )
            btn_cover.place(relx=0, rely=0.05, relwidth=1, relheight=0.95)

            self.room_cards[r["room_id"]] = card

    def inspect_room(self, room):
        self.selected_room = room
        
        # Reset detail canvas
        for child in self.detail_body.winfo_children():
            child.destroy()
            
        self.lbl_details_hdr.configure(text=f"Inspection: Room {room['room_number']}")
        
        # Show specifications card
        spec_box = ctk.CTkFrame(
            self.detail_body, 
            fg_color=COLOR_BOOTSTRAP_BG, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=8
        )
        spec_box.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(spec_box, text=f"Layout Class: {room['type_name']}", font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=12, pady=(12, 2))
        ctk.CTkLabel(spec_box, text=f"Floor Level: {room['floor_assignment']}", font=(FONT_FAMILY, 10), text_color=COLOR_BOOTSTRAP_TEXT_MUTED).pack(anchor="w", pady=2, padx=12)
        
        price_val = f"${float(room.get('semester_base_price', 0)):,.2f}"
        ctk.CTkLabel(spec_box, text=f"Semester Rate: {price_val}", font=(FONT_FAMILY, 10), text_color=COLOR_BOOTSTRAP_TEXT_MUTED).pack(anchor="w", padx=12, pady=(0, 12))

        # Load active occupants
        ctk.CTkLabel(
            self.detail_body, 
            text="ACTIVE BED OCCUPANTS:", 
            font=(FONT_FAMILY, 10, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        ).pack(anchor="w", pady=(0, 5))
        
        try:
            residents = self.db.fetch_all("SELECT * FROM Residents WHERE room_id = %s", (room["room_id"],))
            if not residents:
                ctk.CTkLabel(
                    self.detail_body, 
                    text="No student residents currently allocated to this room unit.", 
                    font=(FONT_FAMILY, FONT_BODY_SIZE), 
                    text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
                    wraplength=280, 
                    justify="left"
                ).pack(pady=15)
            else:
                for idx, res in enumerate(residents):
                    res_card = ctk.CTkFrame(
                        self.detail_body, 
                        fg_color=COLOR_BOOTSTRAP_BG, 
                        border_color=COLOR_BOOTSTRAP_BORDER, 
                        border_width=1,
                        corner_radius=8
                    )
                    res_card.pack(fill="x", pady=6)
                    
                    is_expired = datetime.strptime(res["check_out_date"], "%Y-%m-%d").date() <= datetime.now().date()
                    date_fg = COLOR_BOOTSTRAP_DANGER if is_expired else COLOR_BOOTSTRAP_TEXT_MUTED
                    
                    ctk.CTkLabel(res_card, text=res["full_name"], font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), text_color=COLOR_BOOTSTRAP_TEXT_DARK).pack(anchor="w", padx=12, pady=(10, 0))
                    ctk.CTkLabel(res_card, text=f"ID: {res['student_id']} | Major: {res['academic_major']}", font=(FONT_FAMILY, 10), text_color=COLOR_BOOTSTRAP_TEXT_MUTED).pack(anchor="w", padx=12)
                    
                    lbl_dates = ctk.CTkLabel(res_card, text=f"Checked: {res['check_in_date']} to {res['check_out_date']}", font=(FONT_FAMILY, 10), text_color=date_fg)
                    lbl_dates.pack(anchor="w", pady=(3, 5), padx=12)
                    
                    btn_prolong = ctk.CTkButton(
                        res_card, 
                        text="Prolong Booking Time", 
                        fg_color="transparent",
                        border_color=COLOR_BOOTSTRAP_BORDER,
                        border_width=1,
                        text_color=COLOR_BOOTSTRAP_TEXT_DARK,
                        hover_color=COLOR_BOOTSTRAP_CARD,
                        font=(FONT_FAMILY, 10, "bold"),
                        command=lambda r_id=res["resident_id"], name=res["full_name"], check_out=res["check_out_date"]: self.show_prolong_dialog(r_id, name, check_out),
                        height=28
                    )
                    btn_prolong.pack(fill="x", padx=12, pady=(0, 10))
        except Exception as e:
            print(f"Error loading occupants detail: {e}")

    def show_prolong_dialog(self, resident_id, name, current_checkout):
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

        curr_dt = datetime.strptime(current_checkout, "%Y-%m-%d")
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
                self.load_floor_map()
                if self.selected_room:
                    room_id = self.selected_room["room_id"]
                    refreshed_rooms = self.db.get_rooms()
                    for r in refreshed_rooms:
                        if r["room_id"] == room_id:
                            self.inspect_room(r)
                            break
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

    def run_stay_audit(self):
        try:
            checked_out, rooms_affected = self.db.run_automated_checkout()
            if checked_out > 0:
                msg = f"Auditing Complete!\n\n★ Reactive Hook Fired:\n- {checked_out} students automatically checked out.\n- {rooms_affected} physical room statuses updated back to vacant/partially booked limits."
                messagebox.showinfo("Automation Audit Complete", msg, parent=self)
                self.load_floor_map()
                if self.selected_room:
                    self.inspect_room(self.selected_room)
            else:
                messagebox.showinfo("Automation Audit Complete", "Auditing Complete!\n\nNo student resident booking allocations have reached expired check-out date targets today.", parent=self)
        except Exception as e:
            messagebox.showerror("Automation Failure", f"Failed to execute stay audit:\n{e}", parent=self)
