<script>
export default {
  methods: {
    disconnected() {
      this.$emit("disconnected");
    },
    connected() {
      this.$emit("connected");
    }
  }
};
</script>
