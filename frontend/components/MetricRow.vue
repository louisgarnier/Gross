<template>
  <tr class="hover:bg-gray-50 border-b">
    <td class="px-4 py-3 font-medium text-gray-900">
      {{ ratio.metric }}
    </td>
    <!-- Dynamic source columns -->
    <td
      v-for="source in allSources"
      :key="source"
      class="px-3 py-3 text-center text-sm"
    >
      <span v-if="getSourceValue(source)" class="font-medium text-gray-900">
        {{ formatSourceValue(getSourceValue(source)) }}
      </span>
      <span v-else class="text-gray-300">—</span>
    </td>
    <!-- Number of sources column -->
    <td class="px-4 py-3 text-center text-sm text-gray-600">
      <span class="font-medium">{{ validSourceCount }}</span>
      <span v-if="ratio.spread !== null && ratio.spread !== undefined && ratio.spread > 0" 
            class="block text-xs mt-1" :class="spreadClass">
        Écart: {{ formatSpread(ratio.spread) }}
      </span>
    </td>
    <td class="px-4 py-3 text-gray-600">
      {{ ratio.target }}
    </td>
    <td class="px-4 py-3">
      <StatusBadge :status="ratio.status as 'Pass' | 'Fail' | 'Info Only'" />
    </td>
  </tr>
</template>

<script setup lang="ts">
import type { RatioResult } from '~/types/stock'

interface Props {
  ratio: RatioResult
  allSources: string[]
}

const props = defineProps<Props>()

// Get value for a specific source
const getSourceValue = (source: string): number | null => {
  const sourceValue = props.ratio.values.find(v => v.source === source)
  return sourceValue?.value ?? null
}

const validSourceCount = computed(() => {
  return props.ratio.values.filter(v => v.value !== null).length
})


const formatSourceValue = (value: number | null): string => {
  if (value === null) return 'N/A'
  
  if (props.ratio.metric.includes('Margin') || props.ratio.metric.includes('ROIC')) {
    return `${value.toFixed(2)}%`
  }
  
  if (props.ratio.metric === 'P/E Ratio') {
    return value.toFixed(2)
  }
  
  if (props.ratio.metric === 'Interest Coverage') {
    return `${value.toFixed(2)}x`
  }
  
  return value.toFixed(2)
}

const formatSpread = (spread: number): string => {
  if (props.ratio.metric.includes('Margin') || props.ratio.metric.includes('ROIC')) {
    return `${spread.toFixed(2)}%`
  }
  
  if (props.ratio.metric === 'P/E Ratio') {
    return spread.toFixed(2)
  }
  
  if (props.ratio.metric === 'Interest Coverage') {
    return `${spread.toFixed(2)}x`
  }
  
  return spread.toFixed(2)
}

const spreadClass = computed(() => {
  if (props.ratio.spread === null || props.ratio.spread === undefined) return ''
  
  // Determine if spread is high (inconsistency warning)
  const consensus = props.ratio.consensus
  if (consensus === null || consensus === 0) return 'text-gray-600'
  
  // Calculate spread as percentage of consensus
  const spreadPercent = (props.ratio.spread / Math.abs(consensus)) * 100
  
  // If spread is more than 20% of consensus, it's a warning
  if (spreadPercent > 20) {
    return 'text-orange-600'
  }
  
  return 'text-gray-600'
})
</script>

