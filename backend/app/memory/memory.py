from sqlalchemy import select

from app.database.models import Conversation, Message
from app.database.postgres import Postgres


class ConversationMemory:

    def __init__(self, postgres: Postgres | None = None):
        self.postgres = postgres or Postgres()

    def create_conversation(
        self,
        title: str | None = None,
    ) -> Conversation:

        with self.postgres.get_session() as session:

            conversation = Conversation(
                title=title,
            )

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation

    def get_conversation(
        self,
        conversation_id: int,
    ) -> Conversation | None:

        with self.postgres.get_session() as session:

            return session.get(
                Conversation,
                conversation_id,
            )

    def list_conversations(self, limit: int = 50) -> list[Conversation]:
        with self.postgres.get_session() as session:
            statement = (
                select(Conversation)
                .order_by(Conversation.updated_at.desc())
                .limit(limit)
            )
            return list(session.scalars(statement))

    def add_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:

        with self.postgres.get_session() as session:

            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
            )

            session.add(message)

            conversation = session.get(
                Conversation,
                conversation_id,
            )

            if conversation:
                from datetime import datetime, timezone

                conversation.updated_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(message)

            return message

    def get_recent_messages(
        self,
        conversation_id: int,
        limit: int = 10,
    ) -> list[Message]:

        with self.postgres.get_session() as session:

            statement = (
                select(Message)
                .where(
                    Message.conversation_id == conversation_id
                )
                .order_by(Message.created_at.desc())
                .limit(limit)
            )

            messages = list(
                session.scalars(statement)
            )

            messages.reverse()

            return messages

    def get_summary(
        self,
        conversation_id: int,
    ) -> str | None:

        with self.postgres.get_session() as session:

            conversation = session.get(
                Conversation,
                conversation_id,
            )

            if conversation is None:
                return None

            return conversation.summary

    def update_summary(
        self,
        conversation_id: int,
        summary: str,
    ) -> None:

        with self.postgres.get_session() as session:

            conversation = session.get(
                Conversation,
                conversation_id,
            )

            if conversation is None:
                raise ValueError(
                    f"Conversation {conversation_id} not found"
                )

            conversation.summary = summary
            session.commit()
