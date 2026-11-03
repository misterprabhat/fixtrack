import tkinter as tk
from tkinter import ttk, messagebox
import oracledb

# ====================================================================
# DATABASE CONFIGURATION & HELPER
# ====================================================================
DB_CONFIG = {
    "user": "FIXTRACK",
    "password": "fixtrack@2026",
    "host": "localhost",
    "port": 1521,
    "service_name": "FREEPDB1"
}


def get_connection():
    """Returns an active Oracle database connection."""
    dsn = f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['service_name']}"
    return oracledb.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dsn=dsn
    )


# ====================================================================
# DESIGN TOKENS
# ====================================================================
C_BG = "#F1F5F9"          # app background
C_CARD = "#FFFFFF"        # card surface
C_BORDER = "#E2E8F0"      # subtle borders
C_NAVY = "#0F172A"        # dark navy
C_NAVY_2 = "#1E293B"
C_NAVY_3 = "#334155"
C_TEXT = "#0F172A"
C_MUTED = "#64748B"
C_INDIGO = "#4F46E5"
C_INDIGO_H = "#4338CA"
C_INDIGO_P = "#3730A3"
C_INDIGO_L = "#EEF2FF"
C_INDIGO_L2 = "#E0E7FF"
C_ROSE = "#E11D48"
C_EMERALD = "#059669"
C_AMBER = "#D97706"
C_BLUE = "#2563EB"
C_ZEBRA_A = "#FFFFFF"
C_ZEBRA_B = "#F8FAFC"
C_SELECT = "#C7D2FE"

FONT = "Segoe UI"
F_TITLE = (FONT, 22, "bold")
F_H1 = (FONT, 15, "bold")
F_H2 = (FONT, 12, "bold")
F_BODY = (FONT, 10)
F_SMALL = (FONT, 9)
F_LABEL = (FONT, 9, "bold")
F_KPI = (FONT, 30, "bold")


# ====================================================================
# MAIN APPLICATION WINDOW
# ====================================================================
class FixTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FixTrack — Campus Repair & Maintenance Tracker")
        self.geometry("1100x720")
        self.minsize(980, 640)
        self.configure(bg=C_BG)

        # Current session state
        self.current_user = None  # Dict: id, name, email, role
        self.users_cache = {}

        # Configure visual theme
        self.setup_theme()

        # Master Container for Views
        self.container = tk.Frame(self, bg=C_BG)
        self.container.pack(fill="both", expand=True)

        # Show Login Screen
        self.show_login_frame()

    # ----------------------------------------------------------------
    # THEME
    # ----------------------------------------------------------------
    def setup_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        self.option_add("*TCombobox*Listbox.font", (FONT, 10))
        self.option_add("*TCombobox*Listbox.background", C_CARD)
        self.option_add("*TCombobox*Listbox.foreground", C_TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", C_INDIGO)
        self.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")

        style.configure("TFrame", background=C_BG)

        # ---- Buttons -------------------------------------------------
        def button_style(name, bg, fg, hover, pressed):
            style.configure(
                name, font=(FONT, 10, "bold"), background=bg, foreground=fg,
                padding=(18, 9), borderwidth=0, focusthickness=0,
                focuscolor=bg, relief="flat",
                bordercolor=bg, lightcolor=bg, darkcolor=bg
            )
            style.map(
                name,
                background=[("pressed", pressed), ("active", hover)],
                bordercolor=[("pressed", pressed), ("active", hover)],
                lightcolor=[("pressed", pressed), ("active", hover)],
                darkcolor=[("pressed", pressed), ("active", hover)],
                foreground=[("disabled", "#94A3B8")]
            )

        button_style("Primary.TButton", C_INDIGO, "#FFFFFF", C_INDIGO_H, C_INDIGO_P)
        button_style("Accent.TButton", C_EMERALD, "#FFFFFF", "#047857", "#065F46")
        button_style("Secondary.TButton", C_INDIGO_L, C_INDIGO, C_INDIGO_L2, "#C7D2FE")
        button_style("Nav.TButton", C_NAVY_2, "#E2E8F0", C_NAVY_3, "#475569")

        # ---- Inputs --------------------------------------------------
        style.configure(
            "Modern.TEntry", fieldbackground="#FFFFFF", foreground=C_TEXT,
            bordercolor=C_BORDER, lightcolor=C_BORDER, darkcolor=C_BORDER,
            padding=8, borderwidth=1
        )
        style.map(
            "Modern.TEntry",
            bordercolor=[("focus", C_INDIGO)],
            lightcolor=[("focus", C_INDIGO)],
            darkcolor=[("focus", C_INDIGO)]
        )

        style.configure(
            "Modern.TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF",
            foreground=C_TEXT, arrowcolor=C_MUTED, bordercolor=C_BORDER,
            lightcolor=C_BORDER, darkcolor=C_BORDER, padding=7,
            arrowsize=14, borderwidth=1
        )
        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", "#FFFFFF")],
            background=[("readonly", "#FFFFFF"), ("active", "#FFFFFF")],
            foreground=[("readonly", C_TEXT)],
            selectbackground=[("readonly", "#FFFFFF")],
            selectforeground=[("readonly", C_TEXT)],
            bordercolor=[("focus", C_INDIGO)],
            lightcolor=[("focus", C_INDIGO)],
            darkcolor=[("focus", C_INDIGO)],
            arrowcolor=[("active", C_INDIGO)]
        )

        # ---- Treeview ------------------------------------------------
        def fixed_map(option):
            # Work around a Tk 8.6 bug where tag colors are ignored
            return [e for e in style.map("Treeview", query_opt=option)
                    if e[:2] != ("!disabled", "!selected")]

        style.configure(
            "Treeview", font=(FONT, 10), rowheight=36,
            background="#FFFFFF", fieldbackground="#FFFFFF",
            foreground=C_TEXT, borderwidth=0, relief="flat"
        )
        style.configure(
            "Treeview.Heading", font=(FONT, 9, "bold"), background="#F8FAFC",
            foreground=C_MUTED, relief="flat", padding=(8, 10),
            borderwidth=0
        )
        style.map("Treeview.Heading", background=[("active", C_INDIGO_L)])
        style.map(
            "Treeview",
            foreground=fixed_map("foreground"),
            background=fixed_map("background") + [("selected", C_SELECT)]
        )
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        # ---- Scrollbar -----------------------------------------------
        style.configure(
            "Vertical.TScrollbar", background="#CBD5E1", troughcolor=C_ZEBRA_B,
            bordercolor=C_ZEBRA_B, lightcolor="#CBD5E1", darkcolor="#CBD5E1",
            arrowcolor=C_MUTED, relief="flat", gripcount=0
        )
        style.map("Vertical.TScrollbar", background=[("active", "#94A3B8")])

    # ----------------------------------------------------------------
    # REUSABLE UI HELPERS
    # ----------------------------------------------------------------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def fade_in(self, step=0):
        """Subtle fade transition between views."""
        try:
            alpha = min(1.0, 0.82 + 0.045 * step)
            self.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.after(14, lambda: self.fade_in(step + 1))
        except tk.TclError:
            pass

    def toast(self, message, kind="success"):
        """Non-blocking notification in the bottom-right corner."""
        colors = {"success": C_EMERALD, "error": C_ROSE, "info": C_INDIGO}
        lbl = tk.Label(
            self, text=f"  {message}  ", bg=colors.get(kind, C_INDIGO), fg="#FFFFFF",
            font=(FONT, 10, "bold"), padx=14, pady=12
        )
        lbl.place(relx=1.0, rely=1.0, x=-24, y=-24, anchor="se")
        lbl.lift()
        self.after(2800, lambda: lbl.destroy() if lbl.winfo_exists() else None)

    def make_card(self, parent, padding=22):
        """Returns (outer, inner). Pack/grid the outer; build into inner."""
        outer = tk.Frame(parent, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
        inner = tk.Frame(outer, bg=C_CARD)
        inner.pack(fill="both", expand=True, padx=padding, pady=padding)
        return outer, inner

    def card_header(self, parent, title, subtitle=None):
        row = tk.Frame(parent, bg=C_CARD)
        row.pack(fill="x", pady=(0, 14))
        left = tk.Frame(row, bg=C_CARD)
        left.pack(side="left")
        tk.Label(left, text=title, font=F_H2, bg=C_CARD, fg=C_TEXT).pack(anchor="w")
        if subtitle:
            tk.Label(left, text=subtitle, font=F_SMALL, bg=C_CARD, fg=C_MUTED).pack(anchor="w")
        badge = tk.Label(row, text="", font=F_LABEL, bg=C_INDIGO_L, fg=C_INDIGO, padx=10, pady=3)
        badge.pack(side="right")
        return badge

    def field_label(self, parent, text):
        tk.Label(parent, text=text.upper(), font=(FONT, 8, "bold"), bg=C_CARD,
                 fg=C_MUTED, anchor="w").pack(fill="x", pady=(0, 4))

    def stat_card(self, parent, title, color, subtext):
        outer = tk.Frame(parent, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
        tk.Frame(outer, bg=color, height=5).pack(fill="x")
        inner = tk.Frame(outer, bg=C_CARD)
        inner.pack(fill="both", expand=True, padx=22, pady=(16, 18))
        tk.Label(inner, text=title.upper(), font=(FONT, 9, "bold"), bg=C_CARD,
                 fg=C_MUTED, anchor="w").pack(fill="x")
        value = tk.Label(inner, text="0", font=F_KPI, bg=C_CARD, fg=color, anchor="w")
        value.pack(fill="x", pady=(2, 0))
        tk.Label(inner, text=subtext, font=F_SMALL, bg=C_CARD, fg=C_MUTED, anchor="w").pack(fill="x")
        return outer, value

    def build_table(self, parent, cols, widths, left_aligned=()):
        """Creates a striped, status-tagged Treeview with scrollbar."""
        wrap = tk.Frame(parent, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
        wrap.pack(fill="both", expand=True)

        tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        for col in cols:
            tree.heading(col, text=col.upper())
            anchor = "w" if col in left_aligned else "center"
            tree.column(col, anchor=anchor, width=widths.get(col, 100), minwidth=60)

        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        # Zebra stripes (background only) and status colors (foreground only)
        tree.tag_configure("odd", background=C_ZEBRA_A)
        tree.tag_configure("even", background=C_ZEBRA_B)
        tree.tag_configure("PENDING", foreground=C_AMBER, font=(FONT, 10, "bold"))
        tree.tag_configure("IN_PROGRESS", foreground=C_BLUE, font=(FONT, 10, "bold"))
        tree.tag_configure("RESOLVED", foreground=C_EMERALD, font=(FONT, 10, "bold"))
        tree.tag_configure("REJECTED", foreground=C_ROSE, font=(FONT, 10, "bold"))
        return tree

    def fill_tree(self, tree, rows, status_index):
        """Clears and fills a tree with zebra + status tags. Returns row count."""
        for item in tree.get_children():
            tree.delete(item)
        count = 0
        for i, r in enumerate(rows):
            zebra = "even" if i % 2 else "odd"
            status_tag = str(r[status_index]).replace(" ", "_")
            tree.insert("", "end", values=r, tags=(zebra, status_tag))
            count += 1
        return count

    def make_entry(self, parent, width=34):
        e = ttk.Entry(parent, style="Modern.TEntry", width=width)
        e.pack(fill="x", pady=(0, 14))
        return e

    # ----------------------------------------------------------------
    # 1. LOGIN SCREEN
    # ----------------------------------------------------------------
    def show_login_frame(self):
        self.clear_container()
        self.current_user = None

        # Left brand panel
        left = tk.Frame(self.container, bg=C_NAVY, width=400)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        brand = tk.Frame(left, bg=C_NAVY)
        brand.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(brand, text="FixTrack", font=(FONT, 34, "bold"), bg=C_NAVY, fg="#FFFFFF").pack(anchor="w")
        tk.Label(brand, text="Campus Repair & Maintenance Tracker", font=(FONT, 11),
                 bg=C_NAVY, fg="#94A3B8").pack(anchor="w", pady=(2, 28))
        for text in ("Report issues in seconds", "Track every repair end to end",
                     "Assign staff and resolve faster"):
            row = tk.Frame(brand, bg=C_NAVY)
            row.pack(anchor="w", pady=5)
            tk.Frame(row, bg=C_INDIGO, width=8, height=8).pack(side="left", padx=(0, 12))
            tk.Label(row, text=text, font=(FONT, 11), bg=C_NAVY, fg="#CBD5E1").pack(side="left")

        # Right login area
        right = tk.Frame(self.container, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        card, inner = self.make_card(right, padding=36)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Welcome back", font=F_TITLE, bg=C_CARD, fg=C_TEXT).pack(anchor="w")
        tk.Label(inner, text="Sign in to continue to your dashboard", font=F_BODY,
                 bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(2, 24))

        self.field_label(inner, "Select User (Demo Viva Mode)")

        # Load registered users from database
        user_list = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT USER_ID, FULL_NAME, EMAIL, USER_ROLE FROM USERS ORDER BY USER_ID")
                    self.users_cache = {f"{row[1]} ({row[3]}) - {row[2]}": {"id": row[0], "name": row[1], "email": row[2], "role": row[3]} for row in cur.fetchall()}
                    user_list = list(self.users_cache.keys())
        except Exception as e:
            messagebox.showerror("Database Connection Error", f"Could not connect to Oracle database:\n{str(e)}\n\nCheck password in DB_CONFIG.")
            self.users_cache = {}

        self.user_combo = ttk.Combobox(inner, values=user_list, width=46, state="readonly", style="Modern.TCombobox")
        if user_list:
            self.user_combo.current(0)
        self.user_combo.pack(fill="x", pady=(0, 22))
        self.user_combo.bind("<Return>", lambda e: self.handle_login())

        login_btn = ttk.Button(inner, text="Enter Dashboard", style="Primary.TButton",
                               command=self.handle_login, cursor="hand2")
        login_btn.pack(fill="x")

        self.fade_in()

    def handle_login(self):
        selected_text = self.user_combo.get()
        if not selected_text or selected_text not in self.users_cache:
            messagebox.showwarning("Selection Required", "Please select an account to proceed.")
            return

        self.current_user = self.users_cache[selected_text]
        role = self.current_user["role"]

        if role == "STUDENT":
            self.show_student_dashboard()
        elif role == "STAFF":
            self.show_staff_dashboard()
        elif role == "ADMIN":
            self.show_admin_dashboard()

    def render_nav_bar(self, parent, title_text):
        nav = tk.Frame(parent, bg=C_NAVY)
        nav.pack(fill="x")
        row = tk.Frame(nav, bg=C_NAVY)
        row.pack(fill="x", padx=24, pady=14)

        tk.Label(row, text="FixTrack", font=(FONT, 16, "bold"), bg=C_NAVY, fg="#FFFFFF").pack(side="left")
        tk.Label(row, text="  /  ", font=(FONT, 12), bg=C_NAVY, fg="#475569").pack(side="left")
        tk.Label(row, text=title_text, font=(FONT, 12), bg=C_NAVY, fg="#CBD5E1").pack(side="left")

        logout_btn = ttk.Button(row, text="Logout", style="Nav.TButton",
                                command=self.show_login_frame, cursor="hand2")
        logout_btn.pack(side="right")

        chip = tk.Frame(row, bg=C_NAVY)
        chip.pack(side="right", padx=(0, 18))
        tk.Label(chip, text=self.current_user["name"], font=(FONT, 10, "bold"),
                 bg=C_NAVY, fg="#FFFFFF").pack(side="left", padx=(0, 10))
        tk.Label(chip, text=self.current_user["role"], font=(FONT, 8, "bold"),
                 bg=C_INDIGO, fg="#FFFFFF", padx=9, pady=3).pack(side="left")

    # ----------------------------------------------------------------
    # 2. STUDENT DASHBOARD
    # ----------------------------------------------------------------
    def show_student_dashboard(self):
        self.clear_container()
        self.render_nav_bar(self.container, "Student Portal")

        main_frame = tk.Frame(self.container, bg=C_BG)
        main_frame.pack(fill="both", expand=True, padx=24, pady=22)

        # Left Column: New Request Form
        form_card, form_frame = self.make_card(main_frame)
        form_card.pack(side="left", fill="y", padx=(0, 20))

        self.card_header(form_frame, "Submit Complaint", "Describe the maintenance issue").pack_forget()

        self.field_label(form_frame, "Complaint Title")
        title_entry = self.make_entry(form_frame)

        self.field_label(form_frame, "Category")
        category_combo = ttk.Combobox(form_frame, width=32, state="readonly", style="Modern.TCombobox")
        category_combo.pack(fill="x", pady=(0, 14))

        self.field_label(form_frame, "Location")
        location_entry = self.make_entry(form_frame)

        self.field_label(form_frame, "Priority")
        priority_combo = ttk.Combobox(form_frame, values=["LOW", "MEDIUM", "HIGH"], width=32,
                                      state="readonly", style="Modern.TCombobox")
        priority_combo.current(1)
        priority_combo.pack(fill="x", pady=(0, 14))

        self.field_label(form_frame, "Problem Description")
        desc_text = tk.Text(form_frame, width=34, height=5, font=(FONT, 10), bg="#FFFFFF",
                            fg=C_TEXT, relief="flat", wrap="word", padx=8, pady=8,
                            highlightthickness=1, highlightbackground=C_BORDER,
                            highlightcolor=C_INDIGO, insertbackground=C_TEXT)
        desc_text.pack(fill="x", pady=(0, 20))

        # Populate categories
        categories = {}
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT CATEGORY_ID, CATEGORY_NAME FROM CATEGORIES ORDER BY CATEGORY_ID")
                    for row in cur.fetchall():
                        categories[row[1]] = row[0]
            category_combo['values'] = list(categories.keys())
            if categories:
                category_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch categories: {e}")

        # Right Column: View Submissions
        table_card, table_frame = self.make_card(main_frame, padding=20)
        table_card.pack(side="right", fill="both", expand=True)
        count_badge = self.card_header(table_frame, "My Reported Issues", "Track the progress of your complaints")

        cols = ("ID", "Title", "Category", "Location", "Priority", "Status", "Assigned Staff", "Date")
        tree = self.build_table(
            table_frame, cols,
            {"ID": 50, "Title": 160, "Category": 90, "Location": 130, "Priority": 75,
             "Status": 100, "Assigned Staff": 110, "Date": 115},
            left_aligned=("Title", "Location")
        )

        def refresh_student_table():
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT REQUEST_ID, TITLE, CATEGORY_NAME, LOCATION, PRIORITY, STATUS, ASSIGNED_TO_NAME, CREATED_DATE
                            FROM VIEW_ALL_REQUESTS
                            WHERE SUBMITTED_BY = :1
                            ORDER BY REQUEST_ID DESC
                        """, [self.current_user["id"]])
                        rows = cur.fetchall()
                n = self.fill_tree(tree, rows, status_index=5)
                count_badge.config(text=f"{n} request{'s' if n != 1 else ''}")
            except Exception as e:
                messagebox.showerror("Query Error", f"Error refreshing table: {e}")

        def submit_handler():
            title = title_entry.get().strip()
            cat_name = category_combo.get()
            loc = location_entry.get().strip()
            priority = priority_combo.get()
            desc = desc_text.get("1.0", tk.END).strip()

            if not title or not loc or not desc:
                messagebox.showwarning("Validation Error", "All fields are required.")
                return

            cat_id = categories[cat_name]

            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Calls PL/SQL Procedure SUBMIT_REQUEST
                        out_id = cur.var(oracledb.NUMBER)
                        cur.callproc("SUBMIT_REQUEST", [
                            title, desc, loc, cat_id, self.current_user["id"], priority, out_id
                        ])
                        conn.commit()
                        new_req_id = int(out_id.getvalue())
                        self.toast(f"Complaint submitted — Request ID #{new_req_id}")

                        # Reset form
                        title_entry.delete(0, tk.END)
                        location_entry.delete(0, tk.END)
                        desc_text.delete("1.0", tk.END)
                        refresh_student_table()
            except Exception as e:
                messagebox.showerror("Execution Error", f"Failed to submit complaint:\n{str(e)}")

        ttk.Button(form_frame, text="Submit Complaint", style="Primary.TButton",
                   command=submit_handler, cursor="hand2").pack(fill="x")
        ttk.Button(form_frame, text="Refresh List", style="Secondary.TButton",
                   command=refresh_student_table, cursor="hand2").pack(fill="x", pady=(10, 0))

        refresh_student_table()
        self.fade_in()

    # ----------------------------------------------------------------
    # 3. STAFF DASHBOARD
    # ----------------------------------------------------------------
    def show_staff_dashboard(self):
        self.clear_container()
        self.render_nav_bar(self.container, "Staff Maintenance Portal")

        main_frame = tk.Frame(self.container, bg=C_BG)
        main_frame.pack(fill="both", expand=True, padx=24, pady=22)

        # Summary cards (computed from the loaded rows)
        stats_row = tk.Frame(main_frame, bg=C_BG)
        stats_row.pack(fill="x", pady=(0, 18))
        c1, lbl_assigned = self.stat_card(stats_row, "Assigned to Me", C_INDIGO, "Total tasks on your list")
        c1.pack(side="left", fill="both", expand=True, padx=(0, 16))
        c2, lbl_open = self.stat_card(stats_row, "Open Tasks", C_AMBER, "Pending or in progress")
        c2.pack(side="left", fill="both", expand=True, padx=(0, 16))
        c3, lbl_done = self.stat_card(stats_row, "Completed", C_EMERALD, "Resolved or rejected")
        c3.pack(side="left", fill="both", expand=True)

        table_card, table_frame = self.make_card(main_frame, padding=20)
        table_card.pack(fill="both", expand=True, pady=(0, 18))
        count_badge = self.card_header(table_frame, "Tasks Assigned to Me", "Select a task, then update its status below")

        cols = ("ID", "Title", "Category", "Location", "Priority", "Status", "Student", "Created On")
        tree = self.build_table(
            table_frame, cols,
            {"ID": 50, "Title": 190, "Category": 100, "Location": 150, "Priority": 80,
             "Status": 110, "Student": 120, "Created On": 125},
            left_aligned=("Title", "Location")
        )

        action_card, action_frame = self.make_card(main_frame, padding=16)
        action_card.pack(fill="x")

        tk.Label(action_frame, text="Update Status:", font=(FONT, 10, "bold"),
                 bg=C_CARD, fg=C_TEXT).pack(side="left", padx=(0, 12))
        status_combo = ttk.Combobox(action_frame, values=["IN PROGRESS", "RESOLVED", "REJECTED"],
                                    state="readonly", width=18, style="Modern.TCombobox")
        status_combo.current(0)
        status_combo.pack(side="left", padx=(0, 16))

        def refresh_staff_table():
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT REQUEST_ID, TITLE, CATEGORY_NAME, LOCATION, PRIORITY, STATUS, SUBMITTED_BY_NAME, CREATED_DATE
                            FROM VIEW_ALL_REQUESTS
                            WHERE ASSIGNED_TO = :1
                            ORDER BY REQUEST_ID DESC
                        """, [self.current_user["id"]])
                        rows = cur.fetchall()
                n = self.fill_tree(tree, rows, status_index=5)
                count_badge.config(text=f"{n} task{'s' if n != 1 else ''}")
                lbl_assigned.config(text=str(n))
                open_n = sum(1 for r in rows if r[5] in ("PENDING", "IN PROGRESS"))
                lbl_open.config(text=str(open_n))
                lbl_done.config(text=str(n - open_n))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load requests: {e}")

        def update_status_handler():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Request", "Please highlight a request from the table.")
                return

            req_id = tree.item(selected[0])["values"][0]
            new_status = status_combo.get()

            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Calls PL/SQL Procedure UPDATE_REQUEST_STATUS
                        cur.callproc("UPDATE_REQUEST_STATUS", [req_id, new_status])
                        conn.commit()
                        self.toast(f"Request #{req_id} updated to '{new_status}'")
                        refresh_staff_table()
            except Exception as e:
                messagebox.showerror("Update Error", f"Could not update status:\n{str(e)}")

        ttk.Button(action_frame, text="Apply Status Change", style="Primary.TButton",
                   command=update_status_handler, cursor="hand2").pack(side="left")
        ttk.Button(action_frame, text="Refresh", style="Secondary.TButton",
                   command=refresh_staff_table, cursor="hand2").pack(side="right")

        refresh_staff_table()
        self.fade_in()

    # ----------------------------------------------------------------
    # 4. ADMIN DASHBOARD
    # ----------------------------------------------------------------
    def show_admin_dashboard(self):
        self.clear_container()
        self.render_nav_bar(self.container, "Administrative Overview")

        main_frame = tk.Frame(self.container, bg=C_BG)
        main_frame.pack(fill="both", expand=True, padx=24, pady=22)

        # Statistics Bar (Uses PL/SQL Functions)
        stats_frame = tk.Frame(main_frame, bg=C_BG)
        stats_frame.pack(fill="x", pady=(0, 18))

        card_total, lbl_total = self.stat_card(stats_frame, "Total Requests", C_INDIGO, "All complaints logged on campus")
        card_total.pack(side="left", fill="both", expand=True, padx=(0, 16))

        card_pending, lbl_pending = self.stat_card(stats_frame, "Pending", C_ROSE, "Awaiting action (PL/SQL function)")
        card_pending.pack(side="left", fill="both", expand=True, padx=(0, 16))

        card_resolved, lbl_resolved = self.stat_card(stats_frame, "Resolved", C_EMERALD, "Successfully closed (PL/SQL function)")
        card_resolved.pack(side="left", fill="both", expand=True)

        # All Requests Table (Uses VIEW_ALL_REQUESTS)
        table_card, table_frame = self.make_card(main_frame, padding=20)
        table_card.pack(fill="both", expand=True, pady=(0, 18))
        count_badge = self.card_header(table_frame, "All Campus Complaints", "Live data from VIEW_ALL_REQUESTS")

        cols = ("ID", "Title", "Category", "Location", "Priority", "Status", "Student", "Assigned Staff", "Created")
        tree = self.build_table(
            table_frame, cols,
            {"ID": 50, "Title": 180, "Category": 90, "Location": 140, "Priority": 75,
             "Status": 100, "Student": 105, "Assigned Staff": 110, "Created": 115},
            left_aligned=("Title", "Location")
        )

        # Assignment Action Panel (Calls ASSIGN_REQUEST)
        action_card, action_frame = self.make_card(main_frame, padding=16)
        action_card.pack(fill="x")

        tk.Label(action_frame, text="Assign Staff Member:", font=(FONT, 10, "bold"),
                 bg=C_CARD, fg=C_TEXT).pack(side="left", padx=(0, 12))
        staff_combo = ttk.Combobox(action_frame, state="readonly", width=30, style="Modern.TCombobox")
        staff_combo.pack(side="left", padx=(0, 16))

        # Fetch Staff Members
        staff_dict = {}
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT USER_ID, FULL_NAME FROM USERS WHERE USER_ROLE = 'STAFF' ORDER BY FULL_NAME")
                    for row in cur.fetchall():
                        staff_dict[row[1]] = row[0]
            staff_combo['values'] = list(staff_dict.keys())
            if staff_dict:
                staff_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed loading staff list: {e}")

        def refresh_admin_data():
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # 1. Dashboard Metrics using PL/SQL Functions
                        cur.execute("SELECT COUNT(*) FROM REQUESTS")
                        lbl_total.config(text=str(cur.fetchone()[0]))

                        pending_count = cur.callfunc("GET_PENDING_COUNT", oracledb.NUMBER)
                        lbl_pending.config(text=str(int(pending_count)))

                        resolved_count = cur.callfunc("GET_RESOLVED_COUNT", oracledb.NUMBER)
                        lbl_resolved.config(text=str(int(resolved_count)))

                        # 2. Populate View Data
                        cur.execute("""
                            SELECT REQUEST_ID, TITLE, CATEGORY_NAME, LOCATION, PRIORITY, STATUS, 
                                   SUBMITTED_BY_NAME, ASSIGNED_TO_NAME, CREATED_DATE
                            FROM VIEW_ALL_REQUESTS
                            ORDER BY REQUEST_ID DESC
                        """)
                        rows = cur.fetchall()
                n = self.fill_tree(tree, rows, status_index=5)
                count_badge.config(text=f"{n} request{'s' if n != 1 else ''}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh admin view: {e}")

        def assign_handler():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Row", "Select a request from the table to assign.")
                return

            staff_name = staff_combo.get()
            if not staff_name or staff_name not in staff_dict:
                messagebox.showwarning("Select Staff", "Select a valid staff member.")
                return

            req_id = tree.item(selected[0])["values"][0]
            staff_id = staff_dict[staff_name]

            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        # Calls PL/SQL Procedure ASSIGN_REQUEST
                        cur.callproc("ASSIGN_REQUEST", [req_id, staff_id])
                        conn.commit()
                        self.toast(f"Request #{req_id} assigned to {staff_name}")
                        refresh_admin_data()
            except Exception as e:
                messagebox.showerror("Assignment Error", f"Assignment failed:\n{str(e)}")

        ttk.Button(action_frame, text="Assign Selected Request", style="Primary.TButton",
                   command=assign_handler, cursor="hand2").pack(side="left")
        ttk.Button(action_frame, text="Refresh All", style="Secondary.TButton",
                   command=refresh_admin_data, cursor="hand2").pack(side="right")

        refresh_admin_data()
        self.fade_in()


# ====================================================================
# ENTRY POINT
# ====================================================================
if __name__ == "__main__":
    app = FixTrackApp()
    app.mainloop()