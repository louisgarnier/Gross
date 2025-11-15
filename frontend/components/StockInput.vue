<template>
  <div class="space-y-2">
    <div class="flex gap-2">
      <input
        v-model="tickerInput"
        type="text"
        placeholder="Enter stock ticker (e.g., PLTR)"
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :disabled="loading"
        @keyup.enter="handleSubmit"
      />
      <button
        @click="handleSubmit"
        :disabled="loading || !tickerInput.trim()"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <span v-if="loading" class="animate-spin">⏳</span>
        <span v-else>🔍</span>
        <span>{{ loading ? 'Analyzing...' : 'Analyze' }}</span>
      </button>
    </div>
    <div v-if="error" class="text-red-600 text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  analyze: [ticker: string]
}>()

const tickerInput = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const handleSubmit = () => {
  const ticker = tickerInput.value.trim().toUpperCase()
  
  if (!ticker) {
    error.value = 'Please enter a ticker symbol'
    return
  }

  error.value = null
  loading.value = true
  emit('analyze', ticker)
}

// Allow parent to control loading state
defineExpose({
  setLoading: (value: boolean) => {
    loading.value = value
  },
  setError: (value: string | null) => {
    error.value = value
  },
  clearInput: () => {
    tickerInput.value = ''
  }
})
</script>

