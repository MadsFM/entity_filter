import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
import logging
from sympy import rotations

from database import get_db
from models import Token, Entity, SourceText, EntityResponse, TextInput, EntityItem
from services import extract_entities, tokenize_text
from routes import spacy_router


app = FastAPI(
    title="First Spacy App",
    description="Supports danish and english",
    version="1.0.0")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message": "Welcome to my version of SpaCy"}

@app.post("/entities", response_model=EntityResponse, summary="Save entities from text")
def save_entities(request: TextInput, db: Session = Depends(get_db)):
    logger.info("Processing text: %s", request.text)
    entities = extract_entities(request.text, request.lang)
    source_text = SourceText(text=request.text)
    db.add(source_text)
    db.commit()

    entity_cache = {}

    for entity in entities:
        entity_text = entity["text"]
        entity_label = entity["label"]

        logger.info("Processing entity: %s with label: %s", entity_text, entity_label)

        if (entity_text, entity_label) in entity_cache:
            entity_id = entity_cache[(entity_text, entity_label)]
        else:
            existing_entity = db.query(Entity).filter(
                Entity.text == entity_text,
                Entity.label == entity_label
            ).first()

            if existing_entity:
                entity_id = existing_entity.id
                logger.info("Found existing entity ID: %s", entity_id)
            else:
                new_entity = Entity(
                    text=entity_text,
                    label=entity_label,
                    entity_id=None
                )
                db.add(new_entity)
                db.commit()
                entity_id = new_entity.id
                logger.info("Created new entity ID: %s", entity_id)

            entity_cache[(entity_text, entity_label)] = entity_id

        db.add(
            Entity(
                text=entity_text,
                label=entity_label,
                entity_id=entity_id,
                source_text_id=source_text.id,
            )
        )
    db.commit()

    logger.info("Finished processing entities.")
    return EntityResponse(
        text=request.text,
        entities=[
            EntityItem(
                text=entity["text"],
                label=entity["label"],
            )
            for entity in entities
        ]
    )



@app.get("/entities")
def get_entites(text_id: int, db: Session = Depends(get_db)):
    entities = db.query(Entity).filter(Entity.source_text_id == text_id).all()
    return {"entities": [{"text": e.text, "label": e.label} for e in entities]}

@app.get("/entity-chart", summary="Generate chart of entity frequencies")
def entity_chart(db: Session = Depends(get_db)):
    # Fetch all entities from the database
    entities = db.query(Entity).all()

    # Calculate entity frequencies
    entity_count = {}
    for entity in entities:
        label = entity.label
        entity_count[label] = entity_count.get(label, 0) + 1

    # Use the LABEL_MAPPING to get readable labels
    from services import LABEL_MAPPING
    reverse_label_mapping = {v: k for k, v in LABEL_MAPPING.items()}
    labels = [reverse_label_mapping.get(label, "UNKNOWN") for label in entity_count.keys()]
    counts = list(entity_count.values())

    # Plot the horizontal bar chart
    plt.figure(figsize=(12, 8))
    colors = plt.cm.tab20.colors  # Use a color palette
    y_position = range(len(labels))  # Position for each bar

    # Horizontal bar chart
    plt.barh(y_position, counts, color=colors[:len(labels)])
    plt.yticks(y_position, labels, fontsize=10)

    # Add data labels to the bars (counts and percentages)
    for i, count in enumerate(counts):
        plt.text(count + 0.5, i, f"{count} ({count / sum(counts):.1%})", va="center", fontsize=9)

    # Add titles and labels
    plt.title("Entity Frequency", fontsize=16)
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Entity Type", fontsize=12)

    # Save the chart and return it
    chart_path = "entity_chart.png"
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    return FileResponse(
        chart_path,
        media_type="image/png",
        filename="entity_chart.png"
    )
