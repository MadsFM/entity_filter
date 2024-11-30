import spacy


nlp_models = {}

def extract_entities(text: str, lang: str):
    """

    :param text:the text that is processed
    :param lang: defines language of input
    :return:
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
    return [{"text": ent.text, "label": ent.label} for ent in doc.ents]

def tokenize_text(text: str, lang: str):
    """
    Tokenize text using the specific language
    :param text:
    :param lang:
    :return:
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
    return [token.text for token in doc]