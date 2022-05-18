<template src="./templates/invoices-display.html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: "InvoicesDisplay",
  components: { },
  props: {
    'invoice': {
      type: Object,
      default: window.invoiceData 
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
          url += '/api/relations/invoices'
      return url
    },
    me: function () {
      return window.handle
    },
    userLoggedIn: function () {
       return window.user_logged_in 
    },
  },
  methods: {
    acceptInvoice: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      var url = this.apiUrl + '/' + this.invoice.id + '/accept/'
      var data = this.invoice
      this.$http.patch(url, data).then(response => {
        if(response){
          this.$nextTick(async () => {
            // await this.refreshOnSave()
            this.loader.hide()
            window.location('/relations/invoices')
          })
        }
      }).catch(error => {
          console.log('Invoices api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  },
}
</script>
