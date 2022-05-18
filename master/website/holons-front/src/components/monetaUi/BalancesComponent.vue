<template src="./templates/balances.html" />

<script>

import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import WithdrawModal from './WithdrawModal'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'BalancesComponent',

  components: {
    WithdrawModal
  },

  props: {},

  data() {
    return {
      loader: null,
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/moneta/balances'
      return url
    }
  },
  mounted() {
    console.log('BalancesComponent main')
  },
  methods: {
    openAddBusinessEntityModal() {
      var jQuery = window.$
      jQuery('#addBusinessEntityModal')
        .modal('show')
    },
    getBusinessEntities: function () {
      console.log('Get entities')
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          // await this.refreshOnSave()
          this.businessEntities = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Business Entity api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    open: function (elementId) {
      var jQuery = window.$
      jQuery('#modal__' + elementId).modal('show')
    },
    close: function () {
      var jQuery = window.$
      jQuery('.ui.modal').modal('hide')
    }
  }
}
</script>

<style scoped>
</style>

