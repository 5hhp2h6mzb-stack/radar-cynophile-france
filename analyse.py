from database import get_connection

def analyze_demo():
    """
    Version démo :
    On affecte manuellement un score de risque aux 3 sociétés de test,
    comme si on avait analysé leurs avis Google.
    """

    # Dictionnaire : place_id -> (score, niveau)
    risques_demo = {
        "demo_place_1": (10, "faible"),   # SecuriDog Provence
        "demo_place_2": (80, "élevé"),    # Gardes & Chiens Azur
        "demo_place_3": (40, "modéré"),   # Cynotech Sud Protection
    }

    conn = get_connection()
    cursor = conn.cursor()

    # On vide d'abord la table des risques pour repartir propre
    cursor.execute("DELETE FROM risques")

    # On insère les risques de démo
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
