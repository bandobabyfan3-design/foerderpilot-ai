import streamlit as st
import smtplib
import ssl
from email.mime.text import MIMEText

# EMAIL KONFIGURATION
EMAIL = "bandobabyfan3@gmail.com"
PASSWORD = "wfph ehnf mkxf quro"

# STREAMLIT START
st.set_page_config(page_title="FörderPilot AI", page_icon="🚀")

# EMAIL FUNKTION
def send_email(to, name, bundesland):

    subject = "FörderPilot Analyse gestartet"

    body = f"""
Hallo {name},

Ihre Förderanalyse für {bundesland} wurde erfolgreich gestartet.

Wir senden Ihnen in Kürze die Ergebnisse.

FörderPilot AI
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

        server.login(EMAIL, PASSWORD)

        server.sendmail(EMAIL, to, msg.as_string())


# UI
st.title("🚀 FörderPilot AI")

st.write("Kostenlose Fördermittel Analyse")

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

# BUTTON
if st.button("Analyse starten"):

    if name and email:

        send_email(email, name, bundesland)

        st.success("Analyse gestartet. Email wurde gesendet.")

    else:

        st.error("Bitte alle Felder ausfüllen.")
