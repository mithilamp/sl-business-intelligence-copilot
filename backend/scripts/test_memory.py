from app.database.postgres import Postgres
from app.database.models import Conversation, Message


postgres = Postgres()

with postgres.get_session() as session:

    conversation = Conversation(
        title="Banking in Sri Lanka",
    )

    session.add(conversation)
    session.flush()

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content="What is the minimum capital requirement for opening a new bank?",
    )

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content="The minimum initial capital depends on the type of bank.",
    )

    session.add_all([
        user_message,
        assistant_message,
    ])

    session.commit()

    print(f"Conversation ID: {conversation.id}")

    saved = session.get(
        Conversation,
        conversation.id,
    )

    print(f"Title: {saved.title}")
    print(f"Summary: {saved.summary}")

    for message in saved.messages:
        print(f"{message.role}: {message.content}")