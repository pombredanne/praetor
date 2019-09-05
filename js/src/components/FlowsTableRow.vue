<template>
  <tr>
    <td>
      <router-link :to="link">{{ name }}</router-link>
      <online-badge :is_online="is_online" />
    </td>
    <td>
      <span class="badge badge-dark">{{ schedule }}</span>
    </td>
    <td>{{ last_run }}</td>
    <td>{{ state }}</td>
    <td>
      <flow-runs-indicator :runs="recent_flow_runs" />
    </td>
    <td>
      <states-indicator :states="tasks_states" />
    </td>
    <td>
      <button
        v-if="!isLoading && !is_online"
        type="button"
        class="close"
        aria-label="Close"
        @click="deleteFlow"
      >
        <span aria-hidden="true">&times;</span>
      </button>
      <div v-else-if="isLoading" class="spinner-grow" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </td>
  </tr>
</template>

<script>
import FlowRunsIndicator from "./FlowRunsIndicator";
import StatesIndicator from "./StatesIndicator";
import OnlineBadge from "./OnlineBadge";

export default {
  name: "flows-table-row",
  components: { FlowRunsIndicator, StatesIndicator, OnlineBadge },
  props: [
    "id",
    "name",
    "schedule",
    "recent_flow_runs",
    "is_online",
    "flow_runs_states",
    "tasks_states"
  ],
  data() {
    return {
      isLoading: false
    };
  },
  computed: {
    last_run() {
      if (this.recent_flow_runs.length === 0) return null;
      return this.recent_flow_runs.slice(-1)[0].key;
    },
    state() {
      if (this.recent_flow_runs.length === 0) return null;
      return this.recent_flow_runs.slice(-1)[0].state;
    },
    link() {
      return {
        name: "flowView",
        params: { id: this.id }
      };
    }
  },
  methods: {
    deleteFlow() {
      this.isLoading = true;
      this.$emit("deleteFlow", this.id);
    }
  }
};
</script>

<style scoped></style>
