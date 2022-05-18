<template>
  <div class="hm modal active" v-on-modal-close="closeModal"
  >
    <div class="content">
      <h2 class="title">Add new campaign</h2>
      <div>
        <div class="form-row">
          <label for="campaign_title">name</label>
          <div class="fluid input field ui">
            <input
              type="text"
              class="field ui"
              v-model="title"
              id="campaign_title"
            >
          </div>
        </div>

        <label>owner</label>
        <p>
          [ address book module ]
        </p>
        <!--<div class="form-row">
          <label for="campaign_beneficiary">Beneficiary</label>
          <div class="fluid input field ui">
            <input
              type="text"
              class="field ui"
              v-model="beneficiary"
              id="campaign_beneficiary"
            >
          </div>
        </div>-->
        <div class="form-row">
          &nbsp;<br /><br />
        </div>
        <div>

            <button
              v-on:click.prevent="closeModal()"
              class="ui basic button"
            >
              cancel
            </button>

            <button
              v-on:click.prevent="createCampaignRequest()"
              class="ui basic button right floated"
              v-bind:disabled="title == ''"
            >
              add
            </button>

        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'CampaignAdd',
  data() {
    return {
      title: '',
      beneficiary: ''
    }
  },
  mounted() {
    console.log('Campaign Add')
  },
  computed: {
    apiUrl: function () {
      var url = window.location.protocol + '//' + window.location.host.replace('8080', '8000')
          url += '/api/campaigns/create'
      return url
    },
  },
  methods: {
    closeModal: function () {
      this.$parent.showAddCampaignModal = false
    },
    createCampaignRequest: function () {

      var data = {
        'title': this.title,
        'beneficiary': this.beneficiary,
      }

      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to create a campaign for us
      this.$http.post(this.apiUrl, data).then(response => {
        this.$parent.showAddCampaignModal = false
        console.log('Create campaign')
        console.log(response.data)
        this.loader.hide()
        this.$forceUpdate()
        this.$parent.getCampaigns()
      }).catch(error => {
        console.log(['Campaign api is unavailable at the moment', error])
        this.loader.hide()
      });

    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.3);
    z-index: 9999;
  }
  .settings {
    background: #fff;
    padding: 20px;
    top: 20%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
</style>
