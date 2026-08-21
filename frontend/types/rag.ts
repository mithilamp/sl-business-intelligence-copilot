export interface AskResponse {
  question: string;
  answer: string;
  sources: Source[];
  conversation_id: number;
}

export interface Source {
  title: string;
  filename: string;
  source: string;
  document_url: string | null;
}

export interface BusinessRecommendation {
  business_name: string;
  summary: string;
  suitability_score: number | null;
  estimated_startup_cost: string | null;
  break_even: string | null;
  required_licenses: string[];
  top_risks: string[];
  next_steps: string[];
  supporting_sources: string[];
}

export interface BusinessAdviceResponse {
  question: string;
  recommendation: BusinessRecommendation;
  sources: Source[];
}