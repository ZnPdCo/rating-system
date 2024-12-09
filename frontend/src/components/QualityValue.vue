<script setup>
import { ref, watch } from 'vue'
const quality = defineModel('quality')
const textColor = ref('gray')

const thresholds = [
  { min: 5, color: 'rgb(0,128,0)' },
  { min: 4, color: 'rgb(34,139,34)' },
  { min: 3, color: 'rgb(80,200,120)' },
  { min: 2, color: 'rgb(144,238,144)' },
  { min: 1, color: 'gray' },
  { min: 0, color: 'rgb(157,108,73)' },
]

function colorText(value) {
  if (value == null) {
    textColor.value = 'gray'
    return
  }
  textColor.value = thresholds.find((threshold) => Math.round(value) >= threshold.min).color
}

watch(quality, (value) => {
  colorText(value)
})
colorText(quality.value)
</script>

<template>
  <span :style="{ color: textColor, fontWeight: 500 }">{{
    quality == null ? 'N/A' : (Math.round(quality) == 0 ? '💩' : '') + Math.round(quality * 10) / 10
  }}</span>
</template>
