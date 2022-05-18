<template src="./templates/agenda.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import Workspaces from './WorkSpaces'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'Agenda',

  components: {
    Workspaces
  },
  
  props: {
  },

  data() {
    return {
      loader: null,
      apiUrl: 'https://boards.holons.me/api/v1/',
      userMe: null,
      userCards: {
        mine: [],
        assigned_to_me: [],
        watched_by_me: []
      },

      activeProject: [],
      workspacesAvailable: [],
      workspaceName: [],
      workspacesList: [],
      assignedToMeCount: 0,
      watchedByMeCount: 0,
    }
  },
  computed: {
    token: function () {
      let tokenStorage = window.localStorage
      if (tokenStorage.getItem('token')) {
        return tokenStorage.getItem('token').replace(/['"]+/g, '')
      } else {
        return undefined
      }
    },
    authHeaders: function () {
      return { headers: { Authorization: 'Bearer ' + this.token } }
    },
  },
  async mounted() {
    this.getUserAgenda()
    this.$http.defaults.headers.common['X-CSRFToken'] = window.csrftoken
  },
  methods: {
    async getUserAgenda () {
      this.userMe = await this.sendRequest('users/me')
      this.userCards['mine'] = await this.sendRequest('userstories?owner=' + this.userMe.id)
      this.userCards['watched_by_me'] = await this.sendRequest('userstories?watchers=' + this.userMe.id)
      this.userCards['assigned_to_me'] = await this.getAssignedOnMe('userstories')
      this.watchedByMeCount = this.userCards['watched_by_me'].length
      this.assignedToMeCount = this.userCards['assigned_to_me'].length
    },

    // Adapted from Workspaces component. Maybe eject it into a single file?
    async sendRequest(url) {
      delete this.$http.defaults.headers.common['X-CSRFToken'] // remove CSRF in order to access API by a separate API token
      let prop

      this.authHeaders.headers['x-disable-pagination'] = true

      await this.$http
        .get(this.apiUrl + url, this.authHeaders)
        .then((response) => {
          prop = response.data
        })
        .catch(error => this.handleError(error, url))
      this.$http.defaults.headers.common['X-CSRFToken'] = window.csrftoken
      return prop
    },

    async getAssignedOnMe(url) {
      delete this.$http.defaults.headers.common['X-CSRFToken'] // remove CSRF in order to access API by a separate API token
      let prop
      let filtered
      this.authHeaders.headers['x-disable-pagination'] = true

      await this.$http
        .get(this.apiUrl + url, this.authHeaders)
        .then((response) => {
          prop = response.data
          this.$http.defaults.headers.common['X-CSRFToken'] = window.csrftoken
          filtered = prop.map((el) => {
            if (el && el.assigned_users) {
                for (var i in el.assigned_users) {
                  if (el.assigned_users[i] == this.userMe.id) {
                    return el
                  }
                }
                return false
            } else {
                return false
            }
          }).filter(function (el) {
            return el != false;
          });
        })
        .catch(error => this.handleError(error, url))
      this.$http.defaults.headers.common['X-CSRFToken'] = window.csrftoken
      return filtered
    },
    // This is a cut and paste from CardModal.vue
    // @todo: Mabe centralize this and use parental method in Modal?
    customDateFormatter(date, short = false, human = false) {
      let d = new Date(date)
      let options = {}
      if (short) {
        options = {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        }
      } else {
        options = {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          weekday: 'short',
          hour: '2-digit',
          minute: '2-digit',
        }
      }
      if (human) {
        options = {
          month: 'short',
          day: 'numeric',
        }
      }
      return d.toLocaleDateString('en-US', options)
    },
  },
}
</script>

<style lang="css">
  .agenda-tasks--wrapper {
    display: flex;
    justify-content: unset;
    flex-direction: row;
  }
  .agenda-tasks--wrapper .tasks-card {width: 150px;}
</style>
