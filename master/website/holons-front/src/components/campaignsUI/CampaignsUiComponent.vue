<template src="./templates/campaigns-ui.html" lang="html"></template>
<!-- <style src="./css/workspaces.css" scoped></style> -->

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
import CampaignAdd from './CampaignAdd'
import CampaignEdit from './CampaignEdit'
import TemplateAdd from './TemplateAdd'

Vue.component('campaign-add', CampaignAdd)
Vue.component('campaign-edit', CampaignEdit)
Vue.component('template-add', TemplateAdd)

Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'CampaignsUiComponent',

  data() {
    return {
      loader: null,
      showAddCampaignModal: false,
      showEditCampaignModal: false,
      showAddTemplateModal: false,
      activeCampaign: null,
      campaigns: []
    }
  },
  mounted() {
    console.log('Campaigns loaded')
    this.getCampaigns()
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/campaigns/show'
      return url
    },
  },
  methods: {
    updateRepliesCount(template_id) {
        console.log('Update template usage')
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/campaigns/templates/update'
        var data = {
          template_id: template_id,
          scope: 'replies'
        }
        this.$http.post(url, data).then(response => {
          console.log(response.data)
          this.loader.hide()
          this.getCampaigns()
        }).catch(error => {
          console.log(['Templates api is unavailable at the moment (direct update usage)', error])
          this.loader.hide()
        });

    },
    getCampaigns: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // then get fresh data
      this.$http.get(this.apiUrl).then(response => {
        console.log(response.data.campaigns)
        this.campaigns = response.data.campaigns
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Campaigns api is unavailable at the moment (get campaigns)', error])
        this.loader.hide()
      });
    },
    openAddCampaignModal: function () {
      this.showAddCampaignModal = true
      console.log('add campaign modal')
    },
    openCampaignSettingsModal: function (campaignId) {
      this.showEditCampaignModal = true
      for(var campaign in this.campaigns){
        if(this.campaigns[campaign].id == campaignId){
          this.activeCampaign = this.campaigns[campaign]
        }
      }
      console.log('campaign settings for: ' + campaignId)
    },
    openAddTemplateModal: function (campaignId) {
      for(var campaign in this.campaigns){
        if(this.campaigns[campaign].id == campaignId){
          this.activeCampaign = this.campaigns[campaign]
        }
      }
      this.showAddTemplateModal = true
      console.log('add template for: ' + campaignId)
    }
  }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .campaigns-list {
    overflow: hidden;
    overflow-y: scroll;
    max-height: 800px;
    height: 100%;
  }
  td.archived {
    text-decoration: line-through;
    color: rgba(0,0,0,.35);
    text-align: right;
  }
  td.archived .ui.button {display: none !important}
  .platos-campaign-table {
    border-bottom: 30px solid #23272B;
    padding: 1rem;
    margin: 1rem;
    border-radius: 0;
    width: 100%
  }

  .platos-campaign-table h2 {
    text-transform: uppercase;
    font-size: 4rem;
    font-weight: bolder;
  }
</style>
