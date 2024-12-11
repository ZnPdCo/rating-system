<script setup>
import axios from 'axios'
import { SuiModal } from 'vue-fomantic-ui'
import { ref, watch } from 'vue'
import DifficultyValue from './DifficultyValue.vue'
import QualityValue from './QualityValue.vue'
const show = defineModel('show')
const pid = defineModel('pid')
const votesData = ref([])

function report(id) {
  axios('/backend/report/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      id: id,
    },
  }).then(function () {
    alert('举报成功！管理员将会进行审核。')
  })
}
watch(show, async (value) => {
  if (value != true) return

  axios('/backend/get_votes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      pid: pid.value,
    },
  }).then(function (response) {
    votesData.value = response.data
  })
})
</script>

<template>
  <SuiModal v-model="show">
    <div class="header">显示投票</div>
    <div class="content">
      <table class="ui left aligned table" id="vote-table">
        <thead>
          <tr>
            <th>难度</th>
            <th>质量</th>
            <th>评论</th>
            <th>举报</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in votesData" :key="index">
            <td><DifficultyValue :difficulty="item.difficulty" /></td>
            <td><QualityValue :quality="item.quality" /></td>
            <td>{{ item.comment }}</td>
            <td><a @click="report(item.id)">举报</a></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="actions">
      <div class="ui positive button" @click="show = false">OK</div>
    </div>
  </SuiModal>
</template>

<style scoped>
:deep(.star.icon:nth-child(1)::before) {
  content: '💩';
}

:deep(.star.active.icon:nth-child(1)) {
  text-shadow:
    0 -1px 0 #cc7722,
    -1px 0 0 #cc7722,
    0 1px 0 #cc7722,
    1px 0 0 #cc7722 !important;
}
</style>
