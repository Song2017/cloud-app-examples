<template>
  <div>
    hello VUE
    <nav-header></nav-header>
    <nav-main></nav-main>
    <nav-footer></nav-footer>

    <p>{{ arr.slice(0, 2) }}</p>
    <p>{{ data.data_obj }}, {{ data_obj }}</p>
    <p>Num: {{ num }}, num2 {{ num2 }}, computedNum {{ computedNum }}</p>
    <input v-model="num2" /> /
    <button @click="increaseNumVal(num)">addNumVal</button>

    <p>{{ store.state }}</p>
    <input v-model="store.state.state_name" />
  </div>
</template>

<script>
import { defineComponent, reactive, ref, toRefs, computed } from "vue";
import NavHeader from "@/components/navHeader/NavHeader";
import NavMain from "@/components/navMain/NavMain";
import NavFooter from "@/components/navFooter/NavFooter";

import { useStore } from "vuex";

export default defineComponent({
  name: "HomeComponent",
  components: {
    NavHeader: NavHeader,
    NavMain,
    NavFooter,
  },
  setup() {
    let num = ref(1);
    let num2 = ref(2);
    let computedNum = computed(() => {
      // 必须放回值, 但不应该修改
      return Number(num.value) + Number(num2.value);
    });
    let name = ref("home");
    let arr = ref([1, 2, 3]);
    let data = reactive({
      data_obj: {
        name: "data_obj",
      },
      obj: { name: "name", age: 12 },
    });
    let data2 = reactive({
      data_obj: {
        name: "data_obj",
      },
    });
    let increaseNum = () => {
      num.value += 1;
    };
    let increaseNumVal = (val) => {
      num.value += val;
    };

    let store = useStore();
    // let state = store.state
    return {
      num,
      num2,
      computedNum,
      name,
      arr,
      data,
      ...toRefs(data2),
      increaseNum,
      increaseNumVal,
      store,
    };
  },
});
</script>
