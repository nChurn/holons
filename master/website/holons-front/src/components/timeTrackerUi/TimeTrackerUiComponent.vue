<template src="./templates/timetracker-ui.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import  TimeTrackerJournalComponent from './TimeTrackerJournalComponent'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'TimeTrackerUiComponent',

  components: {
    'journal': TimeTrackerJournalComponent
  },

  props: {},

  data() {
    return {
      workPeriodEntries: [],
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
    this.getWorkPeriodEntries()
  },

  methods: {
    getWorkPeriodEntries: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl + 'timer/work-periods').then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.workPeriodEntries = response.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Timer api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  }
}
</script>

<style lang="css">
</style>
