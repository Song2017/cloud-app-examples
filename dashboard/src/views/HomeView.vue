<template>
  <div>
    <nav-header></nav-header>
    <nav-main></nav-main>
    <nav-footer></nav-footer>

    <p>{{ arr.slice(0, 2) }}</p>
    <p>{{ data.data_obj }}, {{ data_obj }}</p>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from "vue";
import NavHeader from "@/components/navHeader/NavHeader";
import NavMain from "@/components/navMain/NavMain";
import NavFooter from "@/components/navFooter/NavFooter";

export default defineComponent({
  name: "HomeComponent",
  components: {
    NavHeader: NavHeader,
    NavMain,
    NavFooter,
  },
  setup() {
    let num = ref(1);
    let name = ref("home");
    let arr = ref([1, 2, 3]);
    let obj = ref({ name: "name", age: 12 });
    let data = reactive({
      data_obj: {
        name: "data_obj",
      },
    });
    let data2 = reactive({
      data_obj: {
        name: "data_obj",
      },
    });
    return { num, name, arr, data, ...toRefs(data2) };
  },
});
</script>
