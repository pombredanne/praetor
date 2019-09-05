<script>
const fn = (name, ...args) => {
  return `${name}(${args.join(", ")})`;
};

export default {
  methods: {
    transform(...args) {
      return args.join(" ");
    },
    translate(...args) {
      return fn("translate", ...args);
    },
    rotate(...args) {
      return fn("rotate", ...args);
    }
  }
};
</script>
