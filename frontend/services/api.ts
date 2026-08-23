import {
  AskResponse,
  BusinessAdviceResponse,
  LandAnalysisResponse,
  LandBusinessReport,
} from "@/types/rag";

export async function ask(question: string, conversationId?: number | null): Promise<AskResponse> {
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, conversation_id: conversationId ?? null }),
  });

  if (!response.ok) {
    throw new Error("Failed to get answer.");
  }

  return response.json();
}

export async function getBusinessAdvice(
  question: string,
  landReport?: LandBusinessReport | null
): Promise<BusinessAdviceResponse> {
  const response = await fetch(
    "http://localhost:8000/business-advice",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        land_report: landReport ?? null,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to get business advice.");
  }

  return response.json();
}

export async function analyzeLand(
  file: File
): Promise<LandAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    "http://localhost:8000/land-analysis",
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(
      error?.detail ?? "Failed to analyze the land document."
    );
  }

  return response.json();
}
