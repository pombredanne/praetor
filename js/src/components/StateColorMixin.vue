<script>
export default {
  methods: {
    stateColor(state) {
      const mapping = {
        Running: "lime",
        Success: "green",
        Retrying: "orange",
        Failed: "red",
        Canceled: "blue"
      };
      return mapping[state] || "lightgray";
    }
  }
};
</script>
