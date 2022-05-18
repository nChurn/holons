<template src="./templates/offers-main-wrench-menu.html" />

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: "OffersMainWrenchMenuComponent",

  props: ['item', 'showMenu'],
  data() {
    return {
      loader: null,
    }
  },
  methods: {
    menuToggle() {
      this.showMenu = !this.showMenu
      this.$parent.$parent.activeMenu = this.item
    },
  },
}
</script>

<style>
  .menu {
    display: block;
  }
</style>
