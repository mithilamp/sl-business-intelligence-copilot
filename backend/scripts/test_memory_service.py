from app.memory.memory import ConversationMemory


memory = ConversationMemory()


conversation = memory.create_conversation(
    title="Banking in Sri Lanka",
)

print(
    f"Created conversation: {conversation.id}"
)


memory.add_message(
    conversation_id=conversation.id,
    role="user",
    content="What is the minimum capital requirement for opening a new bank?",
)


memory.add_message(
    conversation_id=conversation.id,
    role="assistant",
    content="The minimum initial capital depends on the type of bank.",
)


memory.add_message(
    conversation_id=conversation.id,
    role="user",
    content="What about foreign banks?",
)


messages = memory.get_recent_messages(
    conversation_id=conversation.id,
    limit=10,
)


print("\nConversation history:")

for message in messages:
    print(
        f"{message.role}: {message.content}"
    )


memory.update_summary(
    conversation_id=conversation.id,
    summary=(
        "The user is investigating banking requirements "
        "in Sri Lanka, including minimum capital requirements "
        "and foreign banks."
    ),
)


summary = memory.get_summary(
    conversation.id
)


print("\nSummary:")
print(summary)