from app.llm.openai_llm import OpenAILLM

llm = OpenAILLM()

answer = llm.generate(
    system_prompt="You are a friendly assistant.",
    user_prompt="Say hello in one sentence."
)

print(answer)