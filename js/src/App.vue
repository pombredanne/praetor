<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-primary" style="margin-bottom: 20pt">
      <a class="navbar-brand" href="#">Praetor</a>
      <div class="collapse navbar-collapse">
        <div class="nav navbar-nav mr-auto">
          <router-link class="nav-item nav-link active" :to="{name: 'index'}">Flows</router-link>
          <a v-if="dask !== null" class="nav-item nav-link" :href="dask" target="_blank">Dask</a>
          <a class="nav-item nav-link" href="#">
            Notifications
            <span class="badge badge-light">0</span>
          </a>
        </div>
      </div>
    </nav>
    <div class="container">
      <router-view @connected="connected" @disconnected="disconnected"></router-view>
      <app-overlay v-if="!connection" message="No connection to server" />
    </div>
  </div>
</template>

<script>
import AppOverlay from "./components/AppOverlay";
import router from "./router";
import api from "./api";

export default {
  router,
  components: { AppOverlay },
  data() {
    return {
      connection: true,
      dask: null
    };
  },
  methods: {
    connected() {
      this.connection = true;
    },
    disconnected() {
      this.connection = false;
    },
    getDask() {
      api
        .get("dask/")
        .then(res => (this.dask = res.data))
        .catch(e => (this.dask = null));
    }
  },
  mounted() {
    this.getDask();
  }
};
</script>

<style scoped>
</style>
