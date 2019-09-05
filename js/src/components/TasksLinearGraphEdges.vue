<template>
  <g>
    <path v-for="edge in edges" :key="edge.id" stroke="lightgray" fill="none" :d="edgePath(edge)" />
  </g>
</template>

<script>
import { path } from "d3-path";

export default {
  props: ["edges"],
  computed: {
    displayEdges() {
      return this.edges.filter(e => e.is_visible);
    }
  },
  methods: {
    edgePath(edge) {
      const fromIndex = edge.upstream_task.index;
      const toIndex = edge.downstream_task.index;
      const diff = toIndex - fromIndex - 1;
      const [fromX, fromY] = [0, this.taskY(fromIndex)];
      const [toX, toY] = [0, this.taskY(toIndex)];
      const p = path();
      p.moveTo(fromX, fromY);
      const cpxDiff = 12 * diff;
      p.bezierCurveTo(fromX + cpxDiff, fromY, toX + cpxDiff, toY, toX, toY);
      return p.toString();
    },
    taskY(index) {
      return index * 20;
    }
  }
};
</script>
