import streamlit as st
import json
import os
from datetime import datetime

DB_FILE = "database.json"

st.set_page_config(
    page_title="MIT ADT University — Student ERP Exam Portal",
    page_icon="🎓",
    layout="wide"
)

# Combined course catalog from official curriculum
ALL_COURSES = [
    {"code": "23ASH1109", "name": "Mathematical Foundation for Computing - III", "credits": 3},
    {"code": "23CSE2001", "name": "Microcontroller Application", "credits": 3},
    {"code": "23CSE2003", "name": "Software Engineering", "credits": 3},
    {"code": "23CSE2002", "name": "Data Structures and Algorithms", "credits": 3},
    {"code": "23CSE1010", "name": "Project Based Learning - I", "credits": 2},
    {"code": "23CSE2004", "name": "Database Management Systems", "credits": 3},
    {"code": "23CSE2009", "name": "Database Management Systems Lab", "credits": 1},
    {"code": "23CSE1012", "name": "Python Essentials", "credits": 2},
    {"code": "23CIV1302", "name": "Environmental Studies", "credits": 2},
    {"code": "23SHD1007", "name": "Societal Immersion, Spirituality and Morality - I", "credits": 1},
    {"code": "23SCL2001", "name": "Aptitude and Professional Skills - Foundation", "credits": 2},
    {"code": "23CSE1011", "name": "Economics for Engineers", "credits": 2},
    {"code": "23CSE3004", "name": "Operating System", "credits": 3},
    {"code": "23CSE2011", "name": "Computer Networks", "credits": 3},
    {"code": "23CSE2013", "name": "Project Based Learning-II", "credits": 2},
    {"code": "23MIE5001", "name": "Entrepreneurship", "credits": 2},
    {"code": "23CSE3003", "name": "Web Technology", "credits": 2},
    {"code": "23CSE2016", "name": "Research Writing and Scientific Communication", "credits": 2},
    {"code": "23CSE2017", "name": "Theory of Computation", "credits": 3},
    {"code": "23CSE3082", "name": "Financial Literacy and Securities Market Primer", "credits": 2},
    {"code": "23SHD1008", "name": "Societal Immersion Spirituality and Morality - II", "credits": 1}
]

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

# --- MIT ADT Header ---
st.markdown("""
<div style="background-color: #ffffff; border-bottom: 3px solid #008080; padding: 18px 25px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 6px rgba(0,0,0,0.06); margin-bottom: 20px; border-radius: 4px;">
    <div>
        <h2 style="color: #0b2545; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.3px;">MIT ART, DESIGN & TECHNOLOGY UNIVERSITY, PUNE</h2>
        <p style="color: #008080; margin: 4px 0 0 0; font-size: 13px; font-weight: 600;">CENTRAL ACADEMIC ERP • END SEMESTER EXAMINATION REGISTRATION</p>
    </div>
    <div style="background-color: #e6f7f7; color: #008080; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 700; border: 1px solid #b2e5e5;">
        ACADEMIC TERM: 2026-27
    </div>
</div>
""", unsafe_allow_html=True)

# Candidate Info Card
st.markdown("""
<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 18px; margin-bottom: 18px;">
    <span style="color: #334155; font-weight: 700; font-size: 14px;">👤 Candidate Verification & Contact Information</span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    name = st.text_input("Full Name", value="Atharva Joshi")
with c2:
    enrollment = st.text_input("Enrollment / PRN", value="ADT24SOCB0290")
with c3:
    email = st.text_input("Official Email Address", placeholder="your_email@gmail.com")
with c4:
    phone = st.text_input("Mobile Number (With +91)", value="+918668649090")

st.markdown("""
<div style="background-color: #e6f7f7; color: #007070; padding: 10px 15px; border-left: 4px solid #008080; border-radius: 4px; font-size: 13px; font-weight: 600; margin: 20px 0 12px 0;">
    ℹ️ Enrolled Course Selection — Select your registered courses and exam evaluation components
</div>
""", unsafe_allow_html=True)

# Table Header
h1, h2, h3, h4, h5 = st.columns([0.6, 2.0, 4.0, 3.0, 1.0])
with h1: st.markdown("**Select**")
with h2: st.markdown("**Course Code**")
with h3: st.markdown("**Course Title**")
with h4: st.markdown("**Evaluation Type**")
with h5: st.markdown("**Credits**")
st.markdown("<hr style='margin: 4px 0 10px 0; border: 0; border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)

selected_courses = []

for course in ALL_COURSES:
    row_1, row_2, row_3, row_4, row_5 = st.columns([0.6, 2.0, 4.0, 3.0, 1.0])
    with row_1:
        is_picked = st.checkbox("", key=f"sel_{course['code']}", value=False)
    with row_2:
        st.markdown(f"**{course['code']}**")
    with row_3:
        st.write(course["name"])
    with row_4:
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            ca_check = st.checkbox("Continuous Assessment", key=f"ca_{course['code']}", value=False)
        with sub_c2:
            ete_check = st.checkbox("End Term Exam", key=f"ete_{course['code']}", value=False)
    with row_5:
        st.write(f"{course['credits']}")

    if is_picked:
        selected_courses.append({
            "code": course["code"],
            "name": course["name"],
            "credits": course["credits"],
            "continuous_assessment": ca_check,
            "end_term_exam": ete_check
        })

    st.markdown("<hr style='margin: 2px 0 6px 0; border: 0; border-top: 1px solid #f1f5f9;'>", unsafe_allow_html=True)

st.write("")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    submit_btn = st.button("📤 Submit Examination Form to ERP", type="primary", use_container_width=True)

if submit_btn:
    if not name.strip() or not enrollment.strip() or not email.strip() or not phone.strip():
        st.error("⚠️ All candidate personal details are required.")
    elif not selected_courses:
        st.error("⚠️ Please select at least one course by ticking its checkbox.")
    else:
        db = load_db()
        existing = [s for s in db["students"] if s.get("enrollment") == enrollment.strip()]
        
        if existing:
            st.warning(f"Registration record for PRN {enrollment} already exists!")
        else:
            student_record = {
                "enrollment": enrollment.strip(),
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "courses": selected_courses,
                "registered_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            db["students"].append(student_record)
            save_db(db)

            # Centered Confirmation
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 25px;">
                <div style="background-color: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 25px 35px; max-width: 650px; width: 100%; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.12); text-align: center;">
                    <div style="width: 52px; height: 52px; background-color: #22c55e; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; color: white; font-size: 26px; font-weight: bold;">
                        ✓
                    </div>
                    <h3 style="color: #15803d; margin: 0 0 6px 0; font-size: 20px; font-weight: 700;">
                        You have successfully completed your Examination Form!
                    </h3>
                    <p style="color: #166534; font-size: 14px; margin: 0 0 15px 0;">
                        Your registration has been confirmed and synced with the Central Examination Cell.
                    </p>
                    <div style="background-color: #ffffff; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 18px; text-align: left; font-size: 13px; color: #334155;">
                        <p style="margin: 3px 0;"><b>Candidate:</b> {name} | <b>PRN:</b> <code>{enrollment}</code></p>
                        <p style="margin: 3px 0;"><b>Registered Email:</b> {email} | <b>Mobile:</b> {phone}</p>
                        <p style="margin: 3px 0;"><b>Total Subjects Selected:</b> {len(selected_courses)} Subjects</p>
                    </div>
                    <p style="font-size: 12px; color: #64748b; margin: 12px 0 0 0;">
                        🔔 <b>Automated Communication Timeline:</b> Personalized Timetable ➔ Seating Pass ➔ Exam Day Morning Alert via Institutional Email.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)