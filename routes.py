from fastapi import APIRouter, HTTPException
from models import TextInput, EntityResponse
from services import extract_entities, tokenize_text

spacy_router = APIRouter()

@spacy_router.post("/entities", response_model=EntityResponse)
def get_entities(request: TextInput):
    """
    Extract named entities from text input
    :param request:
    :return:
    """
    try:
        entities = extract_entities(request.text, request.lang)
        return {"text": request.text, "entities": entities}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@spacy_router.post("/tokenize", response_model=dict)
def get_tokens(request: TextInput):
    """
    Tokenize text input
    :param request: 
    :return: tokens
    """
    try:
        tokens = tokenize_text(request.text, request.lang)
        return {"text": request.text, "tokens": tokens}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
