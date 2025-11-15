<template>
  <div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Metric
          </th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Value
          </th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Target
          </th>
          <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Status
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <MetricRow
          v-for="ratio in ratios"
          :key="ratio.metric"
          :ratio="ratio"
        />
        <!-- Overall Score Row -->
        <tr class="bg-gray-50 border-t-2 border-gray-300">
          <td class="px-4 py-3 font-bold text-gray-900" colspan="2">
            Overall Score
          </td>
          <td class="px-4 py-3" colspan="2">
            <OverallScore :score="overallScore" :max-score="maxScore" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { RatioResult } from '~/types/stock'

interface Props {
  ratios: RatioResult[]
  overallScore: number
  maxScore: number
}

defineProps<Props>()
</script>

