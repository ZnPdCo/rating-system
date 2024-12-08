<script setup>
import { ref, watch } from 'vue'
const difficulty = defineModel('difficulty')
const textColor = ref('gray')
const circleStyle = ref({})

const thresholds = [
  { min: 2400, color: 'red' },
  { min: 2100, color: 'rgb(255,140,0)' },
  { min: 1900, color: 'rgb(170,0,170)' },
  { min: 1600, color: 'blue' },
  { min: 1400, color: 'rgb(3,168,158)' },
  { min: 1200, color: 'green' },
  { min: 1000, color: 'rgb(136,204,34)' },
  { min: 0, color: 'gray' },
]

function colorText(value) {
  if (value == null) {
    textColor.value = 'gray'
    return
  }
  textColor.value = thresholds.find(threshold => value >= threshold.min).color
}
function colorCircle(value) {
  var col = ''
  var percentage = 0
  if (value == null) {
    col += 'gray'
    percentage = 0
  } else if (value >= 2400 && value < 3000) {
    col += 'red'
    percentage = (value - 2400) / 6
  } else if (value >= 2100) {
    col += 'rgb(255,140,0)'
    percentage = (value - 2100) / 3
  } else if (value >= 1900) {
    col += 'rgb(170,0,170)'
    percentage = (value - 1900) / 2
  } else if (value >= 1600) {
    col += 'blue'
    percentage = (value - 1600) / 3
  } else if (value >= 1400) {
    col += 'rgb(3,168,158)'
    percentage = (value - 1400) / 2
  } else if (value >= 1200) {
    col += 'green'
    percentage = (value - 1200) / 2
  } else if (value >= 1000) {
    col += 'rgb(136,204,34)'
    percentage = (value - 1000) / 2
  } else {
    col += 'gray'
    percentage = (value - 800) / 2
  }
  if (value >= 3400) {
    circleStyle.value = {
      borderColor: '#FFD700',
      background: 'linear-gradient(to right, #FFD700, white, #FFD700)',
    }
  } else if (value >= 3200) {
    circleStyle.value = {
      borderColor: '#808080',
      background: 'linear-gradient(to right, #808080, white, #808080)',
    }
  } else if (value >= 3000) {
    circleStyle.value = {
      borderColor: '#965C2C',
      background: 'linear-gradient(to right, #965C2C, #FFDABD, #965C2C)',
    }
  } else {
    percentage = Math.round(10 * percentage) / 10
    circleStyle.value = {
      borderColor: col,
      background: `linear-gradient(to top, ${col} 0%, ${col} ${percentage}%, rgba(0, 0, 0, 0) ${percentage}%, rgba(0, 0, 0, 0) 100%)`,
    }
  }
}

watch(difficulty, (value) => {
    colorText(value)
    colorCircle(value)
})
colorText(difficulty.value)
colorCircle(difficulty.value)
</script>

<template>
  <span :style="{ color: textColor, fontWeight: 500 }"
    ><span :style="circleStyle" class="circle"></span>{{ difficulty == null ? 'N/A' : difficulty }}</span
  >
</template>

<style scoped>
.circle {
    display: inline-block;
    border-radius: 50%;
    border-style: solid;
    border-width: 1px;
    margin-right: 5px;
    height: 12px;
    width: 12px;
}
</style>
