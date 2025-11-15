/**
 * API client composable for making requests to the backend.
 * 
 * This is how the frontend talks to the backend API.
 */

export const useApi = () => {
  const config = useRuntimeConfig()
  const apiBaseUrl = config.public.apiBaseUrl || 'http://localhost:8000'

  /**
   * Analyze a stock ticker.
   * Calls the backend API and returns the analysis data.
   */
  const analyzeStock = async (ticker: string): Promise<AnalysisResponse> => {
    try {
      const url = `${apiBaseUrl}/api/analyze/${ticker.toUpperCase()}`
      console.log('Fetching from:', url)
      
      const response = await $fetch<AnalysisResponse>(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      return response
    } catch (error: any) {
      console.error('Error fetching stock analysis:', error)
      console.error('API Base URL:', apiBaseUrl)
      console.error('Full error:', error)
      
      // More detailed error message
      const errorMessage = error.data?.detail || 
                          error.message || 
                          error.toString() || 
                          'Failed to fetch stock analysis. Make sure backend is running on http://localhost:8000'
      
      throw new Error(errorMessage)
    }
  }

  /**
   * Health check endpoint.
   * Tests if the backend is running.
   */
  const healthCheck = async (): Promise<{ status: string; service: string }> => {
    try {
      const response = await $fetch<{ status: string; service: string }>(
        `${apiBaseUrl}/api/health`
      )
      return response
    } catch (error) {
      console.error('Health check failed:', error)
      throw error
    }
  }

  return {
    analyzeStock,
    healthCheck,
  }
}

