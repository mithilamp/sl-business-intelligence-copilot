import {
  AskResponse,
  BusinessAdviceResponse,
} from "@/types/rag";

export async function ask(question: string): Promise<AskResponse> {
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error("Failed to get answer.");
  }

  return response.json();
}

export async function getBusinessAdvice(
  question: string
): Promise<BusinessAdviceResponse> {
  const response = await fetch(
    "http://localhost:8000/business-advice",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to get business advice.");
  }

  return response.json();
}