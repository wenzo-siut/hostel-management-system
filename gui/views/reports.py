import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import os
from datetime import datetime

from gui.theme import (
    COLOR_BOOTSTRAP_BG, COLOR_BOOTSTRAP_CARD, COLOR_BOOTSTRAP_BORDER,
    COLOR_BOOTSTRAP_TEXT_DARK, COLOR_BOOTSTRAP_TEXT_MUTED, COLOR_BOOTSTRAP_PRIMARY,
    COLOR_BOOTSTRAP_TEXT_WHITE, FONT_FAMILY, FONT_TITLE_SIZE, FONT_SUBTITLE_SIZE, FONT_BODY_SIZE
)

class ReportsView(ctk.CTkFrame):
    """View rendering Slide 9 - Administrative Business Intelligence Panel with Export Actions, Line Chart, and Operational Metrics list."""
    def __init__(self, parent, db_manager):
        super().__init__(parent, fg_color=COLOR_BOOTSTRAP_BG, corner_radius=0)
        self.db = db_manager
        self.create_layout()

    def create_layout(self):
        # Operational Panel (Top Automation Actions & Export Buttons)
        action_bar = ctk.CTkFrame(
            self,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12
        )
        action_bar.pack(fill="x", padx=20, pady=(10, 10))

        lbl_desc = ctk.CTkLabel(
            action_bar,
            text="📊 Export Operational Ledger & Allocation Records:",
            font=(FONT_FAMILY, 11, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_desc.pack(side="left", padx=20, pady=12)

        # Export Buttons (Slide 9 colors: Red/White for PDF)
        btn_pdf = ctk.CTkButton(
            action_bar,
            text="Download PDF Report",
            fg_color="#b91c1c", # Red
            hover_color="#991b1b",
            text_color="#ffffff",
            font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"),
            command=self.export_pdf,
            height=36,
            width=170,
            corner_radius=8
        )
        btn_pdf.pack(side="right", padx=20, pady=12)

        # Main view divided into two columns
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left Column: Weekly Dynamics Line Chart
        chart_card = ctk.CTkFrame(
            content_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12
        )
        chart_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lbl_chart_title = ctk.CTkLabel(
            chart_card,
            text="Weekly Allocation Dynamics (Stay Registry)",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_chart_title.pack(anchor="w", padx=20, pady=(15, 2))

        lbl_chart_sub = ctk.CTkLabel(
            chart_card,
            text="Tracking active onboarding registrations processed over the last 6 weeks.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_chart_sub.pack(anchor="w", padx=20, pady=(0, 15))

        # Canvas for line chart
        self.chart_canvas = tk.Canvas(
            chart_card,
            bg=COLOR_BOOTSTRAP_CARD,
            bd=0,
            highlightthickness=0
        )
        self.chart_canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.chart_canvas.bind("<Configure>", lambda event: self.draw_line_chart())

        # Right Column: Real-Time Operational Metrics List
        metrics_card = ctk.CTkFrame(
            content_frame,
            fg_color=COLOR_BOOTSTRAP_CARD,
            border_color=COLOR_BOOTSTRAP_BORDER,
            border_width=1,
            corner_radius=12,
            width=320
        )
        metrics_card.pack(side="right", fill="both", padx=(10, 0))
        metrics_card.pack_propagate(False)

        lbl_metrics_title = ctk.CTkLabel(
            metrics_card,
            text="Real-Time Operational Metrics",
            font=(FONT_FAMILY, FONT_SUBTITLE_SIZE, "bold"),
            text_color=COLOR_BOOTSTRAP_TEXT_DARK
        )
        lbl_metrics_title.pack(anchor="w", padx=20, pady=(15, 2))

        lbl_metrics_sub = ctk.CTkLabel(
            metrics_card,
            text="Infrastructure health audit logs.",
            font=(FONT_FAMILY, FONT_BODY_SIZE),
            text_color=COLOR_BOOTSTRAP_TEXT_MUTED
        )
        lbl_metrics_sub.pack(anchor="w", padx=20, pady=(0, 15))

        # Scrollable metrics frame
        metrics_list_frame = ctk.CTkScrollableFrame(
            metrics_card,
            fg_color="transparent",
            scrollbar_button_color=COLOR_BOOTSTRAP_BG,
            scrollbar_button_hover_color=COLOR_BOOTSTRAP_BORDER
        )
        metrics_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Seed and draw metrics
        self.render_metrics(metrics_list_frame)

    def draw_line_chart(self):
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        if width <= 100 or height <= 100:
            return

        # Data points for line chart: (Week label, Value)
        # Seeded value representation matching the mockup trend
        data = [
            ("Week 21", 5),
            ("Week 22", 12),
            ("Week 23", 8),
            ("Week 24", 19),
            ("Week 25", 14),
            ("Week 26", 25)
        ]

        max_val = 30
        margin_x = 40
        margin_y = 30

        chart_w = width - 2 * margin_x
        chart_h = height - 2 * margin_y

        # Draw grid lines & Y labels
        for y_tick in range(0, max_val + 1, 10):
            norm_y = y_tick / max_val
            canvas_y = margin_y + chart_h * (1 - norm_y)
            self.chart_canvas.create_line(margin_x, canvas_y, width - margin_x, canvas_y, fill="#e2e8f0", dash=(2, 2))
            self.chart_canvas.create_text(margin_x - 10, canvas_y, text=str(y_tick), fill=COLOR_BOOTSTRAP_TEXT_MUTED, font=(FONT_FAMILY, 8), anchor="e")

        # Plot data points
        coords = []
        for i, (label, val) in enumerate(data):
            norm_x = i / (len(data) - 1)
            norm_y = val / max_val

            canvas_x = margin_x + chart_w * norm_x
            canvas_y = margin_y + chart_h * (1 - norm_y)

            coords.append((canvas_x, canvas_y, label, val))

        # Draw smooth line connecting points
        for idx in range(len(coords) - 1):
            x1, y1, _, _ = coords[idx]
            x2, y2, _, _ = coords[idx + 1]
            self.chart_canvas.create_line(x1, y1, x2, y2, fill=COLOR_BOOTSTRAP_PRIMARY, width=3)

        # Draw data points markers and labels
        for x, y, label, val in coords:
            # Point circle
            self.chart_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#ffffff", outline=COLOR_BOOTSTRAP_PRIMARY, width=2)
            # Value tag on top
            self.chart_canvas.create_text(x, y - 14, text=str(val), fill=COLOR_BOOTSTRAP_TEXT_DARK, font=(FONT_FAMILY, 9, "bold"))
            # X Axis label
            self.chart_canvas.create_text(x, height - margin_y + 12, text=label, fill=COLOR_BOOTSTRAP_TEXT_MUTED, font=(FONT_FAMILY, 8))

    def render_metrics(self, parent):
        metrics = [
            ("Uptime Status", "99.98% Active", "normal"),
            ("Database Lock Latency", "12 ms avg", "normal"),
            ("API Transaction Success", "99.4%", "normal"),
            ("Active Sessions count", "3 Officers", "normal"),
            ("Cron Stay Audit Hook", "Operational", "active"),
            ("Last Automatic Checkout", "Today 08:30 AM", "normal"),
            ("Memory Usage", "64.2 MB", "normal"),
            ("MySQL Connection Status", "Secure / Tunneled", "active")
        ]

        for i, (name, val, m_type) in enumerate(metrics):
            item = ctk.CTkFrame(parent, fg_color="transparent")
            item.pack(fill="x", pady=6)

            lbl_name = ctk.CTkLabel(item, text=name, font=(FONT_FAMILY, 10), text_color=COLOR_BOOTSTRAP_TEXT_DARK)
            lbl_name.pack(side="left")

            val_color = COLOR_BOOTSTRAP_PRIMARY if m_type == "active" else COLOR_BOOTSTRAP_TEXT_MUTED
            lbl_val = ctk.CTkLabel(item, text=val, font=(FONT_FAMILY, 10, "bold"), text_color=val_color)
            lbl_val.pack(side="right")

            # Horizontal line divider
            divider = ctk.CTkFrame(parent, fg_color=COLOR_BOOTSTRAP_BORDER, height=1)
            divider.pack(fill="x", pady=(2, 0))


    def export_pdf(self):
        try:
            residents = self.db.search_residents()
            if not residents:
                messagebox.showwarning("No Data", "There are no resident records to export.", parent=self)
                return
            
            # Open file dialog for HTML report (which can be printed to PDF)
            file_path = filedialog.asksaveasfilename(
                parent=self,
                title="Save Printable HTML Report",
                filetypes=[("HTML Document (*.html)", "*.html"), ("All Files (*.*)", "*.*")],
                defaultextension=".html",
                initialfile="HMS_BI_Report_2026.html"
            )
            
            if not file_path:
                return # User cancelled
                
            # Create HTML rows
            html_rows = ""
            for res in residents:
                html_rows += f"""
                <tr>
                    <td>{res.get('student_id', '')}</td>
                    <td>{res.get('full_name', '')}</td>
                    <td>{res.get('room_number', '')}</td>
                    <td>{res.get('type_name', '')}</td>
                    <td>{res.get('academic_major', '')}</td>
                    <td>{res.get('check_in_date', '')}</td>
                    <td>{res.get('check_out_date', '')}</td>
                    <td>${float(res.get('deposit_paid', 0)):,.2f}</td>
                    <td>${float(res.get('hostel_tuition_fee', 0)):,.2f}</td>
                    <td>${float(res.get('academic_tuition_debt', 0)):,.2f}</td>
                    <td><span class="status-badge {res.get('allocation_status', '').lower().replace(' ', '-')}">{res.get('allocation_status', '')}</span></td>
                </tr>
                """
                
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Hostel Management System - Administrative BI Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; margin: 40px; background-color: #f8fafc; }}
        .header {{ margin-bottom: 30px; border-bottom: 2px solid #cbd5e1; padding-bottom: 20px; }}
        h1 {{ color: #0f172a; margin: 0 0 10px 0; font-size: 28px; }}
        .meta {{ color: #64748b; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }}
        th, td {{ padding: 12px 15px; text-align: left; font-size: 13px; }}
        th {{ background-color: #0f172a; color: #ffffff; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }}
        tr {{ border-bottom: 1px solid #e2e8f0; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        .status-badge {{ padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; }}
        .fully-registered {{ background-color: #dcfce7; color: #15803d; }}
        .probation {{ background-color: #fee2e2; color: #b91c1c; }}
        .pending {{ background-color: #fef9c3; color: #a16207; }}
        @media print {{
            body {{ background-color: #ffffff; margin: 0; }}
            table {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Hostel Management System</h1>
        <h2>Administrative Business Intelligence Report</h2>
        <div class="meta">Generated on: {now_str} | Total Records: {len(residents)}</div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Student ID</th>
                <th>Full Name</th>
                <th>Room</th>
                <th>Room Type</th>
                <th>Major</th>
                <th>Check-In</th>
                <th>Check-Out</th>
                <th>Deposit</th>
                <th>Tuition Fee</th>
                <th>Academic Debt</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {html_rows}
        </tbody>
    </table>
</body>
</html>
"""
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            messagebox.showinfo(
                "Export Success",
                f"HMS Report exported successfully as HTML to:\n'{file_path}'\n\nTip: You can open this file in any web browser (Chrome, Edge, etc.) and press 'Ctrl + P' (Print) to save it directly as a PDF.",
                parent=self
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF/HTML report:\n{e}", parent=self)
