<script setup>
import config from '../package.json'
import { RouterLink, RouterView } from 'vue-router'
import { Menu, MenuItem, SuiContainer } from 'vue-fomantic-ui'

const title = window.title
const isAdmin = window.isAdmin
const loggedIn = window.loggedIn
const frontendVersion = config.version
const backendVersion = window.backendVersion
if (frontendVersion !== backendVersion) {
  console.error('前端版本与后端版本不匹配！')
}
</script>

<template>
  <Menu>
    <MenuItem header>{{ title }}</MenuItem>
    <RouterLink to="/">
      <MenuItem>题目</MenuItem>
    </RouterLink>
    <RouterLink to="/legal/">
      <MenuItem>条款</MenuItem>
    </RouterLink>
    <RouterLink to="/admin/" v-if="isAdmin">
      <MenuItem>管理</MenuItem>
    </RouterLink>
    <template #right>
      <RouterLink to="/login/" v-if="!loggedIn">
        <MenuItem>登录/注册</MenuItem>
      </RouterLink>
      <RouterLink to="/update_password/" v-if="loggedIn">
        <MenuItem>更新密码</MenuItem>
      </RouterLink>
      <MenuItem href="/logout/" v-if="loggedIn">登出</MenuItem>
    </template>
  </Menu>
  <SuiContainer>
    <RouterView />
  </SuiContainer>
  <div class="ui vertical footer">
    <div class="ui center aligned container">
      <div class="ui divider"></div>
      <div class="ui horizontal small divided link list" style="margin-top: 0">
        <a class="item" href="https://github.com/ZnPdCo/rating-system"> 由 Rating System 驱动 </a>
        <a class="item"> v{{ frontendVersion }} </a>
      </div>
    </div>
  </div>
</template>
