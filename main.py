import streamlit as st
import smtplib
from email.mime.text import MIMEText
import datetime
import os

EMAIL_SENDER = "bandobabyfan3@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(name, email, programmes):

    subject = "Deine Fördermittel Analyse – FörderPilot AI"

    programme_text = "\n".join(programmes)

    body = f"""Hallo {name},

basierend auf deinen Angaben haben wir folgende Förderprogramme identifiziert:

{programme_text}

Viele Unternehmen sichern sich aktuell 25.000 € bis 100.000 € Förderung.

Wenn du Unterstützung bei der Beantragung möchtest, antworte einfach auf diese Email.

Beste Grüße  
Levin Amatosero  
FörderPilot AI
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()


st.set_page_config(page_title="FörderPilot AI", page_icon="🚀")

st.title("🚀 FörderPilot AI")
st.subheader("Kostenlose Fördermittel Analyse")

name = st.text_input("Name")
email = st.text_input("Email")
mitarbeiter = st.number_input("Anzahl Mitarbeiter", min_value=1, max_value=100000)

bundesland = st.selectbox(
    "Bundesland",
    [
        "Baden-Württemberg",
        "Bayern",
        "Berlin",
        "Hamburg",
        "Nordrhein-Westfalen",
        "Hessen",
        "Sachsen",
        "Niedersachsen"
    ]
)

ki = st.selectbox("KI oder Digitalisierung geplant?", ["Ja", "Nein"])

if st.button("Analyse starten"):

    programmes = [
        "Digital Jetzt – bis zu 50.000 €",
        "ZIM Innovationsprogramm – bis zu 100.000 €"
    ]

    if ki == "Ja":
        programmes.append("KI Förderung – bis zu 100.000 €")

    if mitarbeiter < 50:
        programmes.append("KMU Förderung – bis zu 25.000 €")

    st.subheader("Ergebnis")

    for p in programmes:
        st.write("✔", p)

    if name and email:

        with open("leads.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} | {name} | {email}\n")

        send_email(name, email, programmes)

        st.success("Analyse wurde per Email gesendet.")
