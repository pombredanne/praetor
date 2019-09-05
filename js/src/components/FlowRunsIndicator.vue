<template>
  <svg height="27" :width="12 * 10">
    <!-- TODO: figure out sizing and positioning -->
    <rect
      v-for="(run, index) in runs"
      :key="run.id"
      y="1"
      :x="1 + index * 12"
      width="10"
      height="25"
      :fill="stateColor(run.state)"
      stroke="black"
    >
      <title>
        Flow Run: {{ run.key }}
        ID: {{ run.id }}
        State: {{ run.state }}
      </title>
    </rect>
  </svg>
</template>

<script>
import StateColorMixin from "./StateColorMixin";

export default {
  name: "flow-runs-indicator",
  props: ["runs"],
  mixins: [StateColorMixin]
};
</script>

<style scoped>
rect {
  shape-rendering: crispEdges;
  cursor: pointer;
}
rect:hover {
  stroke-width: 2px;
}
</style>
