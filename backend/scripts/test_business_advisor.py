from app.advisor.business_advisor import BusinessAdvisor


advisor = BusinessAdvisor()

result = advisor.recommend(
    "What are the requirements and considerations for starting a bank in Sri Lanka?"
)

print(result)
print()
print("Type:", type(result))