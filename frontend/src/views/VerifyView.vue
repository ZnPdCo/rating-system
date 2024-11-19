<script setup>
import { Message, SuiHeader, SuiForm, SuiButton } from 'vue-fomantic-ui'
const ojName = window.ojName
const code = window.code
const urlParams = new URLSearchParams(window.location.search)
</script>

<template>
  <main>
    <Message error v-if="urlParams.has('error')" :content="urlParams.get('error')" />
    <Message>
      <SuiHeader
        >验证您的帐户。验证码：<b>"{{ code }}"</b>.</SuiHeader
      >
      请在您在 {{ ojName }} 中的账户 description 前面添加 "{{
        code
      }}"，我们将对此进行验证，以确保它是您的唯一账户。
    </Message>
    <SuiForm method="post">
      <SuiButton type="submit" primary>验证</SuiButton>
    </SuiForm>
  </main>
</template>
