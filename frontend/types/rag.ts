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
  category?: string | null;
  document_type?: string | null;
  published_date?: string | null;
  document_url: string | null;
  chunks?: {
    chunk_index: number;
    relevance_score: number;
  }[];
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

export interface NearbyPlace {
  name: string;
  distance_meters: number;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
  osm_type?: string;
  osm_id?: number;
}

export interface LandBusinessAssessment {
  observations: string[];
  opportunities: string[];
  risks: string[];
  requires_verification: string[];
  next_steps: string[];
}

export interface LandBusinessReport {
  report_version: string;
  property_overview: Record<string, unknown>;
  location_and_accessibility: {
    location_query?: Record<string, unknown> | null;
    geolocation?: LandGeolocation | null;
    document_roads: unknown[];
    nearby_roads: NearbyPlace[];
  };
  nearby_intelligence: Record<string, NearbyPlace[]>;
  business_assessment: LandBusinessAssessment;
  evidence_by_source: Record<string, unknown>;
}

export interface LandGeolocation {
  query?: string;
  matched_query?: string | null;
  found?: boolean;
  accuracy?: string;
  match_quality?: string;
  confidence?: string;
  source_confidence?: string | null;
  location_level?: string;
  address?: string;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

export interface LandAnalysisPage {
  land_business_report: LandBusinessReport;
}

export interface LandAnalysisResponse {
  agent: string;
  input_file: string;
  pages_processed: number;
  analysis: LandAnalysisPage[];
}
