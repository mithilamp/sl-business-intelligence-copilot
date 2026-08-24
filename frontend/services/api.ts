import {
  AskResponse,
  BusinessAdviceResponse,
  ConversationDetail,
  ConversationSummary,
  LandAnalysisResponse,
  LandBusinessReport,
} from "@/types/rag";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, init);

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail ?? "The request could not be completed.");
  }

  return response.json();
}

export async function ask(question: string, conversationId?: number | null): Promise<AskResponse> {
  return requestJson<AskResponse>("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question, conversation_id: conversationId ?? null }),
  });

}

export function getConversations(): Promise<ConversationSummary[]> {
  return requestJson<ConversationSummary[]>("/conversations");
}

export function getConversation(id: number): Promise<ConversationDetail> {
  return requestJson<ConversationDetail>(`/conversations/${id}`);
}

export async function getBusinessAdvice(
  question: string,
  landReport?: LandBusinessReport | null
): Promise<BusinessAdviceResponse> {
  return requestJson<BusinessAdviceResponse>(
    "/business-advice",
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

}

export async function analyzeLand(
  file: File
): Promise<LandAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/land-analysis`,
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
