<script setup>
import $ from 'jquery'
const title = window.title
const ojName = window.ojName
$(document).ready(function () {
  var urlParams = new URLSearchParams(window.location.search)
  if (urlParams.has('error')) {
    $('#message').show()
    $('#message').text(urlParams.get('error'))
    $('#message').addClass('error')
  } else if (urlParams.has('success')) {
    $('#message').show()
    $('#message').text(urlParams.get('success'))
    $('#message').addClass('success')
  }
})
</script>

<template>
  <main>
    <div class="ui attached message" style="display: none" id="message"></div>
    <div class="ui attached message">
      <div class="header">欢迎来到 {{ title }}</div>
      <p>填写表单以登录</p>
    </div>
    <form class="ui form attached fluid segment" method="post">
      <div class="field">
        <label>用户名</label>
        <input placeholder="用户名" type="text" name="username" />
      </div>
      <div class="field">
        <label>密码</label>
        <input placeholder="密码" type="password" name="password" />
      </div>
      <p>按下按钮表示您同意所有条款。</p>
      <button type="submit" class="ui blue submit button">提交</button>
    </form>
    <div class="ui bottom attached warning message">
      <b
        >请将用户名设为您在
        {{ ojName }} 中的用户名，我们将对您的账户进行校验以确保这是您的唯一账户。</b
      >
      <br />
      如果您尚未注册帐户，我们将自动为您创建一个。
    </div>
  </main>
</template>
