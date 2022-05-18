<template src="./templates/rays-ui.html"></template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

import RaysAttached from './RaysAttached';
import RaysDirectMessages from './RaysDirectMessages';
import RaysAddMessage from './RaysAddMessage';
import RaysDisplay from './RaysDisplay';
import RaysDirectMessagesDisplay from './RaysDirectMessagesDisplay';
import RaysWriteNewModal from './RaysWriteNewModal';
import RoutingUiComponent from '../routingUi/RoutingUiComponent';
import RaysNewThreadForm from './RaysNewThreadForm'

Vue.component('rays-attached', RaysAttached)
Vue.component('rays-direct-messages', RaysDirectMessages)
Vue.component('rays-add-message', RaysAddMessage)
Vue.component('rays-display', RaysDisplay)
Vue.component('rays-direct-messages-display', RaysDirectMessagesDisplay)
Vue.component('rays-write-new-modal', RaysWriteNewModal)
Vue.component('routing-ui', RoutingUiComponent)
Vue.component('rays-new-thread-form', RaysNewThreadForm)

Vue.use(Loading, { zIndex: 9999, })

export default {
  name: 'RaysUiComponent',
  data() {
    return {
      loader: null,
      rays: {
        active: [],
        pending: [],
        fixed: []
      },
      selectedRay: {},
      selectedRaySettings: {},
      selectedMessage: null,
      selectedThread: null,
      selectedFixedRay: {},
      isCustom: false,
      addMessageModal: false,
      messageSent: false,
    }
  },
  mounted() {
    this.getRays()
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/direct'
      return url
    }
  },
  methods: {
    getRays: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl
      // then get fresh data
      this.$http.get(url).then(response => {
        this.rays.active = response.data.rays
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
                // @todo: refactor this to be more readable?
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
      console.log('open rays modal')
      this.raysModal = true
    },
    refreshRays: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl += 'refresh'
      this.$http.get(url).then(response => {
        this.rays.active = response.data.rays
        console.log('Refresh rays')
        console.log(this.rays.active)
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    showRaySettingsModal: function (ray) {
      this.raysSettingsModal = true
      this.selectedRaySettings = ray
      // this.updateRaySettings(ray.id, ray)
    },
    showBusinessCard: function () {
      var jQuery = window.$
      jQuery('#raysOwnProfileModal').show()
    },
    hideBusinessCard: function () {
      var jQuery = window.$
      jQuery('#raysOwnProfileModal').hide()
    },
    writeMessage: function () {
      console.log('write')
      var jQuery = window.$
      jQuery('#raysWriteMessageModal')
        .modal('show')
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#email-inboxes {
  padding-bottom: 1000px;
}
.write-new-message {
    font-size: 1rem;
    width: 120px;
    margin: 0 auto 12px auto;
    border: 1px solid rgba(0, 0, 0, 0.35);
    border-radius: 4px;
    padding: 0;
    line-height: 30px;
    height: 30px;
    color: rgba(0, 0, 0, 0.35);
}
#holonsIcon_write {
    position: relative;
    width: 20px;
    top: 4px;
    left: -18px;
    border: 1px solid rgba(0, 0, 0, 0.35);
    border-radius: 50%;
    box-shadow: 2px 0px 1px 0px rgb(35 39 43 / 55%);
}
</style>
