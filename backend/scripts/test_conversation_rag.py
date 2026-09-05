from app.memory.memory import ConversationMemory
from app.rag.rag_pipeline import RAGPipeline


memory = ConversationMemory()
pipeline = RAGPipeline(
    memory=memory,
)

conversation = memory.create_conversation(
    title="Banking conversation",
)

print(f"Conversation ID: {conversation.id}")


print("\n--- Question 1 ---")

result_1 = pipeline.ask(
    "What is the minimum capital requirement for opening a new bank?",
    conversation_id=conversation.id,
)

print(result_1.answer)


print("\n--- Question 2 ---")

result_2 = pipeline.ask(
    "What about foreign banks?",
    conversation_id=conversation.id,
)

print(result_2.answer)


print("\n--- Stored conversation ---")

messages = memory.get_recent_messages(
    conversation.id,
)

for message in messages:
    print(f"{message.role}: {message.content}")