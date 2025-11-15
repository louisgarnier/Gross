/**
 * Composable for managing stock analysis state and operations.
 * 
 * This manages:
 * - What ticker is currently selected
 * - The analysis data we received from the API
 * - Loading states (is it fetching data?)
 * - Error states (did something go wrong?)
 */

export const useStockAnalysis = () => {
  const { analyzeStock } = useApi()

  // Reactive state - these values can change and the UI will update automatically
  const currentTicker = ref<string>('')
  const analysisData = ref<AnalysisResponse | null>(null)
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)

  /**
   * Fetch analysis for a given ticker.
   * This calls the backend API and stores the result.
   */
  const fetchAnalysis = async (ticker: string) => {
    if (!ticker || !ticker.trim()) {
      error.value = 'Please enter a valid ticker symbol'
      return
    }

    isLoading.value = true
    error.value = null
    currentTicker.value = ticker.toUpperCase().trim()

    try {
      const data = await analyzeStock(currentTicker.value)
      analysisData.value = data
      error.value = null
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch analysis'
      analysisData.value = null
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Clear current analysis data.
   * Resets everything to empty state.
   */
  const clearResults = () => {
    currentTicker.value = ''
    analysisData.value = null
    error.value = null
    isLoading.value = false
  }

  return {
    // State (read-only so components can't accidentally change them)
    currentTicker: readonly(currentTicker),
    analysisData: readonly(analysisData),
    isLoading: readonly(isLoading),
    error: readonly(error),
    // Methods
    fetchAnalysis,
    clearResults,
  }
}

