<template src="./templates/invoices.html" />

<script>

import Vue from 'vue'
import Loading from 'vue-loading-overlay'

import InvoicesHeading from './invoices/InvoicesHeading'
import InvoicesTabs from './invoices/InvoicesTabs'
import InvoicesMainThead from './invoices/InvoicesMainThead'
import InvoicesTr from './invoices/InvoicesTr'
import InvoicesDisplay from './invoices/InvoicesDisplay'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'InvoicesComponent',

  components: {
    InvoicesHeading,
    InvoicesMainThead,
    InvoicesTr,
    InvoicesTabs,
    InvoicesDisplay,
  },

  props: {},

  data() {
    return {
      loader: null,
      invoicesList: [],
      selectedInvoice: null,
      activateInvoice: '',
    }
  },
  computed: {
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
  },
  mounted() {
    this.getInvoices()
    this.activateInvoice = document.location.href.split('?invoice_id=')[1]
    
    if(typeof this.activateInvoice !== 'undefined'){
     this.getInvoiceById()
    }
  },
  methods: {
    getInvoices: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.invoicesList = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Invoices api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    getInvoiceById: function () {
      this.$http.get(this.apiUrl + '/' + this.activateInvoice).then(response => {
        if(response){
          this.$nextTick(async () => {
            this.loader.hide()
            this.selectedInvoice = response.data.data
          })
        }
      }).catch(error => {
          console.log('Invoices api is unavailable at the moment')
          console.log(error)
          // this.loader.hide()
      });
    },
  }
}
</script>

<style scoped>
</style>
