<template>
  <svg width="800" :height="50 + 20 * (tasks.length - 1)">
    <g :transform="translate(150, 25)">
      <tasks-linear-graph-edges :edges="selectedEdges" />
      <g v-for="task in tasks" :key="task.id" :transform="translate(0, taskY(task.index))">
        <circle
          cx="0"
          cy="0"
          :r="10 * 2 / 3"
          fill="white"
          :stroke="stateColor(task.state)"
          stroke-width="2"
          @mouseover="selectTask(task.index)"
          @mouseout="unselectTask"
        />
        <text
          x="-13"
          y="5"
          text-anchor="end"
          font-family="monospace"
          font-size="12"
        >{{ task.name }}</text>
      </g>
      <g :transform="translate(150, 0)">
        <flow-runs :flow_runs="flow_runs" />
      </g>
    </g>
  </svg>
</template>

<script>
import StateColorMixin from "./StateColorMixin";
import TransformMixin from "./TransformMixin";
import TasksLinearGraphEdges from "./TasksLinearGraphEdges";
import FlowRuns from "./FlowRuns";

export default {
  props: ["tasks", "edges", "flow_runs"],
  components: { TasksLinearGraphEdges, FlowRuns },
  mixins: [StateColorMixin, TransformMixin],
  data() {
    return {
      selectedTask: null
    };
  },
  computed: {
    selectedEdges() {
      return this.selectedTask === null
        ? this.edges
        : this.selectEdges(this.selectedTask);
    }
  },
  methods: {
    taskY(index) {
      return index * 20;
    },
    selectTask(index) {
      this.selectedTask = this.tasks[index];
    },
    unselectTask() {
      this.selectedTask = null;
    },
    selectEdges(task) {
      /* recursively walk the graph from provided task
         to all incoming edges of upstream tasks */
      return new Set([
        ...task.edges_in,
        ...task.edges_in
          .map(e => e.upstream_task)
          .reduce((a, t) => [...a, ...this.selectEdges(t)], [])
      ]);
    }
  }
};
</script>
