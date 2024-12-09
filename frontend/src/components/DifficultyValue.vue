<script setup>
import { ref, watch } from 'vue'
const difficulty = defineModel('difficulty')
const textColor = ref('gray')
const circleBorder = ref('gray')
const circleBackground = ref('transparent')

const thresholds = [
  { min: 2400, max: 3000, color: 'red' },
  { min: 2100, max: 2400, color: 'rgb(255,140,0)' },
  { min: 1900, max: 2100, color: 'rgb(170,0,170)' },
  { min: 1600, max: 1900, color: 'blue' },
  { min: 1400, max: 1600, color: 'rgb(3,168,158)' },
  { min: 1200, max: 1400, color: 'green' },
  { min: 1000, max: 1200, color: 'rgb(136,204,34)' },
  { min: 800, max: 1000, color: 'gray' },
]

function colorText(value) {
  if (value == null) {
    textColor.value = 'gray'
    return
  }
  textColor.value = thresholds.find((threshold) => value >= threshold.min).color
}
function colorCircle(value) {
  if (value >= 3400) {
    circleBorder.value = '#FFD700'
    circleBackground.value = 'linear-gradient(to right, #FFD700, white, #FFD700)'
  } else if (value >= 3200) {
    circleBorder.value = '#808080'
    circleBackground.value = 'linear-gradient(to right, #808080, white, #808080)'
  } else if (value >= 3000) {
    circleBorder.value = '#965C2C'
    circleBackground.value = 'linear-gradient(to right, #965C2C, #FFDABD, #965C2C)'
  } else {
    var threshold = thresholds.find((threshold) => value >= threshold.min)
    circleBorder.value = threshold.color
    var percentage = ((value - threshold.min) / (threshold.max - threshold.min)) * 100
    percentage = Math.round(10 * percentage) / 10
    circleBackground.value = `linear-gradient(to top, ${circleBorder.value} 0%, ${circleBorder.value} ${percentage}%, rgba(0, 0, 0, 0) ${percentage}%, rgba(0, 0, 0, 0) 100%)`
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
    ><span
      :style="{ borderColor: circleBorder, background: circleBackground }"
      class="circle"
    ></span
    >{{ difficulty == null ? 'N/A' : difficulty }}</span
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
