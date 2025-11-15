<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Tabs -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav class="flex space-x-8" aria-label="Tabs">
          <a
            href="#"
            class="border-blue-500 text-blue-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
          >
            Stock Analysis
          </a>
          <a
            href="#"
            class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
          >
            Batch Analysis
          </a>
          <a
            href="#"
            class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
          >
            Stock Filter
          </a>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="space-y-6">
        <!-- Header -->
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Stock Analysis</h1>
          <p class="mt-2 text-sm text-gray-600">
            Analyze financial ratios from multiple sources
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="bg-white rounded-lg shadow p-8 text-center">
          <div class="animate-spin text-blue-500 text-4xl mb-4">⏳</div>
          <p class="text-gray-600">Analyzing stock data...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <span class="text-red-400 text-xl">✗</span>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">Error</h3>
              <div class="mt-2 text-sm text-red-700">
                <p>{{ error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Table -->
        <div v-else-if="analysisData">
          <div class="mb-4">
            <h2 class="text-xl font-semibold text-gray-900">
              Analysis for {{ analysisData.ticker }}
            </h2>
          </div>
          <SummaryTable
            :ratios="analysisData.ratios"
            :overall-score="analysisData.overall_score"
            :max-score="analysisData.max_score"
          />
        </div>

        <!-- Empty State -->
        <div v-else class="bg-white rounded-lg shadow p-8 text-center">
          <div class="text-gray-400 text-6xl mb-4">📊</div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No analysis yet</h3>
          <p class="text-gray-600">Enter a stock ticker below to get started</p>
        </div>

        <!-- Stock Input -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Analyze Stock</h3>
          <StockInput
            ref="stockInputRef"
            @analyze="handleAnalyze"
          />
        </div>

        <!-- Learning Opportunity Section (Optional) -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 class="text-lg font-medium text-blue-900 mb-2">💡 Learning Opportunity</h3>
          <p class="text-sm text-blue-800">
            This tool compares financial ratios from multiple sources to help you verify data accuracy.
            Each ratio is evaluated against target thresholds to provide a comprehensive analysis.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStockAnalysis } from '~/composables/useStockAnalysis'

const { 
  currentTicker, 
  analysisData, 
  isLoading, 
  error, 
  fetchAnalysis,
  clearResults 
} = useStockAnalysis()

const stockInputRef = ref<any>(null)

const handleAnalyze = async (ticker: string) => {
  // Set loading state on input component
  if (stockInputRef.value) {
    stockInputRef.value.setLoading(true)
    stockInputRef.value.setError(null)
  }
  
  await fetchAnalysis(ticker)
  
  // Update input component state after fetch
  if (stockInputRef.value) {
    stockInputRef.value.setLoading(false)
    if (error.value) {
      stockInputRef.value.setError(error.value)
    } else {
      stockInputRef.value.setError(null)
    }
  }
}
</script>
