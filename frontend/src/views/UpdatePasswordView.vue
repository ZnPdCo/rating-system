<script setup>
import { Message, SuiForm, SuiFormField, SuiButton } from 'vue-fomantic-ui'
const urlParams = new URLSearchParams(window.location.search)
</script>

<template>
  <main>
    <Message error v-if="urlParams.has('error')" :content="urlParams.get('error')" />
    <SuiForm method="post">
      <SuiFormField>
        <label>旧密码</label>
        <input placeholder="旧密码" type="password" name="old_password" />
      </SuiFormField>
      <SuiFormField>
        <label>新密码</label>
        <input placeholder="新密码" type="password" name="new_password" />
      </SuiFormField>
      <SuiButton type="submit" primary>提交</SuiButton>
    </SuiForm>
  </main>
</template>
