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
      <tasks-linear-graph :tasks="flow.tasks" :edges="flow.edges" :flow_runs="flow.flow_runs" />
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
      flow: this.defaultFlow(),
      isLoaded: false
    };
  },
  methods: {
    defaultFlow() {
      return {
        name: "",
        tasks: [],
        edges: [],
        flow_runs: []
      };
    },
    refresh() {
      api
        .get(`/flows/${this.id}/`)
        .then(res => {
          const flow = this.linkFlow(res.data);
          flow.tasks = this.sortTasks(flow.tasks);
          this.flow = flow;
        })
        .catch(e => {
          this.disconnected();
          console.error(e);
        })
        .finally(() => {
          this.isLoaded = true;
        });
    },
    getEdgesIn(id, edges) {
      return edges.filter(e => e.downstream_task_id == id);
    },
    getEdgesOut(id, edges) {
      return edges.filter(e => e.upstream_task_id == id);
    },
    sortTasks(tasks) {
      /* traverses task in the order of fake sequential execution
          and sets an appropriate index for each task (mutating)
          ugly and hacky, some elegant map-reduce functional magic needed */
      const ids = [];
      var res = [];
      const dependenciesMet = task => {
        return task.edges_in
          .map(e => ids.indexOf(e.upstream_task.id) > -1)
          .reduce((acc, x) => acc && x, true);
      };
      // tasks with less out-connections come first
      const terminalFirst = (a, b) =>
        a.edges_out.length - b.edges_out.length || a.name > b.name ? 1 : -1;
      const walk = task => {
        if (dependenciesMet(task) && ids.indexOf(task.id) === -1) {
          ids.push(task.id);
          res.push(task);
          task.edges_out
            .map(e => e.downstream_task)
            .sort(terminalFirst)
            .forEach(t => walk(t));
        }
      };
      const rootTasks = tasks.filter(t => t.edges_in.length === 0);
      rootTasks.sort(terminalFirst).forEach(walk);
      res = res.map((t, i) => {
        t.index = i;
        return t;
      });
      return res;
    },
    linkFlow(flow) {
      // link tasks and edges together
      flow.tasks = flow.tasks.map(t => {
        return Object.assign(t, {
          edges_in: this.getEdgesIn(t.id, flow.edges),
          edges_out: this.getEdgesOut(t.id, flow.edges)
        });
      });
      flow.edges = flow.edges.map(e => {
        return Object.assign(e, {
          upstream_task: this.getById(flow.tasks, e.upstream_task_id),
          downstream_task: this.getById(flow.tasks, e.downstream_task_id)
        });
      });
      flow.flow_runs = flow.flow_runs.map(fr => {
        return Object.assign(fr, {
          task_runs: fr.task_runs.map(tr => {
            return Object.assign(tr, {
              task: this.getById(flow.tasks, tr.task_id)
            });
          })
        });
      });
      return flow;
    },
    getById(objs, id) {
      return objs.filter(o => o.id === id)[0];
    }
  },
  beforeRouteEnter(from, to, next) {
    next(self => {
      self.refresh();
      self.refreshInterval = setInterval(() => {
        self.refresh();
      }, 10000);
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
