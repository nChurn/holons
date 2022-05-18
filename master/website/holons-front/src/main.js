import Vue from 'vue'
import App from './App.vue'
import IdentityApp from './IdentityApp.vue'
import SendRayApp from './SendRayApp.vue'
import PublicProfileApp from './PublicProfileApp.vue'
import SubscriptionApp from './SubscriptionApp.vue'
import SubscriptionControlApp from './SubscriptionControlApp.vue'
import SemanticUI from 'semantic-ui-vue'
Vue.config.devtools = true
Vue.config.silent = true // this is not cool but we need it to get rid of warnings in local env

Vue.config.productionTip = false

import axios from 'axios'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
import 'vue-wysiwyg/dist/vueWysiwyg.css'
import 'cropperjs/dist/cropper.css'
import TextareaAutosize from 'vue-textarea-autosize'
import screenfull from 'screenfull'
//import * as WordsGenerateFrom from './words'
window.screenfull = screenfull

Vue.component('loading', Loading)

// Set csrftoken
if (window.csrftoken) {
  axios.defaults.headers.common['X-CSRFToken'] = window.csrftoken
} else console.log('No csrftoken')

Vue.prototype.$http = axios

Vue.prototype.$isLoading = false
Vue.prototype.$paidAccount = window.paid_account

import MonetaUiComponent from './components/monetaUi/MonetaUiComponent.vue'
Vue.component('moneta-ui', MonetaUiComponent)

import EmailUiComponent from './components/emailUi/EmailUiComponent'
Vue.component('email-ui', EmailUiComponent)

import Agenda from './components/workSpacesUI/Agenda'
Vue.component('agenda', Agenda)

import WsCreator from './components/workSpacesUI/WsCreator'
Vue.component('ws-creator', WsCreator)

import WorkSpaces from './components/workSpacesUI/WorkSpaces'
Vue.component('work-spaces', WorkSpaces)

import RaysUiComponent from './components/raysUi/RaysUiComponent'
Vue.component('rays-ui', RaysUiComponent)

import PlatosFlyWheelComponent from './components/platosFlyWheelUi/PlatosFlyWheelUiComponent'
Vue.component('platos-flywheel-ui', PlatosFlyWheelComponent)

import TalentsUiComponent from './components/talentsUi/TalentsUiComponent'
Vue.component('talents-ui', TalentsUiComponent)

import CampaignsUiComponent from './components/campaignsUI/CampaignsUiComponent'
Vue.component('campaigns-ui', CampaignsUiComponent)
 
import TimeTrackerUiComponent from './components/timeTrackerUi/TimeTrackerUiComponent'
Vue.component('timetracker-ui', TimeTrackerUiComponent)

import TimeTrackerModalComponent from './components/timeTrackerUi/TimeTrackerModalComponent'
Vue.component('timetracker-modal', TimeTrackerModalComponent)

import TimeTrackerSidebarComponent from './components/timeTrackerUi/TimeTrackerSidebarComponent'
Vue.component('timetracker-sidebar', TimeTrackerSidebarComponent)

import CalendarUiComponent from './components/calendarUi/CalendarUiComponent'
Vue.component('calendar-ui', CalendarUiComponent)
import CalendarAgendaUiComponent from './components/calendarUi/CalendarAgendaUiComponent'
Vue.component('calendar-agenda-ui', CalendarAgendaUiComponent)

import PurposeUiComponent from './components/purposeUi/PurposeUiComponent'
Vue.component('purpose-ui', PurposeUiComponent)

import LoginForm from './components/LoginForm'
Vue.component('login-form', LoginForm)

import RegistrationForm from './components/RegistrationForm'
Vue.component('registration-form', RegistrationForm)

import InvoicesDisplay from './components/relationsUi/invoices/InvoicesDisplay'
Vue.component('invoice-component', InvoicesDisplay)

import OfferDisplay from './components/relationsUi/offers/OfferDisplay'
Vue.component('offer-component', OfferDisplay)

Vue.use(SemanticUI)
Vue.use(TextareaAutosize)
Vue.use(require('vue-shortkey'), { prevent: ['input', 'textarea', '.editr--content'] })

Vue.prototype.$generateRandomPhrase = function () {
  return (
    'conf-' + getRandomInt((36 ** 7) - 1).toString(36).padStart(7, '0')
    /*WordsGenerateFrom.adjs[getRandomInt(WordsGenerateFrom.adjs.length - 1)] +
    "-" +
    WordsGenerateFrom.nouns[getRandomInt(WordsGenerateFrom.nouns.length - 1)]*/
  )
}
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

Vue.directive("on-modal-close", {

  bind (modal, binding) {
    const observer = new MutationObserver(mutations => {
      for (const m of mutations) {
        const newValue = m.target.getAttribute(m.attributeName);
        if (!newValue.includes("active") && m.oldValue.includes("active"))
          observer.disconnect();
          binding.value();
      }
    });
  
    observer.observe(modal, {
      attributes: true,
      attributeOldValue : true,
      attributeFilter: ['class'],
    });
  }
})

new Vue({
  render: (h) => h(IdentityApp),
  el: '#identity-app',
}).$mount('#identity-app')

new Vue({
  render: (h) => h(SendRayApp),
  el: '#send-ray-app',
}).$mount('#send-ray-app')

new Vue({
  render: (h) => h(PublicProfileApp),
  el: '#public-profile-app',
}).$mount('#public-profile-app')


// @todo: this is an ugly quickfix,
// but we need it to get rid of errors on non-subscribe pages
if(window.subscriptionActive == true) {
  new Vue({
    render: (h) => h(SubscriptionApp),
    el: '#subscription-app',
  }).$mount('#subscription-app')
}

if(window.offerIsActive == true) {
  new Vue({
    render: (h) => h(OfferDisplay),
    el: '#offer-app',
  }).$mount('#offer-app')
}

if(window.invoiceIsActive == true) {
  new Vue({
    render: (h) => h(InvoicesDisplay),
    el: '#invoice-app',
  }).$mount('#invoice-app')
}

new Vue({
  render: (h) => h(SubscriptionControlApp),
  el: '#subscription-control',
}).$mount('#subscription-control')

new Vue({
  render: (h) => h(Agenda),
  el: '#agenda',
}).$mount('#agenda')

new Vue({
  render: (h) => h(TimeTrackerModalComponent),
  el: '#timetracker-modal',
}).$mount('#timetracker-modal')

new Vue({
  render: (h) => h(TimeTrackerSidebarComponent),
  el: '#timetracker-sidebar',
}).$mount('#timetracker-sidebar')

new Vue({
  render: (h) => h(CalendarAgendaUiComponent),
  el: '#calendar-agenda-ui',
}).$mount('#calendar-agenda-ui')

new Vue({
  render: (h) => h(App),
  el: '#app',
}).$mount('#app')
