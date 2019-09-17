<template>
  <g>
    <g v-for="(flow_run, i) in flow_runs" :key="flow_run.id" :transform="translate(i * 17, 0)">
      <task-runs :task_runs="flow_run.task_runs" />
    </g>
  </g>
</template>

<script>
import TransformMixin from "./TransformMixin";
import TaskRuns from "./TaskRuns";

export default {
  props: ["flow_runs"],
  mixins: [TransformMixin],
  components: { TaskRuns }
};
</script>
