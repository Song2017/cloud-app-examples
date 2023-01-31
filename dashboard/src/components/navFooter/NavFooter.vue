<template>
  <div>footer</div>
</template>

<script>
// js 内容

import { defineComponent } from "vue";
// es6
export default defineComponent({
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
<!-- CSS -->
<style lang="sass" scoped></style>
