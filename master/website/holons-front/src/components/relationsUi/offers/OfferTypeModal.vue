<template>
    <offer-type-fixed
      v-if="offerType == 'fixed'"
      v-bind:offer="offer"
      v-on:preview-event="previewEvent"
      v-on:return2edit-event="editEvent"
      v-on:save-event="saveEvent"
    />
    <offer-type-time
      v-else-if="offerType == 'time'"
      v-bind:offer="offer"
      v-on:preview-event="previewEvent"
      v-on:return2edit-event="editEvent"
      v-on:save-event="saveEvent"
    />
    <offer-type-recurring
      v-else-if="offerType == 'recurring'"
      v-bind:offer="offer"
      v-on:preview-event="previewEvent"
      v-on:return2edit-event="editEvent"
      v-on:save-event="saveEvent"
    />
    <offer-type-employment
      v-else-if="offerType == 'employment'"
      v-bind:offer="offer"
      v-on:preview-event="previewEvent"
      v-on:return2edit-event="editEvent"
      v-on:save-event="saveEvent"
    />
    <offer-type-generic
      v-else-if="offerType == 'generic'"
      v-bind:offer="offer"
      v-on:preview-event="previewEvent"
      v-on:return2edit-event="editEvent"
      v-on:save-event="saveEvent"
    />
</template>


<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

// these components are essentially templates
// we have to wrap them in .vue files to be able to link them dynamically from here 

import offerTypeFixed from './offerTypes/fixed'
import offerTypeRecurring from './offerTypes/recurring'
import offerTypeEmployment from './offerTypes/employment'
import offerTypeTime from './offerTypes/time'

Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'OfferTypeModal',
  components: {
    offerTypeFixed,
    offerTypeRecurring,
    offerTypeEmployment,
    offerTypeTime,
  },
  props: {
    offerType: {
      type: String
    },
    offer: {
      type: Object,
      default: function() {
        return {
          id: '',
          contractTitle: 'Generic contract',
          fromName: '',
          toName: '',
          termsFrom: 'sample terms from',
          termsTo: 'sample terms to',
          consideration: 'sample consideration',
          timeframe: 'sample timeframe',
          inviteToken: '',
          status: 'created',
          isAccepted: false,
          contractType: 'generic',
          paragraphs: '',
          createdAt: '',
          preview: false,
          membershipSponsor: false,
        }
      }
    }
  },
  computed: {
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations/offers'
      return url
    },
    me: function () {
      return window.handle
    },
  },
  data() {
    return {
    }
  },
  mounted() {
    this.offer.fromName = (this.offer.fromName == '') ? this.me : this.offer.fromName 
  },
  methods: {
    // event handlers
    editEvent: function () {
      this.offer.preview = false
    },
    saveEvent: function (offerObject) {
      this.offer.preview = false
      this.storeOffer(offerObject)
    },
    previewEvent: function (offerObject) {
      this.offer.preview = true
      this.storeOffer(offerObject)
    },
    // ajax
    storeOffer: function (offerObject) {
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      this.loader = this.$loading.show({zIndex: 30,})
      var data = offerObject
      var url = this.apiUrl
      if(this.offer.id == ''){
        url = url + '/create'
        this.$http.post(url, data).then(response => {
          this.$nextTick(async () => {
              this.offer = offerObject
              this.offer.id = response.data.data.id
              this.offer.inviteToken = response.data.data.invite_token
              this.$emit('refresh-offers')
              this.loader.hide()
              })
          }).catch(error => {
            console.log('Offers api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
          });
          this.$forceUpdate()
      } else {
        url = this.apiUrl + '/' + this.offer.id + '/edit/'
        this.$http.patch(url, data).then(response => {
          this.$forceUpdate()
          this.$nextTick(async () => {
              this.$emit('refresh-offers')
              this.offer.id = response.data.data.id
              this.loader.hide()
              })
          }).catch(error => {
            console.log('Offers api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
          });
      }
    },
  },
}
</script>
