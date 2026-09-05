# Clarifications to accompany the presentation

The original presentation is preserved as presented. The final report and audit clarify the following statements.

1. **Deployment on slides 13 and 15:** the project brief explicitly accepts running the application on your own machine. A publicly reachable URL is a strong bonus. The statement that a public URL is the remaining mandatory submission risk was incorrect. Local browser deployment satisfies that requirement when demonstrated.
2. **Evaluation on slides 12 and 13:** the completed measurements concern retrieval/source authority matching across 30 tasks. End-to-end factual-answer grading and executed Land Intelligence scenario scores remain unreported. The chart expresses MRR multiplied by 100 for plotting; the numeric MRR values are 0.611 and 0.600, not answer accuracy percentages.
3. **Reranker interpretation:** the two pipelines also use different document-selection policies. The baseline finds up to three unique documents among 20 chunks, while production deduplicates after selecting three chunks. The report explains why this can affect Precision@3 and why the difference should not be attributed solely to the cross-encoder.
4. **Land-to-advisor integration:** the dedicated UI action calls /business-advice directly. An /agent request with a land report can also select the advisor, but the direct UI path need not produce a Choose Agent Tool span. The dynamic routing claim applies to /agent.
5. **Land trace evidence:** instrumentation exists, but the available packaged screenshot is the actual Business Copilot Agent run. Attach a real land-run screenshot/link if you want to substantiate a specific land trace independently of the code.
