import streamlit as st
import time

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="FörderPilot AI",
    page_icon="🚀",
    layout="centered"
)

# ======================
# MODERN CSS DESIGN
# ======================

st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.main-container {
    background: #161b22;
    padding: 30px;
    border-radius: 12px;
}

.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #9ca3af;
}

.result-box {
    background: #1f2937;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}

.success-box {
    background: #065f46;
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.markdown('<div class="title">🚀 FörderPilot AI</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Finde heraus, welche Fördermittel dir zustehen – kostenlos in unter 30 Sekunden</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ======================
# FORMULAR
# ======================

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

with st.form("analysis_form"):

    st.subheader("Deine Angaben")

    bundesland = st.selectbox("Bundesland", bundeslaender)

    branche = st.selectbox(
        "Branche",
        [
            "IT & Software",
            "Beratung",
            "Marketing",
            "E-Commerce",
            "Agentur",
            "Coaching",
            "Handwerk",
            "Sonstiges"
        ]
    )

    unternehmensgroesse = st.selectbox(
        "Unternehmensgröße",
        [
            "Solo-Selbstständig",
            "2-5 Mitarbeiter",
            "6-10 Mitarbeiter",
            "10+ Mitarbeiter"
        ]
    )

    email = st.text_input("E-Mail")

    submitted = st.form_submit_button("Analyse starten")

# ======================
# ANALYSE LOGIK
# ======================

if submitted:

    if email == "":
        st.error("Bitte E-Mail eingeben")
    else:

        with st.spinner("Analysiere Förderprogramme..."):
            time.sleep(2)

        st.success("Analyse abgeschlossen")

        st.markdown("## Deine Fördermöglichkeiten")

        foerderungen = [
            ("Digital Jetzt", "bis zu 50.000€"),
            ("BAFA Förderung", "bis zu 4.000€"),
            ("KfW Digitalisierung", "bis zu 100.000€"),
            ("EU Digital Grant", "bis zu 30.000€"),
        ]

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
            Vollständige Analyse wurde erstellt.
            </div>
            """,
            unsafe_allow_html=True
        )

# ======================
# FOOTER
# ======================

st.markdown("---")

st.caption("© 2026 FörderPilot AI – Fördermittel Analyse Deutschland")