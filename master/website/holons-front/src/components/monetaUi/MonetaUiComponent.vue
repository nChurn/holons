<template src="./templates/moneta-ui.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import AddBusinessEntityModal from './AddBusinessEntityModal'
import WithdrawModal from './WithdrawModal'
import CashFlowComponent from './CashFlowComponent'
import BalancesComponent from './BalancesComponent'
import EquityComponent from './EquityComponent'
import InvestmentsComponent from './InvestmentsComponent'
import LoansDepositsComponent from './LoansDepositsComponent'
import PlComponent from './PlComponent'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'MonetaUiComponent',

  components: {
    AddBusinessEntityModal,
    BalancesComponent,
    CashFlowComponent,
    EquityComponent,
    InvestmentsComponent,
    LoansDepositsComponent,
    PlComponent,
    WithdrawModal
  },

  props: {},

  data() {
    return {
      contexts: [],
      activeTab: 'balances',
      activeContext: null,
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/moneta/business-entities'
      return url
    },
    me: function () {
      return window.handle
    }
  },

  mounted() {
    this.getContexts()
  },

  methods: {
    getContexts(switchToFirst = true){
      fetch(window.location.origin + '/api/purpose/contexts/')
      .then(res => res.ok && res.json())
      .then(res => {
        if(!res) return

        this.contexts = res.filter(c => c.type != 'user_personal')
        this.$forceUpdate()

        if(switchToFirst){
          this.switchContext(this.contexts[0])
        }
      })
    },
    switchContext(context){
      this.activeContext = context
    }
  }
}
</script>

<style lang="css">
  #moneta {
    background: #F7F8FA;
    color: black !important;
  }
  .mm-cta {
    display: inline-block;
    padding: 3px;
  }
</style>
