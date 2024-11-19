<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { Menu, MenuItem, SuiContainer } from 'vue-fomantic-ui'

const title = window.title
const isAdmin = window.isAdmin
const loggedIn = window.loggedIn
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
    <div class="ui center aligned container">
      <div class="ui horizontal small divided link list">
        <p class="item">
          基于
          <a href="https://github.com/ZnPdCo/rating-system">Rating System</a>
        </p>
      </div>
    </div>
  </SuiContainer>
</template>
