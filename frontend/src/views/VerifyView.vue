<script setup>
import { Message } from 'vue-fomantic-ui'
const ojName = window.ojName
const code = window.code
const urlParams = new URLSearchParams(window.location.search)
</script>

<template>
  <main>
    <Message error v-if="urlParams.has('error')" :content="urlParams.get('error')" />
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
