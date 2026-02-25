import streamlit as st
import datetime

st.set_page_config(page_title="FörderPilot AI", page_icon="🚀")

st.title("🚀 FörderPilot AI")
st.subheader("Kostenlose Fördermittel Analyse")

st.write("""
Finde in unter 30 Sekunden heraus, welche Förderprogramme für dein Unternehmen möglich sind.
""")

st.markdown("---")

# INPUTS

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
        "Nordrhein-Westfalen"
    ]
)

ki = st.selectbox("KI oder Digitalisierung geplant?", ["Ja", "Nein"])

# ANALYSE

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

        with open("leads.txt", "a") as file:
            file.write(f"{datetime.datetime.now()} | {name} | {email}\n")

        st.success("Analyse gespeichert")
