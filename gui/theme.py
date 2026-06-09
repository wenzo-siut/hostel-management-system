import customtkinter as ctk
import ttkbootstrap as tb

# --- CustomTkinter Global Visual Configuration ---
ctk.set_appearance_mode("light")  # Set light mode natively for light content scrollbars/windows
ctk.set_default_color_theme("blue")

# --- Premium Slate & White Theme Palette Constants ---
COLOR_BOOTSTRAP_BG = "#f8fafc"          # Slate-50 Light Canvas Background
COLOR_BOOTSTRAP_SIDEBAR = "#0f172a"     # Slate-900 Dark Sidebar
COLOR_BOOTSTRAP_SIDEBAR_ACTIVE = "#1e293b" # Slate-800 Active Sidebar Selection
COLOR_BOOTSTRAP_CARD = "#ffffff"        # Pure White Card background
COLOR_BOOTSTRAP_BORDER = "#e2e8f0"      # Slate-200 light border slate
COLOR_BOOTSTRAP_TEXT_DARK = "#0f172a"    # Slate-900 Dark text
COLOR_BOOTSTRAP_TEXT_WHITE = "#ffffff"   # White contrast text (for sidebar/dark boxes)
COLOR_BOOTSTRAP_TEXT_MUTED = "#64748b"   # Slate-500 Muted text

# Standard Bootstrap Accent Colors
COLOR_BOOTSTRAP_PRIMARY = "#2563eb"     # Modern Blue (Primary)
COLOR_BOOTSTRAP_PRIMARY_HOVER = "#1d4ed8"

# Status Badges Colors (Background & Text)
COLOR_BOOTSTRAP_SUCCESS_BG = "#dcfce7"   # Light Green bg
COLOR_BOOTSTRAP_SUCCESS_TEXT = "#15803d" # Dark Green text
COLOR_BOOTSTRAP_SUCCESS = "#16a34a"      # Primary green (Success standard)
COLOR_BOOTSTRAP_SUCCESS_HOVER = "#15803d"

COLOR_BOOTSTRAP_WARNING_BG = "#fef9c3"   # Light Yellow bg
COLOR_BOOTSTRAP_WARNING_TEXT = "#a16207" # Dark Yellow/Brown text
COLOR_BOOTSTRAP_WARNING = "#ca8a04"      # Primary yellow (Warning standard)
COLOR_BOOTSTRAP_WARNING_HOVER = "#a16207"

COLOR_BOOTSTRAP_DANGER_BG = "#fee2e2"    # Light Red bg
COLOR_BOOTSTRAP_DANGER_TEXT = "#b91c1c"  # Dark Red text
COLOR_BOOTSTRAP_DANGER = "#dc2626"       # Primary red (Danger standard)
COLOR_BOOTSTRAP_DANGER_HOVER = "#b91c1c"

# --- Typography Font Profiles ---
FONT_FAMILY = "Segoe UI"
FONT_TITLE_SIZE = 18
FONT_SUBTITLE_SIZE = 14
FONT_BODY_SIZE = 11

def setup_treeview_style():
    """Styles the standard ttk.Treeview using ttkbootstrap with the flatly light theme."""
    # Initialize ttkbootstrap with flatly light theme
    style = tb.Style(theme="flatly")
    
    # Reset standard Tkinter options to prevent double-borders in CTkEntry and other widgets
    style.master.option_add("*Entry.borderWidth", 0)
    style.master.option_add("*Entry.highlightThickness", 0)
    style.master.option_add("*Entry.relief", "flat")
    style.master.option_add("*Listbox.borderWidth", 0)
    style.master.option_add("*Listbox.highlightThickness", 0)
    
    # Customise Treeview for our premium look
    style.configure(
        "Treeview", 
        background=COLOR_BOOTSTRAP_CARD, 
        foreground=COLOR_BOOTSTRAP_TEXT_DARK, 
        rowheight=38, 
        fieldbackground=COLOR_BOOTSTRAP_CARD,
        font=(FONT_FAMILY, FONT_BODY_SIZE),
        borderwidth=0
    )
    
    # Styles Treeview Headings
    style.configure(
        "Treeview.Heading", 
        background="#f1f5f9", # slate-100
        foreground=COLOR_BOOTSTRAP_TEXT_DARK, 
        font=(FONT_FAMILY, FONT_BODY_SIZE, "bold"), 
        borderwidth=0
    )
    
    # Active Selections
    style.map(
        "Treeview", 
        background=[("selected", COLOR_BOOTSTRAP_PRIMARY)],
        foreground=[("selected", COLOR_BOOTSTRAP_TEXT_WHITE)]
    )
