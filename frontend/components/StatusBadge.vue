<template>
  <span
    :class="badgeClasses"
    class="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-semibold"
  >
    <span v-if="status === 'Pass'" class="text-white">✓</span>
    <span v-else-if="status === 'Fail'" class="text-white">✗</span>
    <span v-else-if="status === 'Info Only'" class="text-white">ℹ</span>
    <span>{{ status }}</span>
  </span>
</template>

<script setup lang="ts">
interface Props {
  status: 'Pass' | 'Fail' | 'Info Only'
}

const props = defineProps<Props>()

const badgeClasses = computed(() => {
  switch (props.status) {
    case 'Pass':
      return 'bg-green-500 text-white'
    case 'Fail':
      return 'bg-red-500 text-white'
    case 'Info Only':
      return 'bg-blue-500 text-white'
    default:
      return 'bg-gray-500 text-white'
  }
})
</script>

