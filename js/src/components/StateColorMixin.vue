<script>
export default {
  methods: {
    stateColor(state) {
      const mapping = {
        Running: "#b2df8a",
        Success: "#33a02c",
        Retrying: "#ff7f00",
        Failed: "#e31a1c",
        Canceled: "#fb9a99",
        Mapped: "#1f78b4"
      };
      return mapping[state] || "lightgray";
    }
  }
};
</script>
