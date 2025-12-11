import streamlit as st
import pandas as pd
from database import init_db, get_connection

# Initialisation de la base de données (création des tables si besoin)
init_db()

st.title("🐕‍🦺 Radar Cynophile France")
st.subheader("Analyse des avis Google des sociétés de sécurité cynophiles")

st.write(
    "Bienvenue Mathieu. "
    "Cette application a pour objectif d'identifier les sociétés de sécurité cynophiles "
    "qui pourraient présenter des manquements au Livre 6 du CSI, à partir des avis Google."
)

st.markdown("---")

st.header("📊 Tableau des entreprises cynophiles")

# Connexion à la base
conn = get_connection()

# On essaie de charger les entreprises + risques (même si pour l'instant c'est vide)
query = """
SELECT 
    e.nom AS 'Nom de l’entreprise',
    e.adresse AS 'Adresse',
    e.departement AS 'Département',
    IFNULL(r.score, 0) AS 'Score de risque',
    IFNULL(r.niveau, 'non analysé') AS 'Niveau de risque'
FROM entreprises e
LEFT JOIN risques r ON e.place_id = r.place_id
ORDER BY r.score DESC
"""
try:
    df = pd.read_sql_query(query, conn)
except Exception:
    df = pd.DataFrame(columns=[
        "Nom de l’entreprise", "Adresse", "Département",
        "Score de risque", "Niveau de risque"
    ])

conn.close()

if df.empty:
    st.info(
        "Pour l’instant, aucune entreprise n’est enregistrée dans la base. "
        "Dans les prochaines étapes, nous allons :\n"
        "- récupérer automatiquement les sociétés cynophiles par département,\n"
        "- collecter leurs avis Google,\n"
        "- calculer un score de risque pour chacune."
    )
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.subheader("🚧 Prochaines étapes")
st.write("""
- Ajouter un bouton **“Scanner la France”** qui ira chercher automatiquement les sociétés cynophiles.
- Récupérer leurs **avis Google**.
- Analyser les textes avec un moteur simple (mots-clés) pour calculer un **score de risque Livre 6**.
""")
