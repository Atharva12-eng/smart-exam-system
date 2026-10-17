import streamlit as st
import json
import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime, timedelta
import pandas as pd

DB_FILE = "database.json"

st.set_page_config(
    page_title="MIT ADT University | Central Examination Authority",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BASE64 BACKGROUND IMAGE LOADER ---
def get_base64_bg():
    possible_names = [
        "campus.webp", "campus.jpg", "campus.png", 
        "image_9dacdc.webp", "image_9dacdc.jpg", "bg.webp"
    ]
    for fname in possible_names:
        if os.path.exists(fname):
            ext = "webp" if fname.endswith(".webp") else "jpeg"
            with open(fname, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                return f"data:image/{ext};base64,{encoded}"
    return None

bg_data_uri = get_base64_bg()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("#### System Viewport & Sync")
    theme_dark = st.toggle("Enable Dark Room Interface", value=False)
    
    st.markdown("---")
    st.markdown("#### Registry Refresh Controller")
    st.caption("Synchronize database entries instantly without reloading the entire window.")
    if st.button("🔄 Sync & Refresh Registry Now", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown("#### Mail Gateway Credentials")
    st.caption("Secure TLS relay for student notification dispatches.")
    default_sender = os.getenv("SMTP_SENDER_EMAIL", "")
    default_pwd = os.getenv("SMTP_APP_PASSWORD", "")
    sender_email = st.text_input("Institutional SMTP Sender", value=default_sender, placeholder="your_email@gmail.com")
    app_password = st.text_input("Google App Password (16-char)", value=default_pwd, type="password", placeholder="xxxx xxxx xxxx xxxx")
    
    # LIVE CONNECTION TEST BUTTON
    if st.button("⚡ Test Email Gateway Connection", use_container_width=True):
        if not sender_email or not app_password:
            st.error("Please fill both Sender Email and 16-character App Password.")
        else:
            try:
                clean_pwd = app_password.replace(" ", "").strip()
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
                server.starttls()
                server.login(sender_email.strip(), clean_pwd)
                server.quit()
                st.success("✅ Google SMTP Connected Successfully! Credentials are 100% valid.")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")

    st.markdown("---")
    st.markdown("#### Database Maintenance")
    if st.button("Purge Candidate Registry", use_container_width=True):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"students": [], "timetable": []}, f, indent=4)
        st.success("Candidate registry purged successfully.")
        st.rerun()

# --- THEME STYLING ---
if not theme_dark:  # Default Light Mode
    bg_overlay = "linear-gradient(rgba(248, 250, 252, 0.88), rgba(241, 245, 249, 0.94))"
    body_color = "#0f172a"
    surface_bg = "rgba(255, 255, 255, 0.88)"
    surface_border = "rgba(15, 23, 42, 0.12)"
    metric_val_color = "#0284c7"
    banner_bg = "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)"
    banner_border = "1px solid #cbd5e1"
    banner_title = "#0f172a"
    subtext_color = "#475569"
    badge_bg = "#e0f2fe"
    badge_color = "#0369a1"
    badge_border = "#bae6fd"
else:  # Dark Mode Option
    bg_overlay = "linear-gradient(rgba(10, 15, 29, 0.90), rgba(15, 23, 42, 0.95))"
    body_color = "#f8fafc"
    surface_bg = "rgba(15, 23, 42, 0.75)"
    surface_border = "rgba(255, 255, 255, 0.08)"
    metric_val_color = "#38bdf8"
    banner_bg = "linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(30, 41, 59, 0.75) 100%)"
    banner_border = "1px solid rgba(56, 189, 248, 0.25)"
    banner_title = "#ffffff"
    subtext_color = "#94a3b8"
    badge_bg = "rgba(14, 165, 233, 0.15)"
    badge_color = "#38bdf8"
    badge_border = "rgba(56, 189, 248, 0.3)"

bg_css = f'url("{bg_data_uri}") no-repeat center center fixed' if bg_data_uri else "#f1f5f9"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: {body_color};
    }}
    
    code, pre, .mono {{
        font-family: 'JetBrains Mono', monospace !important;
    }}
    
    .stApp {{
        background: {bg_overlay}, {bg_css};
        background-size: cover;
    }}
    
    .gov-masthead {{
        background: {banner_bg};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: {banner_border};
        border-radius: 8px;
        padding: 22px 30px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .status-chip {{
        background: {badge_bg};
        border: 1px solid {badge_border};
        color: {badge_color};
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: inline-block;
    }}
    
    div[data-testid="metric-container"] {{
        background: {surface_bg} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid {surface_border} !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: {metric_val_color} !important;
        letter-spacing: -0.5px !important;
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: {subtext_color} !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: {surface_bg};
        backdrop-filter: blur(12px);
        padding: 6px;
        border-radius: 8px;
        border: 1px solid {surface_border};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 38px;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 6px;
        padding: 0 16px;
        color: {subtext_color};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }}
    
    .stButton>button {{
        background: #0284c7;
        color: #ffffff;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        padding: 9px 20px;
        transition: all 0.15s ease-in-out;
    }}
    
    .stButton>button:hover {{
        background: #0369a1;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
    }}
</style>
""", unsafe_allow_html=True)

def load_db():
    if not os.path.exists(DB_FILE):
        return {"students": [], "timetable": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {"students": [], "timetable": []}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

db = load_db()

# Seed curriculum timetable if not initialized
if not db.get("timetable"):
    initial_tt = []
    base_date = date.today() + timedelta(days=21)
    courses_seed = [
        ("23ASH1109", "Mathematical Foundation for Computing - III"),
        ("23CSE2001", "Microcontroller Application"),
        ("23CSE2003", "Software Engineering"),
        ("23CSE2002", "Data Structures and Algorithms"),
        ("23CSE1010", "Project Based Learning - I"),
        ("23CSE2004", "Database Management Systems"),
        ("23CSE2009", "Database Management Systems Lab"),
        ("23CSE1012", "Python Essentials"),
        ("23CIV1302", "Environmental Studies"),
        ("23SHD1007", "Societal Immersion, Spirituality and Morality - I"),
        ("23SCL2001", "Aptitude and Professional Skills - Foundation"),
        ("23CSE1011", "Economics for Engineers"),
        ("23CSE3004", "Operating System"),
        ("23CSE2011", "Computer Networks"),
        ("23CSE2013", "Project Based Learning-II"),
        ("23MIE5001", "Entrepreneurship"),
        ("23CSE3003", "Web Technology"),
        ("23CSE2016", "Research Writing and Scientific Communication"),
        ("23CSE2017", "Theory of Computation"),
        ("23CSE3082", "Financial Literacy and Securities Market Primer"),
        ("23SHD1008", "Societal Immersion Spirituality and Morality - II")
    ]
    for idx, (code, cname) in enumerate(courses_seed):
        initial_tt.append({
            "code": code,
            "name": cname,
            "date": str(base_date + timedelta(days=(idx // 2) * 2)),
            "time": "10:00 AM - 01:00 PM" if idx % 2 == 0 else "02:00 PM - 05:00 PM"
        })
    db["timetable"] = initial_tt
    save_db(db)

# --- BULLETPROOF DISPATCH ENGINE (PORT 587 STARTTLS) ---
def dispatch_email(to_email, subject, html_content):
    if not sender_email or not app_password:
        st.error(f"⚠️ Credentials Missing: Could not send email to {to_email}. Please fill Sender Email and App Password in the sidebar.")
        return False
    try:
        clean_pwd = app_password.replace(" ", "").strip()
        clean_sender = sender_email.strip()
        clean_recipient = to_email.strip()

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Office of Controller of Examinations <{clean_sender}>"
        msg["To"] = clean_recipient
        msg.attach(MIMEText(html_content, "html"))

        # Using Port 587 TLS (Industry standard for reliable Gmail delivery)
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(clean_sender, clean_pwd)
        server.sendmail(clean_sender, clean_recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"❌ Delivery Error to {to_email}: {e}")
        return False

# --- TOP MASTHEAD ---
st.markdown(f"""
<div class="gov-masthead">
    <div>
        <div style="font-size: 0.72rem; font-weight: 700; color: #0284c7; letter-spacing: 1.2px; text-transform: uppercase;">
            Office of the Controller of Examinations
        </div>
        <h2 style="margin: 4px 0 0 0; font-size: 1.45rem; font-weight: 800; color: {banner_title}; letter-spacing: -0.4px;">
            MIT ART, DESIGN AND TECHNOLOGY UNIVERSITY
        </h2>
        <div style="font-size: 0.85rem; color: {subtext_color}; margin-top: 2px;">
            Autonomous End-Semester Examination Orchestrator and Dispatch Engine
        </div>
    </div>
    <div style="text-align: right;">
        <span class="status-chip">Channel: Pure Email Relay (100% Reliability)</span>
        <div style="font-size: 0.75rem; color: {subtext_color}; margin-top: 6px;">Academic Session 2026-27</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs for the 3 Phases + Registry
tab_registry, tab_p1, tab_p2, tab_p3 = st.tabs([
    "Candidate Registry",
    "Phase 1: Timetable Declaration (3 Weeks Prior)",
    "Phase 2: Seating Pass & Admit Slip (2 Days Prior)",
    "Phase 3: Date-Scanned Morning Reminders (Exam Day)"
])

# -------------------------------------------------------------------------
# REGISTRY INGESTION OVERVIEW
# -------------------------------------------------------------------------
with tab_registry:
    students = db.get("students", [])

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Ingested Candidates", len(students))
    with k2:
        st.metric("Phase 1 Timetables Issued", sum(1 for s in students if s.get("timetable_sent")))
    with k3:
        st.metric("Phase 2 Admit Passes Issued", sum(1 for s in students if s.get("ticket_sent")))
    with k4:
        st.metric("Phase 3 Morning Alerts Issued", sum(1 for s in students if s.get("reminder_sent")))

    st.markdown("---")
    col_reg_header, col_reg_btn = st.columns([3, 1])
    with col_reg_header:
        st.markdown("#### Live Candidate Registry Roster")
    with col_reg_btn:
        if st.button("🔄 Sync Records Table", use_container_width=True):
            st.rerun()

    if not students:
        st.info("No candidates registered in active roster. Registrations completed on the student portal appear here automatically.")
    else:
        grid_data = []
        for s in students:
            c_codes = ", ".join([c["code"] for c in s.get("courses", [])])
            grid_data.append({
                "PRN / Enrollment": s.get("enrollment"),
                "Candidate Name": s.get("name"),
                "Official Email": s.get("email"),
                "Contact Telephony": s.get("phone"),
                "Selected Courses": c_codes,
                "Submission Timestamp": s.get("registered_on", "N/A"),
                "Phase 1 Status": "Delivered" if s.get("timetable_sent") else "Pending",
                "Phase 2 Status": "Delivered" if s.get("ticket_sent") else "Pending",
                "Phase 3 Status": "Delivered" if s.get("reminder_sent") else "Pending"
            })
        st.dataframe(pd.DataFrame(grid_data), use_container_width=True, hide_index=True)

# -------------------------------------------------------------------------
# PHASE 1: 3 WEEKS PRIOR (STRICTLY SELECTED SUBJECTS ONLY)
# -------------------------------------------------------------------------
with tab_p1:
    st.markdown("#### Phase 1: Advance Master Timetable Declaration (3 Weeks Notice)")
    st.caption("Filters and dispatches personalized examination timetables containing strictly only the courses selected by each individual candidate.")

    tt_records = db.get("timetable", [])
    edited_tt = st.data_editor(tt_records, num_rows="dynamic", use_container_width=True)
    db["timetable"] = edited_tt
    save_db(db)

    st.markdown("---")
    if st.button("Broadcast Personalized Timetables (Strict Subject Filter)", type="primary"):
        students = db.get("students", [])
        if not students:
            st.warning("Candidate roster is empty.")
        else:
            dispatched = 0
            for s in students:
                student_course_codes = [c["code"] for c in s.get("courses", [])]
                matched_schedule = [item for item in edited_tt if item["code"] in student_course_codes]

                if not matched_schedule:
                    continue

                table_rows = ""
                for m in matched_schedule:
                    table_rows += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #cbd5e1; font-family: monospace;"><b>{m['code']}</b></td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1;">{m['name']}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; color: #0284c7;">{m['date']}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1;">{m['time']}</td>
                    </tr>
                    """

                email_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 25px; border-radius: 6px; border: 1px solid #cbd5e1; background-color: #ffffff; max-width: 650px; margin: auto;">
                    <div style="background-color: #0b1528; padding: 18px; border-radius: 4px; color: white; text-align: center;">
                        <h2 style="margin: 0; font-size: 19px; letter-spacing: 0.5px;">MIT ART, DESIGN AND TECHNOLOGY UNIVERSITY</h2>
                        <p style="margin: 4px 0 0 0; font-size: 12px; color: #94a3b8; text-transform: uppercase;">Central Examination Directive - Advance Timetable Notice</p>
                    </div>
                    <div style="padding: 20px 0;">
                        <p>Candidate: <b>{s['name']}</b> (PRN: <code style="background:#f1f5f9; padding:2px 6px;">{s['enrollment']}</code>)</p>
                        <p>This is your officially finalized examination schedule issued 3 weeks prior. This schedule contains strictly the courses you registered for:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px;">
                            <tr style="background-color: #f8fafc;">
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Course Code</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Subject Title</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Examination Date</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Session Slot</th>
                            </tr>
                            {table_rows}
                        </table>
                        <div style="background-color: #f0f9ff; border-left: 4px solid #0284c7; padding: 12px; font-size: 12px; color: #0369a1;">
                            <b>Next Step:</b> Individual Admit Slips detailing assigned examination hall coordinates and bench numbers will be dispatched <b>2 days prior</b> to each examination.
                        </div>
                    </div>
                </div>
                """

                ok = dispatch_email(s["email"], f"Official Examination Schedule | PRN {s['enrollment']}", email_html)
                if ok:
                    s["timetable_sent"] = True
                    dispatched += 1

            save_db(db)
            if dispatched > 0:
                st.success(f"Phase 1 personalized timetables delivered to {dispatched} candidates.")

# -------------------------------------------------------------------------
# PHASE 2: 2 DAYS PRIOR (EXAM SLIP: NAME, PRN, SUB, DATE, TIME, HALL, SEAT)
# -------------------------------------------------------------------------
with tab_p2:
    st.markdown("#### Phase 2: Seating Pass & Admit Slip Dispatch (2 Days Notice)")
    st.caption("Allocates unique hall and non-overlapping bench coordinates and dispatches the official examination slip.")

    students = db.get("students", [])
    tt_records = db.get("timetable", [])

    if st.button("Generate Seating Matrix & Dispatch Admit Slips", type="primary"):
        if not students:
            st.warning("Candidate roster is empty.")
        else:
            slips_issued = 0
            for idx, s in enumerate(students):
                student_course_codes = [c["code"] for c in s.get("courses", [])]
                matched_schedule = [item for item in tt_records if item["code"] in student_course_codes]

                if not matched_schedule:
                    continue

                block_id = (idx // 40) + 1
                bench_id = (idx % 40) + 1
                hall_name = f"Academic Complex {((idx // 120) + 1)} Hall {100 + block_id}"
                seat_code = f"SEAT-B{block_id}-{bench_id:02d}"

                slip_rows = ""
                for m in matched_schedule:
                    slip_rows += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #cbd5e1; font-family: monospace;"><b>{m['code']}</b></td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1;">{m['name']}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1;">{m['date']}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1;">{m['time']}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; color: #0284c7;">{hall_name}</td>
                        <td style="padding: 10px; border: 1px solid #cbd5e1; font-weight: bold; font-family: monospace; color: #059669;">{seat_code}</td>
                    </tr>
                    """

                admit_slip_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 25px; border-radius: 6px; border: 2px solid #0284c7; background-color: #ffffff; max-width: 720px; margin: auto;">
                    <div style="background-color: #0284c7; padding: 16px; border-radius: 4px; color: white; text-align: center;">
                        <h2 style="margin: 0; font-size: 20px; letter-spacing: 0.5px;">MIT ART, DESIGN AND TECHNOLOGY UNIVERSITY</h2>
                        <p style="margin: 4px 0 0 0; font-size: 13px;">Official Examination Hall Ticket & Admit Pass (48 Hours Prior)</p>
                    </div>
                    <div style="padding: 20px 0;">
                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; background-color: #f8fafc; padding: 12px; border: 1px solid #e2e8f0;">
                            <tr>
                                <td style="padding: 6px 12px;"><b>Candidate Full Name:</b></td>
                                <td style="padding: 6px 12px; font-size: 14px; color: #0f172a;"><b>{s['name']}</b></td>
                                <td style="padding: 6px 12px;"><b>Enrollment / PRN:</b></td>
                                <td style="padding: 6px 12px; font-size: 14px; font-family: monospace; color: #0284c7;"><b>{s['enrollment']}</b></td>
                            </tr>
                            <tr>
                                <td style="padding: 6px 12px;"><b>Official Institutional Email:</b></td>
                                <td style="padding: 6px 12px;">{s['email']}</td>
                                <td style="padding: 6px 12px;"><b>Contact Number:</b></td>
                                <td style="padding: 6px 12px;">{s.get('phone', 'N/A')}</td>
                            </tr>
                        </table>

                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 13px;">
                            <tr style="background-color: #f1f5f9;">
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Code</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Subject Title</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Exam Date</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Session Time</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Hall No.</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1; text-align: left;">Seat No.</th>
                            </tr>
                            {slip_rows}
                        </table>

                        <div style="background-color: #fefce8; border-left: 4px solid #ca8a04; padding: 12px; font-size: 12px; color: #854d0e;">
                            <b>Admit Instructions:</b> Presentation of physical Institute Identity Card is mandatory. Reporting cutoff is 30 minutes prior to paper commencement.
                        </div>
                    </div>
                </div>
                """

                ok = dispatch_email(s["email"], f"Official Admit Slip Issued | {s['name']} (Seat: {seat_code})", admit_slip_html)
                if ok:
                    s["ticket_sent"] = True
                    slips_issued += 1

            save_db(db)
            if slips_issued > 0:
                st.success(f"Phase 2 admit slips successfully delivered to {slips_issued} candidates.")

# -------------------------------------------------------------------------
# PHASE 3: EXAM DAY MORNING REMINDER (AUTOMATIC DATE SCANNER)
# -------------------------------------------------------------------------
with tab_p3:
    st.markdown("#### Phase 3: Automatic Date-Scanned Morning Reminders")
    st.caption("Automatically scans system date against candidate timetables. Identifies examinations scheduled for today and dispatches urgent wake-up reminders with room and bench details.")

    today_str = date.today().strftime("%Y-%m-%d")
    
    col_scan1, col_scan2 = st.columns([2, 1])
    with col_scan1:
        st.markdown(f"**Current System Date**: `<span class='mono' style='font-size:1.1rem; color:#0284c7;'>{today_str}</span>`", unsafe_allow_html=True)
    with col_scan2:
        override_test_date = st.text_input("Simulate Scan Date (YYYY-MM-DD)", value=today_str)

    active_scan_date = override_test_date.strip()

    students = db.get("students", [])
    tt_records = db.get("timetable", [])

    scheduled_today_candidates = []
    for idx, s in enumerate(students):
        student_course_codes = [c["code"] for c in s.get("courses", [])]
        today_papers = [t for t in tt_records if t["code"] in student_course_codes and t["date"] == active_scan_date]
        if today_papers:
            block_id = (idx // 40) + 1
            bench_id = (idx % 40) + 1
            hall_name = f"Academic Complex {((idx // 120) + 1)} Hall {100 + block_id}"
            seat_code = f"SEAT-B{block_id}-{bench_id:02d}"
            
            scheduled_today_candidates.append({
                "student": s,
                "papers": today_papers,
                "hall": hall_name,
                "seat": seat_code
            })

    st.markdown(f"**Automatic Scan Result**: Found **`{len(scheduled_today_candidates)}`** candidate paper(s) occurring on **`{active_scan_date}`**.")

    if scheduled_today_candidates:
        preview_data = []
        for item in scheduled_today_candidates:
            cand = item["student"]
            papers_str = ", ".join([f"{p['code']} ({p['time']})" for p in item["papers"]])
            preview_data.append({
                "PRN": cand.get("enrollment"),
                "Candidate Name": cand.get("name"),
                "Email": cand.get("email"),
                "Papers Today": papers_str,
                "Allotted Hall": item["hall"],
                "Allotted Seat": item["seat"]
            })
        st.dataframe(pd.DataFrame(preview_data), use_container_width=True, hide_index=True)

    if st.button("Execute Automatic Date-Scan & Transmit Morning Reminders", type="primary"):
        if not scheduled_today_candidates:
            st.warning(f"No papers found on {active_scan_date}. Use the date override field above to simulate any date from your master timetable.")
        else:
            reminders_sent = 0
            for item in scheduled_today_candidates:
                s = item["student"]
                papers = item["papers"]
                curr_exam = papers[0]
                hall_name = item["hall"]
                seat_code = item["seat"]

                reminder_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 25px; border-radius: 6px; border: 2px solid #b91c1c; background-color: #ffffff; max-width: 650px; margin: auto;">
                    <div style="background-color: #b91c1c; padding: 16px; border-radius: 4px; color: white; text-align: center;">
                        <h2 style="margin: 0; font-size: 19px; text-transform: uppercase;">Official Examination Day Morning Reminder</h2>
                        <p style="margin: 4px 0 0 0; font-size: 12px; letter-spacing: 0.5px;">Urgent Candidate Advisory - Central Examination Cell</p>
                    </div>

                    <div style="padding: 20px 0;">
                        <p style="font-size: 14px; color: #1e293b;">
                            Candidate: <b>{s['name']}</b> (PRN: <code style="background:#f1f5f9; padding:2px 6px;">{s['enrollment']}</code>)
                        </p>
                        <p style="font-size: 13px; color: #475569; line-height: 1.5;">
                            This is an automated priority advisory confirming that your scheduled End Semester Examination is taking place <b>TODAY ({active_scan_date})</b>. Please verify your room allotment parameters below:
                        </p>

                        <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 16px; margin: 18px 0;">
                            <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                                <tr>
                                    <td style="padding: 6px 0; color: #64748b; width: 35%;">Examination Paper:</td>
                                    <td style="padding: 6px 0; color: #0f172a; font-weight: bold;">{curr_exam['code']} - {curr_exam['name']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 6px 0; color: #64748b;">Scheduled Session:</td>
                                    <td style="padding: 6px 0; color: #b91c1c; font-weight: bold;">{curr_exam['time']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 6px 0; color: #64748b;">Assigned Examination Hall:</td>
                                    <td style="padding: 6px 0; color: #0284c7; font-weight: bold;">{hall_name}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 6px 0; color: #64748b;">Designated Bench / Seat:</td>
                                    <td style="padding: 6px 0; color: #059669; font-weight: bold; font-family: monospace;">{seat_code}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 6px 0; color: #64748b;">Mandatory Reporting Time:</td>
                                    <td style="padding: 6px 0; color: #334155; font-weight: bold;">09:30 AM (Strict Cutoff)</td>
                                </tr>
                            </table>
                        </div>

                        <div style="background-color: #fefce8; border-left: 4px solid #ca8a04; padding: 12px; font-size: 12px; color: #854d0e;">
                            <b>Critical Instructions:</b> Carry your physical Institute Identity Card and Hall Ticket. Entry doors close strictly 15 minutes prior to session commencement.
                        </div>

                        <p style="font-size: 13px; color: #334155; margin-top: 20px;">
                            Office of the Controller of Examinations<br>
                            MIT Art, Design and Technology University, Pune
                        </p>
                    </div>
                </div>
                """

                ok = dispatch_email(s["email"], f"Urgent: Today's Exam Reminder | {curr_exam['name']} ({hall_name} - {seat_code})", reminder_html)
                if ok:
                    s["reminder_sent"] = True
                    reminders_sent += 1

            save_db(db)
            if reminders_sent > 0:
                st.success(f"Phase 3 morning reminders successfully dispatched to {reminders_sent} candidates.")