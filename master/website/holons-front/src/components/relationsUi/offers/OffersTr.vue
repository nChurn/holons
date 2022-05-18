<template src="./templates/offers-tr.html"></template>

<script>
import OffersMainWrenchMenuComponent from './OffersMainWrenchMenuComponent'
export default {
  name: "OffersTr",
  components: {
    OffersMainWrenchMenuComponent,
  },
  props: ['offer', 'showMenu'],
  computed: {
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations/offers'
      return url
    }
  },
  methods: {
    showLink: function () {
      window.open(
        this.apiUrl.replace('/api/', '/')
        + '?offer_id='
        + this.offer.invite_token
      )
    },
    withdraw: function () {
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/' + this.offer.id + '/delete'
      this.$http.delete(url).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.$emit('refresh-offers')
          this.loader.hide()
          return response.data.data
        })
      }).catch(error => {
          console.log('Offers api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  },
}
</script>
