<template>
  编写html内容
  <div></div>
</template>

<script>
// js 内容

import { defineComponent } from "vue";
// es6
export default defineComponent({
  name: "DefaultButton",
  //   接收父组件的属性
  props: {},
  //   定义子组件
  components: {},
  // 没有this
  setup(props, ctx) {
    console.log(props, ctx);
    return {};
  },
});
</script>

<style lang="sass" scoped>
<!-- CSS -->
</style>
