<script setup>
import $ from 'jquery'
import { ref } from 'vue'
import { SuiModal } from 'vue-fomantic-ui'
import { useRouter } from 'vue-router'
import VoteModal from '../components/VoteModal.vue'

const router = useRouter()
var problemsData = []
var statusData = {}
const voteModal = ref(false)
const pid = ref(1)
const showVotesModal = ref(false)
const detailsModal = ref(false)
const loggedIn = window.loggedIn

function name2Str(pid, name, func) {
  statusData = JSON.parse(localStorage.getItem('status'))
  var content = $('<a>').text(name).click(func)
  if (!(pid in statusData)) return $('<td>').append(content)
  if (statusData[pid] == 0)
    return $('<td>').css({ 'background-color': 'rgb(255, 238, 186)' }).append(content)
  if (statusData[pid] == 1)
    return $('<td>').css({ 'background-color': 'rgb(195, 230, 203)' }).append(content)
  return $('<td>').append(content)
}

function difficulty2Str(difficulty, cnt) {
  var res = $('<td>')
  if (difficulty == null) {
    res.css('color', 'gray')
  } else if (difficulty >= 2400) {
    res.css('color', 'red')
  } else if (difficulty >= 2100) {
    res.css('color', 'rgb(255,140,0)')
  } else if (difficulty >= 1900) {
    res.css('color', 'rgb(170,0,170)')
  } else if (difficulty >= 1600) {
    res.css('color', 'blue')
  } else if (difficulty >= 1400) {
    res.css('color', 'rgb(3,168,158)')
  } else if (difficulty >= 1200) {
    res.css('color', 'green')
  } else if (difficulty >= 1000) {
    res.css('color', 'rgb(136,204,34)')
  } else {
    res.css('color', 'gray')
  }
  res.css('font-weight', '500')
  res.attr('data-toggle', 'popover')
  if (cnt != null) res.attr('data-tooltip', `投票人数： ${cnt}`)
  res.append(difficulty2Circle(difficulty))
  res.append(` ${difficulty == null ? 'N/A' : Math.round(difficulty)}`)
  return res
}

function difficulty2Circle(difficulty) {
  var percentage = 0
  var col = ''
  var res = $('<span>')
  res.css({
    display: 'inline-block',
    'border-radius': '50%',
    'border-style': 'solid',
    'border-width': '1px',
    'margin-right': '5px',
    height: '12px',
    width: '12px',
  })
  if (difficulty == null) {
    col += 'gray'
    percentage = 0
  } else if (difficulty >= 2400 && difficulty < 3000) {
    col += 'red'
    percentage = (difficulty - 2400) / 6
  } else if (difficulty >= 2100) {
    col += 'rgb(255,140,0)'
    percentage = (difficulty - 2100) / 3
  } else if (difficulty >= 1900) {
    col += 'rgb(170,0,170)'
    percentage = (difficulty - 1900) / 2
  } else if (difficulty >= 1600) {
    col += 'blue'
    percentage = (difficulty - 1600) / 3
  } else if (difficulty >= 1400) {
    col += 'rgb(3,168,158)'
    percentage = (difficulty - 1400) / 2
  } else if (difficulty >= 1200) {
    col += 'green'
    percentage = (difficulty - 1200) / 2
  } else if (difficulty >= 1000) {
    col += 'rgb(136,204,34)'
    percentage = (difficulty - 1000) / 2
  } else {
    col += 'gray'
    percentage = (difficulty - 800) / 2
  }
  if (difficulty >= 3400) {
    res.css({
      'border-color': '#FFD700',
      background: 'linear-gradient(to right, #FFD700, white, #FFD700)',
    })
  } else if (difficulty >= 3200) {
    res.css({
      'border-color': '#808080',
      background: 'linear-gradient(to right, #808080, white, #808080)',
    })
  } else if (difficulty >= 3000) {
    res.css({
      'border-color': '#965C2C',
      background: 'linear-gradient(to right, #965C2C, #FFDABD, #965C2C)',
    })
  } else {
    percentage = Math.round(10 * percentage) / 10
    res.css({
      'border-color': col,
      background: `linear-gradient(to top, ${col} 0%, ${col} ${percentage}%, rgba(0, 0, 0, 0) ${percentage}%, rgba(0, 0, 0, 0) 100%)`,
    })
  }
  return res
}

function quality2Str(quality, cnt) {
  var showQuality = Math.round(quality * 10) / 10
  var res = $('<td>')
  if (quality == null) {
    res.css('color', 'gray')
    showQuality = 'N/A'
  } else {
    quality = Math.round(quality)
    if (quality == 0) {
      res.css('color', 'rgb(157, 108, 73)')
      showQuality = '💩 ' + showQuality
    } else if (quality == 1) {
      res.css('color', 'gray')
    } else if (quality == 2) {
      res.css('color', 'rgb(144, 238, 144)')
    } else if (quality == 3) {
      res.css('color', 'rgb(80, 200, 120)')
    } else if (quality == 4) {
      res.css('color', 'rgb(34, 139, 34)')
    } else {
      res.css('color', 'rgb(0, 128, 0)')
    }
  }
  res.css('font-weight', '500')
  res.attr('data-toggle', 'popover')
  if (cnt != null) res.attr('data-tooltip', `投票人数： ${cnt}`)
  res.text(showQuality)
  return res
}

function showTable() {
  let table = $('#problems-table tbody')
  table.empty()
  for (let i = 0; i < problemsData.length; i++) {
    let row = $('<tr>')
    ;(function (data) {
      row.append($('<td>').text(data['pid']))
      row.append($('<td>').text(data['contest']))
      row.append(
        name2Str(data['pid'], data['name'], function () {
          Details(data)
        }).click(function (e) {
          if ($(e.target).prop('tagName') == 'TD' && !window.autoStatus) changeStatus(data['pid'])
        }),
      )
      row.append(difficulty2Str(data['difficulty'], data['cnt1']))
      row.append(quality2Str(data['quality'], data['cnt2']))
      row.append(
        $('<td>')
          .html('<a>投票</a>')
          .click(function () {
            pid.value = data['pid']
            if (!loggedIn) {
              router.push('/login')
            }
            voteModal.value = true
          }),
      )
      row.append(
        $('<td>')
          .html('<a>显示投票</a>')
          .click(function () {
            window.pid = data['pid']
            showVotesModal.value = true
            showVotes()
          }),
      )
    })(problemsData[i])
    table.append(row)
  }
}
function updateProblemsData() {
  $.ajax({
    url: '/backend/get_problems/',
    type: 'GET',
    success: function (data) {
      for (let i = 0; i < problemsData.length; i++) {
        problemsData[i] = data.find((item) => item['pid'] == problemsData[i]['pid'])
      }
      showTable()
    },
  })
}
function changeStatus(pid) {
  statusData = JSON.parse(localStorage.getItem('status'))
  if (!(pid in statusData)) statusData[pid] = 0
  else if (statusData[pid] == 0) statusData[pid] = 1
  else if (statusData[pid] == 1) delete statusData[pid]
  localStorage.setItem('status', JSON.stringify(statusData))
  showTable()
  $.ajax({
    url: '/backend/update_status/',
    type: 'POST',
    data: {
      status: JSON.stringify(statusData),
    },
  })
}
function showVotes() {
  let table = $('#vote-table tbody')
  table.empty()

  $.ajax({
    url: '/backend/get_votes/',
    type: 'POST',
    data: {
      pid: window.pid,
    },
    success: function (data) {
      data.forEach(function (vote) {
        let row = $('<tr>')
        row.append(difficulty2Str(vote['difficulty'], null))
        row.append(quality2Str(vote['quality'], null))
        row.append($('<td>').text(vote['comment']))
        addReportLink(row, vote['id'])
        table.append(row)
      })
    },
  })
}
function Details(details) {
  detailsModal.value = true
  $('#details').empty()
  $('#details').append($('<li>').text(`Contest: ${details['contest']}`))
  $('#details').append($('<li>').text(`Name: ${details['name']}`))
  $('#details').append(
    $('<li>').append(
      $('<a>').text(`Links: ${details['info']['links']}`).attr('href', details['info']['links']),
    ),
  )
  Object.entries(details['info']).forEach(function ([key, value]) {
    if (key != 'links') {
      $('#details').append($('<li>').text(`${key}: ${value}`))
    }
  })
}

function addReportLink(row, id) {
  row.append(
    $('<td>')
      .html('<a>Report</a>')
      .click(function () {
        $.ajax({
          url: '/backend/report/',
          type: 'POST',
          data: {
            id: id,
          },
          success: function () {
            alert('Report!')
          },
        })
      }),
  )
}

function sortData(sortBy) {
  try {
    problemsData.sort(function (a, b) {
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
    showTable()
  } catch (error) {
    console.error('Sorting error: ', error)
  }
}

$(document).ready(function () {
  if (localStorage.getItem('status') == null) {
    localStorage.setItem('status', JSON.stringify('{}'))
  }
  $.ajax({
    url: '/backend/get_problems/',
    type: 'GET',
    success: function (data) {
      problemsData = data
      sortData('contest')
      showTable()
    },
  })
  $.ajax({
    url: '/backend/get_status/',
    type: 'POST',
    success: function (data) {
      localStorage.setItem('status', JSON.stringify(data))
      showTable()
    },
  })
  $.ajax({
    url: '/backend/get_announcement/',
    type: 'POST',
    success: function (data) {
      if (data != '') {
        $('#announcement').html(data).show()
      }
    },
  })

  $('#contest-header').click(function () {
    $('#contest-header').text('比赛 ▾')
    $('#difficulty-header').text('难度 ▴')
    $('#quality-header').text('质量 ▴')
    sortData('contest')
  })

  $('#difficulty-header').click(function () {
    $('#contest-header').text('比赛 ▴')
    $('#difficulty-header').text('难度 ▾')
    $('#quality-header').text('质量 ▴')
    sortData('difficulty')
  })

  $('#quality-header').click(function () {
    $('#contest-header').text('比赛 ▴')
    $('#difficulty-header').text('难度 ▴')
    $('#quality-header').text('质量 ▾')
    sortData('quality')
  })

  $('#use-median').click(function () {
    for (let i = 0; i < problemsData.length; i++) {
      ;[problemsData[i]['difficulty'], problemsData[i]['difficulty2']] = [
        problemsData[i]['difficulty2'],
        problemsData[i]['difficulty'],
      ]
      ;[problemsData[i]['quality'], problemsData[i]['quality2']] = [
        problemsData[i]['quality2'],
        problemsData[i]['quality'],
      ]
    }
    showTable()
  })
})
</script>

<style scoped>
table {
  table-layout: fixed;
  word-break: break-all;
}

#problems-table th:nth-child(1) {
  width: 10%;
}

#problems-table th:nth-child(2) {
  width: 20%;
}

#problems-table th:nth-child(3) {
  width: 40%;
}

#problems-table th:nth-child(4) {
  width: 7%;
}

#problems-table th:nth-child(5) {
  width: 7%;
}

#problems-table th:nth-child(6) {
  width: 7%;
}

#problems-table th:nth-child(7) {
  width: 9%;
}
</style>

<template>
  <div class="ui bottom attached warning message" style="display: none" id="announcement"></div>
  <div class="ui toggle checkbox" style="margin-top: 20px">
    <input type="checkbox" id="use-median" />
    <label>显示中位数数据</label>
  </div>
  <div class="column" style="margin-top: 20px">
    <table class="ui left aligned table" id="problems-table">
      <thead>
        <tr>
          <th>Pid</th>
          <th id="contest-header">比赛 ▾</th>
          <th>题目名</th>
          <th id="difficulty-header">难度 ▴</th>
          <th id="quality-header">质量 ▴</th>
          <th>投票</th>
          <th>显示投票</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
  <VoteModal v-model:show="voteModal" v-model:pid="pid" @rating-change="updateProblemsData()" />
  <SuiModal v-model="showVotesModal">
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
        <tbody></tbody>
      </table>
    </div>
    <div class="actions">
      <div class="ui positive button" @click="showVotesModal = false">OK</div>
    </div>
  </SuiModal>
  <SuiModal v-model="detailsModal">
    <div class="header">详细信息</div>
    <div class="content">
      <ul class="ui list" id="details"></ul>
    </div>
    <div class="actions">
      <div class="ui positive button" @click="detailsModal = false">OK</div>
    </div>
  </SuiModal>
</template>
