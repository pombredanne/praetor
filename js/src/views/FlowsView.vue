<template>
  <flows-table :flows="flows" @deleteFlow="deleteFlow" />
</template>

<script>
import api from "../api";
import FlowsTable from "../components/FlowsTable";
import DisconnectMixin from "../components/DisconnectMixin";

export default {
  data() {
    return {
      flows: []
    };
  },
  components: { FlowsTable },
  mixins: [DisconnectMixin],
  methods: {
    refresh() {
      // TODO: handle connecction errors
      api
        .get("/flows/")
        .then(res => {
          this.flows = res.data;
          this.connected();
        })
        .catch(e => {
          this.disconnected();
          console.log(e);
        });
    },
    deleteFlow(id) {
      api
        .delete(`/flows/${id}/`)
        .then(res => (this.flows = res.data))
        .catch(e => console.log(e));
    }
  },
  beforeRouteEnter(from, to, next) {
    next(self => {
      self.refresh();
      self.refreshInterval = setInterval(() => {
        self.refresh();
      }, 1000);
    });
  },
  beforeRouteLeave(from, to, next) {
    clearInterval(this.refreshInterval);
    next();
  }
};
</script>
