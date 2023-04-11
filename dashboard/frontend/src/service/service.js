import axios from "axios";

// 创建axios实例
const service = axios.create({
  baseURL: "http://0.0.0.0:9010/api", // api的base_url
  timeout: 5000, // 请求超时时间
});

// request拦截器
service.interceptors.request.use(
  (config) => {
    // Do something before request is sent
    config.headers["X-Token"] = "getToken"; // 让每个请求携带token--['X-Token']为自定义key 请根据实际情况自行修改
    return config;
  },
  (error) => {
    // Do something with request error
    console.log(error); // for debug
    Promise.reject(error);
  }
);

// respone拦截器
service.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log("err" + error); // for debug
    return Promise.reject(error);
  }
);

// export const api = {
//   async runRedis() {
//     return axios.post(`/run_shell`, {
//       img_url: "img_url",
//     });
//   },
// }
service.runRedis = () => {
  return axios.post(`/run_shell`, {
      img_url: "img_url",
    });
  }
export default service;
