<template>
  <span :class="cls">{{ is_online ? 'online' : 'offline' }}</span>
</template>

<script>
export default {
  props: ["is_online"],
  computed: {
    cls() {
      return `badge badge-${this.is_online ? "success" : "secondary"}`;
    }
  }
};
</script>
