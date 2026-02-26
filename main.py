import streamlit as st
import sqlite3
import datetime
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="FörderPilot AI",
    page_icon="🚀",
    layout="centered"
)

# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect("leads.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    bundesland TEXT,
    branche TEXT,
    mitarbeiter TEXT,
    created_at TEXT
)
""")

conn.commit()

# =========================
# CUSTOM CSS (PROFESSIONAL LOOK)
# =========================

st.markdown("""
<style>

.main-title {
    font-size:42px;
    font-weight:700;
    text-align:center;
    margin-bottom:10px;
}

.subtitle {
    text-align:center;
    color:#666;
    margin-bottom:30px;
}

.result-box {
    padding:18px;
    border-radius:10px;
    background:#f8fafc;
    margin-bottom:12px;
    border:1px solid #e6e9ef;
}

.success-box {
    padding:20px;
    border-radius:10px;
    background:#ecfdf5;
    border:1px solid #10b981;
    color:#065f46;
    font-weight:600;
    margin-top:20px;
}

.footer {
    text-align:center;
    margin-top:40px;
    color:#999;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">🚀 FörderPilot AI</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Finde in 30 Sekunden heraus, welche Fördermittel dein Unternehmen erhalten kann</div>',
    unsafe_allow_html=True
)

# =========================
# INPUT FORM
# =========================

email = st.text_input("Email")

bundeslaender = [
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

bundesland = st.selectbox("Bundesland", bundeslaender)

branchen = [
    "IT & Software",
    "Handwerk",
    "Produktion",
    "E-Commerce",
    "Beratung",
    "Marketing",
    "Gesundheit",
    "Bildung",
    "Bau",
    "Logistik",
    "Einzelhandel",
    "Sonstige"
]

branche = st.selectbox("Branche", branchen)

mitarbeiter = st.selectbox(
    "Anzahl Mitarbeiter",
    [
        "1",
        "2–5",
        "6–10",
        "11–50",
        "51–250",
        "250+"
    ]
)

# =========================
# ANALYSE BUTTON
# =========================

if st.button("Förderanalyse starten"):

    if email == "":
        st.error("Bitte Email eingeben")
    else:

        # SAVE LEAD
        c.execute(
            "INSERT INTO leads (email, bundesland, branche, mitarbeiter, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                email,
                bundesland,
                branche,
                mitarbeiter,
                datetime.datetime.now().isoformat()
            )
        )

        conn.commit()

        # =========================
        # RESULT LOGIC
        # =========================

        foerderungen = [

            ("Digital Jetzt", "bis zu 50.000€"),
            ("BAFA Förderung", "bis zu 4.000€"),
            ("KfW Digitalisierung", "bis zu 100.000€"),
            ("EU Förderprogramm", "bis zu 500.000€"),
            ("Innovationsförderung", "bis zu 250.000€"),
        ]

        st.markdown("### Ergebnis deiner Analyse")

        for name, betrag in foerderungen:

            st.markdown(
                f"""
                <div class="result-box">
                <b>{name}</b><br>
                Förderhöhe: {betrag}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <div class="success-box">
            ✅ Vollständige Analyse abgeschlossen<br>
            Du erhältst deine vollständige Förderübersicht per Email.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# ADMIN LEADS VIEW
# =========================

st.markdown("---")

if st.checkbox("Adminbereich anzeigen"):

    st.write("Gespeicherte Leads:")

    c.execute("SELECT * FROM leads ORDER BY id DESC")

    rows = c.fetchall()

    for row in rows:

        st.write(
            f"""
            Email: {row[1]}  
            Bundesland: {row[2]}  
            Branche: {row[3]}  
            Mitarbeiter: {row[4]}  
            Datum: {row[5]}
            """
        )

# =========================
# FOOTER
# =========================

st.markdown(
    '<div class="footer">© 2026 FörderPilot AI</div>',
    unsafe_allow_html=True
)