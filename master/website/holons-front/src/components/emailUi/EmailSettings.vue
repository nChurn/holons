<template>
  <div class="mailbox-add modal">
      <div class="settings">
        <h1>Add your Frontapp API token</h1>
        <label for="">Token is necessary to import mailboxes from your Frontapp account</label>
        <div class="ui field">
            <input type="text" v-model="frontappToken" />
        </div>
        <div class="field">
          <button
            v-on:click.prevent="closeModal()"
            class="ui button cancel"
          >Cancel</button>
          <button
            v-on:click.prevent="updateEmailSettings()"
            v-bind:disabled="frontappToken  == ''"
            class="ui button"
          >Save</button>
        </div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'EmailSettings',
  data() {
    return {
      frontappToken: '',
    }
  },
  mounted() {
    console.log('Email Settings')
    this.getEmailSettings()
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/mailboxes/'
      return url
    }
  },
  methods: {
    closeModal: function () {
      this.$parent.emailSettingsModal = false
    },
    getEmailSettings: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to send us our settings
      var url = this.apiUrl + 'settings'
      this.$http.get(url).then(response => {
        this.loader.hide()
        this.frontappToken = response.data.email_settings.frontapp_token
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    updateEmailSettings: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.$parent.emailSettingsModal = false
      // ask backend to save email settings
      var url = this.apiUrl + 'settings'
      var data = {frontapp_token: this.frontappToken}
      this.$http.post(url, data).then(() => {
        this.loader.hide()
        this.$parent.emailSettingsModal = false
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
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
  .field {
    margin-bottom: 10px;
  }
</style>