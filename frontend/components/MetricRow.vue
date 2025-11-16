<template>
  <tr class="hover:bg-gray-50 border-b">
    <td class="px-4 py-3 font-medium text-gray-900">
      {{ ratio.metric }}
    </td>
    <td class="px-4 py-3 text-gray-700">
      <div v-if="formattedValue" class="font-semibold">
        {{ formattedValue }}
      </div>
      <div v-else class="text-gray-400 italic">
        No data
      </div>
      <!-- Show individual source values -->
      <div v-if="hasMultipleSources && hasValidValues" class="text-xs text-gray-500 mt-1 space-y-0.5">
        <div v-for="sourceValue in validSourceValues" :key="sourceValue.source" class="flex justify-between">
          <span>{{ sourceValue.source }}:</span>
          <span class="font-medium">{{ formatSourceValue(sourceValue.value) }}</span>
        </div>
        <!-- Show spread if available -->
        <div v-if="ratio.spread !== null && ratio.spread !== undefined" class="mt-1 pt-1 border-t border-gray-300">
          <span class="font-semibold" :class="spreadClass">
            Écart: {{ formatSpread(ratio.spread) }}
          </span>
        </div>
      </div>
      <div v-else-if="hasMultipleSources" class="text-xs text-gray-500 mt-1">
        {{ sourceCount }} sources
      </div>
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
}

const props = defineProps<Props>()

const formattedValue = computed(() => {
  if (props.ratio.consensus === null) return null
  
  // Format based on metric type
  if (props.ratio.metric.includes('Margin') || props.ratio.metric.includes('ROIC')) {
    return `${props.ratio.consensus.toFixed(2)}%`
  }
  
  if (props.ratio.metric === 'P/E Ratio') {
    return props.ratio.consensus.toFixed(2)
  }
  
  if (props.ratio.metric === 'Interest Coverage') {
    return `${props.ratio.consensus.toFixed(2)}x`
  }
  
  return props.ratio.consensus.toFixed(2)
})

const hasMultipleSources = computed(() => {
  return props.ratio.values.length > 1
})

const sourceCount = computed(() => {
  const validSources = props.ratio.values.filter(v => v.value !== null).length
  return validSources > 0 ? validSources : props.ratio.values.length
})

const hasValidValues = computed(() => {
  return props.ratio.values.some(v => v.value !== null)
})

const validSourceValues = computed(() => {
  return props.ratio.values.filter(v => v.value !== null)
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

