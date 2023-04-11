<template>
  <div>
    Start RedisInsight Service:
    <button @click="run_redis_service">Start</button>
    <br />
    <p>Host is: {{ host }}</p>
    <input v-model="host" placeholder="edit me" />
    <p>Port is: {{ port }}</p>
    <input v-model="port" placeholder="edit me" />
    <br />
    <button type="submit">Run</button>
  </div>
</template>

<script>
import { defineComponent, reactive, toRefs } from "vue";
import axios from "axios";
export default defineComponent({
  setup() {
    let data = reactive({
      host: "127.0.0.1",
      port: "6443",
    });

    let run_redis_service = () => {
      axios
        .post(`http://localhost:9010/api/run_shell`, { connector: "redis" })
        .then(function (res) {
          var rs = res.data;
          console.log(res);
          console.log(rs.data);
        })
        .catch(function (err) {
          console.log(err);
        });
      // return axios.post(`http://0.0.0.0:9010/api/test`, {
      //   img_url: "img_url",
      // });
    };

    return { ...toRefs(data), run_redis_service };
  },
});
</script>
