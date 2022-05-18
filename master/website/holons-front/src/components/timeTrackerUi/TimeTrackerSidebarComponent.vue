<template src="./templates/timetracker-sidebar.html" lang="html"></template>

<script>
import Vue from 'vue'
import bus from '../utils/bus'

export default {
  name: 'TimeTrackerSidebarComponent',

  components: {},

  props: {
  },

  data() {
    return {
      showModal: false,
      timerTicking: false,
      disabled: false,
      timerStatus: 0,
      timeSpentUpdated: '00:00'
    }
  },

  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/'
      return url
    },
    csrfToken: function () { return window.csrftoken },
    userId: function () {
      return window.user_id
    },
    timerIsActive: function () {
      return window.timer_active
    },
    timeSpentToday: function () {
      return window.user_timer
    },
  },

  mounted() {
    window.bus.$on("switch-timer-indicator-off", () => this.switchTimerIndicator())
    if(this.timerIsActive === false) {
        this.timerTicking = false
    } else {
        this.timerTicking = true
    }
    this.timeSpentUpdated = this.timeSpentToday
    
    this.timerStatus = setInterval(this.checkTimerStatus, 1000)
  },

  methods: {
    delayStartTimer () {
      this.disabled = true
      this.timeout = setTimeout(() => {
        this.disabled = false
      }, 5000)
      this.startTimer()
    },
    startTimer () {
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      var data = { 'user_id': this.userId }
      this.$http.post(this.apiUrl + 'timer/start', data).then(response => {
        this.timerTicking = true
        // this.timerTicking = false
        this.$forceUpdate()
        this.$nextTick(async () => {
          console.log(response.data.data)
        })
      }).catch(error => {
          console.log('Timer api is unavailable at the moment')
          console.log(error)
      });
    },
    switchTimerIndicator () {
      this.timerTicking = !this.timerTicking
    }, 
    showTimerModal () {
      window.bus.$emit("show-timer-modal")
    }, 
    beforeDestroy () {
     clearTimeout(this.timeout)
    },
    checkTimerStatus () {
      var data = { 'user_id': this.userId }
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      this.$http.post(this.apiUrl + 'timer/current-status/', data).then(response => {
          this.timeSpentUpdated = response.data.time_spent_current_task
          window.bus.$emit("update-timer-value",
            response.data.time_spent_current_task,
            response.data.time_spent_today_total
          )
      })
    },
  }
}
</script>

<style lang="css" scoped>
    #ttracker-btn {
        cursor: pointer;
    }
    #ttracker-btn.active .ttracker-status {
        background-color: #FFCF4A !important;
    }
    #ttracker-btn .ttracker-status-text::before {
        font-size: 8px !important;
        width: 100% !important;
        color: rgba(255, 255, 255, 0.55) !important;
        text-align: center;
        letter-spacing: 1px;
        text-transform: lowercase;
    }
    #ttracker-btn .ttracker-status-text {
      display: block;
    }
    #ttracker-btn.active .ttracker-status {
      background-color: #FFCF4A !important;
    }
    #ttracker .ttracker-status-text::before {
      display: block;
    }
    #ttracker-btn.active .ttracker-status-text::before {
      content: "on";
    }
</style>
