<template src="./templates/equity.html" />

<script>

import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'EquityComponent',

  components: {},

  props: {},

  data() {
    return {
      loader: null,
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/moneta'
      return url
    },
    me: function () {
      return window.handle
    },
  },
  mounted() {
  },
  methods: {
  }
}
</script>

<style scoped>
</style>


