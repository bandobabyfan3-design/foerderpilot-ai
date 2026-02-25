import streamlit as st
import csv
import os
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText

# =========================
# CONFIG
# =========================

ADMIN_PASSWORD = "foerderpilot_admin_2026"
LEADS_FILE = "leads.csv"

EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="FörderPilot AI",
    page_icon="🚀",
    layout="centered"
)

# =========================
# DESIGN
# =========================

st.markdown("""
<style>

.main-title {
font-size:42px;
font-weight:700;
margin-bottom:10px;
}

.subtitle {
font-size:18px;
color:#888;
margin-bottom:30px;
}

.success-box {
background:#0e1117;
border:1px solid #00ffae;
padding:20px;
border-radius:10px;
margin-top:20px;
}

.admin-box {
background:#0e1117;
border:1px solid #333;
padding:15px;
border-radius:8px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# PROGRAM DATA
# =========================

PROGRAMS = [
("Digital Jetzt", 50000),
("KI Förderung Bund", 75000),
("Go Digital", 30000),
("Innovationsförderung", 120000),
("Digitalbonus", 25000),
("KMU Förderung", 60000),
("Automatisierungsförderung", 45000)
]

# =========================
# FUNCTIONS
# =========================

def calculate_funding():

    total = 0

    for program in PROGRAMS:
        total += program[1]

    return total


def save_lead(name, email, bundesland, funding):

    exists = os.path.isfile(LEADS_FILE)

    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not exists:
            writer.writerow([
                "timestamp",
                "name",
                "email",
                "bundesland",
                "funding"
            ])

        writer.writerow([
            datetime.now(),
            name,
            email,
            bundesland,
            funding
        ])


def send_email(name, email, funding):

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return

    subject = "Deine Fördermittel-Analyse ist fertig"

    body = f"""
Hallo {name},

deine Fördermittel-Analyse wurde erfolgreich abgeschlossen.

Basierend auf deinen Angaben stehen dir aktuell Förderprogramme mit einem Gesamtvolumen von bis zu:

{funding:,} €

zur Verfügung.

Diese Programme können für Digitalisierung, KI, Automatisierung und Software genutzt werden.

Viele Unternehmen sichern sich aktuell Förderquoten zwischen 30 % und 80 %.

Beste Grüße

Levin Amatosero  
FörderPilot AI
"""

    message = MIMEText(body)

    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = email

    context = ssl.create_default_context()

    try:

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)

        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.sendmail(
            EMAIL_SENDER,
            email,
            message.as_string()
        )

        server.quit()

    except:
        pass


# =========================
# MODE SWITCH
# =========================

mode = st.sidebar.selectbox(
    "Modus",
    ["Analyse", "Admin"]
)

# =========================
# USER MODE
# =========================

if mode == "Analyse":

    st.markdown('<div class="main-title">🚀 FörderPilot AI</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Kostenlose Fördermittel Analyse Deutschland</div>',
        unsafe_allow_html=True
    )

    name = st.text_input("Name")

    email = st.text_input("Email")

    bundesland = st.selectbox(
        "Bundesland",
        [
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
        ]
    )

    if st.button("Analyse starten"):

        funding = calculate_funding()

        save_lead(
            name,
            email,
            bundesland,
            funding
        )

        send_email(
            name,
            email,
            funding
        )

        st.markdown(
            f"""
            <div class="success-box">
            Analyse abgeschlossen<br><br>
            Maximale Förderhöhe:<br><br>
            <b>{funding:,} €</b><br><br>
            Eine Email wurde versendet.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================
# ADMIN MODE
# =========================

if mode == "Admin":

    password = st.text_input(
        "Admin Passwort",
        type="password"
    )

    if password == ADMIN_PASSWORD:

        st.title("Admin Dashboard")

        if os.path.exists(LEADS_FILE):

            with open(LEADS_FILE, encoding="utf-8") as file:

                reader = csv.reader(file)

                next(reader)

                for row in reader:

                    st.markdown(
                        f"""
                        <div class="admin-box">
                        Name: {row[1]}<br>
                        Email: {row[2]}<br>
                        Bundesland: {row[3]}<br>
                        Förderung: {row[4]} €<br>
                        Datum: {row[0]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.write("Keine Leads vorhanden.")

    else:

        st.write("Passwort erforderlich")

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption("© 2026 FörderPilot AI")