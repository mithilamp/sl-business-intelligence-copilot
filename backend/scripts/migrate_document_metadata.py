"""Add source-aware metadata columns to an existing database."""

from sqlalchemy import text

from app.database.postgres import Postgres


def main():
    postgres = Postgres()
    with postgres.engine.begin() as connection:
        connection.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS geography VARCHAR(255)"))
        connection.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS sector VARCHAR(255)"))
        connection.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS year INTEGER"))


if __name__ == "__main__":
    main()
