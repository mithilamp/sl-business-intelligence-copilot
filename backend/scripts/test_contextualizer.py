from app.llm.openai_llm import OpenAILLM
from app.memory.contextualizer import QuestionContextualizer


llm = OpenAILLM()

contextualizer = QuestionContextualizer(llm)


history = """
User: What is the minimum capital requirement for opening a new bank?

Assistant: The minimum initial capital depends on the type of bank.
For a locally incorporated commercial bank it is Rs. 20 billion.

User: I am specifically interested in banks incorporated outside Sri Lanka.
"""


question = "What about foreign banks?"


result = contextualizer.contextualize(
    question=question,
    history=history,
)


print("Original:")
print(question)

print("\nContextualized:")
print(result)