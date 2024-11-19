<script setup>
import { Message } from 'vue-fomantic-ui'
const urlParams = new URLSearchParams(window.location.search)
</script>

<template>
  <main>
    <Message error v-if="urlParams.has('error')" :content="urlParams.get('error')" />
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
