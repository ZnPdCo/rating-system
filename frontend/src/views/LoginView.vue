<script setup>
import $ from 'jquery'
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
      <div class="header">Welcome to %% title %%</div>
      <p>Fill out the form to login.</p>
    </div>
    <form class="ui form attached fluid segment" method="post">
      <div class="field">
        <label>Username</label>
        <input placeholder="Username" type="text" name="username" />
      </div>
      <div class="field">
        <label>Password</label>
        <input placeholder="Password" type="password" name="password" />
      </div>
      <p>Pressing the button indicates your agreement to all terms.</p>
      <button type="submit" class="ui blue submit button">Submit</button>
    </form>
    <div class="ui bottom attached warning message">
      <b>Please set your username to the one in %% oj_name %% , we will verify your identity.</b>
      <br />
      If you haven't registered an account yet, we will automatically create one for you.
    </div>
  </main>
</template>
