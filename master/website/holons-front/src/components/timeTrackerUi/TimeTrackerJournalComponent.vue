<template src="./templates/timetracker-journal.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'TimeTrackerJournalComponent',

  components: {},

  props: {
    'work-periods': {
      type: Array(),
      default: []
    }
  },

  data() {
    return {
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/'
      return url
    },
  },

  mounted() {
  },

  methods: {
  }
}
</script>

<style lang="css">
<
