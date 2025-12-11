from database import get_connection

def analyze_demo():
    """
    Version démo :
    On affecte manuellement un score de risque aux 3 sociétés de test,
    comme si on avait analysé leurs avis Google.
    """

    risques_demo = {
        "demo_place_1": (10, "faible"),   
        "demo_place_2": (80, "élevé"),    
        "demo_place_3": (40, "modéré"),   
    }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM risques")

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
