import spacy


nlp_models = {}

LABEL_MAPPING = {
    "PERSON": 380,  # People, including fictional
    "ORG": 384,  # Organizations, companies, institutions, etc.
    "MONEY": 394,  # Monetary values, including currency
    "GPE": 386,  # Geopolitical entities (countries, cities, states)
    "LOC": 385,  # Non-GPE locations, mountain ranges, bodies of water
    "DATE": 387,  # Absolute or relative dates or periods
    "TIME": 388,  # Times smaller than a day
    "PERCENT": 389,  # Percentage values
    "QUANTITY": 390,  # Measurements, including weight, distance
    "ORDINAL": 391,  # 'first', 'second', etc.
    "CARDINAL": 392,  # Numerals that do not fall under another type
    "EVENT": 393,  # Named events, e.g., 'Olympics'
    "PRODUCT": 395,  # Objects, vehicles, foods, etc. (not services)
    "LAW": 396,  # Named documents made into laws
    "LANGUAGE": 397,  # Any named language
    "NORP": 398,  # Nationalities, religious groups, political groups
    "FAC": 399,  # Buildings, airports, highways, bridges, etc.
    "WORK_OF_ART": 400,  # Titles of books, songs, etc.
    "ART": 401,  # Creative works (paintings, sculptures, etc.)
    "ANIMAL": 402,  # Animals (e.g., 'dog', 'cat', 'dinosaur')
    "PLANT": 403,  # Plant names (e.g., 'oak', 'rose', 'algae')
}


def extract_entities(text: str, lang: str):
    """
    Extract named entities from text.

    :param text: The text to process
    :param lang: The language of the input (en = English, da = Danish)
    :return: A list of entities with their text and mapped numeric labels
    """
    if lang not in nlp_models:
        if lang == "en":
            nlp_models[lang] = spacy.load("en_core_web_trf")
        elif lang == "da":
            nlp_models[lang] = spacy.load("da_core_news_trf")
        else:
            raise ValueError(f"Language '{lang}' is not supported.")
    nlp = nlp_models[lang]
    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        readable_label = ent.label_  # Get the human-readable label (e.g., PERSON)
        numeric_label = LABEL_MAPPING.get(readable_label, -1)  # Convert to numeric or fallback to -1
        entities.append({"text": ent.text, "label": numeric_label})

    return entities


def tokenize_text(text: str, lang: str):
    """
    Tokenize text using the specific language model.

    :param text: The text to tokenize
    :param lang: The language of the input (en = English, da = Danish)
    :return: A list of tokens
    """
    if lang not in nlp_models:
        # Dynamically load models for the first time
        if lang == "en":
            nlp_models[lang] = spacy.load("en_core_web_trf")
        elif lang == "da":
            nlp_models[lang] = spacy.load("da_core_news_trf")
        else:
            raise ValueError(f"Language '{lang}' is not supported.")

    nlp = nlp_models[lang]
    doc = nlp(text)

    return [token.text for token in doc]