import googlemaps
import os
from database import get_connection

def get_gmaps_client():
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        return None
    return googlemaps.Client(key=key)

def fetch_reviews_for_place(place_id):
    """
    Récupère les avis Google pour un place_id donné
    et les ajoute dans la table 'avis'.
    """

    gmaps = get_gmaps_client()
    if not gmaps:
        return "No API key"

    try:
        details = gmaps.place(place_id=place_id, fields=["review"])
    except Exception as e:
        return f"Erreur API Google: {e}"

    reviews = details.get("result", {}).get("reviews", [])
    if not reviews:
        return "Aucun avis trouvé"

    conn = get_connection()
    cursor = conn.cursor()

    for r in reviews:
        auteur = r.get("author_name", "Inconnu")
        note = r.get("rating", None)
        texte = r.get("text", "")
        date = r.get("relative_time_description", "")

        cursor.execute(
            """
            INSERT INTO avis (place_id, auteur, note, texte, date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (place_id, auteur, note, texte, date),
        )

    conn.commit()
    conn.close()
    return f"{len(reviews)} avis ajoutés"


def fetch_reviews_for_all_companies():
    """
    Récupère les avis pour toutes les entreprises présentes dans la base.
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT place_id, nom FROM entreprises")
    rows = cursor.fetchall()
    conn.close()

    results = {}

    for place_id, nom in rows:
        res = fetch_reviews_for_place(place_id)
        results[nom] = res

    return results
