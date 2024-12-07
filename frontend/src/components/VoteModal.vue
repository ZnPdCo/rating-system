<script setup>
import axios from 'axios'
import { SuiModal, SuiButton, Rating } from 'vue-fomantic-ui'
import { ref, watch } from 'vue'
const show = defineModel('show')
const pid = defineModel('pid')
const emit = defineEmits(['rating-change'])
const qualityValue = ref(0)
const reloadKey = ref(0) // for reloading the rating when the modal is closed and reopened or the rating is zero
const difficulty = ref(0)
const comment = ref('')

function SendVote() {
  if (difficulty.value < 800 || difficulty.value > 3500) {
    difficulty.value = ''
  }
  axios('/backend/vote/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      pid: pid.value,
      difficulty: difficulty.value == '' ? -1 : difficulty.value,
      quality: qualityValue.value - 1,
      comment: comment.value,
    },
  }).then(function (response) {
    if (response.data == -1) {
      alert('您暂无投票权限，请联系管理员')
      return
    }
    emit('rating-change')
  })
}
watch(show, async (value) => {
  if (value != true) return
  axios('/backend/get_vote/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      pid: pid.value,
    },
  }).then(function (response) {
    difficulty.value = response.data['difficulty'] == '-1' ? '' : response.data['difficulty']
    qualityValue.value = parseInt(response.data['quality']) + 1
    reloadKey.value++
    comment.value = response.data['comment']
  })
})
function cancleQuality() {
  qualityValue.value = 0
  reloadKey.value++
}
</script>

<template>
  <SuiModal v-model="show">
    <div class="header">投票</div>
    <div class="content">
      <div class="ui labeled input" style="margin-right: 10px">
        <div class="ui label">难度(800-3500)</div>
        <input
          type="number"
          placeholder="难度"
          data-tribute="true"
          v-model="difficulty"
          oninput="this.value = this.value.replace(/[^0-9]/g, '');"
        />
      </div>
      <div class="ui labeled input">
        <div class="ui label">质量(0-5)</div>
        <Rating
          :key="reloadKey"
          size="massive"
          v-model="qualityValue"
          :maxRating="6"
          color="yellow"
        />
        <SuiButton @click="cancleQuality()">取消</SuiButton>
      </div>
      <br />
      <div class="ui labeled input" style="margin-top: 10px">
        <div class="ui label">评论</div>
        <textarea
          type="text"
          placeholder="评论"
          data-tribute="true"
          v-model="comment"
          maxlength="255"
        ></textarea>
      </div>
    </div>
    <div class="actions">
      <SuiButton black @click="show = false">取消</SuiButton>
      <SuiButton positive @click="SendVote(), (show = false)">保存</SuiButton>
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
