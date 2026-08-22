from app.database.postgres import Postgres
from app.database.models import Base


postgres = Postgres()


print("Dropping tables...")

Base.metadata.drop_all(
    postgres.engine
)


print("Creating tables...")

Base.metadata.create_all(
    postgres.engine
)


print("Database reset complete.")