import streamlit as st
import smtplib
from email.mime.text import MIMEText
import sqlite3
import json
import os
from datetime import datetime

# =====================
# CONFIG
# =====================

EMAIL_SENDER = "bandobabyfan3@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

st.set_page_config(page_title="FörderPilot AI", page_icon="🚀")

# =====================
# DATABASE
# =====================

conn = sqlite3.connect("leads.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    bundesland TEXT,
    created_at TEXT,
    followup_sent INTEGER DEFAULT 0
)
""")

conn.commit()

# =====================
# LOAD PROGRAMS
# =====================

with open("foerderprogramme.json", "r") as f:
    foerder = json.load(f)

# =====================
# EMAIL FUNCTION
# =====================

def send_email(to_email, subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

# =====================
# UI
# =====================

st.title("🚀 FörderPilot AI")
st.subheader("Kostenlose Fördermittel Analyse")

name = st.text_input("Name")
email = st.text_input("Email")

bundesland = st.selectbox("Bundesland", [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
])

if st.button("Analyse starten"):

    if not name or not email:
        st.warning("Bitte alle Felder ausfüllen.")
    else:

        bundes_key = bundesland.lower().replace("ä","ae").replace("ü","ue").replace("ö","oe")

        programme = foerder.get("bund", []) + foerder.get(bundes_key, [])

        st.subheader("Relevante Programme:")

        html_programme = ""

        for p in programme:
            st.write(f"✔ {p['name']} – {p['max_betrag']}")
            html_programme += f"<li><b>{p['name']}</b> – {p['max_betrag']} ({p['quote']})</li>"

        # Save lead
        c.execute("INSERT INTO leads (name,email,bundesland,created_at) VALUES (?,?,?,?)",
                  (name,email,bundesland,datetime.now().isoformat()))
        conn.commit()

        # Send Email
        send_email(
            email,
            "Deine Fördermittel Analyse",
            f"""
            Hallo {name},<br><br>
            hier sind deine potenziellen Förderprogramme:<br><br>
            <ul>{html_programme}</ul>
            <br>
            Wenn du eine detaillierte Förderstrategie möchtest, antworte mit <b>START</b>.
            <br><br>
            Levin Amatosero<br>
            FörderPilot AI
            """
        )

        st.success("Analyse per Email gesendet.")
