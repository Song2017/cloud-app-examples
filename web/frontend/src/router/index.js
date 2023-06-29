import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ToolView from "../views/ToolView";

// 路由path必须以/开头, name不能重复
const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/",
    name: "index",
    component: ToolView,
  },
  {
    path: "/tool",
    name: "tool",
    component: ToolView,
  },
  {
    path: "/redis",
    name: "redis",
    component: ()=> import('../views/DockerRedisView'),
  },
];

const router = createRouter({
  history: createWebHistory("ui"), //"process.env.BASE_URL"
  routes,
});

export default router;
