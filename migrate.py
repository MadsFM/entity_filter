from database import Base, engine
from models import SourceText, Entity, Token

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database created")