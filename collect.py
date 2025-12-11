import os
from database import get_connection

# On n'importe googlemaps uniquement si disponible
try:
    import googlemaps
except ImportError:
    googlemaps = None


def scanner_france_demo():
    """
    Version démo : on simule un scan national en ajoutant plusieurs entreprises
    réalistes dans plusieurs départements.
    """
    entreprises = [
        ("Alpha Cynotech", "Montpellier (34000)", "34", "scan_place_1"),
        ("DogsGuard Sécurité", "Lyon (69008)", "69", "scan_place_2"),
        ("Nord Cyno Services", "Lille (59000)", "59", "scan_place_3"),
        ("Ouest Patrouille", "Nantes (44000)", "44", "scan_place_4"),
        ("Sécurité Canine Rhône", "Villeurbanne (69100)", "69", "scan_place_5"),
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for nom, adresse, dep, place_id in entreprises:
        cursor.execute(
            """
            INSERT OR IGNORE INTO entreprises (nom, adresse, departement, place_id)
            VALUES (?, ?, ?, ?)
            """,
            (nom, adresse, dep, place_id),
        )

    conn.commit()
    conn.close()


def get_google_client():
    """
    Prépare le client Google Maps à partir d'une clé stockée
    dans la variable d'environnement GOOGLE_MAPS_API_KEY.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

    if not api_key or googlemaps is None:
        return None

    return googlemaps.Client(key=api_key)


def scanner_france_reel(departements=None):
    """
    Version réelle (structure prête) :
    - utilise l'API Google Maps pour chercher des sociétés cynophiles.
    - Pour l'instant, on se limite à quelques départements si 'departements' est fourni.
    - Si pas de clé API, la fonction ne fait rien et renvoie un message.
    """
    gmaps = get_google_client()
    if gmaps is None:
        # Pas de clé ou pas de module googlemaps installé
        return "Aucune clé Google Maps détectée (GOOGLE_MAPS_API_KEY)."

    # Si aucun département n'est précisé, on en prend quelques-uns pour commencer
    if not departements:
        departements = ["13", "06", "83"]  # PACA pour démarrer

    KEYWORDS = [
        "sécurité cynophile",
        "agent cynophile",
        "maître-chien sécurité",
        "protection cynophile",
        "gardiennage chien",
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for dep in departements:
        for kw in KEYWORDS:
            query = f"{kw} département {dep}"
            try:
                result = gmaps.places(query=query)
            except Exception as e:
                print(f"Erreur Google Maps pour {query}: {e}")
                continue

            for r in result.get("results", []):
                nom = r.get("name")
                adresse = r.get("formatted_address", "")
                place_id = r.get("place_id", "")

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO entreprises (nom, adresse, departement, place_id)
                    VALUES (?, ?, ?, ?)
                    """,
                    (nom, adresse, dep, place_id),
                )

    conn.commit()
    conn.close()
    return "Scan réel terminé pour les départements : " + ", ".join(departements)
