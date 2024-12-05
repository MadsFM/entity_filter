from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database import Base

class TextInput(BaseModel):
    text: str
    lang: str # en = English, da = Danish

class EntityItem(BaseModel):
    text: str
    label: int

class EntityResponse(BaseModel):
    text: str
    entities: List[EntityItem]

class SourceText(Base):
    __tablename__ = "source_texts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    # Relationships
    entities = relationship("Entity", back_populates="source_text")
    tokens = relationship("Token", back_populates="source_text")


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    label = Column(BigInteger, nullable=False)
    entity_id = Column(BigInteger, nullable=True)
    source_text_id = Column(Integer, ForeignKey("source_texts.id"))

    # Relationships
    source_text = relationship("SourceText", back_populates="entities")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    source_text_id = Column(Integer, ForeignKey("source_texts.id"))

    # Relationships
    source_text = relationship("SourceText", back_populates="tokens")