<template>
  <div class="card">
    <div class="card-header">
      <div v-if="!isLoaded" class="spinner-grow" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <h3 v-if="isLoaded" class="card-title">{{ flow.name }}</h3>
      <online-badge :is_online="flow.is_online" />
    </div>
    <div class="card-body">
      <tasks-linear-graph
        :tasks="sortedTasks"
        :edges="flow.edges"
        :flow_runs="flow.recent_flow_runs"
      />
    </div>
  </div>
</template>

<script>
// TODO: loading indicator
import api from "../api";
import DisconnectMixin from "../components/DisconnectMixin";
import TasksLinearGraph from "../components/TasksLinearGraph";
import OnlineBadge from "../components/OnlineBadge";

export default {
  props: ["id"],
  components: { TasksLinearGraph, OnlineBadge },
  mixins: [DisconnectMixin],
  data() {
    return {
      flow: {
        name: "test",
        tasks: [],
        edges: []
      },
      isLoaded: false
    };
  },
  computed: {
    sortedTasks() {
      /* traverses task in the order of fake sequential execution
         and sets an appropriate index for each task (mutating)
         ugly and hacky, some elegant map-reduce functional magic needed */
      const ids = [];
      var tasks = [];
      const dependenciesMet = task => {
        return task.edges_in
          .map(e => ids.indexOf(e.upstream_task.id) > -1)
          .reduce((acc, x) => acc && x, true);
      };
      // tasks with less out-connections come first
      const terminalFirst = (a, b) => a.edges_out.length - b.edges_out.length;
      const walk = task => {
        if (dependenciesMet(task) && ids.indexOf(task.id) === -1) {
          ids.push(task.id);
          tasks.push(task);
          task.edges_out
            .map(e => e.downstream_task)
            .sort(terminalFirst)
            .forEach(t => walk(t));
        }
      };
      const rootTasks = this.flow.tasks.filter(t => t.edges_in.length === 0);
      rootTasks.sort(terminalFirst).forEach(walk);
      tasks = tasks.map((t, i) => {
        t.index = i;
        return t;
      });
      return tasks;
    },
    taskByName() {
      return this.flow.tasks.reduce((o, t) => {
        o[t.name] = t;
        return o;
      }, {});
    }
  },
  methods: {
    defaultFlow() {
      return {
        name: "test",
        tasks: [],
        edges: [],
        flow_runs: []
      };
    },
    refresh() {
      this.isLoading = true;
      api
        .get(`/flows/${this.id}/`)
        .then(res => {
          this.flow = res.data;
          this.updateLinks();
          this.connected();
        })
        .catch(e => {
          this.disconnected();
          console.error(e);
        })
        .finally(() => {
          this.isLoaded = true;
        });
    },
    updateLinks() {
      // link tasks and edges together
      this.flow.tasks = this.flow.tasks.map(t => {
        t.edges_in = this.getEdgesIn(t.index);
        t.edges_out = this.getEdgesOut(t.index);
        return t;
      });
      this.flow.edges = this.flow.edges.map(e => {
        e.upstream_task = this.flow.tasks[e.upstream_task.index];
        e.downstream_task = this.flow.tasks[e.downstream_task.index];
        return e;
      });
      this.flow.recent_flow_runs = this.flow.recent_flow_runs.map(flow_run => {
        flow_run.task_runs = flow_run.task_runs.map(task_run => {
          task_run.task = this.taskByName[task_run.task.name];
          return task_run;
        });
        return flow_run;
      });
    },
    getEdgesIn(index) {
      return this.flow.edges.filter(e => e.downstream_task.index == index);
    },
    getEdgesOut(index) {
      return this.flow.edges.filter(e => e.upstream_task.index == index);
    }
  },
  beforeRouteEnter(from, to, next) {
    next(self => {
      self.refreshInterval = setInterval(() => {
        self.refresh();
      }, 1000);
    });
  },
  beforeRouteLeave(from, to, next) {
    this.flow = this.defaultFlow();
    clearInterval(this.refreshInterval);
    next();
  }
};
</script>

<style scoped>
h1,
h2,
h3 {
  display: inline;
}
</style>
