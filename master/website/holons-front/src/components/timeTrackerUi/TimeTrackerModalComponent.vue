<template src="./templates/timetracker-modal.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import bus from '../utils/bus'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'TimeTrackerModalComponent',

  components: {},

  props: {},

  data() {
    return {
      entitiesList: [
        'Add entities in moneta'
      ],
      commitmentsList: [
        'Create commitments via Relations/Offers',
      ],
      selectedEntity: null,
      selectedCommitment: null,
      timeEntryStatus: 'billed',
      isBillable: false,
      showModal: false,
      timeSpentTodayUpdated: '',
      timeSpentCurrentTaskUpdated: '',
    }
  },

  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/'
      return url
    },
    timeEntryTitle: function () {
      return window.time_entry_title
    },
    currentTaskTime: function () {
      return window.timer_current_time
    },
    timeSpentToday: function () {
      return window.user_timer
    },
  },

  mounted() {
    window.bus.$on("show-timer-modal", () => this.showTimerModal())
    window.bus.$on("update-timer-value",
      (tsCurrentTask, tsTodayTotal) => this.updateTimeSpentToday(tsCurrentTask, tsTodayTotal))
    this.getBusinessEntities()
    this.getCommitments()
  },

  methods: {
    showTimerModal () {
        console.log('show modal')
        document.getElementById('ttrackerModal').classList.add('active')
    },
    closeModal () {
        console.log('hide modal')
        document.getElementById('ttrackerModal').classList.remove('active')
    },
    getBusinessEntities () {
      // Yes, we don't give a flying fuck about DRY principle
      // @todo: import this thingie from moneta UI
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl + 'moneta/business-entities').then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.entitiesList = response.data.entities
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Business Entity api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    getCommitments () {
      // Yes, we don't give a flying fuck about DRY principle
      // @todo: import this thingie from relations UI
      // this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl + 'relations/commitments').then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.commitmentsList = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Commitments api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    logTime () {
      var data = {
        business_entity: this.selectedEntity,
        commitment: this.selectedCommitment,
        comment: this.timeEntryTitle,
        is_billable: this.isBillable,
      }
      this.$http.post(this.apiUrl + 'timer/stop', data).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          window.bus.$emit("switch-timer-indicator-off", response.data.data)
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Timer api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
      this.closeModal()
    },
    doNotLogTime () {
      this.$http.delete(this.apiUrl + 'timer/cancel').then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          window.bus.$emit("switch-timer-indicator-off", response.data.data)
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Timer api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
      this.closeModal()
    },
    updateTimeSpentToday (tsCurrentTask, tsTodayTotal) {
      this.timeSpentCurrentTaskUpdated = tsCurrentTask
      this.timeSpentTodayUpdated = tsTodayTotal
    },
  }
}
</script>

<style lang="css">
</style>
