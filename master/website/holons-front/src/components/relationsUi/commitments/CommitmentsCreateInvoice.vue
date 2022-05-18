<template src="./templates/commitments-create-invoice.html"></template>

<script>

/*
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
*/
export default {
  name: 'CommitmentsCreateInvoice',
  props: ['item'],

  data() {
    return {
      loader: null,
      activeMenu: {},
      commitmentsList: [],
    }
  },
  computed: {
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations/invoices'
      return url
    }
  },
  mounted() { },
  methods: {
    storeInvoice: function () {
      this.$http.defaults.headers.common['X-CSRFToken'] = this.csrfToken
      this.loader = this.$loading.show({zIndex: 30,})
      var data = this.item
      var url = this.apiUrl + '/create'
      this.$http.post(url, data).then(response => {
        this.$nextTick(async () => {
            if(response){
              // @todo: switch to the events, will ya?
              this.$parent.createInvoice = false
              this.$parent.selectedCommitment = null
            }
            // this.$emit('refresh-offers')
            this.loader.hide()
            })
        }).catch(error => {
          console.log('Invoices api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
        });
        this.$forceUpdate()
    },
  },
}
</script>
<style>
  .hm.modal.active {
    display: block;
  }
</style>
