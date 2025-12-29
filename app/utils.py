from langdetect import detect

LANG_MAP = {
    "ar": "arb_Arab",
    "en": "eng_Latn",
    "tr": "tur_Latn",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
    "it": "ita_Latn"
}


def detect_source_language(text: str) -> str:
    try:
        return LANG_MAP.get(detect(text), "eng_Latn")
    except:
        return "eng_Latn"


def split_article(text: str, max_words: int = 300):
    words = text.split()
    chunks, current = [], []

    for word in words:
        current.append(word)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks