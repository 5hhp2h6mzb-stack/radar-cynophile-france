import streamlit as st
import pandas as pd

st.title("🐕‍🦺 Radar Cynophile France")
st.subheader("Prototype en construction")

st.write("Bienvenue Mathieu, cette application servira à analyser les avis Google des sociétés de sécurité cynophiles sur toute la France.")

data = {
    "Message": ["Étape 1 : l'application est bien en ligne ✅",
                "Étape 2 : on ajoutera la collecte des avis Google 🐾",
                "Étape 3 : on ajoutera l'analyse des risques Livre 6 ⚖️"]
}

df = pd.DataFrame(data)
st.table(df)
