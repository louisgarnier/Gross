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
      <div v-if="hasMultipleSources" class="text-xs text-gray-500 mt-1">
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
</script>

