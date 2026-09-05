from app.database.models import Base
from app.database.postgres import Postgres

postgres = Postgres()

Base.metadata.create_all(postgres.engine)

print("Tables created successfully.")