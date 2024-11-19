<script setup>
import $ from 'jquery'
$(document).ready(function () {
  var urlParams = new URLSearchParams(window.location.search)
  if (urlParams.has('error')) {
    $('#message').show()
    $('#message').text(urlParams.get('error'))
    $('#message').addClass('error')
  }
})
</script>

<template>
  <main>
    <div class="ui attached message" style="display: none" id="message"></div>
    <form class="ui form attached fluid segment" method="post">
      <div class="field">
        <label>旧密码</label>
        <input placeholder="旧密码" type="password" name="old_password" />
      </div>
      <div class="field">
        <label>新密码</label>
        <input placeholder="新密码" type="password" name="new_password" />
      </div>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
  </main>
</template>
