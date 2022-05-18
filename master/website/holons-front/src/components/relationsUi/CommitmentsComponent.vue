<template src="./templates/commitments.html" />

<script>

import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import CommitmentsHeading from './commitments/CommitmentsHeading'
import CommitmentsTabs from './commitments/CommitmentsTabs'
import CommitmentsMainThead from './commitments/CommitmentsMainThead'
import CommitmentsTr from './commitments/CommitmentsTr'
import CommitmentsCreateInvoice from './commitments/CommitmentsCreateInvoice'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'CommitmentsComponent',

  components: {
    CommitmentsHeading,
    CommitmentsMainThead,
    CommitmentsTr,
    CommitmentsTabs,
    CommitmentsCreateInvoice,
  },

  props: {},

  data() {
    return {
      loader: null,
      activeMenu: {},
      commitmentsList: [],
      createInvoice: false,
      selectedCommitment: null,
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol 
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations/commitments'
      return url
    }
  },
  mounted() {
    this.getCommitments()
  },
  methods: {
    getCommitments: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          this.commitmentsList = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Commitments api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    showCreateInvoiceModal: function(item) {
      console.log('showCreateInvoiceModal')
      this.createInvoice = true
      this.selectedCommitment = item
    }
  }
}
</script>

<style scoped>
</style>
