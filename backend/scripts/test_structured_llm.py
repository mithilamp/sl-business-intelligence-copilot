from app.llm.openai_llm import OpenAILLM
from app.advisor.models import BusinessRecommendation


llm = OpenAILLM()

result = llm.generate_structured(
    system_prompt="""
    You are a business advisor.

    Return a business recommendation based only
    on the information provided.
    """,

    user_prompt="""
    The user wants to start vanilla farming in Sri Lanka.

    The available information says:
    - Vanilla farming is an agricultural business.
    - Export registration may be required for exporting products.
    - Disease management is an important consideration.

    Do not invent specific costs or break-even periods.
    Use 'Not available' where information is missing.
    """,

    response_model=BusinessRecommendation,
)

print(result)
print()
print("Type:", type(result))