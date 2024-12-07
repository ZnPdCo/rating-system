<script setup>
import $ from 'jquery'
import axios from 'axios'
import { SuiModal, SuiButton } from 'vue-fomantic-ui'
import { ref, watch } from 'vue'
const show = defineModel('show')
const pid = defineModel('pid')

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

function addReportLink(row, id) {
  row.append(
    $('<td>')
      .html('<a>举报</a>')
      .click(function () {
        $.ajax({
          url: '/backend/report/',
          type: 'POST',
          data: {
            id: id,
          },
          success: function () {
            alert('举报成功！管理员将会进行审核。')
          },
        })
      }),
  )
}
watch(show, async (value) => {
  if (value != true) return
  let table = $('#vote-table tbody')
  table.empty()

  $.ajax({
    url: '/backend/get_votes/',
    type: 'POST',
    data: {
      pid: pid.value,
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
        <tbody></tbody>
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
