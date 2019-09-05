<template>
  <div>{{ message }}</div>
</template>


<script>
export default {
  props: ["message"]
};
</script>

<style scoped>
div {
  width: 100%;
  height: 100%;
  border: none;
  left: 0;
  top: 0;
  position: fixed;
  display: table-cell;
  color: black;
  background: white;
  opacity: 0.8;
  text-align: center;
  padding-top: 10%;
}
</style>
