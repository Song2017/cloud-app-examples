<script setup>
import { useStore } from "vuex";
import {useRouter}from 'vue-router'
let store = useStore();
let router = useRouter()
let back = ()=>{
  // router.go(-1)
  router.back()
}
</script>

<template>
  <div class="about">
    <p @click="back">回退</p>
    <h1>This is an about page</h1>
    <p>Store state_name: {{ store.state.state_name }}</p>

  </div>
</template>
