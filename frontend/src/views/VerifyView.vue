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
    <div class="ui attached message">
      <div class="header">Verify your account. CODE: <b>"%% code %%"</b>.</div>
      <p>
        Please add "%% code %%" at the beginning of the description of your account in %% oj_name %%
        (no prefix is required be added). We will verify this to ensure that it is your unique
        account.
      </p>
    </div>
    <form class="ui form attached fluid segment" method="post">
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
  </main>
</template>
