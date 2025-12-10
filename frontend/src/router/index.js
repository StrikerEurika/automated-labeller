import { createRouter, createWebHistory } from "vue-router";
import AnnotateView from "@/views/AnnotateView.vue";

const routes = [
  {
    path: "/",
    name: "Annotate",
    component: AnnotateView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
