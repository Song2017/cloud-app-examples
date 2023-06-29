<template>
  <div>
    <h2>{{ page_name }}</h2>
    <p>Avaialble Connectors</p>

    <nav>
      <RouterLink to="/redis">Redis Connector</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs } from "vue";
// import NavHeader from "@/components/navHeader/NavHeader";
// import NavMain from "@/components/navMain/NavMain";
// import NavFooter from "@/components/navFooter/NavFooter";

export default defineComponent({
  name: "ToolView",
  components: {
    // NavHeader: NavHeader,
    // NavMain,
    // NavFooter,
  },
  setup() {
    let data = reactive({
      page_name: "ToolSet",
      obj: { name: "name", age: 12 },
    });

    let increaseNum = () => {
      num.value += 1;
    };

    return {
      ...toRefs(data),
      increaseNum,
    };
  },
});
</script>
