/**
 * TypeScript interfaces matching the backend API schemas.
 * 
 * This is the "contract" - it tells TypeScript exactly what data structure
 * to expect from the backend API. It must match the backend schemas exactly.
 */

export interface SourceValue {
  source: string
  value: number | null
}

export interface RatioResult {
  metric: string
  values: SourceValue[]
  consensus: number | null
  target: string
  status: 'Pass' | 'Fail' | 'Info Only'
}

export interface AnalysisResponse {
  ticker: string
  ratios: RatioResult[]
  overall_score: number
  max_score: number
}

