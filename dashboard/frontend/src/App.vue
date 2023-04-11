<template>
  <nav>
    <router-link to="/tool">Tool</router-link> /
    <router-link to="/home">Home</router-link> /
    <router-link to="/about">About</router-link>
  </nav>
  <hr/>
  <router-view />
</template>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
</style>
