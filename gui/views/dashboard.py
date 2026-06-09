import tkinter as tk
import customtkinter as ctk

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_SUCCESS, COLOR_BOOTSTRAP_WARNING, COLOR_BOOTSTRAP_DANGER,
    COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY, FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE
)

class DashboardView(ctk.CTkFrame):
    """View rendering operational stats, financial summaries, canvas-based charts, and inventory audits in CustomTkinter."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        
        self.pack_propagate(False)
        self.create_layout()
        self.refresh_data()

    def create_layout(self):
        # Header Section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", side="top", pady=(15, 5), padx=25)
        
        # Breadcrumbs & Profile Badge
        top_bar = ctk.CTkFrame(header, fg_color="transparent")
        top_bar.pack(fill="x")
        
        lbl_breadcrumb = ctk.CTkLabel(
            top_bar, 
            text="Console  >  Dashboard View", 
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
        # Dashboard is "AM" (Analytical Monitor) initials per Slide 2
        ctk.CTkLabel(badge_circle, text="AM", text_color=COLOR_BOOTSTRAP_TEXT_WHITE, font=(FONT_FAMILY, 10, "bold")).pack(expand=True)
        
        lbl_title = ctk.CTkLabel(
            header, 
            text="System Analytics & Ledger Summary", 
            font=(FONT_FAMILY, FONT_TITLE_SIZE, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_title.pack(anchor="w", pady=(10, 0))
        
        lbl_subtitle = ctk.CTkLabel(
            header, 
            text="Live operational performance, visual occupancy models, and physical assets summary.", 
            font=(FONT_FAMILY, FONT_BODY_SIZE), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_subtitle.pack(anchor="w", pady=2)
        
        # Native scrollable frame for all body elements
        self.scroll_content = ctk.CTkScrollableFrame(
            self, 
            fg_color=COLOR_BOOTSTRAP_BG, 
            scrollbar_button_color=COLOR_BOOTSTRAP_BORDER,
            scrollbar_button_hover_color=COLOR_BOOTSTRAP_BORDER
        )
        self.scroll_content.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # 1. Operational KPIs Header
        lbl_ops_hdr = ctk.CTkLabel(
            self.scroll_content, 
            text="OPERATIONAL BED-SPACE STATS", 
            font=(FONT_FAMILY, 11, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_ops_hdr.pack(fill="x", pady=(10, 5))
        
        self.kpi_frame = ctk.CTkFrame(self.scroll_content, fg_color="transparent")
        self.kpi_frame.pack(fill="x", pady=5)
        
        # Grid layout for KPI Cards
        self.kpi_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.lbl_kpi_rooms = self.create_kpi_card(self.kpi_frame, "Total Active Rooms", "0", 0)
        self.lbl_kpi_occupied = self.create_kpi_card(self.kpi_frame, "Total Beds Occupied", "0", 1)
        self.lbl_kpi_open = self.create_kpi_card(self.kpi_frame, "Open Beds Available", "0", 2)
        self.lbl_kpi_residents = self.create_kpi_card(self.kpi_frame, "Active Registrés", "0", 3)
        
        # --- Analytical Visualizations Panel (Slide 2 Charts) ---
        lbl_chart_hdr = ctk.CTkLabel(
            self.scroll_content,
            text="REAL-TIME MONITORING CHARTS",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_chart_hdr.pack(fill="x", pady=(20, 5))

        self.charts_frame = ctk.CTkFrame(self.scroll_content, fg_color="transparent")
        self.charts_frame.pack(fill="x", pady=5)
        self.charts_frame.columnconfigure(0, weight=6) # Bar chart takes more horizontal width
        self.charts_frame.columnconfigure(1, weight=4) # Donut chart is square/smaller

        # A. Monthly Booking Trends Card
        bar_card = ctk.CTkFrame(
            self.charts_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            height=250
        )
        bar_card.grid(row=0, column=0, padx=(0, 8), pady=5, sticky="nsew")
        bar_card.pack_propagate(False)

        ctk.CTkLabel(
            bar_card,
            text="Monthly Booking Trends (Registrations)",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.bar_canvas = tk.Canvas(
            bar_card,
            bg=COLOR_BOOTSTRAP_CARD,
            bd=0,
            highlightthickness=0
        )
        self.bar_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # B. Accommodations Donut Chart Card
        donut_card = ctk.CTkFrame(
            self.charts_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            height=250
        )
        donut_card.grid(row=0, column=1, padx=(8, 0), pady=5, sticky="nsew")
        donut_card.pack_propagate(False)

        ctk.CTkLabel(
            donut_card,
            text="Accommodations Occupancy Status",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.donut_canvas = tk.Canvas(
            donut_card,
            bg=COLOR_BOOTSTRAP_CARD,
            bd=0,
            highlightthickness=0
        )
        self.donut_canvas.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Bind configure events to draw charts dynamically
        self.bar_canvas.bind("<Configure>", lambda e: self.draw_bar_chart())
        self.donut_canvas.bind("<Configure>", lambda e: self.draw_donut_chart())

        # 2. Financial Overview Header
        lbl_fin_hdr = ctk.CTkLabel(
            self.scroll_content, 
            text="FINANCIAL LEDGER OVERVIEW (HOSTEL VS ACADEMIC)", 
            font=(FONT_FAMILY, 11, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_fin_hdr.pack(fill="x", pady=(25, 5))
        
        self.fin_frame = ctk.CTkFrame(self.scroll_content, fg_color="transparent")
        self.fin_frame.pack(fill="x", pady=5)
        
        # Grid layout for Financial Cards
        self.fin_frame.columnconfigure((0, 1, 2), weight=1)
        self.lbl_fin_deposits = self.create_financial_card(self.fin_frame, "Security Deposits Held", "$0.00", 0, COLOR_BOOTSTRAP_PRIMARY)
        self.lbl_fin_fees = self.create_financial_card(self.fin_frame, "Hostel Fees Collected", "$0.00", 1, COLOR_BOOTSTRAP_SUCCESS)
        self.lbl_fin_debt = self.create_financial_card(self.fin_frame, "Academic Tuition Arrears", "$0.00", 2, COLOR_BOOTSTRAP_DANGER)

        # 3. Facility Equipment Header
        lbl_inv_hdr = ctk.CTkLabel(
            self.scroll_content, 
            text="FACILITY EQUIPMENT DIRECTORY (PARSED ROOM LAYOUT ASSETS)", 
            font=(FONT_FAMILY, 11, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_inv_hdr.pack(fill="x", pady=(30, 5))
        
        self.inv_card = ctk.CTkFrame(
            self.scroll_content, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12
        )
        self.inv_card.pack(fill="x", pady=(5, 30))
        
        self.inv_container = ctk.CTkFrame(self.inv_card, fg_color="transparent")
        self.inv_container.pack(fill="both", expand=True, padx=25, pady=25)

    def create_kpi_card(self, parent, title, val, col_idx):
        card = ctk.CTkFrame(
            parent, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12,
            height=100
        )
        card.grid(row=0, column=col_idx, padx=6, pady=5, sticky="nsew")
        card.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            card, 
            text=title.upper(), 
            font=(FONT_FAMILY, 9, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_title.pack(anchor="w", padx=15, pady=(15, 0))
        
        lbl_val = ctk.CTkLabel(
            card, 
            text=val, 
            font=(FONT_FAMILY, 26, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_DARK,
            anchor="w"
        )
        lbl_val.pack(anchor="w", padx=15, pady=(2, 0))
        
        return lbl_val

    def create_financial_card(self, parent, title, val, col_idx, value_color):
        card = ctk.CTkFrame(
            parent, 
            fg_color=COLOR_BOOTSTRAP_CARD, 
            border_color=COLOR_BOOTSTRAP_BORDER, 
            border_width=1,
            corner_radius=12,
            height=110
        )
        card.grid(row=0, column=col_idx, padx=8, pady=5, sticky="nsew")
        card.pack_propagate(False)
        
        lbl_title = ctk.CTkLabel(
            card, 
            text=title.upper(), 
            font=(FONT_FAMILY, 9, "bold"), 
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED,
            anchor="w"
        )
        lbl_title.pack(anchor="w", padx=18, pady=(18, 0))
        
        lbl_val = ctk.CTkLabel(
            card, 
            text=val, 
            font=(FONT_FAMILY, 22, "bold"), 
            text_color=value_color,
            anchor="w"
        )
        lbl_val.pack(anchor="w", padx=18, pady=(2, 0))
        
        return lbl_val

    def draw_bar_chart(self):
        self.bar_canvas.delete("all")
        width = self.bar_canvas.winfo_width()
        height = self.bar_canvas.winfo_height()
        if width <= 50 or height <= 50:
            return

        from datetime import date, datetime
        from collections import defaultdict
        
        # Calculate last 6 months list dynamically
        today = date.today()
        months_list = []
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            months_list.append((y, m))

        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        months = [f"{month_names[m-1]} {str(y)[2:]}" for (y, m) in months_list]

        # Gather data from DB
        counts = defaultdict(int)
        try:
            records = self.db.fetch_all("SELECT check_in_date FROM Residents")
            for r in records:
                try:
                    dt_val = r["check_in_date"]
                    if isinstance(dt_val, str):
                        dt = datetime.strptime(dt_val[:10], "%Y-%m-%d").date()
                    elif isinstance(dt_val, (date, datetime)):
                        dt = dt_val
                    else:
                        continue
                    if (dt.year, dt.month) in months_list:
                        counts[(dt.year, dt.month)] += 1
                except Exception:
                    pass
        except Exception as e:
            print(f"Error querying dashboard booking trends: {e}")

        values = [counts[m_tuple] for m_tuple in months_list]

        # Determine y-axis scale based on data
        max_val = max(values)
        if max_val <= 0:
            max_val = 5
        else:
            max_val = int(max_val * 1.3)
            if max_val < 5:
                max_val = 5

        margin_y = 20
        margin_x = 30
        chart_w = width - 2 * margin_x
        chart_h = height - 2 * margin_y - 20 # bottom margin for month tags

        col_w = chart_w / len(months)
        bar_w = col_w * 0.55

        # Draw gridlines & labels
        tick_step = max(1, max_val // 4)
        for y_tick in range(0, max_val + 1, tick_step):
            norm_y = y_tick / max_val
            canvas_y = margin_y + chart_h * (1 - norm_y)
            self.bar_canvas.create_line(margin_x, canvas_y, width - margin_x, canvas_y, fill="#e2e8f0", dash=(2, 2))
            self.bar_canvas.create_text(margin_x - 8, canvas_y, text=str(y_tick), fill=COLOR_BOOTSTRAP_TEXT_MUTED, font=(FONT_FAMILY, 8), anchor="e")

        # Draw columns
        for idx, month in enumerate(months):
            val = values[idx]
            norm_y = val / max_val
            bar_h = chart_h * norm_y

            x_center = margin_x + idx * col_w + col_w / 2
            x1 = x_center - bar_w / 2
            x2 = x_center + bar_w / 2
            y1 = margin_y + chart_h - bar_h
            y2 = margin_y + chart_h

            # Draw bar rectangle
            self.bar_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=COLOR_BOOTSTRAP_PRIMARY,
                outline=COLOR_BOOTSTRAP_PRIMARY,
                width=0
            )

            # Draw value text above bar
            self.bar_canvas.create_text(
                x_center, y1 - 8,
                text=str(val),
                fill=COLOR_BOOTSTRAP_TEXT_DARK,
                font=(FONT_FAMILY, 8, "bold")
            )

            # Draw month text under bar
            self.bar_canvas.create_text(
                x_center, y2 + 12,
                text=month,
                fill=COLOR_BOOTSTRAP_TEXT_MUTED,
                font=(FONT_FAMILY, 9)
            )

    def draw_donut_chart(self):
        self.donut_canvas.delete("all")
        width = self.donut_canvas.winfo_width()
        height = self.donut_canvas.winfo_height()
        if width <= 50 or height <= 50:
            return

        # Fetch live metrics
        try:
            kpis = self.db.get_kpi_metrics()
            occupied = kpis["occupied_beds"]
            total = kpis["occupied_beds"] + kpis["open_beds"]
        except Exception:
            occupied = 0
            total = 0

        pct = int((occupied / total) * 100) if total > 0 else 0

        # Circle bbox
        size = min(width, height) - 40
        x1 = (width - size) / 2
        y1 = (height - size) / 2
        x2 = x1 + size
        y2 = y1 + size

        # Draw arcs based on live occupancy percentage
        if pct == 0:
            self.donut_canvas.create_oval(x1, y1, x2, y2, fill="#dc2626", outline="#dc2626", width=0)
        elif pct == 100:
            self.donut_canvas.create_oval(x1, y1, x2, y2, fill="#16a34a", outline="#16a34a", width=0)
        else:
            green_extent = - (pct / 100.0) * 360
            self.donut_canvas.create_arc(
                x1, y1, x2, y2,
                start=90, extent=green_extent,
                fill="#16a34a", outline="#16a34a", width=0
            )
            red_extent = -360 - green_extent
            self.donut_canvas.create_arc(
                x1, y1, x2, y2,
                start=90 + green_extent, extent=red_extent,
                fill="#dc2626", outline="#dc2626", width=0
            )

        # Center circle to make it a donut
        hole_size = size * 0.55
        hx1 = x1 + (size - hole_size) / 2
        hy1 = y1 + (size - hole_size) / 2
        hx2 = hx1 + hole_size
        hy2 = hy1 + hole_size

        self.donut_canvas.create_oval(
            hx1, hy1, hx2, hy2,
            fill=COLOR_BOOTSTRAP_CARD,
            outline=COLOR_BOOTSTRAP_CARD,
            width=0
        )

        # Center Text
        self.donut_canvas.create_text(
            width / 2, height / 2 - 8,
            text=f"{pct}%",
            fill=COLOR_BOOTSTRAP_TEXT_DARK,
            font=(FONT_FAMILY, 14, "bold"),
            anchor="center"
        )
        self.donut_canvas.create_text(
            width / 2, height / 2 + 8,
            text="OCCUPANCY",
            fill=COLOR_BOOTSTRAP_TEXT_MUTED,
            font=(FONT_FAMILY, 8, "bold"),
            anchor="center"
        )

    def refresh_data(self):
        """Fetches fresh operational metrics and redraws the cards and asset grids."""
        try:
            # 1. Update KPIs
            kpis = self.db.get_kpi_metrics()
            self.lbl_kpi_rooms.configure(text=str(kpis["total_rooms"]))
            self.lbl_kpi_occupied.configure(text=str(kpis["occupied_beds"]))
            self.lbl_kpi_open.configure(text=str(kpis["open_beds"]))
            self.lbl_kpi_residents.configure(text=str(kpis["active_residents"]))
            
            # 2. Update Financials
            fin = self.db.get_financial_summary()
            self.lbl_fin_deposits.configure(text=f"${fin['deposits']:,.2f}")
            self.lbl_fin_fees.configure(text=f"${fin['fees']:,.2f}")
            self.lbl_fin_debt.configure(text=f"${fin['debt']:,.2f}")
            
            # 3. Rebuild assets breakdown grid
            for child in self.inv_container.winfo_children():
                child.destroy()
                
            assets = self.db.get_inventory_summary()
            if not assets:
                lbl_empty = ctk.CTkLabel(
                    self.inv_container, 
                    text="No active facility equipment registered. Set up layouts to view asset metrics.", 
                    font=(FONT_FAMILY, FONT_BODY_SIZE), 
                    text_color=COLOR_BOOTSTRAP_TEXT_MUTED
                )
                lbl_empty.pack(pady=10)
            else:
                r, c = 0, 0
                max_cols = 3
                for idx, (asset_name, count) in enumerate(assets.items()):
                    item_frame = ctk.CTkFrame(
                        self.inv_container, 
                        fg_color=COLOR_BOOTSTRAP_BG, 
                        border_color=COLOR_BOOTSTRAP_BORDER, 
                        border_width=1,
                        corner_radius=8,
                        height=45
                    )
                    item_frame.grid(row=r, column=c, padx=8, pady=6, sticky="ew")
                    item_frame.pack_propagate(False)
                    self.inv_container.columnconfigure(c, weight=1)
                    
                    lbl_name = ctk.CTkLabel(
                        item_frame, 
                        text=asset_name, 
                        font=(FONT_FAMILY, FONT_BODY_SIZE), 
                        text_color=COLOR_BOOTSTRAP_TEXT_DARK
                    )
                    lbl_name.pack(side="left", padx=15)
                    
                    lbl_count = ctk.CTkLabel(
                        item_frame, 
                        text=f"{count} Active", 
                        font=(FONT_FAMILY, FONT_BODY_SIZE - 1, "bold"), 
                        text_color=COLOR_BOOTSTRAP_TEXT_WHITE, 
                        fg_color=COLOR_BOOTSTRAP_PRIMARY, 
                        corner_radius=6,
                        padx=8,
                        pady=3,
                        height=22
                    )
                    lbl_count.pack(side="right", padx=10)
                    
                    c += 1
                    if c >= max_cols:
                        c = 0
                        r += 1
        except Exception as e:
            print(f"Error refreshing dashboard data: {e}")
