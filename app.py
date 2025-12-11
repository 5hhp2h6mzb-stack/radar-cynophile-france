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


def ajouter_entreprises_test():
    """
    Insère quelques sociétés de test dans la base,
    pour vérifier que tout fonctionne.
    """
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


st.header("📊 Tableau des entreprises cynophiles")

# Bouton pour injecter des sociétés de test
if st.button("➕ Ajouter quelques sociétés de test"):
    ajouter_entreprises_test()
    st.success("Des sociétés de test ont été ajoutées à la base. 👌")

# Connexion à la base
conn = get_connection()

# On charge les entreprises + risques (même si les risques ne sont pas encore calculés)
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
        "Pour l’instant, aucune entreprise n’est enregistrée dans la base.\n\n"
        "Clique sur le bouton ci-dessus pour ajouter quelques sociétés de test, "
        "puis, dans les étapes suivantes, nous brancherons la collecte automatique "
        "et l'analyse des avis Google."
    )
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.subheader("🚧 Prochaines étapes")
st.write(
    """
- Remplacer les sociétés de test par une collecte automatique (Google Maps, par département).
- Ajouter la collecte des **avis Google** pour chaque société.
- Mettre en place l’**analyse des textes** (mots-clés / signaux faibles) pour calculer un **score de risque Livre 6**.
"""
)
