import streamlit as st
import pandas as pd

from database import init_db, get_connection
from analyse import analyze_demo, analyze_from_reviews
from collect import scanner_france_demo

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


# --- FONCTIONS D'AIDE ---
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


def ajouter_avis_test():
    """
    Ajoute quelques avis de test liés aux entreprises existantes,
    pour tester le moteur d'analyse réelle.
    """
    conn = get_connection()
    cursor = conn.cursor()

    avis_demo = [
        # Sur Gardes & Chiens Azur (demo_place_2) : cas très grave (maltraitance + violence + alcool)
        (
            "demo_place_2",
            "Client anonyme",
            1,
            "Les agents étaient alcoolisés et agressifs, on plaignait vraiment les chiens, "
            "chien maltraite et maigre, comportement violent.",
            "il y a 2 semaines",
        ),
        # Sur Cynotech Sud Protection (demo_place_3) : cas modéré (service + tensions)
        (
            "demo_place_3",
            "Locataire du site",
            2,
            "Agents souvent absents, aucune ronde, non professionnel. "
            "Pas de maltraitance apparente des chiens mais grosse insatisfaction.",
            "il y a 1 mois",
        ),
        # Sur Alpha Cynotech (scan_place_1) : problème de service
        (
            "scan_place_1",
            "Responsable magasin",
            2,
            "Service très inégal, parfois personne sur site, absence prolongée.",
            "il y a 3 semaines",
        ),
        # Sur DogsGuard Sécurité (scan_place_2) : suspicion maltraitance chien
        (
            "scan_place_2",
            "Voisin",
            1,
            "On voit les chiens enfermés toute la journée, chiens maigres, "
            "on parle clairement de maltraitance.",
            "il y a 4 jours",
        ),
    ]

    for place_id, auteur, note, texte, date in avis_demo:
        cursor.execute(
            """
            INSERT INTO avis (place_id, auteur, note, texte, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (place_id, auteur, note, texte, date),
        )

    conn.commit()
    conn.close()


# --- BOUTONS D'ACTION ---
st.header("⚙️ Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Sociétés de test"):
        ajouter_entreprises_test()
        st.success("Sociétés de test ajoutées 👌")

with col2:
    if st.button("🔍 Scanner la France (démo)"):
        scanner_france_demo()
        st.success("Scan national démo effectué 🇫🇷")

with col3:
    if st.button("⚖️ Analyse risques (démo)"):
        analyze_demo()
        st.success("Analyse démo réalisée ✔️")

st.markdown("---")

st.subheader("📝 Avis et analyse réelle")

col4, col5 = st.columns(2)

with col4:
    if st.button("📝 Ajouter des avis de test"):
        ajouter_avis_test()
        st.success("Avis de test ajoutés à la base 💬")

with col5:
    if st.button("⚖️ Analyse risques (à partir des avis)"):
        analyze_from_reviews()
        st.success(
            "Analyse des risques à partir des avis effectuée. "
            "La table des risques a été mise à jour."
        )

st.markdown("---")

# --- AFFICHAGE DU TABLEAU ---
st.header("📊 Tableau des entreprises cynophiles")

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
        "Clique sur **Sociétés de test** ou **Scanner la France (démo)**, "
        "puis éventuellement ajoute des avis de test et lance l'analyse."
    )
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

# --- PROCHAINES ÉTAPES ---
st.subheader("🚧 Prochaines étapes")
st.write(
    """
- Remplacer les avis de test par de **vrais avis Google** (Places API).
- Étendre les mots-clés et affiner le scoring.
- Ajouter un filtre par département et par niveau de risque.
- Ajouter une carte de France (heatmap des risques cynophiles).
"""
)
