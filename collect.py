from database import get_connection

def scanner_france_demo():
    """
    Version démo : on simule un scan national en ajoutant plusieurs entreprises
    réalistes dans plusieurs départements.
    La vraie version Google sera ajoutée après.
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
        cursor.execute("""
            INSERT OR IGNORE INTO entreprises (nom, adresse, departement, place_id)
            VALUES (?, ?, ?, ?)
        """, (nom, adresse, dep, place_id))

    conn.commit()
    conn.close()
