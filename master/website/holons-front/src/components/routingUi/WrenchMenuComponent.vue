<template src="./templates/wrench-menu.html"></template>

<script>
export default {
  name: 'WrenchMenuComponent',
  props: ['item', 'showMenu'],
  mounted() {
  },
  methods: {
    menuToggle() {
      this.showMenu = !this.showMenu
      this.$parent.activeMenu = this.item
    }
  },
}
</script>
<style scoped>
  .menu {
    display: block;
  }
</style>
