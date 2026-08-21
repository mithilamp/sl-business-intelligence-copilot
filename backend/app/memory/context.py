from app.memory.memory import ConversationMemory


class MemoryContext:

    def __init__(
        self,
        memory: ConversationMemory | None = None,
    ):
        self.memory = memory or ConversationMemory()

    def build(
        self,
        conversation_id: int,
        recent_limit: int = 10,
    ) -> str:

        summary = self.memory.get_summary(
            conversation_id
        )

        messages = self.memory.get_recent_messages(
            conversation_id,
            limit=recent_limit,
        )

        sections = []

        if summary:
            sections.append(
                f"Conversation summary:\n{summary}"
            )

        if messages:
            history = "\n".join(
                f"{message.role.capitalize()}: "
                f"{message.content}"
                for message in messages
            )

            sections.append(
                f"Recent conversation:\n{history}"
            )

        return "\n\n".join(sections)