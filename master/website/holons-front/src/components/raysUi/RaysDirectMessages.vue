<template src="./templates/rays-direct-messages.html"/>

<script>

import Vue from 'vue';
import ThreadControls from './ThreadControls'
Vue.component('thread-controls', ThreadControls)

export default {
  name: 'RaysDirectMessages',
  props: [
    'ray',
  ],
  data() {
    return {
      showOpen: true,
      showArchived: false,
      showDeleted: false,
      showSnoozed: false,
      addMessageModal: false,
    }
  },
  mounted() {
    console.log('Rays messages UI')
  },
  methods: {
    refreshRays: function () {
      this.$parent.refreshRays()
    },
    addCustomMessage: function () {
      this.$parent.addMessageModal = true
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .thread-previews__item.active {
    background: #fff;
  }
  .message-wrap {
    cursor: pointer;
  }
  .modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.3);
    z-index: 9999;
  }
  .settings {
    background: #fff;
    padding: 20px;
    top: 12%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
  .thread-previews__item {
    height: auto !important;
  }
</style>
