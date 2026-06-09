import tkinter as tk
import customtkinter as ctk

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY, FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE
)

class ErSchemaView(ctk.CTkFrame):
    """View rendering the database Entity-Relationship schema diagram using tk.Canvas."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        self.create_layout()

    def create_layout(self):
        # Header Info Banner
        info_banner = ctk.CTkFrame(
            self,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12
        )
        info_banner.pack(fill="x", padx=20, pady=(10, 10))

        lbl_banner_title = ctk.CTkLabel(
            info_banner,
            text="HMS Relational Schema & Integrity Model (Slide 8 Diagram)",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_banner_title.pack(anchor="w", padx=20, pady=(12, 2))

        lbl_banner_desc = ctk.CTkLabel(
            info_banner,
            text="Visual blueprint mapping the relational dependency between Room Inventories and Student Onboarding records.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_banner_desc.pack(anchor="w", padx=20, pady=(0, 12))

        # Main Diagram Area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left panel: The diagram Canvas
        diagram_container = ctk.CTkFrame(
            content_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12
        )
        diagram_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Canvas for drawing the ER diagram
        self.canvas = tk.Canvas(
            diagram_container,
            bg=COLOR_BOOTSTRAP_CARD,
            bd=0,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        self.canvas.bind("<Configure>", lambda event: self.draw_er_diagram())

        # Right panel: Integrity rules description card
        rules_container = ctk.CTkFrame(
            content_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            width=300
        )
        rules_container.pack(side="right", fill="both", padx=(10, 0))
        rules_container.pack_propagate(False)

        lbl_rules_title = ctk.CTkLabel(
            rules_container,
            text="Referential Integrity & Rules",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_rules_title.pack(anchor="w", padx=20, pady=(20, 10))

        rules_text = (
            "1. Primary Key Constraints:\n"
            "   • Rooms.room_id is the unique integer PK identifier.\n"
            "   • Residents.resident_id is the unique integer PK identifier.\n\n"
            "2. Foreign Key Constraint:\n"
            "   • Residents.room_id references Rooms.room_id.\n\n"
            "3. Referential Actions:\n"
            "   • ON DELETE RESTRICT: A room unit record cannot be deleted if any "
            "student residents are currently assigned to it.\n"
            "   • ON UPDATE CASCADE: Modifications to room identification keys "
            "will automatically propagate to residents.\n\n"
            "4. Domain Validation Checks:\n"
            "   • Check-In & Check-Out date formats must strictly validate (YYYY-MM-DD).\n"
            "   • Current occupancy must never exceed the room's total capacity."
        )

        lbl_rules = ctk.CTkLabel(
            rules_container,
            text=rules_text,
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            justify="left",
            wraplength=260
        )
        lbl_rules.pack(anchor="w", padx=20, pady=5)

    def draw_er_diagram(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 100 or height <= 100:
            return # Canvas not yet fully initialized/sized

        # Positions
        y_start = 40
        box_width = 240
        box_height_rooms = 200
        box_height_residents = 290

        x_rooms = 40
        x_residents = width - box_width - 40
        if x_residents < 320:
            x_residents = 320 # Prevent overlap

        # --- Draw Rooms Table ---
        # Header Box
        self.canvas.create_rectangle(
            x_rooms, y_start, x_rooms + box_width, y_start + 35,
            fill="#2563eb", outline="#2563eb", width=0
        )
        self.canvas.create_text(
            x_rooms + 12, y_start + 18,
            text="Rooms (TABLE_ROOMS)", fill="#ffffff",
            font=(FONT_FAMILY, 10, "bold"), anchor="w"
        )
        # Body Box
        self.canvas.create_rectangle(
            x_rooms, y_start + 35, x_rooms + box_width, y_start + box_height_rooms,
            fill="#f8fafc", outline="#cbd5e1", width=1
        )
        # Columns
        rooms_cols = [
            ("room_id", "INT AUTO_INC [PK]"),
            ("room_type_id", "INT [FK]"),
            ("room_number", "VARCHAR(50) [UQ]"),
            ("floor_assignment", "VARCHAR(50)"),
            ("total_capacity", "INT"),
            ("current_occupancy", "INT"),
            ("room_status", "VARCHAR(50)"),
        ]
        curr_y = y_start + 50
        for col_name, col_type in rooms_cols:
            is_pk = "[PK]" in col_type
            is_fk = "[FK]" in col_type
            font_w = "bold" if (is_pk or is_fk) else "normal"
            text_color = "#0f172a" if (is_pk or is_fk) else "#475569"

            # Column Name
            self.canvas.create_text(
                x_rooms + 15, curr_y,
                text=col_name, fill=text_color,
                font=(FONT_FAMILY, 9, font_w), anchor="w"
            )
            # Column Type
            self.canvas.create_text(
                x_rooms + box_width - 15, curr_y,
                text=col_type, fill="#94a3b8",
                font=(FONT_FAMILY, 8, "italic"), anchor="e"
            )
            curr_y += 20

        # --- Draw Residents Table ---
        # Header Box
        self.canvas.create_rectangle(
            x_residents, y_start, x_residents + box_width, y_start + 35,
            fill="#0f172a", outline="#0f172a", width=0
        )
        self.canvas.create_text(
            x_residents + 12, y_start + 18,
            text="Residents (TABLE_RESIDENTS)", fill="#ffffff",
            font=(FONT_FAMILY, 10, "bold"), anchor="w"
        )
        # Body Box
        self.canvas.create_rectangle(
            x_residents, y_start + 35, x_residents + box_width, y_start + box_height_residents,
            fill="#f8fafc", outline="#cbd5e1", width=1
        )
        # Columns
        res_cols = [
            ("resident_id", "INT AUTO_INC [PK]"),
            ("room_id", "INT [FK]"),
            ("student_id", "VARCHAR(100) [UQ]"),
            ("full_name", "VARCHAR(255)"),
            ("academic_major", "VARCHAR(255)"),
            ("check_in_date", "DATE"),
            ("check_out_date", "DATE"),
            ("deposit_paid", "DECIMAL(10,2)"),
            ("hostel_tuition_fee", "DECIMAL(10,2)"),
            ("academic_tuition_debt", "DECIMAL(10,2)"),
            ("allocation_status", "VARCHAR(100)"),
            ("probation_reason", "TEXT"),
        ]
        curr_y = y_start + 50
        for col_name, col_type in res_cols:
            is_pk = "[PK]" in col_type
            is_fk = "[FK]" in col_type
            font_w = "bold" if (is_pk or is_fk) else "normal"
            text_color = "#0f172a" if (is_pk or is_fk) else "#475569"

            # Column Name
            self.canvas.create_text(
                x_residents + 15, curr_y,
                text=col_name, fill=text_color,
                font=(FONT_FAMILY, 9, font_w), anchor="w"
            )
            # Column Type
            self.canvas.create_text(
                x_residents + box_width - 15, curr_y,
                text=col_type, fill="#94a3b8",
                font=(FONT_FAMILY, 8, "italic"), anchor="e"
            )
            curr_y += 20

        # --- Draw Relationship Link (1-to-N connector line) ---
        # Rooms side connection anchor: room_id column is the PK (y_start + 50)
        y_rooms_anchor = y_start + 50
        # Residents side connection anchor: room_id column is the FK (y_start + 70)
        y_residents_anchor = y_start + 70

        # Draw connecting line with routing points
        # Rooms right edge anchor
        x_rooms_edge = x_rooms + box_width
        # Residents left edge anchor
        x_residents_edge = x_residents

        # Control Points
        pt_mid_x = (x_rooms_edge + x_residents_edge) / 2

        # Draw line segment
        self.canvas.create_line(
            x_rooms_edge, y_rooms_anchor,
            pt_mid_x, y_rooms_anchor,
            pt_mid_x, y_residents_anchor,
            x_residents_edge, y_residents_anchor,
            fill="#2563eb", width=2
        )

        # 1-Side Indicator (Rooms side key/dot)
        self.canvas.create_oval(
            x_rooms_edge - 4, y_rooms_anchor - 4,
            x_rooms_edge + 4, y_rooms_anchor + 4,
            fill="#2563eb", outline="#2563eb"
        )
        self.canvas.create_text(
            x_rooms_edge + 10, y_rooms_anchor - 10,
            text="1 (PK)", fill="#2563eb",
            font=(FONT_FAMILY, 8, "bold")
        )

        # N-Side Indicator (Residents side crows foot / infinity notation)
        self.canvas.create_line(
            x_residents_edge, y_residents_anchor,
            x_residents_edge - 10, y_residents_anchor - 6,
            fill="#2563eb", width=2
        )
        self.canvas.create_line(
            x_residents_edge, y_residents_anchor,
            x_residents_edge - 10, y_residents_anchor + 6,
            fill="#2563eb", width=2
        )
        self.canvas.create_text(
            x_residents_edge - 18, y_residents_anchor - 12,
            text="N (FK)", fill="#2563eb",
            font=(FONT_FAMILY, 8, "bold")
        )
