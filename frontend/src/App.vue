<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { Menu, MenuItem, SuiContainer } from 'vue-fomantic-ui'
</script>

<template>
  <Menu>
    <MenuItem header>%% title %%</MenuItem>
    <RouterLink to="/">
      <MenuItem>Problems</MenuItem>
    </RouterLink>
    <RouterLink to="/legal">
      <MenuItem>Legal</MenuItem>
    </RouterLink>
    {% if is_admin == True %}
    <RouterLink to="/admin">
      <MenuItem>Admin</MenuItem>
    </RouterLink>
    {% endif %}
    <template #right>
      {% if logged_in == False %}
      <RouterLink to="/login">
        <MenuItem>Login</MenuItem>
      </RouterLink>
      {% endif %} {% if logged_in == True %}
      <RouterLink to="/update_password">
        <MenuItem>Update Password</MenuItem>
      </RouterLink>
      <RouterLink to="/logout">
        <MenuItem>Logout</MenuItem>
      </RouterLink>
      {% endif %}
    </template>
  </Menu>
  <SuiContainer>
    <RouterView />
  </SuiContainer>
</template>
