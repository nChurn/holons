<template src="./templates/offer-display.html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: "OfferDisplay",
  components: { },
  props: {
    'offer': {
      type: Object,
      default: window.offerData
    }
  },
  computed: {
    modalOff: {
      function () { return window.invoiceData }
    },
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations/offers'
      return url
    },
  },
  methods: {
    acceptOffer: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      var url = this.apiUrl + '/' + this.offer.id + '/accept/'
      var data = this.offer
      this.$http.patch(url, data).then(response => {
        if(response){
          this.$nextTick(async () => {
            // await this.refreshOnSave()
            window.location.href = '/relations/offers'
            this.loader.hide()
          })
        }
      }).catch(error => {
          console.log('Offers api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  },
}
</script>
