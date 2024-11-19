<script setup>
import $ from 'jquery'
import { useRouter } from 'vue-router'

const router = useRouter()

$.ajax({
  url: '/logout',
  type: 'GET',
  success: function () {
    router.push('/login')
  },
})
</script>

<template>
  <main></main>
</template>
