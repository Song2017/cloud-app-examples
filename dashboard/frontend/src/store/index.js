import { createStore } from "vuex";

export default createStore({
  // 定义需要的状态, 每个组件都可以用
  state: {
    state_name: "state_name",
  },
  getters: {},
  // 同步修改state,都是方法
  // 第一个参数是state, 第二个是要修改的值
  mutations: {
    setStateName(state, payload) {
      state.state_name = payload;
    },
  },
  // 异步提交mutation
  // 第一个参数是store对象, 第二个是要修改的值
  actions: {
    asyncSetStateName(store, params) {
      setTimeout(() => {
        store.commit("setStateName", params);
      }, 2000);
    },
  },
  // 模块化
  modules: {},
});
