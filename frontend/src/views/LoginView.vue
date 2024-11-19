<script setup>
import { Message, SuiHeader, SuiForm, SuiSegment, SuiFormField, SuiButton } from 'vue-fomantic-ui'
const title = window.title
const ojName = window.ojName
const urlParams = new URLSearchParams(window.location.search)
</script>

<template>
  <main>
    <Message error v-if="urlParams.has('error')" :content="urlParams.get('error')" />
    <Message success v-if="urlParams.has('success')" :content="urlParams.get('success')" />
    <Message>
      <SuiHeader>欢迎来到 {{ title }}</SuiHeader>
      <p>填写表单以登录</p>
    </Message>
    <SuiSegment>
      <SuiForm method="post">
        <SuiFormField>
          <label>用户名</label>
          <input placeholder="用户名" type="text" name="username" />
        </SuiFormField>
        <SuiFormField>
          <label>密码</label>
          <input placeholder="密码" type="password" name="password" />
        </SuiFormField>
        <p>按下按钮表示您同意所有条款。</p>
        <SuiButton type="submit" primary>登录</SuiButton>
      </SuiForm>
    </SuiSegment>
    <Message warning>
      <b
        >请将用户名设为您在
        {{ ojName }} 中的用户名，我们将对您的账户进行校验以确保这是您的唯一账户。</b
      >
      <br />
      如果您尚未注册帐户，我们将自动为您创建一个。
    </Message>
  </main>
</template>
