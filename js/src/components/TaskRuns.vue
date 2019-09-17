<template>
  <g>
    <g
      v-for="task_run in task_runs"
      :key="task_run.task.id"
      :transform="translate(0, taskY(task_run.task.index))"
    >
      <rect width="15" height="15" :fill="stateColor(task_run.state)">
        <title>{{ title(task_run) }}</title>
      </rect>
      <text
        v-if="task_run.map_index + 1 > 0"
        font-size="11"
        x="7.5"
        y="11.5"
        text-anchor="middle"
        fill="white"
      >{{ task_run.map_index + 1 }}</text>
    </g>
  </g>
</template>

<script>
import StateColorMixin from "./StateColorMixin";
import TransformMixin from "./TransformMixin";

export default {
  props: ["task_runs"],
  mixins: [StateColorMixin, TransformMixin],
  methods: {
    taskY(index) {
      return index * 20 - 7.5;
    },
    title(task_run) {
      return `Task: ${task_run.task.name}\nKey: ${task_run.flow_run.key}\nState: ${task_run.state}`;
    }
  }
};
</script>

<style scoped>
rect {
  shape-rendering: crispEdges;
  cursor: pointer;
}

rect:hover {
  stroke: black;
  stroke-width: 2;
}

text {
  pointer-events: none;
}
</style>
