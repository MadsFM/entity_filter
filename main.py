from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Token, Entity, SourceText, EntityResponse, TextInput, EntityItem
from services import extract_entities, tokenize_text

from routes import spacy_router
app = FastAPI(
    title="First Spacy App",
    description="Supports danish and english",
    version="1.0.0")

#app.include_router(spacy_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my version of SpaCy"}

@app.post("/entities", response_model=EntityResponse, summary="Save entities from text", description="Extracts entities from text and saves them in a database.")
def save_entities(request: TextInput, db: Session = Depends(get_db)):
    entities = extract_entities(request.text, request.lang)
    source_text = SourceText(text=request.text)
    db.add(source_text)
    db.commit()

    for entity in entities:
        db.add(Entity(text=entity["text"], label=entity["label"], source_text_id=source_text.id))
    db.commit()

    return EntityResponse(
        text=request.text,
        entities=[EntityItem(text=entity["text"], label=entity["label"]) for entity in entities]
    )

@app.get("/entities")
def get_entites(text_id: int, db: Session = Depends(get_db)):
    entities = db.query(Entity).filter(Entity.source_text_id == text_id).all()
    return {"entities": [{"text": e.text, "label": e.label} for e in entities]}