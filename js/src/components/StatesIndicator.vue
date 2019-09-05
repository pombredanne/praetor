<template>
  <svg width="160" height="28">
    <g v-for="(s, i) in _states" :key="i" :transform="translate(14 + i * 29, 14)">
      <circle
        :stroke="s.count > 0 ? stateColor(s.state) : 'lightgray'"
        :stroke-width="s.count > 0 ? 2 : 1"
        fill-opacity="0"
        r="12.5"
      />
      <text font-size="8" text-anchor="middle" y="3">{{ s.count > 0 ? s.count : null }}</text>
      <title>{{ s.state }}</title>
    </g>
  </svg>
</template>

<script>
import StateColorMixin from "./StateColorMixin";

export default {
  name: "states-indicator",
  props: ["states"],
  mixins: [StateColorMixin],
  computed: {
    _states() {
      const statesOrder = [
        "Running",
        "Success",
        "Retrying",
        "Failed",
        "Canceled"
      ];
      return statesOrder.map(s => {
        return { state: s, count: this.states[s] || 0 };
      });
    }
  },
  methods: {
    translate(x, y) {
      return `translate(${x}, ${y})`;
    }
  }
};
</script>

<style scoped>
g {
  cursor: pointer;
  opacity: 1;
}
</style>
