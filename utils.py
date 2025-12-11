import unidecode

def normalize(text: str) -> str:
    """
    Normalise un texte pour faciliter la recherche de mots-clés :
    - gère le None
    - passe en minuscules
    - enlève les accents
    """
    if not text:
        return ""
    text = text.lower()
    text = unidecode.unidecode(text)
    return text
