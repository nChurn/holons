<template>
  <div class="hm modal active" v-on-modal-close="closeModal">
      <div class="content">
        <h2 class="title">Add template</h2>
        <div class="form-row">
          <label for="campaign_title">Title</label>
          <div class="fluid input field ui">
            <input
              type="text"
              class="field ui"
              v-model="title"
              id="template_title"
            >
          </div>
        </div>
        <div class="form-row">
          &nbsp;<br /><br />
        </div>
        <div class="form-row">
          <div class="input ui">
            <button
              v-on:click.prevent="createTemplateRequest()"
              class="button ui"
              v-bind:disabled="title == ''"
            >
              Save
            </button>
            <button
              v-on:click.prevent="closeModal()"
              class="button ui"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'AddTemplate',
  props: [
      'campaign',
  ],
  data() {
    return {
    }
  },
  mounted() {
    console.log('Create template')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/campaigns/templates/create'
      return url
    },
  },
  methods: {
    closeModal: function () {
      this.$parent.showAddTemplateModal = false
    },
    createTemplateRequest: function () {

      var data = {
        'title': this.title,
        'campaign': this.$parent.activeCampaign.id
      }

      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to create a template for us
      this.$http.post(this.apiUrl, data).then(response => {
        this.$parent.showAddTemplateModal = false
        console.log('Create template')
        console.log(response)
        this.loader.hide()
        this.$forceUpdate()
        this.$parent.getCampaigns()
      }).catch(error => {
        console.log(['Template api is unavailable at the moment', error])
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
