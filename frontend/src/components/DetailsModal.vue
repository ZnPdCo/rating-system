<script setup>
import { SuiModal } from 'vue-fomantic-ui'
const show = defineModel('show')
const details = defineModel('details')
function isUrl(string) {
  try {
    new URL(string)
    return true
  } catch {
    return false
  }
}
</script>

<template>
  <SuiModal v-model="show">
    <div class="header">详细信息</div>
    <div class="content">
      <ul class="ui list">
        <li>比赛: {{ details.contest }}</li>
        <li>题目名: {{ details.name }}</li>
        <li v-for="(value, key, index) in details.info" :key="index">
          <span v-if="key == 'links'"
            >题目链接：<a :href="value" target="_blank">{{ value }}</a></span
          >
          <span v-else-if="key == 'source' && isUrl(value)"
            >来源/作者：<a :href="value" target="_blank">{{ value }}</a></span
          >
          <span v-else-if="key == 'source'">来源/作者：{{ value }}</span>
          <span v-else-if="key == 'type'">分类：{{ value }}</span>
          <span v-else>{{ key }}：{{ value }}</span>
        </li>
      </ul>
    </div>
    <div class="actions">
      <div class="ui positive button" @click="show = false">OK</div>
    </div>
  </SuiModal>
</template>
