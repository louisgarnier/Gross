<template>
  <div class="flex items-center gap-2">
    <span class="text-lg font-bold" :class="scoreColor">
      {{ score }}/{{ maxScore }}
    </span>
    <span v-if="showWarning" class="text-yellow-500 text-xl">⚠</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  score: number
  maxScore: number
}

const props = defineProps<Props>()

const scoreColor = computed(() => {
  const percentage = (props.score / props.maxScore) * 100
  if (percentage >= 75) return 'text-green-600'
  if (percentage >= 50) return 'text-yellow-600'
  return 'text-red-600'
})

const showWarning = computed(() => {
  const percentage = (props.score / props.maxScore) * 100
  return percentage < 50
})
</script>

