<template>
  <div class="hm modal platos active" v-on-modal-close="closeModal">
      <h2 class="title">campaign settings</h2>
      <div class="content">
        <div class="form-row">
        </div>
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
        <div class="form-row">

            <button
              v-on:click.prevent="closeModal()"
              class="button ui"
            >
              cancel
            </button>
            <button class="ui basic positive button">
              move to ongoing campaigns
            </button>

            <button
              v-on:click.prevent="createCampaignRequest()"
              class="ui basic button right floated"
              v-bind:disabled="title == ''"
            >
              save
            </button>


        </div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'CampaignEdit',
  props: [
      'title',
      'beneficiary'
  ],
  data() {
    return {
    }
  },
  mounted() {
    console.log('Campaign edit')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/campaigns/'
      return url
    },
  },
  methods: {
    closeModal: function () {
      this.$parent.showEditCampaignModal = false
    },
    createCampaignRequest: function () {

      // var data = {
      //   'mailbox': this.mailboxHash,
      // }

      // this.loader = this.$loading.show({zIndex: 30,})
      // // ask backend to create a random mailbox for us
      // var url = this.apiUrl + 'user_add_mailbox'
      // this.$http.post(url, data).then(response => {
      //   this.mailboxHash = response.data.name
      //   this.$parent.createMailbox = false
      //   this.mailbox = response.data
      //   // this.setDNS = true
      //   this.loader.hide()
      //   this.$forceUpdate()
      // }).catch(error => {
      //   console.log(['Mailbox api is unavailable at the moment', error])
      //   this.loader.hide()
      // });

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
