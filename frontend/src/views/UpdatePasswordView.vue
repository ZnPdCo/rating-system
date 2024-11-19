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
        <label>Old Password</label>
        <input placeholder="Old Password" type="password" name="old_password" />
      </div>
      <div class="field">
        <label>New Password</label>
        <input placeholder="New Password" type="password" name="new_password" />
      </div>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
  </main>
</template>
