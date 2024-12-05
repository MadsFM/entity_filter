import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from sympy import rotations

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

@app.post("/entities", response_model=EntityResponse, summary="Save entities from text", description="Extracts entities from text and saves them.")
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

@app.get("/entity-chart", summary="Generate chart of entity frequencies")
def entity_chart(db: Session = Depends(get_db)):
    entities = db.query(Entity).all()

    entity_count = {}
    for entity in entities:
        label = entity.label
        entity_count[label] = entity_count.get(label, 0) + 1

    colors = plt.cm.tab20.colors
    label_names = {380: "PERSON", 384: "ORG", 394: "MONEY"}
    labels = [label_names.get(label, "UNKNOWN") for label in entity_count.keys()]
    counts = list(entity_count.values())


    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=colors[:len(labels)])
    for i, count in enumerate(counts):
        plt.text(i, count + 0.5, f"{count} ({count / sum(counts):.1%})", ha="center")
    plt.title("Entity frequency")
    plt.xlabel("Entity type")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")

    chart_path = "entity_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return FileResponse(
        chart_path,
        media_type="image/png",
        filename="entity_chart.png"
    )