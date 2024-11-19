<script setup>
import $ from 'jquery'
const ojName = window.ojName
const code = window.code
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
    <div class="ui attached message">
      <div class="header">
        验证您的帐户。验证码：<b>"{{ code }}"</b>.
      </div>
      <p>
        请在您在 {{ ojName }} 中的账户 description 前面添加 "{{
          code
        }}"，我们将对此进行验证，以确保它是您的唯一账户。
      </p>
    </div>
    <form class="ui form attached fluid segment" method="post">
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
  </main>
</template>
