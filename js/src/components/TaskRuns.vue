<template>
  <g>
    <rect
      v-for="task_run in task_runs"
      :key="task_run.task.index"
      width="10"
      height="10"
      :y="taskY(task_run.task.index)"
      :fill="stateColor(task_run.state)"
      stroke="black"
      stroke-width="1"
    >
      <title>{{ title(task_run) }}</title>
    </rect>
  </g>
</template>

<script>
import StateColorMixin from "./StateColorMixin";

export default {
  props: ["task_runs"],
  mixins: [StateColorMixin],
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
  stroke-width: 2;
}
</style>
