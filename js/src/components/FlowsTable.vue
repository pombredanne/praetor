<template>
  <table class="table">
    <thead>
      <th>Flow Name</th>
      <th>Schedule</th>
      <th>Last Run</th>
      <th>State</th>
      <th>Recent Runs</th>
      <th>Recent Tasks</th>
      <th></th>
    </thead>
    <tbody>
      <flows-table-row
        v-for="flow in flows"
        :key="flow.id"
        :id="flow.id"
        :name="flow.name"
        :schedule="flow.schedule"
        :recent_flow_runs="flow.recent_flow_runs"
        :is_online="flow.is_online"
        :flow_runs_states="flow.flow_runs_states"
        :tasks_states="flow.tasks_states"
        @deleteFlow="deleteFlow"
      />
    </tbody>
  </table>
</template>

<script>
import FlowsTableRow from "./FlowsTableRow";

export default {
  name: "flows-table",
  components: { FlowsTableRow },
  props: ["flows"],
  methods: {
    deleteFlow(id) {
      this.$emit("deleteFlow", id);
    }
  }
};
</script>

<style scoped>
</style>
