<script setup>
import $ from 'jquery'
import { SuiModal, SuiButton, Rating } from 'vue-fomantic-ui'
import { ref, watch } from 'vue'
const show = defineModel('show')
const pid = defineModel('pid')
const emit = defineEmits(['rating-change'])
const qualityValue = ref(0)
const reloadKey = ref(0) // 用于重新渲染rating组件

function SendVote() {
  let difficulty = $('#difficulty').val()
  let quality = qualityValue.value - 1
  let comment = $('#comment').val()
  if (difficulty < 800 || difficulty > 3500 || difficulty == '') {
    difficulty = -1
  }
  if (quality < 0 || quality > 5) {
    quality = -1
  }
  $.ajax({
    url: '/backend/vote/',
    type: 'POST',
    data: {
      pid: pid.value,
      difficulty: difficulty,
      quality: quality,
      comment: comment,
    },
    success: function (data) {
      if (data == -1) {
        alert('您暂无投票权限，请联系管理员')
        return
      }
      emit('rating-change')
    },
  })
}
watch(show, async (value) => {
  if (value != true) return
  $.ajax({
    url: '/backend/get_vote/',
    type: 'POST',
    data: {
      pid: pid.value,
    },
    success: function (data) {
      $('#difficulty').val(data['difficulty'] == '-1' ? '' : data['difficulty'])
      qualityValue.value = parseInt(data['quality']) + 1
      reloadKey.value++
      $('#comment').val(data['comment'])
    },
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
          id="difficulty"
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
        <textarea type="text" placeholder="评论" data-tribute="true" id="comment"></textarea>
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
