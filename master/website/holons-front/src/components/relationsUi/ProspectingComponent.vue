<template src="./templates/prospecting.html" />

<script>

import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'ProspectingComponent',

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
          url += '/api/relations/prospecting'
      return url
    }
  },
  mounted() {
    console.log('Prospecting main')
  },
  methods: {
  }
}
</script>

<style scoped>
</style>
