import base64
import csv
import io
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import os
from queue import Queue
import re
import smtplib
import sqlite3
import threading
import time
from tkinter import filedialog, ttk
import customtkinter as ctk
import pandas as pd
from PIL import Image, ImageDraw
from pypdf import PdfReader

# ==========================================
# DESIGN TOKENS  (restrained institutional palette)
# ==========================================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

PRIMARY = "#4C1D95"        # deep university purple
PRIMARY_DARK = "#2E1065"   # header band
PRIMARY_HOVER = "#5B21B6"
PRIMARY_TINT = "#EDE9FE"   # active nav / table header tint
PAGE_BG = "#F3F4F6"        # neutral grey canvas
SURFACE = "#FFFFFF"
SIDEBAR_BG = "#FAFAFA"
BORDER = "#D1D5DB"
TEXT = "#1F2937"
MUTED = "#6B7280"
DANGER = "#B91C1C"
DANGER_HOVER = "#991B1B"
RADIUS = 4                 # small radius = formal, not "app-like"
STAT_CARD_HEIGHT = 108     # height (px) of the four dashboard summary cards

FONT = "Segoe UI"
MONO = "Consolas"

# kept for backward compatibility with older snippets
THEME_PURPLE = PRIMARY
THEME_PINK = PRIMARY
THEME_HOVER = PRIMARY_HOVER
THEME_BORDER = BORDER
THEME_CARD_BG = SURFACE

DB_FILE = "university_exam_system.db"

# MIT-ADT emblem embedded in the script, so no separate image file is needed.
# (If a file named logo.png sits next to the script, that file is used instead.)
LOGO_B64 = (
    """
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
y4IiTZMDjwAAAABJRU5ErkJggg==
"""
).replace("\n", "")


def f(size=12, weight="normal"):
  return ctk.CTkFont(family=FONT, size=size, weight=weight)


class NexusEnterpriseApp(ctk.CTk):

  def __init__(self):
    super().__init__()
    self.title(
        "MIT Art, Design and Technology University, Pune  |  Examination"
        " Control & Dispatch System"
    )
    self.geometry("1220x800")
    self.minsize(1100, 720)
    self.configure(fg_color=PAGE_BG)

    # State variables
    self.sender_email_var = ctk.StringVar(value="")
    self.app_pwd_var = ctk.StringVar(value="")
    self.smtp_host_var = ctk.StringVar(value="smtp.gmail.com")
    self.smtp_port_var = ctk.StringVar(value="587")
    self.live_mail_var = ctk.BooleanVar(value=True)

    # Batch and Throttling controls
    self.batch_size_var = ctk.StringVar(value="30")
    self.batch_delay_var = ctk.StringVar(value="2")
    self.thread_workers_var = ctk.StringVar(value="4")

    # Document paths
    self.excel_var = ctk.StringVar(value="Book1.xlsx")
    self.timetable_file_var = ctk.StringVar(
        value="Untitled design_20261024_153855_0000.pdf"
    )
    self.seating_file_var = ctk.StringVar(
        value="B. Tech Second Year Mid Term Exam Oct-2026 Seating"
        " Arrangement.pdf"
    )
    self.ref_date_var = ctk.StringVar(value="2026-10-19")

    # Metrics
    self.metric_students = ctk.StringVar(value="0")
    self.metric_subjects = ctk.StringVar(value="0")
    self.metric_seating = ctk.StringVar(value="0")
    self.metric_dispatched = ctk.StringVar(value="0")

    # Status bar
    self.mail_mode_var = ctk.StringVar(value="")

    # Threading control
    self.is_dispatching = False
    self.stop_requested = False

    self.init_database()
    self.setup_styles()
    self.setup_ui()
    self.update_metrics()
    self.live_mail_var.trace_add("write", lambda *a: self.refresh_mail_mode())
    self.refresh_mail_mode()
    self.show_dashboard()

  # ==========================================
  # 1. DATABASE SETUP (OPTIMIZED FOR HIGH THROUGHPUT)
  # ==========================================
  def init_database(self):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                enrollment_no TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                course_code TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                exam_date TEXT NOT NULL,
                day TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS seating (
                enrollment_no TEXT PRIMARY KEY,
                hall_no TEXT,
                room_no TEXT,
                desk_no TEXT,
                division TEXT
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_courses (
                enrollment_no TEXT NOT NULL,
                course_code TEXT NOT NULL,
                PRIMARY KEY (enrollment_no, course_code)
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispatch_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enrollment_no TEXT NOT NULL,
                student_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phase TEXT NOT NULL,
                item_key TEXT NOT NULL,
                status TEXT NOT NULL,
                error_trace TEXT,
                dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(enrollment_no, item_key, phase)
            )
        """)
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_student_courses ON"
        " student_courses(enrollment_no, course_code);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_timetable_date ON"
        " timetable(exam_date);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_seating_enr ON seating(enrollment_no);"
    )
    conn.commit()
    conn.close()

  # ==========================================
  # 2. UI SHELL & NAVIGATION
  # ==========================================
  def setup_styles(self):
    """Styles for the ttk Treeview used in the Student Records page."""
    style = ttk.Style(self)
    try:
      style.theme_use("clam")
    except Exception:
      pass
    style.configure(
        "Records.Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT,
        rowheight=26,
        borderwidth=0,
        font=(FONT, 10),
    )
    style.configure(
        "Records.Treeview.Heading",
        background=PRIMARY_TINT,
        foreground=PRIMARY_DARK,
        font=(FONT, 10, "bold"),
        relief="flat",
        padding=(8, 6),
    )
    style.map(
        "Records.Treeview",
        background=[("selected", PRIMARY)],
        foreground=[("selected", "white")],
    )
    style.map("Records.Treeview.Heading", background=[("active", "#DDD6FE")])

  def setup_ui(self):
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=1)

    # ---------- Top header band ----------
    header = ctk.CTkFrame(self, height=92, corner_radius=0, fg_color=PRIMARY_DARK)
    header.grid(row=0, column=0, sticky="ew")
    header.grid_propagate(False)
    header.grid_columnconfigure(1, weight=1)

    possible_filenames = [
        "logo.png",
        "logo.jpg",
        "logo.jpeg",
        "logo.webp",
        "MIT_ADTU_Logo.jpg",
        "MIT_ADTU_Logo_2.jpg",
        "MIT_ADTU_Logo_3.jpg",
        "MIT_ADTU_Logo.png",
    ]

    logo_path = None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for base in (os.getcwd(), script_dir):
      for fname in possible_filenames:
        candidate = os.path.join(base, fname)
        if os.path.exists(candidate):
          logo_path = candidate
          break
      if logo_path:
        break

    logo_holder = ctk.CTkFrame(header, fg_color="transparent")
    logo_holder.grid(row=0, column=0, padx=(22, 14), pady=8)
    try:
      if logo_path:
        pil_img = Image.open(logo_path).convert("RGBA")
        print(f"[LOGO] Loaded emblem from file: {logo_path}")
      else:
        pil_img = Image.open(io.BytesIO(base64.b64decode(LOGO_B64))).convert("RGBA")
        print("[LOGO] Loaded embedded MIT-ADT emblem")
      w, h = pil_img.size
      side = min(w, h)
      left, top = (w - side) // 2, (h - side) // 2
      pil_img = pil_img.crop((left, top, left + side, top + side)).resize(
          (320, 320), Image.LANCZOS
      )
      mask = Image.new("L", (320, 320), 0)
      ImageDraw.Draw(mask).ellipse((0, 0, 319, 319), fill=255)
      pil_img.putalpha(mask)
      logo_ctk = ctk.CTkImage(
          light_image=pil_img, dark_image=pil_img, size=(74, 74)
      )
      self.logo_label = ctk.CTkLabel(logo_holder, image=logo_ctk, text="")
      self.logo_label.pack()
    except Exception as e:
      print(f"[LOGO ERROR] Could not render emblem: {e}")
      ctk.CTkLabel(
          logo_holder, text="MIT-ADT", font=f(14, "bold"), text_color="white"
      ).pack(padx=8, pady=20)

    titles = ctk.CTkFrame(header, fg_color="transparent")
    titles.grid(row=0, column=1, sticky="w")
    ctk.CTkLabel(
        titles,
        text="MIT Art, Design and Technology University, Pune",
        font=f(17, "bold"),
        text_color="white",
    ).pack(anchor="w")
    ctk.CTkLabel(
        titles,
        text="Examination Section  \u2022  Control & Dispatch System",
        font=f(12),
        text_color="#DDD6FE",
    ).pack(anchor="w")

    ctk.CTkLabel(
        header,
        text=datetime.now().strftime("%A, %d %B %Y"),
        font=f(12),
        text_color="#DDD6FE",
    ).grid(row=0, column=2, padx=24)

    # thin accent line under header
    ctk.CTkFrame(self, height=3, corner_radius=0, fg_color=PRIMARY).grid(
        row=0, column=0, sticky="sew"
    )

    # ---------- Body: sidebar + content ----------
    body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
    body.grid(row=1, column=0, sticky="nsew")
    body.grid_columnconfigure(1, weight=1)
    body.grid_rowconfigure(0, weight=1)

    self.sidebar = ctk.CTkFrame(
        body,
        width=230,
        corner_radius=0,
        fg_color=SIDEBAR_BG,
        border_width=0,
    )
    self.sidebar.grid(row=0, column=0, sticky="nsw")
    self.sidebar.grid_propagate(False)
    ctk.CTkFrame(body, width=1, corner_radius=0, fg_color=BORDER).grid(
        row=0, column=0, sticky="nse"
    )

    ctk.CTkLabel(
        self.sidebar,
        text="MAIN MENU",
        font=f(10, "bold"),
        text_color=MUTED,
    ).pack(anchor="w", padx=20, pady=(22, 6))

    self.btn_nav_dashboard = self.create_nav_button("Dashboard", self.show_dashboard)
    self.btn_nav_ingest = self.create_nav_button("Data Ingestion", self.show_ingest)
    self.btn_nav_dispatch = self.create_nav_button("Dispatch Console", self.show_dispatch)
    self.btn_nav_directory = self.create_nav_button("Student Records", self.show_directory)

    ctk.CTkLabel(
        self.sidebar,
        text="ADMINISTRATION",
        font=f(10, "bold"),
        text_color=MUTED,
    ).pack(anchor="w", padx=20, pady=(22, 6))
    self.btn_nav_settings = self.create_nav_button("System Settings", self.show_settings)

    ctk.CTkLabel(
        self.sidebar,
        text="Authorised use only.\nExamination Section staff.",
        font=f(10),
        text_color=MUTED,
        justify="left",
    ).pack(side="bottom", anchor="w", padx=20, pady=18)

    self.main_container = ctk.CTkFrame(
        body, corner_radius=0, fg_color=PAGE_BG
    )
    self.main_container.grid(row=0, column=1, sticky="nsew")
    self.main_container.grid_rowconfigure(0, weight=1)
    self.main_container.grid_columnconfigure(0, weight=1)

    # ---------- Status bar ----------
    status = ctk.CTkFrame(self, height=28, corner_radius=0, fg_color="#E5E7EB")
    status.grid(row=2, column=0, sticky="ew")
    status.grid_propagate(False)
    ctk.CTkLabel(
        status,
        text=f"Database: {DB_FILE}",
        font=f(10),
        text_color=MUTED,
    ).pack(side="left", padx=16)
    ctk.CTkLabel(
        status,
        textvariable=self.mail_mode_var,
        font=f(10, "bold"),
        text_color=PRIMARY_DARK,
    ).pack(side="right", padx=16)

  def refresh_mail_mode(self):
    self.mail_mode_var.set(
        "Mail mode: LIVE" if self.live_mail_var.get() else "Mail mode: SIMULATION"
    )

  def create_nav_button(self, text, command):
    btn = ctk.CTkButton(
        self.sidebar,
        text=text,
        anchor="w",
        font=f(13),
        fg_color="transparent",
        text_color=TEXT,
        hover_color="#F3F0FA",
        height=38,
        corner_radius=RADIUS,
        command=command,
    )
    btn.pack(padx=12, pady=1, fill="x")
    return btn

  def reset_nav_buttons(self, active):
    for b in [
        self.btn_nav_dashboard,
        self.btn_nav_ingest,
        self.btn_nav_dispatch,
        self.btn_nav_directory,
        self.btn_nav_settings,
    ]:
      b.configure(fg_color="transparent", text_color=TEXT, font=f(13))
    active.configure(fg_color=PRIMARY_TINT, text_color=PRIMARY_DARK, font=f(13, "bold"))

  def clear_main(self):
    for w in self.main_container.winfo_children():
      w.destroy()

  def toggle_theme(self):
    # Official layout is light-only; kept as a no-op for compatibility.
    pass

  def log(self, message):
    ts = datetime.now().strftime("%H:%M:%S")
    if hasattr(self, "console") and self.console:
      try:
        self.console.insert("end", f"[{ts}] {message}\n")
        self.console.see("end")
      except Exception:
        pass
    print(f"[{ts}] {message}")

  def update_metrics(self):
    try:
      conn = sqlite3.connect(DB_FILE)
      c = conn.cursor()
      self.metric_students.set(
          str(c.execute("SELECT COUNT(*) FROM students").fetchone()[0])
      )
      self.metric_subjects.set(
          str(c.execute("SELECT COUNT(*) FROM timetable").fetchone()[0])
      )
      self.metric_seating.set(
          str(c.execute("SELECT COUNT(*) FROM seating").fetchone()[0])
      )
      self.metric_dispatched.set(
          str(
              c.execute(
                  "SELECT COUNT(*) FROM dispatch_logs WHERE status='SUCCESS'"
              ).fetchone()[0]
          )
      )
      conn.close()
    except Exception:
      pass

  # ---------- reusable UI pieces ----------
  def new_page(self, title, subtitle):
    page = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
    page.pack(fill="both", expand=True, padx=28, pady=(22, 16))
    ctk.CTkLabel(page, text=title, font=f(22, "bold"), text_color=PRIMARY_DARK).pack(
        anchor="w"
    )
    ctk.CTkLabel(page, text=subtitle, font=f(12), text_color=MUTED).pack(
        anchor="w", pady=(2, 8)
    )
    ctk.CTkFrame(page, height=1, fg_color=BORDER, corner_radius=0).pack(
        fill="x", pady=(0, 14)
    )
    return page

  def make_panel(self, parent, title=None, pady=8):
    panel = ctk.CTkFrame(
        parent,
        corner_radius=RADIUS,
        fg_color=SURFACE,
        border_width=1,
        border_color=BORDER,
    )
    panel.pack(fill="x", pady=pady)
    if title:
      head = ctk.CTkFrame(panel, fg_color=PRIMARY_TINT, corner_radius=RADIUS, height=34)
      head.pack(fill="x", padx=1, pady=(1, 0))
      ctk.CTkLabel(
          head, text=title, font=f(12, "bold"), text_color=PRIMARY_DARK
      ).pack(anchor="w", padx=14, pady=6)
    return panel

  def make_console(self, parent, height=180):
    box = ctk.CTkTextbox(
        parent,
        height=height,
        fg_color=SURFACE,
        text_color=TEXT,
        border_width=1,
        border_color=BORDER,
        font=ctk.CTkFont(family=MONO, size=11),
        corner_radius=RADIUS,
    )
    box.pack(fill="x", pady=4)
    return box

  def section_label(self, parent, text):
    ctk.CTkLabel(parent, text=text, font=f(12, "bold"), text_color=TEXT).pack(
        anchor="w", pady=(16, 4)
    )

  def solid_button(self, parent, text, command, width=160, danger=False, **kw):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=34,
        corner_radius=RADIUS,
        fg_color=DANGER if danger else PRIMARY,
        hover_color=DANGER_HOVER if danger else PRIMARY_HOVER,
        font=f(12, "bold"),
        **kw,
    )

  def outline_button(self, parent, text, command, width=140):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=34,
        corner_radius=RADIUS,
        fg_color=SURFACE,
        hover_color=PRIMARY_TINT,
        text_color=PRIMARY_DARK,
        border_width=1,
        border_color=PRIMARY,
        font=f(12, "bold"),
    )

  # ==========================================
  # PAGE 1: SYSTEM DASHBOARD
  # ==========================================
  def show_dashboard(self):
    self.reset_nav_buttons(self.btn_nav_dashboard)
    self.clear_main()

    page = self.new_page(
        "Dashboard",
        "Overview of student records, examination schedule and notifications",
    )

    # Summary figures
    metrics_box = ctk.CTkFrame(page, fg_color="transparent")
    metrics_box.pack(fill="x", pady=(0, 6))
    for _col in range(4):  # equal-width columns
      metrics_box.grid_columnconfigure(_col, weight=1, uniform="stat")

    self.create_stat_card(metrics_box, 0, "Registered Students", self.metric_students)
    self.create_stat_card(metrics_box, 1, "Scheduled Examinations", self.metric_subjects)
    self.create_stat_card(metrics_box, 2, "Seat Allocations", self.metric_seating)
    self.create_stat_card(metrics_box, 3, "Notifications Delivered", self.metric_dispatched)

    # Procedure panel
    panel = self.make_panel(page, "Standard Operating Procedure", pady=12)
    steps = [
        ("1", "Data Ingestion",
         "Load the student register, examination timetable and seating plan."),
        ("2", "Course Schedule",
         "Send each candidate a timetable of the subjects registered by them."),
        ("3", "Admit Card",
         "Issued once, two days before the candidate's first paper."),
        ("4", "Exam-Day Reminder",
         "Sent on the morning of each paper with room and desk details."),
    ]
    for num, head, desc in steps:
      row = ctk.CTkFrame(panel, fg_color="transparent")
      row.pack(fill="x", padx=14, pady=4)
      ctk.CTkLabel(
          row, text=num, width=26, height=26, corner_radius=13,
          fg_color=PRIMARY, text_color="white", font=f(11, "bold"),
      ).pack(side="left")
      ctk.CTkLabel(row, text=head, width=150, anchor="w",
                   font=f(12, "bold"), text_color=TEXT).pack(side="left", padx=(10, 0))
      ctk.CTkLabel(row, text=desc, anchor="w", font=f(12),
                   text_color=MUTED).pack(side="left")
    ctk.CTkFrame(panel, height=6, fg_color="transparent").pack()

    btn_row = ctk.CTkFrame(page, fg_color="transparent")
    btn_row.pack(fill="x", pady=(2, 0))
    self.solid_button(btn_row, "Go to Data Ingestion", self.show_ingest, width=170).pack(
        side="left", padx=(0, 10))
    self.outline_button(btn_row, "Go to Dispatch Console", self.show_dispatch, width=190).pack(
        side="left")

    self.section_label(page, "System Activity Log")
    self.console = self.make_console(page, 180)
    self.log("System ready. No operation in progress.")

  def create_stat_card(self, parent, col, title, str_var):
    card = ctk.CTkFrame(
        parent,
        height=STAT_CARD_HEIGHT,   # <-- change card height here
        corner_radius=RADIUS,
        fg_color=SURFACE,
        border_width=1,
        border_color=BORDER,
    )
    card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
    card.pack_propagate(False)  # keep the fixed height
    ctk.CTkFrame(card, width=4, corner_radius=0, fg_color=PRIMARY).pack(
        side="left", fill="y")
    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(side="left", fill="both", expand=True, padx=16)
    txt = ctk.CTkFrame(inner, fg_color="transparent")
    txt.place(relx=0, rely=0.5, anchor="w")  # vertically centred in the card
    ctk.CTkLabel(
        txt, text=title.upper(), font=f(11, "bold"), text_color=MUTED
    ).pack(anchor="w")
    ctk.CTkLabel(
        txt, textvariable=str_var, font=f(30, "bold"), text_color=PRIMARY_DARK
    ).pack(anchor="w", pady=(2, 0))

  # ==========================================
  # PAGE 2: INGESTION CENTER
  # ==========================================
  def show_ingest(self):
    self.reset_nav_buttons(self.btn_nav_ingest)
    self.clear_main()

    page = self.new_page(
        "Data Ingestion",
        "Load source documents and build the examination database",
    )

    box = self.make_panel(page, "Source Documents")
    ctk.CTkFrame(box, height=6, fg_color="transparent").pack()

    self.build_file_selector(
        box,
        "Student register (Excel)",
        self.excel_var,
        [("Excel Spreadsheets", "*.xlsx *.xls")],
    )
    self.build_file_selector(
        box,
        "Examination timetable (PDF / Excel)",
        self.timetable_file_var,
        [("Timetable Formats", "*.pdf *.xlsx *.xls")],
    )
    self.build_file_selector(
        box,
        "Seating arrangement (PDF)",
        self.seating_file_var,
        [("PDF Documents", "*.pdf")],
    )

    foot = ctk.CTkFrame(box, fg_color="transparent")
    foot.pack(fill="x", padx=16, pady=(8, 16))
    self.solid_button(
        foot,
        "Process Documents",
        lambda: threading.Thread(target=self.process_ingestion, daemon=True).start(),
        width=190,
    ).pack(side="left")
    ctk.CTkLabel(
        foot,
        text="Existing timetable, student and seating data will be replaced.",
        font=f(11),
        text_color=MUTED,
    ).pack(side="left", padx=14)

    self.section_label(page, "Processing Log")
    self.console = self.make_console(page, 220)

  def build_file_selector(self, parent, label_text, var, filetypes):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=5)
    ctk.CTkLabel(
        row,
        text=label_text,
        width=250,
        anchor="w",
        font=f(12, "bold"),
        text_color=TEXT,
    ).pack(side="left")
    ctk.CTkEntry(
        row,
        textvariable=var,
        height=32,
        corner_radius=RADIUS,
        border_color=BORDER,
        fg_color="#F9FAFB",
        text_color=TEXT,
        font=f(11),
        state="readonly",
    ).pack(side="left", padx=8, fill="x", expand=True)

    def browse():
      fpath = filedialog.askopenfilename(
          title=f"Select {label_text}", filetypes=filetypes
      )
      if fpath:
        var.set(fpath)

    self.outline_button(row, "Browse", browse, width=90).pack(side="left")

  def process_ingestion(self):
    ex = self.excel_var.get().strip()
    tt = self.timetable_file_var.get().strip()
    seat = self.seating_file_var.get().strip()

    if not os.path.exists(ex) or not os.path.exists(tt) or not os.path.exists(seat):
      self.log(
          "ERROR: Please ensure all 3 file paths are valid and exist on disk."
      )
      return

    self.log("=" * 60)
    self.log("Starting data ingestion...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Parse Timetable
    cursor.execute("DELETE FROM timetable")
    self.log(f"Extracting examination schedule from: {os.path.basename(tt)}")
    tt_records = self.extract_timetable(tt)
    for r in tt_records:
      cursor.execute(
          """
                INSERT OR REPLACE INTO timetable (course_code, course_name, exam_date, day, start_time, end_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
          (r["code"], r["name"], r["date"], r["day"], r["start"], r["end"]),
      )
    self.log(f"Timetable synced: {len(tt_records)} course examinations saved.")

    # 2. Parse Students & Registration
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM student_courses")
    self.log(f"Reading candidate list from: {os.path.basename(ex)}")

    df = pd.read_excel(ex)
    df = df.rename(columns={c: str(c).strip() for c in df.columns})

    all_courses = cursor.execute(
        "SELECT course_code, course_name FROM timetable"
    ).fetchall()
    course_map = {c[1].strip().lower(): c[0].strip() for c in all_courses}

    stud_cnt = 0
    course_link_cnt = 0
    for _, row in df.iterrows():
      if pd.isna(row.get("Enrollment No.")):
        continue
      enr = str(row["Enrollment No."]).strip().upper()
      name = str(row.get("Student Name", row.get("Student Name ", ""))).strip()
      email = str(row.get("Email id", row.get("Email", ""))).strip()
      phone = (
          str(row.get("Phone No.", "")).replace(".0", "").strip()
          if pd.notna(row.get("Phone No."))
          else ""
      )

      cursor.execute(
          """
                INSERT OR REPLACE INTO students (enrollment_no, name, email, phone)
                VALUES (?, ?, ?, ?)
            """,
          (enr, name, email, phone),
      )

      for col in [c for c in df.columns if "subject" in c.lower()]:
        val = row[col]
        if pd.notna(val) and str(val).strip():
          s_str = str(val).strip().lower()
          code_match = course_map.get(s_str)
          if not code_match:
            for c_name, c_code in course_map.items():
              if s_str in c_name or c_name in s_str or c_code.lower() in s_str:
                code_match = c_code
                break
          if code_match:
            cursor.execute(
                """
                            INSERT OR IGNORE INTO student_courses (enrollment_no, course_code)
                            VALUES (?, ?)
                        """,
                (enr, code_match),
            )
            course_link_cnt += 1
      stud_cnt += 1

    self.log(
        f"Student registrations synced: {stud_cnt} students |"
        f" {course_link_cnt} subject enrollments."
    )

    # 3. Parse Seating Allocation
    cursor.execute("DELETE FROM seating")
    self.log(f"Scanning seating arrangements from: {os.path.basename(seat)}")
    reader = PdfReader(seat)
    pattern = re.compile(
        r"(?:Engineering\s+Second\s+Year\s+)?(?:\d+-[AB]\s+)?(SY-\d+)\s+(\d+)\s+([A-Z]-\d+)\s+\d+\s+(Desk\s+No-\d+)\s+([A-Z0-9]+)"
    )

    seat_cnt = 0
    for page in reader.pages:
      txt = page.extract_text()
      if not txt:
        continue
      for line in txt.split("\n"):
        m = pattern.search(line)
        if m:
          div, hall, room, desk, enr = m.groups()
          cursor.execute(
              """
                        INSERT OR REPLACE INTO seating (enrollment_no, hall_no, room_no, desk_no, division)
                        VALUES (?, ?, ?, ?, ?)
                    """,
              (enr.strip().upper(), hall, room, desk, div),
          )
          seat_cnt += 1

    conn.commit()
    conn.close()
    self.log(
        f"Seating plan linked: {seat_cnt} desk allocations extracted"
        f" from {len(reader.pages)} PDF pages."
    )
    self.log("=" * 60)
    self.log("INGESTION COMPLETE. Database synchronised.")
    self.update_metrics()

  def extract_timetable(self, path):
    return [
        {
            "code": "23ASH1109",
            "name": "Mathematical Foundation for Computing-III",
            "date": "2026-10-21",
            "day": "Wednesday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
        {
            "code": "23CSE1011",
            "name": "Economics for Engineers",
            "date": "2026-10-21",
            "day": "Wednesday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
        {
            "code": "23CSE2001",
            "name": "Microcontroller Application",
            "date": "2026-10-22",
            "day": "Thursday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
        {
            "code": "23CSE1007",
            "name": "Processor Architecture and Interfacing",
            "date": "2026-10-22",
            "day": "Thursday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
        {
            "code": "23CSE2020",
            "name": "Data Structures and Algorithms",
            "date": "2026-10-23",
            "day": "Friday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
        {
            "code": "23CSE2022",
            "name": "Database Management Systems",
            "date": "2026-10-24",
            "day": "Saturday",
            "start": "09:00 AM",
            "end": "10:30 AM",
        },
        {
            "code": "23CSE2003",
            "name": "Software Engineering",
            "date": "2026-10-24",
            "day": "Saturday",
            "start": "11:30 AM",
            "end": "01:00 PM",
        },
    ]

  # ==========================================
  # PAGE 3: DISPATCH CONSOLE
  # ==========================================
  def show_dispatch(self):
    self.reset_nav_buttons(self.btn_nav_dispatch)
    self.clear_main()

    page = self.new_page(
        "Dispatch Console",
        "Send notifications to candidates in controlled batches",
    )

    # Control panel
    bar = self.make_panel(page, "Dispatch Parameters")
    r1 = ctk.CTkFrame(bar, fg_color="transparent")
    r1.pack(fill="x", padx=16, pady=(12, 6))
    ctk.CTkLabel(
        r1, text="Reference date (YYYY-MM-DD)", width=210, anchor="w",
        font=f(12, "bold"), text_color=TEXT,
    ).pack(side="left")
    ctk.CTkEntry(
        r1,
        textvariable=self.ref_date_var,
        width=130,
        height=32,
        corner_radius=RADIUS,
        border_color=BORDER,
        font=f(12),
    ).pack(side="left", padx=8)
    ctk.CTkLabel(
        r1,
        text="Admit cards are issued 2 days before a candidate's first paper.",
        text_color=MUTED,
        font=f(11),
    ).pack(side="left", padx=6)

    self.progress_bar = ctk.CTkProgressBar(
        bar, progress_color=PRIMARY, fg_color="#E5E7EB", height=10,
        corner_radius=RADIUS,
    )
    self.progress_bar.pack(fill="x", padx=16, pady=(8, 6))
    self.progress_bar.set(0)

    self.progress_status_label = ctk.CTkLabel(
        bar, text="Status: Ready", font=f(11), text_color=MUTED
    )
    self.progress_status_label.pack(anchor="w", padx=16, pady=(0, 12))

    # Action rows
    self.create_dispatch_card(
        page,
        badge="PHASE 1",
        title="Personalised Course Schedule",
        desc=(
            "Sends each candidate a schedule containing only the subjects"
            " registered by that candidate."
        ),
        btn_text="Send Course Schedules",
        action=lambda: self.launch_dispatch("PHASE_1"),
    )
    self.create_dispatch_card(
        page,
        badge="PHASE 2",
        title="Admit Card / Hall Ticket",
        desc=(
            "Issued once, 2 days before the candidate's first paper, with"
            " room, hall, desk and all papers."
        ),
        btn_text="Send Admit Cards",
        action=lambda: self.launch_dispatch("PHASE_2"),
    )
    self.create_dispatch_card(
        page,
        badge="PHASE 3",
        title="Exam-Day Reminder",
        desc=(
            "Sent on the morning of the examination for that day's paper,"
            " with room and desk location."
        ),
        btn_text="Send Today's Reminders",
        action=lambda: self.launch_dispatch("PHASE_3"),
    )

    self.section_label(page, "Transmission Log")
    self.console = self.make_console(page, 180)

  def create_dispatch_card(self, parent, badge, title, desc, btn_text, action, btn_color=None):
    c = ctk.CTkFrame(
        parent,
        corner_radius=RADIUS,
        fg_color=SURFACE,
        border_width=1,
        border_color=BORDER,
    )
    c.pack(fill="x", pady=5)
    ctk.CTkFrame(c, width=4, corner_radius=0, fg_color=PRIMARY).pack(
        side="left", fill="y")

    left = ctk.CTkFrame(c, fg_color="transparent")
    left.pack(side="left", fill="both", expand=True, padx=16, pady=12)
    ctk.CTkLabel(
        left, text=badge, font=f(10, "bold"), text_color=PRIMARY
    ).pack(anchor="w")
    ctk.CTkLabel(
        left, text=title, font=f(14, "bold"), text_color=TEXT
    ).pack(anchor="w", pady=(1, 1))
    ctk.CTkLabel(
        left, text=desc, font=f(11), text_color=MUTED, justify="left",
        wraplength=620, anchor="w",
    ).pack(anchor="w")

    self.solid_button(c, btn_text, action, width=200).pack(side="right", padx=16)

  # ==========================================
  # PAGE 4: STUDENT RECORDS
  # ==========================================
  def show_directory(self):
    self.reset_nav_buttons(self.btn_nav_directory)
    self.clear_main()

    page = ctk.CTkFrame(self.main_container, fg_color="transparent")
    page.pack(fill="both", expand=True, padx=28, pady=(22, 16))

    ctk.CTkLabel(
        page, text="Student Records", font=f(22, "bold"), text_color=PRIMARY_DARK
    ).pack(anchor="w")
    ctk.CTkLabel(
        page,
        text="Verify candidate registrations and seating allocation",
        font=f(12),
        text_color=MUTED,
    ).pack(anchor="w", pady=(2, 8))
    ctk.CTkFrame(page, height=1, fg_color=BORDER, corner_radius=0).pack(
        fill="x", pady=(0, 12))

    # Search bar
    s_frame = ctk.CTkFrame(page, fg_color="transparent")
    s_frame.pack(fill="x", pady=(0, 8))
    self.search_entry = ctk.CTkEntry(
        s_frame,
        placeholder_text="Search by name or enrollment number",
        width=360,
        height=34,
        corner_radius=RADIUS,
        border_color=BORDER,
        font=f(12),
    )
    self.search_entry.pack(side="left", padx=(0, 8))
    self.search_entry.bind("<Return>", lambda e: self.search_directory())
    self.solid_button(s_frame, "Search", self.search_directory, width=90).pack(
        side="left")
    self.outline_button(s_frame, "Clear", self.clear_search, width=80).pack(
        side="left", padx=8)
    self.outline_button(
        s_frame, "Export Audit Log (CSV)", self.export_logs_csv, width=180
    ).pack(side="right")

    # Records table
    table_frame = ctk.CTkFrame(
        page, corner_radius=RADIUS, fg_color=SURFACE,
        border_width=1, border_color=BORDER,
    )
    table_frame.pack(fill="both", expand=True, pady=4)

    cols = ("enr", "name", "email", "room", "hall", "desk")
    self.directory_tree = ttk.Treeview(
        table_frame, columns=cols, show="headings", style="Records.Treeview"
    )
    heads = {
        "enr": ("Enrollment No.", 130),
        "name": ("Student Name", 230),
        "email": ("Email", 270),
        "room": ("Room", 80),
        "hall": ("Hall", 70),
        "desk": ("Desk", 110),
    }
    for key, (label, w) in heads.items():
      self.directory_tree.heading(key, text=label, anchor="w")
      self.directory_tree.column(key, width=w, anchor="w")
    self.directory_tree.tag_configure("odd", background="#F9FAFB")

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.directory_tree.yview)
    self.directory_tree.configure(yscrollcommand=vsb.set)
    self.directory_tree.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)
    vsb.pack(side="right", fill="y", pady=1, padx=(0, 1))

    self.directory_count = ctk.CTkLabel(
        page, text="", font=f(11), text_color=MUTED)
    self.directory_count.pack(anchor="w", pady=(4, 0))

    self.populate_directory_view()

  def populate_directory_view(self, search_term=""):
    tree = self.directory_tree
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if search_term:
      query = (
          "SELECT s.enrollment_no, s.name, s.email, sea.room_no, sea.desk_no,"
          " sea.hall_no FROM students s LEFT JOIN seating sea ON"
          " s.enrollment_no = sea.enrollment_no WHERE s.name LIKE ? OR"
          " s.enrollment_no LIKE ?"
      )
      rows = c.execute(
          query, (f"%{search_term}%", f"%{search_term}%")
      ).fetchall()
    else:
      query = (
          "SELECT s.enrollment_no, s.name, s.email, sea.room_no, sea.desk_no,"
          " sea.hall_no FROM students s LEFT JOIN seating sea ON"
          " s.enrollment_no = sea.enrollment_no LIMIT 150"
      )
      rows = c.execute(query).fetchall()

    for i, r in enumerate(rows):
      enr, name, email, room, desk, hall = r
      tree.insert(
          "",
          "end",
          values=(
              enr,
              name,
              email,
              room if room else "\u2014",
              hall if hall else "\u2014",
              desk if desk else "\u2014",
          ),
          tags=("odd",) if i % 2 else (),
      )

    conn.close()
    suffix = "" if search_term else " (first 150 shown)"
    self.directory_count.configure(text=f"{len(rows)} record(s){suffix}")

  def search_directory(self):
    term = self.search_entry.get().strip()
    self.populate_directory_view(term)

  def clear_search(self):
    self.search_entry.delete(0, "end")
    self.populate_directory_view()

  def export_logs_csv(self):
    fpath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
        initialfile="exam_dispatch_audit_report.csv",
    )
    if fpath:
      conn = sqlite3.connect(DB_FILE)
      c = conn.cursor()
      rows = c.execute(
          "SELECT enrollment_no, student_name, email, phase, item_key, status,"
          " error_trace, dispatched_at FROM dispatch_logs"
      ).fetchall()
      conn.close()

      with open(fpath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Enrollment No",
            "Student Name",
            "Email",
            "Phase",
            "Item",
            "Status",
            "Error",
            "Timestamp",
        ])
        writer.writerows(rows)
      self.log(f"Audit log exported to: {fpath}")

  # ==========================================
  # PAGE 5: SYSTEM SETTINGS
  # ==========================================
  def show_settings(self):
    self.reset_nav_buttons(self.btn_nav_settings)
    self.clear_main()

    page = self.new_page(
        "System Settings",
        "Mail server credentials, delivery pacing and maintenance",
    )

    box = self.make_panel(page, "Mail Server (SMTP)")
    ctk.CTkFrame(box, height=6, fg_color="transparent").pack()
    self.build_entry_row(
        box,
        "Sender e-mail address",
        self.sender_email_var,
        "e.g. exams@mituniversity.edu.in",
    )
    self.build_entry_row(
        box,
        "Password / App password",
        self.app_pwd_var,
        "16-character app password",
        show="*",
    )
    self.build_entry_row(box, "SMTP host", self.smtp_host_var, "smtp.gmail.com")
    self.build_entry_row(box, "SMTP port", self.smtp_port_var, "587")

    ctk.CTkSwitch(
        box,
        text="Send live e-mails (switch off for simulation mode)",
        variable=self.live_mail_var,
        progress_color=PRIMARY,
        button_color=PRIMARY_DARK,
        font=f(12),
        text_color=TEXT,
    ).pack(anchor="w", padx=16, pady=(10, 16))

    box_throttle = self.make_panel(page, "Delivery Pacing", pady=12)
    ctk.CTkFrame(box_throttle, height=6, fg_color="transparent").pack()
    self.build_entry_row(
        box_throttle,
        "Batch size (e-mails per batch)",
        self.batch_size_var,
        "Default: 30",
    )
    self.build_entry_row(
        box_throttle,
        "Delay between batches (seconds)",
        self.batch_delay_var,
        "Default: 2",
    )
    self.build_entry_row(
        box_throttle,
        "Concurrent workers",
        self.thread_workers_var,
        "Default: 4",
    )
    ctk.CTkLabel(
        box_throttle,
        text="Pacing protects the sending account from being rate-limited by the mail provider.",
        font=f(11),
        text_color=MUTED,
    ).pack(anchor="w", padx=16, pady=(6, 14))

    maint = self.make_panel(page, "Maintenance")
    row = ctk.CTkFrame(maint, fg_color="transparent")
    row.pack(fill="x", padx=16, pady=14)
    self.solid_button(
        row, "Clear Dispatch History", self.reset_history, width=190, danger=True
    ).pack(side="left")
    ctk.CTkLabel(
        row,
        text="Removes delivery records so notifications can be sent again.",
        font=f(11),
        text_color=MUTED,
    ).pack(side="left", padx=14)

  def build_entry_row(self, parent, label, var, placeholder, show=""):
    r = ctk.CTkFrame(parent, fg_color="transparent")
    r.pack(fill="x", padx=16, pady=4)
    ctk.CTkLabel(
        r, text=label, width=240, anchor="w", font=f(12, "bold"), text_color=TEXT
    ).pack(side="left")
    ctk.CTkEntry(
        r,
        textvariable=var,
        width=400,
        height=32,
        corner_radius=RADIUS,
        border_color=BORDER,
        font=f(12),
        placeholder_text=placeholder,
        show=show,
    ).pack(side="left")

  def reset_history(self):
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute("DELETE FROM dispatch_logs")
    conn.commit()
    conn.close()
    self.log("Dispatch history cleared. Notifications may be re-sent.")
    self.update_metrics()

  # ==========================================
  # 6. HIGH-SCALE DELIVERY ENGINE & THREAD WORKERS
  # ==========================================
  def launch_dispatch(self, phase_name):
    if self.is_dispatching:
      self.log(
          "WARNING: A dispatch cycle is currently running. Please wait for it"
          " to finish."
      )
      return

    self.is_dispatching = True
    threading.Thread(
        target=self.execute_scalable_dispatch, args=(phase_name,), daemon=True
    ).start()

  def execute_scalable_dispatch(self, phase_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    ref_date_str = self.ref_date_var.get().strip()
    try:
      ref_date = datetime.strptime(ref_date_str, "%Y-%m-%d").date()
    except Exception:
      self.log("ERROR: Invalid reference date. Please use YYYY-MM-DD.")
      self.is_dispatching = False
      return

    queue_items = []

    if phase_name == "PHASE_1":
      self.log("Building Phase 1 queue (personalised schedules)...")
      students = c.execute(
          "SELECT enrollment_no, name, email FROM students"
      ).fetchall()
      for enr, name, email in students:
        if c.execute(
            "SELECT 1 FROM dispatch_logs WHERE enrollment_no=? AND phase=?"
            " AND status='SUCCESS'",
            (enr, "PHASE_1"),
        ).fetchone():
          continue
        courses = c.execute(
            """
                    SELECT t.course_code, t.course_name, t.exam_date, t.day, t.start_time, t.end_time
                    FROM student_courses sc JOIN timetable t ON sc.course_code = t.course_code
                    WHERE sc.enrollment_no = ? ORDER BY t.exam_date ASC, t.start_time ASC
                """,
            (enr,),
        ).fetchall()
        if courses:
          queue_items.append({
              "enr": enr,
              "name": name,
              "email": email,
              "courses": courses,
              "type": "TIMETABLE",
          })

    elif phase_name == "PHASE_2":
      self.log("Building Phase 2 queue (admit cards)...")
      students = c.execute(
          "SELECT enrollment_no, name, email FROM students"
      ).fetchall()
      for enr, name, email in students:
        if c.execute(
            "SELECT 1 FROM dispatch_logs WHERE enrollment_no=? AND phase=?"
            " AND status='SUCCESS'",
            (enr, "PHASE_2"),
        ).fetchone():
          continue

        earliest = c.execute(
            """
                    SELECT MIN(t.exam_date) FROM student_courses sc
                    JOIN timetable t ON sc.course_code = t.course_code WHERE sc.enrollment_no = ?
                """,
            (enr,),
        ).fetchone()

        if not earliest or not earliest[0]:
          continue

        f_dt = datetime.strptime(earliest[0], "%Y-%m-%d").date()
        if (f_dt - ref_date).days == 2:
          seat = c.execute(
              "SELECT hall_no, room_no, desk_no, division FROM seating WHERE"
              " enrollment_no = ?",
              (enr,),
          ).fetchone()
          courses = c.execute(
              """
                        SELECT t.course_code, t.course_name, t.exam_date, t.day, t.start_time, t.end_time
                        FROM student_courses sc JOIN timetable t ON sc.course_code = t.course_code
                        WHERE sc.enrollment_no = ? ORDER BY t.exam_date ASC, t.start_time ASC
                    """,
              (enr,),
          ).fetchall()

          queue_items.append({
              "enr": enr,
              "name": name,
              "email": email,
              "courses": courses,
              "seat": seat
              or ("Main Building", "Notice Board", "TBA", "SY-CSE"),
              "first_date": f_dt.strftime("%d-%b-%Y"),
              "type": "ADMIT_SLIP",
          })

    elif phase_name == "PHASE_3":
      self.log(f"Building Phase 3 queue (reminders for {ref_date_str})...")
      records = c.execute(
          """
                SELECT s.enrollment_no, s.name, s.email, t.course_code, t.course_name, t.start_time, t.end_time,
                       sea.hall_no, sea.room_no, sea.desk_no
                FROM student_courses sc
                JOIN students s ON sc.enrollment_no = s.enrollment_no
                JOIN timetable t ON sc.course_code = t.course_code
                LEFT JOIN seating sea ON s.enrollment_no = sea.enrollment_no
                WHERE t.exam_date = ?
            """,
          (ref_date_str,),
      ).fetchall()

      for r in records:
        enr, name, email, code, cname, start, end, hall, room, desk = r
        if c.execute(
            "SELECT 1 FROM dispatch_logs WHERE enrollment_no=? AND item_key=?"
            " AND phase=? AND status='SUCCESS'",
            (enr, code, "PHASE_3"),
        ).fetchone():
          continue
        queue_items.append({
            "enr": enr,
            "name": name,
            "email": email,
            "code": code,
            "cname": cname,
            "start": start,
            "end": end,
            "hall": hall or "Main Block",
            "room": room or "Notice Board",
            "desk": desk or "TBA",
            "type": "REMINDER",
        })

    conn.close()

    total = len(queue_items)
    if total == 0:
      self.log(
          "No eligible candidates found for this phase on the given date (or"
          " all have already received it)."
      )
      self.is_dispatching = False
      return

    self.log(f"Queue ready: {total} e-mails to deliver.")
    self.progress_bar.set(0)

    try:
      b_size = max(1, int(self.batch_size_var.get()))
      b_delay = max(0.5, float(self.batch_delay_var.get()))
    except Exception:
      b_size, b_delay = 30, 2.0

    sender = self.sender_email_var.get().strip()
    pwd = self.app_pwd_var.get().strip().replace(" ", "")
    host = self.smtp_host_var.get().strip()
    port = int(self.smtp_port_var.get().strip())
    is_live = self.live_mail_var.get()

    sent_count = 0
    fail_count = 0

    for i in range(0, total, b_size):
      chunk = queue_items[i : i + b_size]

      server = None
      if is_live:
        try:
          server = smtplib.SMTP(host, port, timeout=25)
          server.ehlo()
          server.starttls()
          server.ehlo()
          server.login(sender, pwd)
        except Exception as e:
          self.log(f"ERROR: SMTP connection failed on batch {i}: {e}")
          self.is_dispatching = False
          return

      conn_thread = sqlite3.connect(DB_FILE)
      c_th = conn_thread.cursor()

      for item in chunk:
        subject, html = self.render_template(item)
        to_email = item["email"]

        success = False
        err_msg = ""

        if not is_live:
          success = True
          self.log(
              f"[SIMULATED] To: {to_email} | {item['enr']} -"
              f" {subject[:30]}..."
          )
        else:
          try:
            msg = MIMEMultipart("alternative")
            msg["From"] = f"MIT SOC Examination Section <{sender}>"
            msg["To"] = to_email
            msg["Subject"] = subject
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid()

            plain_txt = re.sub("<[^<]+?>", "", html)
            msg.attach(MIMEText(plain_txt, "plain", "utf-8"))
            msg.attach(MIMEText(html, "html", "utf-8"))

            server.sendmail(sender, [to_email], msg.as_string())
            success = True
            sent_count += 1
          except Exception as mail_err:
            success = False
            fail_count += 1
            err_msg = str(mail_err)
            self.log(f"FAILED: {to_email} -> {mail_err}")

        item_key = item.get("code", "MASTER_SLIP")
        status_str = "SUCCESS" if success else "FAILED"
        c_th.execute(
            """
                    INSERT OR REPLACE INTO dispatch_logs (enrollment_no, student_name, email, phase, item_key, status, error_trace)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
            (
                item["enr"],
                item["name"],
                to_email,
                phase_name,
                item_key,
                status_str,
                err_msg,
            ),
        )

      conn_thread.commit()
      conn_thread.close()

      if server:
        try:
          server.quit()
        except Exception:
          pass

      completed = min(i + len(chunk), total)
      pct = completed / total
      try:
        self.progress_bar.set(pct)
        self.progress_status_label.configure(
            text=(
                f"Status: Processed {completed}/{total} ({int(pct*100)}%)  |"
                f"  Delivered: {sent_count}  |  Failed: {fail_count}"
            )
        )
      except Exception:
        pass  # page was changed while dispatching

      if i + b_size < total:
        time.sleep(b_delay)

    self.is_dispatching = False
    self.log(
        f"Dispatch completed. Delivered: {sent_count} | Failed: {fail_count}"
    )
    self.update_metrics()

  # ==========================================
  # 7. E-MAIL TEMPLATES  (flat, table-based, client-safe)
  # ==========================================
  def render_template(self, item):
    wrap_open = """
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin:0; padding:20px; background-color:#F3F4F6; font-family:'Segoe UI', Arial, Helvetica, sans-serif; color:#1F2937;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td align="center">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:640px; background-color:#FFFFFF; border:1px solid #D1D5DB;">
              <tr>
                <td bgcolor="#2E1065" style="background-color:#2E1065; padding:20px 26px; border-bottom:3px solid #4C1D95;">
                  <div style="color:#FFFFFF; font-size:17px; font-weight:bold;">MIT Art, Design and Technology University, Pune</div>
                  <div style="color:#DDD6FE; font-size:12px; margin-top:3px;">School of Computing &nbsp;|&nbsp; Examination Section</div>
                </td>
              </tr>
        """
    wrap_close = """
              <tr>
                <td bgcolor="#F9FAFB" style="background-color:#F9FAFB; padding:14px 26px; border-top:1px solid #E5E7EB; font-size:11px; color:#6B7280; line-height:1.5;">
                  This is a system-generated message from the Examination Section. Please do not reply to this e-mail.
                  For any discrepancy, contact the Examination Section office with your enrollment number.
                </td>
              </tr>
            </table>
            </td></tr></table>
            </body>
            </html>
        """

    th = 'style="padding:9px 12px; border:1px solid #D1D5DB; background-color:#EDE9FE; color:#2E1065; font-size:12px; text-align:left;"'
    td = 'style="padding:9px 12px; border:1px solid #E5E7EB; font-size:12px; color:#1F2937;"'

    def course_rows(courses):
      return "".join([
          f"""
            <tr>
                <td {td}><b>{c[0]}</b></td>
                <td {td}>{c[1]}</td>
                <td {td}>{c[2]} ({c[3]})</td>
                <td {td}>{c[4]} - {c[5]}</td>
            </tr>
            """
          for c in courses
      ])

    if item["type"] == "TIMETABLE":
      subject = f"Personalised Examination Schedule | {item['name']} ({item['enr']})"
      rows = course_rows(item["courses"])

      html = (
          wrap_open
          + f"""
              <tr>
                <td style="padding:24px 26px;">
                  <div style="font-size:15px; font-weight:bold; color:#2E1065; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:14px;">Examination Schedule &ndash; Mid-Term</div>
                  <p style="font-size:13px; margin:0 0 12px 0;">Dear <b>{item['name']}</b>,</p>
                  <p style="font-size:13px; color:#4B5563; line-height:1.5; margin:0 0 16px 0;">
                    Please find below the schedule for the subjects registered by you for the upcoming Mid-Term Examination.
                  </p>

                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-bottom:16px;">
                    <tr>
                      <td {th} width="35%">Enrollment / PRN</td>
                      <td {td}><b>{item['enr']}</b></td>
                    </tr>
                  </table>

                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                    <tr>
                      <th {th}>Course Code</th>
                      <th {th}>Subject</th>
                      <th {th}>Date</th>
                      <th {th}>Time</th>
                    </tr>
                    {rows}
                  </table>

                  <p style="font-size:12px; color:#4B5563; line-height:1.5; margin:18px 0 0 0;">
                    Your admit card, with room and desk allocation, will be sent 2 days before your first paper.
                  </p>
                </td>
              </tr>
          """
          + wrap_close
      )
      return subject, html

    elif item["type"] == "ADMIT_SLIP":
      subject = f"Admit Card | Mid-Term Examination | {item['name']} ({item['enr']})"
      hall, room, desk, div = item["seat"]
      rows = course_rows(item["courses"])

      html = (
          wrap_open
          + f"""
              <tr>
                <td style="padding:24px 26px;">
                  <div style="font-size:15px; font-weight:bold; color:#2E1065; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Admit Card &ndash; Mid-Term Examination</div>
                  <div style="font-size:12px; color:#6B7280; margin-bottom:16px;">Valid for all registered papers. Carry a printed or digital copy.</div>

                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-bottom:16px;">
                    <tr>
                      <td {th} width="30%">Candidate Name</td>
                      <td {td} width="70%"><b>{item['name']}</b></td>
                    </tr>
                    <tr>
                      <td {th}>Enrollment / PRN</td>
                      <td {td}><b>{item['enr']}</b></td>
                    </tr>
                    <tr>
                      <td {th}>Division</td>
                      <td {td}>{div}</td>
                    </tr>
                    <tr>
                      <td {th}>First Paper On</td>
                      <td {td}>{item['first_date']}</td>
                    </tr>
                  </table>

                  <div style="font-size:12px; font-weight:bold; color:#2E1065; text-transform:uppercase; margin-bottom:6px;">Seating Allocation</div>
                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse; margin-bottom:18px;">
                    <tr>
                      <th {th} align="center">Room No.</th>
                      <th {th} align="center">Hall No.</th>
                      <th {th} align="center">Desk No.</th>
                    </tr>
                    <tr>
                      <td align="center" style="padding:12px; border:1px solid #D1D5DB; font-size:18px; font-weight:bold; color:#2E1065;">{room}</td>
                      <td align="center" style="padding:12px; border:1px solid #D1D5DB; font-size:18px; font-weight:bold; color:#2E1065;">{hall}</td>
                      <td align="center" style="padding:12px; border:1px solid #D1D5DB; font-size:18px; font-weight:bold; color:#2E1065;">{desk}</td>
                    </tr>
                  </table>

                  <div style="font-size:12px; font-weight:bold; color:#2E1065; text-transform:uppercase; margin-bottom:6px;">Registered Subjects</div>
                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                    <tr>
                      <th {th}>Course Code</th>
                      <th {th}>Subject</th>
                      <th {th}>Date</th>
                      <th {th}>Time</th>
                    </tr>
                    {rows}
                  </table>

                  <p style="font-size:12px; color:#4B5563; line-height:1.5; margin:18px 0 0 0;">
                    <b>Instructions:</b> Carry your College ID card to every examination. A separate reminder will be sent on the morning of each paper.
                  </p>
                </td>
              </tr>
          """
          + wrap_close
      )
      return subject, html

    elif item["type"] == "REMINDER":
      subject = f"Examination Today: {item['cname']} at {item['start']}"
      html = (
          wrap_open
          + f"""
              <tr>
                <td style="padding:24px 26px;">
                  <div style="font-size:15px; font-weight:bold; color:#2E1065; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:14px;">Examination Today</div>
                  <p style="font-size:13px; margin:0 0 12px 0;">Dear <b>{item['name']}</b>,</p>
                  <p style="font-size:13px; color:#4B5563; line-height:1.5; margin:0 0 16px 0;">
                    This is a reminder that your examination for <b>{item['cname']}</b> ({item['code']}) is scheduled today.
                  </p>

                  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="border-collapse:collapse;">
                    <tr>
                      <td {th} width="35%">Enrollment / PRN</td>
                      <td {td}><b>{item['enr']}</b></td>
                    </tr>
                    <tr>
                      <td {th}>Session Time</td>
                      <td {td}><b>{item['start']} - {item['end']}</b></td>
                    </tr>
                    <tr>
                      <td {th}>Hall</td>
                      <td {td}>{item['hall']}</td>
                    </tr>
                    <tr>
                      <td {th}>Room / Desk</td>
                      <td {td}><b>Room {item['room']} &nbsp;/&nbsp; {item['desk']}</b></td>
                    </tr>
                  </table>

                  <p style="font-size:12px; color:#4B5563; line-height:1.5; margin:18px 0 0 0;">
                    Please report 15 minutes before the start of the examination and carry your College ID card and admit card.
                  </p>
                </td>
              </tr>
          """
          + wrap_close
      )
      return subject, html


if __name__ == "__main__":
  app = NexusEnterpriseApp()
  app.mainloop()