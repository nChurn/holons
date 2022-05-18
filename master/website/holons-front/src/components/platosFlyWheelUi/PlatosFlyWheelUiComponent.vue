<template src="./templates/platos-ui.html"></template>

<script>
import Vue from 'vue';
import VueHotkey from 'v-hotkey';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

import RaysAdd from './RaysAdd';
import RaysSettings from './RaysSettings';
import PlatosRaysAttached from './PlatosRaysAttached';
import RaysMessages from './RaysMessages';
import RaysAddMessage from './RaysAddMessage';
import RaysDisplay from './RaysDisplay';

Vue.component('rays-add', RaysAdd)
Vue.component('rays-settings', RaysSettings)
Vue.component('platos-rays-attached', PlatosRaysAttached)
Vue.component('rays-messages', RaysMessages)
Vue.component('rays-add-message', RaysAddMessage)
Vue.component('rays-display', RaysDisplay)

Vue.use(Loading, { zIndex: 9999, })
Vue.use(VueHotkey)

export default {
  name: 'PlatosFlyWheelUiComponent',
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/'
      return url
    },
    platoBidsCount: function () {
      return window.platos_bids
    },
    platoAccountIsPaid: function () {
      return window.plato_account_is_paid
    }
  },
  data() {
    return {
      loader: null,
      raysModal: false,
      raysSettingsModal: false,
      rays: {
        active: [],
        pending: [],
        fixed: []
      },
      selectedRay: {},
      selectedRaySettings: {},
      selectedMessage: null,
      selectedFixedRay: {},
      isCustom: false,
      addMessageModal: false,
    }
  },
  mounted() {
    this.getRays()
  },
  methods: {
    getRays: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl
      // then get fresh data
      this.$http.get(url).then(response => {
        this.rays.active = response.data.rays
        this.rays.bids = response.data.bids
        this.rays.fixed = response.data.fixed_rays
        if(this.selectedRay != {}){
          // keep selected ray even after refresh
          for (var ray in response.data.rays) {
            if(response.data.rays[ray].short_name == 'ALL'){
              var upwork_ray = JSON.parse(JSON.stringify(response.data.rays[ray]))
              upwork_ray.short_name = 'Upwork'
              this.rays.active.push(upwork_ray)
            }
            if(response.data.rays[ray].id == this.selectedRay.id){
              this.selectedRay = response.data.rays[ray]
              for (var message in this.selectedRay.messages){
                if (this.selectedRay.messages[message].archived == false && this.selectedRay.messages[message].deleted == false){
                  this.selectedMessage = this.selectedRay.messages[message]
                  break
                }
              }
            }
          }
        }
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (get rays)', error])
        this.loader.hide()
      });
    },
    openRaysModal: function () {
      this.raysModal = true
    },
    refreshRays: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl += 'refresh'
      this.$http.get(url).then(response => {
        this.rays.active = response.data.rays
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    showRaySettingsModal(ray) {
      this.raysSettingsModal = true
      this.selectedRaySettings = ray
      this.$forceUpdate()
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#email-inboxes {
  padding-bottom: 1000px;
}
/*  #parent {
    overflow: auto !important;
  }
  .ray {
    font-family: sans-serif;
  }*/
</style>
