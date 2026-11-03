
from datetime import date
import requests
import streamlit as st

st.set_page_config(
    page_title="Goutte d'Eau",
    page_icon=None,
    layout="centered"
)

st.title("Goutte d'Eau")
st.subheader("Estimation du risque de pluie à Paris")

st.write(
    "Cette application estime le risque statistique de pluie "
    "à partir de la date choisie."
)

date_choisie = st.date_input(
    "Sélectionnez une date :",
    value=date.today(),
    format="DD/MM/YYYY"
)

if st.button("Estimer le risque de pluie", type="primary"):

    try:
        reponse = requests.get(
            "http://127.0.0.1:8000/prediction",
            params={"date_prevision": date_choisie.isoformat()},
            timeout=10
        )

        reponse.raise_for_status()
        resultat = reponse.json()

        risque = resultat["risque_pluie_pourcentage"]

        st.metric(
            label="Risque estimé de pluie",
            value=f"{risque:.1f} %"
        )

        st.progress(min(max(risque / 100, 0.0), 1.0))

        st.caption(
            "Estimation statistique basée sur les données historiques "
            "de précipitations à Paris (seuil : 1 mm/jour). "
            "Ne constitue pas une prévision météorologique quotidienne."
        )

    except requests.exceptions.RequestException:
        st.error(
            "Impossible de contacter l'API FastAPI. "
            "Vérifiez que le serveur est démarré."
        )
