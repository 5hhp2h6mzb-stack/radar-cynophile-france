import streamlit as st
import pandas as pd

from database import init_db, get_connection
from analyse import analyze_demo          # fichier analyse.py (nom en français)
from collect import scanner_france_demo   # fichier collect.py (scan démo)

# Initialisation de la base de données
init_db()

# --- TITRES ---
st.title("🐕‍🦺 Radar Cynophile France")
st.subheader("Analyse des avis Google des sociétés de sécurité cynophiles")

st.write(
    "Bienvenue Mathieu. "
    "Cette application a pour objectif d'identifier les sociétés de sécurité cynophiles "
    "qui pourraient présenter des manquements au Livre 6 du CSI, à partir des avis Google."
)

st.markdown("---")


# --- FONCTION POUR AJOUTER DES ENTREPRISES DE TEST ---
def ajouter_entreprises_test():
    conn = get_connection()
    cursor = conn.cursor()

    entreprises_demo = [
        ("SecuriDog Provence", "Marseille (13008)", "13", "demo_place_1"),
        ("Gardes & Chiens Azur", "Nice (06000)", "06", "demo_place_2"),
        ("Cynotech Sud Protection", "Toulon (83000)", "83", "demo_place_3"),
    ]

    for nom, adresse, dep, place_id in entreprises_demo:
        cursor.execute(
            """
            INSERT OR IGNORE INTO entreprises (nom, adresse, departement, place_id)
            VALUES (?, ?, ?, ?)
            """,
            (nom, adresse, dep, place_id),
        )

    conn.commit()
    conn.close()


# --- BOUTONS ---
st.header("📊 Tableau des entreprises cynophiles")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Sociétés de test"):
        ajouter_entreprises_test()
        st.success("Sociétés de test ajoutées 👌")

with col2:
    if st.button("⚖️ Analyse risques (démo)"):
        analyze_demo()
        st.success("Analyse démo réalisée ✔️")

with col3:
    if st.button("🔍 Scanner la France (démo)"):
        scanner_france_demo()
        st.success("Scan national démo effectué 🇫🇷")


# --- AFFICHAGE DU TABLEAU ---
conn = get_connection()

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
    df = pd.DataFrame(
        columns=[
            "Nom de l’entreprise",
            "Adresse",
            "Département",
            "Score de risque",
            "Niveau de risque",
        ]
    )

conn.close()


if df.empty:
    st.info(
        "Aucune entreprise enregistrée.\n\n"
        "Clique sur **Sociétés de test** ou **Scanner la France (démo)**."
    )
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")


# --- PROCHAINES ÉTAPES ---
st.subheader("🚧 Prochaines étapes")
st.write(
    """
- Remplacer le scan démo par une **vraie recherche Google Maps (API)**.
- Ajouter la collecte des **avis Google**.
- Remplacer l'analyse démo par une **vraie analyse automatique** :
  - maltraitance de chiens 🐕  
  - alcool / violence ⚠️  
  - absence de service ❌  
- Ajouter une carte de France + heatmap.
"""
)
