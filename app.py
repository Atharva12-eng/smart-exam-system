import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
import os
import json

# ================= CONFIGURATION =================
# Replace with your actual credentials:
SENDER_EMAIL = "dtgroup03@gmail.com"
APP_PASSWORD = "adwj nhir xdlv kyom"  # 16-character Google App Password
STUDENT_FILE = "students.csv"
TIMETABLE_FILE = "timetable.csv"
# =================================================

st.set_page_config(page_title="Smart Exam System", page_icon="🎓", layout="wide")

# Helper function to initialize timetable if not present
def initialize_files():
    if not os.path.exists(STUDENT_FILE):
        df_students = pd.DataFrame(columns=[
            "enrollment_no", "name", "email", "phone", 
            "registered_courses", "timetable_sent", "ticket_sent"
        ])
        df_students.to_csv(STUDENT_FILE, index=False)

    if not os.path.exists(TIMETABLE_FILE):
        default_tt = [
            {"course_code": "23CSE2019", "course_name": "Cyber Security Essentials", "exam_date": str(date.today() + timedelta(days=2)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE3155", "course_name": "Foundation of Cloud Computing", "exam_date": str(date.today() + timedelta(days=2)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE2018", "course_name": "Foundations of Artificial Intelligence", "exam_date": str(date.today() + timedelta(days=3)), "exam_time": "02:00 PM"},
            {"course_code": "23CSE2017", "course_name": "Theory of Computation", "exam_date": str(date.today() + timedelta(days=3)), "exam_time": "02:00 PM"},
            {"course_code": "23MIE5001", "course_name": "Entrepreneurship", "exam_date": str(date.today() + timedelta(days=5)), "exam_time": "10:00 AM"},
            {"course_code": "23CIV1302", "course_name": "Environmental Studies", "exam_date": str(date.today() + timedelta(days=5)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE3003", "course_name": "Web Technology", "exam_date": str(date.today() + timedelta(days=7)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE3002R", "course_name": "Advanced Java Programming", "exam_date": str(date.today() + timedelta(days=7)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE3001R", "course_name": "Professional Python Programming", "exam_date": str(date.today() + timedelta(days=7)), "exam_time": "10:00 AM"},
            {"course_code": "23CSE3082", "course_name": "Financial Literacy and Securities", "exam_date": str(date.today() + timedelta(days=9)), "exam_time": "02:00 PM"},
            {"course_code": "23CSE3133", "course_name": "Emotional Intelligence", "exam_date": str(date.today() + timedelta(days=9)), "exam_time": "02:00 PM"},
            {"course_code": "23CSE1011", "course_name": "Economics for Engineers", "exam_date": str(date.today() + timedelta(days=11)), "exam_time": "10:00 AM"}
        ]
        pd.DataFrame(default_tt).to_csv(TIMETABLE_FILE, index=False)

initialize_files()

def send_email(to_email, subject_line, html_body):
    """Sends email via Gmail SMTP with error handling."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject_line
    msg["From"] = f"Examination Department <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD.replace(" ", ""))
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

# ================= UI TABS =================
tab_student, tab_admin_tt, tab_admin_seating, tab_master = st.tabs([
    "🎓 Student Portal: ERP Exam Form", 
    "📅 Exam Cell: Timetable Declaration", 
    "🪑 Exam Cell: Seating & Hall Tickets",
    "📊 Master ERP Database"
])

# -------------------------------------------------------------
# TAB 1: STUDENT ERP EXAM FORM
# -------------------------------------------------------------
with tab_student:
    st.subheader("🏛 College Student Portal — Examination Form Registration")
    st.caption("Integrated Academic ERP • Form Submission Phase")

    with st.form("exam_reg_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Full Name", value="Atharva Joshi")
            enrollment = st.text_input("Enrollment No / PRN", value="ADT24SOCB0290")
        with col2:
            email = st.text_input("Registered College Email", placeholder="your_email@gmail.com")
            phone = st.text_input("Contact Number", value="+918668649090")

        st.markdown("### 📋 Elective Course Allotment")

        spc_choice = st.radio(
            "SPC Specialization Program Core (Select 1):",
            [
                "23CSE2019 - Cyber Security Essentials (Credits: 3)",
                "23CSE3155 - Foundation of Cloud Computing (Credits: 3)",
                "23CSE2018 - Foundations of Artificial Intelligence (Credits: 3)",
                "23CSE2017 - Theory of Computation (Credits: 3)"
            ]
        )

        hssm_choice = st.radio(
            "HSSM Elective (Select 1):",
            [
                "23MIE5001 - Entrepreneurship (Credits: 2)",
                "23CIV1302 - Environmental Studies (Credits: 2)"
            ]
        )

        esc_choice = st.radio(
            "ESC Programming Language (Select 1):",
            [
                "23CSE3003 - Web Technology (Credits: 2)",
                "23CSE3002R - Advanced Java Programming (Credits: 2)",
                "23CSE3001R - Professional Python Programming (Credits: 2)"
            ]
        )

        oe_choice = st.radio(
            "Open Elective MDM-OE (Select 1):",
            [
                "23CSE3082 - Financial Literacy and Securities (Credits: 2)",
                "23CSE3133 - Emotional Intelligence (Credits: 2)"
            ]
        )

        bsc_choice = st.radio(
            "BSC Mandatory Core:",
            ["23CSE1011 - Economics for Engineers (Credits: 2)"]
        )

        submit_btn = st.form_submit_button("📤 Submit Examination Form", type="primary")

    if submit_btn:
        if not name.strip() or not enrollment.strip() or not email.strip():
            st.error("Please fill in Name, Enrollment Number, and a valid Email address.")
        else:
            df_st = pd.read_csv(STUDENT_FILE, dtype=str)
            
            # Check for existing registration
            if not df_st.empty and enrollment in df_st["enrollment_no"].values:
                st.warning(f"Candidate {enrollment} has already submitted an exam form!")
            else:
                courses_selected = [
                    spc_choice.split(" - ")[0],
                    hssm_choice.split(" - ")[0],
                    esc_choice.split(" - ")[0],
                    oe_choice.split(" - ")[0],
                    bsc_choice.split(" - ")[0]
                ]

                new_row = {
                    "enrollment_no": enrollment,
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "registered_courses": json.dumps(courses_selected),
                    "timetable_sent": "No",
                    "ticket_sent": "No"
                }

                df_st = pd.concat([df_st, pd.DataFrame([new_row])], ignore_index=True)
                df_st.to_csv(STUDENT_FILE, index=False)

                # Send Acknowledgement Email
                course_list_html = "".join([f"<li><b>{c}</b></li>" for c in [spc_choice, hssm_choice, esc_choice, oe_choice, bsc_choice]])
                ack_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h3 style="color: #007bff;">ERP Exam Form Submitted Successfully</h3>
                    <p>Dear <b>{name}</b> (<code>{enrollment}</code>),</p>
                    <p>Your examination registration has been confirmed in the University ERP system.</p>
                    <p><b>Registered Subjects:</b></p>
                    <ul>{course_list_html}</ul>
                    <p style="background: #eef; padding: 10px; border-radius: 4px; font-size: 13px;">
                        📌 <b>Timetable</b> will be declared 2–3 weeks prior to exams.<br>
                        📌 <b>Seating Allocation (Hall & Seat Pass)</b> will be emailed 2 days prior to each exam.
                    </p>
                </div>
                """

                try:
                    send_email(email, "ERP Confirmation: Examination Form Submitted", ack_html)
                    st.success(f"Form submitted successfully! Acknowledgment sent to {email}.")
                except Exception as ex:
                    st.warning(f"Saved locally to database! (Email notice: {ex})")

# -------------------------------------------------------------
# TAB 2: EXAM CELL - TIMETABLE DECLARATION
# -------------------------------------------------------------
with tab_admin_tt:
    st.header("📅 Phase 2: Examination Cell Timetable Authority")
    st.caption("Published 2–3 weeks before exams. Automatically filters and dispatches only each student's registered subjects.")

    df_tt = pd.read_csv(TIMETABLE_FILE)
    edited_tt = st.data_editor(df_tt, num_rows="dynamic", use_container_width=True)

    if st.button("🚀 Publish & Dispatch Personalized Timetables", type="primary"):
        edited_tt.to_csv(TIMETABLE_FILE, index=False)
        df_students = pd.read_csv(STUDENT_FILE, dtype=str)

        if df_students.empty:
            st.warning("No students registered yet! Fill the form in Tab 1 first.")
        else:
            sent_count = 0
            for idx, student in df_students.iterrows():
                try:
                    student_courses = json.loads(student["registered_courses"])
                except Exception:
                    continue

                matched = edited_tt[edited_tt["course_code"].isin(student_courses)]

                rows_html = ""
                for _, r in matched.iterrows():
                    rows_html += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;"><b>{r['course_code']}</b></td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{r['course_name']}</td>
                        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; color: #007bff;">{r['exam_date']}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{r['exam_time']}</td>
                    </tr>
                    """

                email_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 20px; border: 2px solid #0056b3; border-radius: 8px;">
                    <h2 style="color: #0056b3; margin-top: 0;">PERSONALIZED EXAMINATION TIMETABLE</h2>
                    <p>Dear <b>{student['name']}</b> (<code>{student['enrollment_no']}</code>),</p>
                    <p>The examination schedule has been officially declared for your courses:</p>
                    <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                        <tr style="background: #f1f4f9;">
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Code</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Subject</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Date</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Time</th>
                        </tr>
                        {rows_html}
                    </table>
                    <p style="font-size: 13px; color: #555;">Seating allocations will be delivered 2 days prior to your exam.</p>
                </div>
                """

                try:
                    send_email(student["email"], "OFFICIAL: Your Personalized Exam Timetable", email_html)
                    df_students.at[idx, "timetable_sent"] = "Yes"
                    sent_count += 1
                except Exception as e:
                    st.warning(f"Email failed for {student['name']}: {e}")

            df_students.to_csv(STUDENT_FILE, index=False)
            st.success(f"Timetable published and emailed to {sent_count} student(s)!")

# -------------------------------------------------------------
# TAB 3: EXAM CELL - SEATING ALLOCATION (2 DAYS PRIOR)
# -------------------------------------------------------------
with tab_admin_seating:
    st.header("🪑 Phase 3: Seating Allocation & Hall Tickets")
    st.caption("Published 2 days before exams. Generates room and bench assignments.")

    df_students = pd.read_csv(STUDENT_FILE, dtype=str)
    df_tt = pd.read_csv(TIMETABLE_FILE)

    if st.button("🚀 Generate Seating & Broadcast Hall Tickets", type="primary"):
        if df_students.empty:
            st.warning("No registered students found! Register in Tab 1 first.")
        else:
            sent_passes = 0
            for idx, student in df_students.iterrows():
                try:
                    student_courses = json.loads(student["registered_courses"])
                except Exception:
                    continue

                matched = df_tt[df_tt["course_code"].isin(student_courses)]
                hall = "Hall A-201" if idx < 30 else "Hall B-104"
                seat = f"S-{idx + 1:02d}"

                pass_rows = ""
                for _, r in matched.iterrows():
                    pass_rows += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">{r['course_code']} - {r['course_name']}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{r['exam_date']} ({r['exam_time']})</td>
                        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; color: #0056b3;">{hall}</td>
                        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold; color: #28a745;">{seat}</td>
                    </tr>
                    """

                pass_html = f"""
                <div style="font-family: Arial, sans-serif; padding: 20px; border: 2px solid #28a745; border-radius: 8px;">
                    <h2 style="color: #28a745; margin-top: 0;">FINAL EXAMINATION HALL TICKET</h2>
                    <p>Dear <b>{student['name']}</b> (<code>{student['enrollment_no']}</code>),</p>
                    <p>Your seating allocation is finalized. Please present this ticket at the examination block:</p>
                    <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                        <tr style="background: #f1f8e9;">
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Course</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Schedule</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Hall</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Seat</th>
                        </tr>
                        {pass_rows}
                    </table>
                    <p style="background: #fff3cd; color: #856404; padding: 10px; border-radius: 4px; font-size: 13px;">
                        ⚠️ Bring your physical Institute ID card. Report 20 minutes prior to exam time.
                    </p>
                </div>
                """

                try:
                    send_email(student["email"], f"FINAL EXAM PASS: {hall} - Seat {seat}", pass_html)
                    df_students.at[idx, "ticket_sent"] = "Yes"
                    sent_passes += 1
                except Exception as e:
                    st.warning(f"Delivery failed for {student['name']}: {e}")

            df_students.to_csv(STUDENT_FILE, index=False)
            st.success(f"Hall tickets emailed to {sent_passes} student(s)!")

# -------------------------------------------------------------
# TAB 4: MASTER DATABASE LOG
# -------------------------------------------------------------
with tab_master:
    st.subheader("📊 Master Registered Candidates & Logs")
    df_live = pd.read_csv(STUDENT_FILE, dtype=str)
    st.dataframe(df_live, use_container_width=True)