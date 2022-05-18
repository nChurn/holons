<template src="./templates/offers-main.html" />

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import OffersHeading from './offers/OffersHeading'
import OffersTabs from './offers/OffersTabs'
import OffersTr from './offers/OffersTr'
import OffersMainThead from './offers/OffersMainThead'
import OfferTypeModal from './offers/OfferTypeModal'
import OfferDisplay from './offers/OfferDisplay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'OffersComponent',
  components: {
    OffersMainThead,
    OffersTabs,
    OffersHeading,
    OffersTr,
    OfferTypeModal,
    OfferDisplay,
  },
  props: {},
  data() {
    return {
      loader: null,
      showOfferForm: false,
      selectedOffer: null,
      showOffersList: true,
      offersList: [],
      showOffer: false,
      createOfferType: 'default',
      activeMenu: {},
      offerType: '',
      activateOffer: '',
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
  mounted() {
    this.getOffers()
    this.activateOffer = document.location.href.split('?offer_id=')[1]
    
    if(typeof this.activateOffer !== 'undefined'){
     this.getOfferByToken()
    }
  },
  methods: {
    refreshOffers: function () {
      this.getOffers()
    },
    getOffers: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          // await this.refreshOnSave()
          this.offersList = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Offers api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    getOfferByToken: function () {
      this.$http.get(this.apiUrl + '/' + this.activateOffer).then(response => {
        if(response){
          this.$nextTick(async () => {
            this.loader.hide()
            this.selectedOffer = response.data.data
          })
        }
      }).catch(error => {
          console.log('Offers api is unavailable at the moment')
          console.log(error)
          // this.loader.hide()
      });

    },
    showOfferModal: function () {
      this.showOffer = true
      var jQuery = window.$
      jQuery('#offerModalHolder')
        .modal('show')
      ;
    },
    selectOffer: function (offer_id) {
      // @todo: seems like we don't need this method anymore
      for (var i in this.offersList){
        if(this.offersList[i].id == offer_id){
          console.log('select offer')
          this.selectedOffer = this.offersList[i]
          this.showOfferForm = false
          this.showOffersList = true
          this.showOfferModal()
          this.$forceUpdate()
          break
        }
      }
    },
    createContract: function () {
      this.showOfferForm = true
      this.showOffersList = false
      // this.selectedOffer = null
    },
    goBackToOffers: function () {
      this.showOfferForm = false
      this.showOffersList = true
      this.selectedOffer = null
    },
    customDateFormatter: function (date, short = false) {
      let d = new Date(date)
      let options = short ? {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      } : {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        weekday: 'short',
        hour: '2-digit',
        minute: '2-digit',
      }
      return d.toLocaleDateString('en-US', options)
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
