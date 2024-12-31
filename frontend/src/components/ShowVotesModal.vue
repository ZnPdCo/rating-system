<script setup>
import axios from 'axios'
import { SuiModal, SuiLoader, SuiSegment } from 'vue-fomantic-ui'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import DifficultyValue from './DifficultyValue.vue'
import QualityValue from './QualityValue.vue'

const router = useRouter()
const show = defineModel('show')
const pid = defineModel('pid')
const votesData = ref([])
const loader = ref(false)
const loggedIn = window.loggedIn

function report(id) {
  loader.value = true
  axios('/backend/report/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      id: id,
    },
  }).then(function () {
    if (!loggedIn) {
      router.push('/login?error=请先登录')
      return
    }
    loader.value = false
    alert('举报成功！管理员将会进行审核。')
  })
}
watch(show, async (value) => {
  if (value != true) return
  loader.value = true
  votesData.value = []

  axios('/backend/get_votes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      pid: pid.value,
    },
  }).then(function (response) {
    votesData.value = response.data
    loader.value = false
  })
})
</script>

<template>
  <SuiModal v-model="show">
    <div class="header">显示投票</div>
    <div class="content">
      <SuiSegment basic>
        <SuiLoader :active="loader" />
        <table class="ui left aligned table unstackable scrolling" id="vote-table">
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
              <td>
                <DifficultyValue :difficulty="item.difficulty" />
              </td>
              <td>
                <QualityValue :quality="item.quality" />
              </td>
              <td style="overflow: hidden">{{ item.comment }}</td>
              <td><a @click="report(item.id)">举报</a></td>
            </tr>
          </tbody>
        </table>
      </SuiSegment>
    </div>
    <div class="actions">
      <div class="ui positive button" @click="show = false">OK</div>
    </div>
  </SuiModal>
</template>
