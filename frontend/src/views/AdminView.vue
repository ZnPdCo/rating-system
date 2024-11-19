<script setup>
import $ from 'jquery'
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
        row.append($('<td>').text(user['admin']))
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
        .text('Delete')
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
        .text('Keep')
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
    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Permission settings</div>
    </div>
    <form class="ui form attached fluid segment" method="post" action="/admin/edit_permissions/">
      <div class="field">
        <label>Username</label>
        <input placeholder="Username" type="text" name="username" />
      </div>
      <div class="field">
        <label>Admin(1 for admin, 0 for normal user)</label>
        <input placeholder="Admin" type="number" name="admin" value="1" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
    <table class="ui left aligned table" id="user-table">
      <thead>
        <th>Username</th>
        <th>Admin</th>
      </thead>
      <tbody></tbody>
    </table>
    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Update Password</div>
    </div>
    <form
      class="ui form attached fluid segment"
      method="post"
      action="/admin/update_user_password/"
    >
      <div class="field">
        <label>Username</label>
        <input placeholder="Username" type="text" name="username" />
      </div>
      <div class="field">
        <label>Password</label>
        <input placeholder="Password" type="password" name="password" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Add Problem</div>
    </div>
    <form class="ui form attached fluid segment" method="post" action="/admin/add_problem/">
      <div class="field">
        <label>Contest</label>
        <input placeholder="Contest" type="text" name="contest" />
      </div>
      <div class="field">
        <label>Name</label>
        <input placeholder="Name" type="text" name="name" />
      </div>
      <div class="field">
        <label>Extra Info(JSON)</label>
        <input
          placeholder="Extra Info"
          type="text"
          name="info"
          value='{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}'
        />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
    <div class="ui bottom attached warning message">
      Extra Info Must have a links key with the problem link. For example:
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A"}
</pre
      >
      <br />
      Extra Info should have a pid key refer to the pid on oj if you want auto update status. For
      example:
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}
</pre
      >
    </div>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Update Problem</div>
    </div>
    <form class="ui form attached fluid segment" method="post" action="/admin/update_problem/">
      <div class="field">
        <label>Pid</label>
        <input placeholder="Pid" type="number" name="pid" />
      </div>
      <div class="field">
        <label>Contest</label>
        <input placeholder="Contest" type="text" name="contest" />
      </div>
      <div class="field">
        <label>Name</label>
        <input placeholder="Name" type="text" name="name" />
      </div>
      <div class="field">
        <label>Extra Info(JSON)</label>
        <input
          placeholder="Extra Info"
          type="text"
          name="info"
          value='{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}'
        />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
    <div class="ui bottom attached warning message">
      Extra Info Must have a links key with the problem link. For example:
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A"}
</pre
      >
      <br />
      Extra Info should have a pid key refer to the pid on oj if you want auto update status. For
      example:
      <pre>
{"links": "https://codeforces.com/contest/2024/problem/A", "pid": "2024A"}
</pre
      >
    </div>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Delete Problem</div>
    </div>
    <form class="ui form attached fluid segment" method="post" action="/admin/delete_problem/">
      <div class="field">
        <label>Pid</label>
        <input placeholder="Pid" type="number" name="pid" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
    <div class="ui bottom attached error message">
      Be careful when deleting problems, it will delete all the ratings to that problem.
    </div>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Rating Reports</div>
    </div>
    <table class="ui left aligned table" id="report-table">
      <thead>
        <th>Difficulty</th>
        <th>Quality</th>
        <th>Comment</th>
        <th>Delete</th>
        <th>Keep</th>
      </thead>
      <tbody></tbody>
    </table>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Auto Update Problem</div>
    </div>
    <form
      class="ui form attached fluid segment"
      method="post"
      action="/admin/auto_update_problems/"
    >
      <div class="field">
        <label></label>
        <input placeholder="" type="text" name="params" value="{}" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>

    <div class="ui attached message" style="margin-top: 20px">
      <div class="header">Announcement</div>
    </div>
    <form class="ui form attached fluid segment" method="post" action="/admin/update_announcement/">
      <div class="field">
        <label>Announcement</label>
        <input placeholder="Announcement" type="text" name="announcement" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
  </main>
</template>
