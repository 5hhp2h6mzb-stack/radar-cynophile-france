from database import get_connection

# Mots-clés par catégorie (en minuscule, sans accents)
MOTS_CLES = {
    "maltraitance_chien": [
        "chien maltraite",
        "chiens maltraites",
        "chien blesse",
        "chien maigre",
        "chien enferme",
        "pauvres chiens",
        "maltraitance",
    ],
    "violence": [
        "agresse",
        "agression",
        "insulte",
        "insultes",
        "menace",
        "menaces",
        "violence",
        "violent",
    ],
    "alcool": [
        "alcoolise",
        "ivre",
        "bourre",
        "alcool",
    ],
    "service": [
        "jamais la",
        "absence",
        "absent",
        "aucune ronde",
        "aucune surveillance",
        "non professionnel",
        "incompetent",
    ],
}

SCORES = {
    "maltraitance_chien": 50,
    "violence": 30,
    "alcool": 25,
    "service": 10,
}


def _reset_risques(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM risques")
    conn.commit()


def analyze_demo():
    """
    Version démo : scores fixés pour les sociétés de test.
    """
    risques_demo = {
        "demo_place_1": (10, "faible"),   # SecuriDog Provence
        "demo_place_2": (80, "élevé"),    # Gardes & Chiens Azur
        "demo_place_3": (40, "modéré"),   # Cynotech Sud Protection
    }

    conn = get_connection()
    _reset_risques(conn)
    cursor = conn.cursor()

    for place_id, (score, niveau) in risques_demo.items():
        cursor.execute(
            """
            INSERT INTO risques (place_id, score, niveau)
            VALUES (?, ?, ?)
            """,
            (place_id, score, niveau),
        )

    conn.commit()
    conn.close()


def analyze_from_reviews():
    """
    Analyse réelle à partir de la table 'avis' :
    - parcourt tous les avis
    - calcule un score par entreprise (place_id)
    - stocke les scores dans la table 'risques'
    """
    conn = get_connection()
    cursor = conn.cursor()

    # On repart de zéro
    _reset_risques(conn)

    # Récupérer tous les avis
    cursor.execute("SELECT place_id, note, texte FROM avis")
    rows = cursor.fetchall()

    # Accumulateur de scores par place_id
    scores_par_place = {}

    for place_id, note, texte in rows:
        if not texte:
            continue

        t_norm = texte.lower()
        score_avis = 0

        for categorie, mots in MOTS_CLES.items():
            for mot in mots:
                if mot in t_norm:
                    score_avis += SCORES[categorie]

        # Bonus si la note est très basse (1 ou 2 étoiles)
        try:
            if note is not None and int(note) <= 2:
                score_avis += 5
        except ValueError:
            pass

        if score_avis > 0:
            scores_par_place[place_id] = scores_par_place.get(place_id, 0) + score_avis

    # Transformer les scores en niveaux et les enregistrer
    cursor = conn.cursor()
    for place_id, score in scores_par_place.items():
        niveau = "faible"
        if score > 20:
            niveau = "modéré"
        if score > 60:
            niveau = "élevé"

        cursor.execute(
            """
            INSERT INTO risques (place_id, score, niveau)
            VALUES (?, ?, ?)
            """,
            (place_id, score, niveau),
        )

    conn.commit()
    conn.close()
