<script setup>
import $ from 'jquery'
import { Message } from 'vue-fomantic-ui'
$(document).ready(function () {
  window.data = []
  $.ajax({
    url: '/backend/get_problems',
    type: 'GET',
    success: function (data) {
      window.data = data
    },
  })
  $('form[action="/admin/update_problem/"] input[name="pid"]').focusout(function () {
    window.data.forEach(function (problem) {
      if (
        problem['pid'].toString() ==
        $('form[action="/admin/update_problem/"] input[name="pid"]').val()
      ) {
        $('form[action="/admin/update_problem/"] input[name="contest"]').val(problem['contest'])
        $('form[action="/admin/update_problem/"] input[name="name"]').val(problem['name'])
        $('form[action="/admin/update_problem/"] input[name="info"]').val(
          JSON.stringify(problem['info']),
        )
      }
    })
  })
  $.ajax({
    url: '/admin/get_users/',
    type: 'POST',
    success: function (data) {
      var table = $('#user-table tbody')
      data.forEach(function (user) {
        var row = $('<tr>')
        row.append($('<td>').text(user['username']))
        row.append($('<td>').text(user['permission']))
        table.append(row)
      })
    },
  })
})
$.ajax({
  url: '/admin/get_reports/',
  type: 'POST',
  success: function (data) {
    var table = $('#report-table tbody')
    data.forEach(function (report) {
      var row = $('<tr>')
      row.append($('<td>').text(report['pid']))
      row.append($('<td>').text(report['username']))
      row.append($('<td>').text(report['difficulty']))
      row.append($('<td>').text(report['quality']))
      row.append($('<td>').text(report['comment']))
      addUpdateLinks(row, report['id'])
      table.append(row)
    })
  },
})
function addUpdateLinks(row, id) {
  row.append(
    $('<td>').append(
      $('<a>')
        .text('删除')
        .click(function () {
          $.post('/admin/update_report/', { id: id, delete: 1 }, function () {
            row.remove()
          })
        }),
    ),
  )
  row.append(
    $('<td>').append(
      $('<a>')
        .text('保留')
        .click(function () {
          $.post('/admin/update_report/', { id: id, delete: 0 }, function () {
            row.remove()
          })
        }),
    ),
  )
}
</script>

<template>
  <main>
    <Message attached header="权限设置" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="post" action="/admin/edit_permissions/">
      <div class="field">
        <label>用户名</label>
        <input placeholder="用户名" type="text" name="username" />
      </div>
      <div class="field">
        <label>管理员(1表示登录权限，2表示投票权限，4表示管理权限，或起来)</label>
        <input placeholder="管理员" type="number" name="permission" value="3" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
    <table class="ui left aligned table" id="user-table">
      <thead>
        <tr>
          <th>用户名</th>
          <th>权限</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <Message attached header="更新密码" style="margin-top: 20px" />
    <form
      class="ui form attached fluid segment"
      method="post"
      action="/admin/update_user_password/"
    >
      <div class="field">
        <label>用户名</label>
        <input placeholder="用户名" type="text" name="username" />
      </div>
      <div class="field">
        <label>密码</label>
        <input placeholder="密码" type="password" name="password" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>

    <Message attached header="添加题目" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="post" action="/admin/add_problem/">
      <div class="field">
        <label>比赛</label>
        <input placeholder="比赛" type="text" name="contest" />
      </div>
      <div class="field">
        <label>题目名</label>
        <input placeholder="题目名" type="text" name="name" />
      </div>
      <div class="field">
        <label>额外信息(JSON)</label>
        <input
          placeholder="额外信息"
          type="text"
          name="info"
          value='{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}'
        />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
    <Message warning attached="bottom">
      额外信息必须有一个带有问题链接的 <code>links</code> 键。例如：
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A"}
</pre
      >
      <br />
      如果你想自动更新通过状态，额外信息应该有一个 <code>pid</code> 键，表示 oj 上的 pid。例如：
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}
</pre
      >
    </Message>

    <Message attached header="更新题目" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="post" action="/admin/update_problem/">
      <div class="field">
        <label>Pid</label>
        <input placeholder="Pid" type="number" name="pid" />
      </div>
      <div class="field">
        <label>比赛</label>
        <input placeholder="比赛" type="text" name="contest" />
      </div>
      <div class="field">
        <label>题目名</label>
        <input placeholder="题目名" type="text" name="name" />
      </div>
      <div class="field">
        <label>额外信息(JSON)</label>
        <input
          placeholder="额外信息"
          type="text"
          name="info"
          value='{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}'
        />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
    <Message warning attached="bottom">
      额外信息必须有一个带有问题链接的 <code>links</code> 键。例如：
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A"}
</pre
      >
      <br />
      如果你想自动更新通过状态，额外信息应该有一个 <code>pid</code> 键，表示 oj 上的 pid。例如：
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}
</pre
      >
    </Message>

    <Message attached header="删除问题" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="post" action="/admin/delete_problem/">
      <div class="field">
        <label>Pid</label>
        <input placeholder="Pid" type="number" name="pid" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
    <Message warning attached="error"> 删除问题时要小心，它将删除该问题的所有评分。 </Message>

    <Message attached header="举报" style="margin-top: 20px" />
    <table class="ui left aligned table" id="report-table">
      <thead>
        <tr>
          <th>Pid</th>
          <th>用户名</th>
          <th>难度</th>
          <th>质量</th>
          <th>评论</th>
          <th>删除</th>
          <th>保留</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>

    <Message attached header="自动拉取题目" style="margin-top: 20px" />
    <form
      class="ui form attached fluid segment"
      method="post"
      action="/admin/auto_update_problems/"
    >
      <div class="field">
        <label>参数</label>
        <input placeholder="参数" type="text" name="params" value="{}" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>

    <Message attached header="设置公告" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="post" action="/admin/update_announcement/">
      <div class="field">
        <label>公告</label>
        <input placeholder="公告" type="text" name="announcement" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>

    <Message attached header="导出数据库" style="margin-top: 20px" />
    <form class="ui form attached fluid segment" method="get" action="/admin/export_database/">
      <button type="submit" class="ui blue submit button">导出</button>
    </form>
  </main>
</template>
