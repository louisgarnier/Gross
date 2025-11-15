<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-gray-900">
        Gross Financial Analysis - Phase 2 Test
      </h1>

      <!-- Backend Connection Test -->
      <div class="bg-white rounded-lg shadow p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Backend Connection Test</h2>
        
        <div class="space-y-4">
          <!-- Health Check -->
          <div>
            <button
              @click="testHealth"
              :disabled="healthLoading"
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
              {{ healthLoading ? 'Testing...' : 'Test Health Check' }}
            </button>
            <div v-if="healthStatus" class="mt-2">
              <span :class="healthStatus === 'success' ? 'text-green-600' : 'text-red-600'">
                {{ healthStatus === 'success' ? '✅ Backend is healthy' : '❌ Backend connection failed' }}
              </span>
              <pre v-if="healthData" class="mt-2 text-sm bg-gray-100 p-2 rounded">{{ JSON.stringify(healthData, null, 2) }}</pre>
            </div>
          </div>

          <!-- Test Stock Analysis -->
          <div>
            <div class="flex gap-2 mb-2">
              <input
                v-model="testTicker"
                type="text"
                placeholder="Enter ticker (e.g., PLTR)"
                class="px-4 py-2 border rounded flex-1"
                @keyup.enter="testAnalysis"
              />
              <button
                @click="testAnalysis"
                :disabled="analysisLoading"
                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:bg-gray-400"
              >
                {{ analysisLoading ? 'Loading...' : 'Test Analysis' }}
              </button>
            </div>
            <div v-if="analysisStatus" class="mt-2">
              <span :class="analysisStatus === 'success' ? 'text-green-600' : 'text-red-600'">
                {{ analysisStatus === 'success' ? '✅ API call successful' : '❌ API call failed' }}
              </span>
              <div v-if="analysisError" class="mt-2 text-red-600 text-sm">
                Error: {{ analysisError }}
              </div>
              <pre v-if="analysisData" class="mt-2 text-sm bg-gray-100 p-2 rounded overflow-auto max-h-96">{{ JSON.stringify(analysisData, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Test Buttons -->
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-xl font-semibold mb-4">Quick Test Stocks</h2>
        <div class="flex gap-2">
          <button
            @click="quickTest('PLTR')"
            class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            Test PLTR
          </button>
          <button
            @click="quickTest('NVDA')"
            class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            Test NVDA
          </button>
          <button
            @click="quickTest('MSFT')"
            class="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          >
            Test MSFT
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '~/composables/useApi'

const { healthCheck, analyzeStock } = useApi()

// Health check state
const healthLoading = ref(false)
const healthStatus = ref<'success' | 'error' | null>(null)
const healthData = ref<any>(null)

// Analysis state
const testTicker = ref('PLTR')
const analysisLoading = ref(false)
const analysisStatus = ref<'success' | 'error' | null>(null)
const analysisData = ref<any>(null)
const analysisError = ref<string | null>(null)

const testHealth = async () => {
  healthLoading.value = true
  healthStatus.value = null
  healthData.value = null
  
  try {
    const data = await healthCheck()
    healthData.value = data
    healthStatus.value = 'success'
  } catch (error: any) {
    healthStatus.value = 'error'
    healthData.value = { error: error.message }
  } finally {
    healthLoading.value = false
  }
}

const testAnalysis = async () => {
  if (!testTicker.value.trim()) return
  
  analysisLoading.value = true
  analysisStatus.value = null
  analysisData.value = null
  analysisError.value = null
  
  try {
    const data = await analyzeStock(testTicker.value.trim())
    analysisData.value = data
    analysisStatus.value = 'success'
  } catch (error: any) {
    analysisStatus.value = 'error'
    analysisError.value = error.message || 'Unknown error'
  } finally {
    analysisLoading.value = false
  }
}

const quickTest = (ticker: string) => {
  testTicker.value = ticker
  testAnalysis()
}
</script>

