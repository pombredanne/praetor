import VueRouter from "vue-router";
import FlowsView from "./views/FlowsView";
import FlowView from "./views/FlowView";

const routes = [
  { path: "/", component: FlowsView, name: "index" },
  {
    path: "/flow/:id",
    name: "flowView",
    component: FlowView,
    props: true
  }
];

export default new VueRouter({ routes, mode: "hash" });
