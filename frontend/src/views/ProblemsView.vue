<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'
import { Dropdown, SuiLoader, SuiSegment } from 'vue-fomantic-ui'
import { useRouter } from 'vue-router'
import DifficultyValue from '../components/DifficultyValue.vue'
import QualityValue from '../components/QualityValue.vue'
import VoteModal from '../components/VoteModal.vue'
import ShowVotesModal from '../components/ShowVotesModal.vue'
import DetailsModal from '../components/DetailsModal.vue'

const router = useRouter()
const route = router.currentRoute.value
const problemsData = ref([])
const statusData = ref(() => {
  try {
    return JSON.parse(localStorage.getItem('status')) || {}
  } catch {
    return {}
  }
})
const announcement = ref('')
const pid = ref(1)
const details = ref({})
const voteModal = ref(false)
const showVotesModal = ref(false)
const detailsModal = ref(false)
const selectedType = ref(
  route.query.type != undefined ? { text: route.query.type, value: route.query.type } : undefined,
)
const sortBy = ref(route.query.sortBy != undefined ? route.query.sortBy : 'contest')
const typeData = ref([])
const loggedIn = window.loggedIn
const autoStatus = window.autoStatus
const loader = ref(true)

function updateURL() {
  if (selectedType.value == undefined) router.replace({ query: { sortBy: sortBy.value } })
  else router.replace({ query: { type: selectedType.value.value, sortBy: sortBy.value } })
}
function switchMedian() {
  for (let i = 0; i < problemsData.value.length; i++) {
    ;[problemsData.value[i]['difficulty'], problemsData.value[i]['difficulty2']] = [
      problemsData.value[i]['difficulty2'],
      problemsData.value[i]['difficulty'],
    ]
    ;[problemsData.value[i]['quality'], problemsData.value[i]['quality2']] = [
      problemsData.value[i]['quality2'],
      problemsData.value[i]['quality'],
    ]
  }
}
watch(selectedType, () => {
  updateURL()
})
watch(problemsData, (value) => {
  for (let i = 0; i < value.length; i++) {
    var type = ['未分类']
    if ('type' in value[i]['info']) type = value[i]['info']['type']
    type.forEach(function (t) {
      if (!typeData.value.some((el) => el.value == t)) {
        typeData.value.push({ text: t, value: t })
      }
    })
  }
})
watch(sortBy, (value) => {
  sortData(value)
  updateURL()
})
function updateProblemsData() {
  axios('/backend/get_problems/', {
    method: 'GET',
  }).then(function (response) {
    for (let i = 0; i < problemsData.value.length; i++) {
      problemsData.value[i] = response.data.find(
        (item) => item['pid'] == problemsData.value[i]['pid'],
      )
    }
  })
}
function saveStatus() {
  localStorage.setItem('status', JSON.stringify(statusData.value))
  axios('/backend/update_status/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
    data: {
      status: JSON.stringify(statusData.value),
    },
  })
}
function changeStatus(pid) {
  if (!(pid in statusData.value)) statusData.value[pid] = 0
  else if (statusData.value[pid] == 0) statusData.value[pid] = 1
  else if (statusData.value[pid] == 1) delete statusData.value[pid]
  saveStatus()
}

function sortData(sortBy) {
  try {
    problemsData.value.sort(function (a, b) {
      if (a[sortBy] == null && b[sortBy] == null) {
        return 0
      }
      if (a[sortBy] == null) {
        return 1
      }
      if (b[sortBy] == null) {
        return -1
      }
      return a[sortBy] > b[sortBy] ? -1 : 1
    })
  } catch (error) {
    console.error('Sorting error: ', error)
  }
}

axios('/backend/get_problems/', {
  method: 'GET',
}).then(function (response) {
  problemsData.value = response.data
  sortData(sortBy.value)
  loader.value = false
})
axios('/backend/get_status/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
}).then(function (response) {
  statusData.value = response.data
  saveStatus()
})
axios('/backend/get_announcement/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' },
}).then(function (response) {
  announcement.value = response.data
})
</script>

<style scoped>
table {
  table-layout: fixed;
  word-break: break-all;
}

table th:nth-child(1) {
  width: 10%;
}

table th:nth-child(2) {
  width: 20%;
}

table th:nth-child(3) {
  width: 40%;
}

table th:nth-child(4) {
  width: 7%;
}

table th:nth-child(5) {
  width: 7%;
}

table th:nth-child(6) {
  width: 7%;
}

table th:nth-child(7) {
  width: 9%;
}
</style>

<template>
  <SuiSegment basic>
    <SuiLoader :active="loader" />
    <div
      class="ui bottom attached warning message"
      v-if="announcement.length > 0"
      v-html="announcement"
    ></div>
    <div class="ui toggle checkbox" style="margin-top: 20px; margin-right: 20px">
      <input type="checkbox" @click="switchMedian()" />
      <label>显示中位数数据</label>
    </div>
    <Dropdown
      v-model="selectedType"
      :options="typeData"
      clearable
      selection
      placeholder="选择分类"
    />

    <div class="column" style="margin-top: 20px">
      <table class="ui left aligned table">
        <thead>
          <tr>
            <th>Pid</th>
            <th>
              比赛
              <span @click="sortBy = 'contest'"
                ><span v-if="sortBy == 'contest'">▾</span><span v-else>▴</span></span
              >
            </th>
            <th>题目名</th>
            <th>
              难度
              <span @click="sortBy = 'difficulty'"
                ><span v-if="sortBy == 'difficulty'">▾</span><span v-else>▴</span></span
              >
            </th>
            <th>
              质量
              <span @click="sortBy = 'quality'"
                ><span v-if="sortBy == 'quality'">▾</span><span v-else>▴</span></span
              >
            </th>
            <th>投票</th>
            <th>显示投票</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in problemsData" :key="index">
            <slot
              v-if="
                selectedType == undefined ||
                (item.info.type != undefined && item.info.type.includes(selectedType.value)) ||
                (item.info.type == undefined && selectedType.value == '未分类')
              "
            >
              <td>{{ item.pid }}</td>
              <td>{{ item.contest }}</td>
              <td
                @click="$event.target.tagName == 'TD' && !autoStatus && changeStatus(item.pid)"
                :style="{
                  'background-color':
                    statusData[item.pid] == 1
                      ? 'rgb(195, 230, 203)'
                      : statusData[item.pid] == 0
                        ? 'rgb(255, 238, 186)'
                        : '',
                }"
              >
                <a @click="(detailsModal = true), (details = item)">{{ item.name }}</a>
              </td>
              <td :data-tooltip="'投票人数：' + item.cnt1">
                <DifficultyValue :difficulty="item.difficulty" />
              </td>
              <td :data-tooltip="'投票人数：' + item.cnt2">
                <QualityValue :quality="item.quality" />
              </td>
              <td>
                <a
                  @click="
                    !loggedIn && router.push('/login?error=请先登录'),
                      (pid = item.pid),
                      (voteModal = true)
                  "
                  >投票</a
                >
              </td>
              <td>
                <a @click="(pid = item.pid), (showVotesModal = true)">显示投票</a>
              </td>
            </slot>
          </tr>
        </tbody>
      </table>
    </div>
  </SuiSegment>
  <VoteModal v-model:show="voteModal" v-model:pid="pid" @rating-change="updateProblemsData()" />
  <ShowVotesModal v-model:show="showVotesModal" v-model:pid="pid" />
  <DetailsModal v-model:show="detailsModal" v-model:details="details" />
</template>
