from sqlalchemy import text

from app.database.postgres import Postgres

postgres = Postgres()

session = postgres.get_session()

result = session.execute(
    text("SELECT version();")
)

print(result.scalar())

session.close()