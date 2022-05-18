<template>
  <div class="mailbox-add modal">

      <div class="settings">
        <div class="setemail" v-if="mailboxHash === ''">
          <h1>Import mailbox from the FrontApp account</h1>
          <div class="message">
            <p>
              Give us your incomming email address must be the same as Frontapp inbox <input class="input" type="text" v-model="incomingEmail">, we need it to set up forwarding for you<br />
            </p>
            <p>

            </p>
          </div>
          <h2>Add your Frontapp API token</h2>
          <label for="">Token is necessary to import mailboxes from your Frontapp account</label>
          <div class="ui fluid input field">
              <input class="input" type="text" v-model="frontappToken" />
          </div>
          <div class="field">
            <button
              v-on:click.prevent="closeModal()"
              class="ui button cancel"
            >Cancel</button>
            <button
              v-on:click.prevent="createMailboxRequest()"
              v-bind:disabled="incomingEmail  == '' && frontappToken == ''"
              class="ui button"
            >Use this mailbox</button>
          </div>
        </div>

        <div class="setredirect" v-if="mailboxHash && !setDNS">
          <h1>Add redirect</h1>
          <div class="message">
            <p>
              Forward mail to this address: {{ mailboxHash }} to enable your inbox (this message will disappear after we receive at least one email from you)<br />
            </p>
          </div>
          <button
            v-on:click.prevent="closeModal()"
            class="ui button cancel"
          >Close</button>
          <button
            v-on:click.prevent="checkForwarding()"
            class="ui button"
          >Check mail forwarding</button>
          <button
            v-on:click.prevent="completeMailboxRequest()"
            v-if="mailboxHash != '' && !setDNS"
            class="ui button"
            v-bind:disabled="true"
          >Set up DNS-records</button>
        </div>

        <div class="setdns" v-if="setDNS">
          <h1>Set up your DNS</h1>
          <div class="message">
            <p>
              These DNS records are necessary to authorise mail forwarding.
            </p>
            <mailbox-dns-settings
              v-if="mailbox"
              v-bind:mailbox="mailbox"
            />
          </div>
          <!-- <button
            v-on:click.prevent="this.MailboxDnsSettings.validateDNS()"
            v-if="mailboxHash != ''"
            v-bind:disabled="incomingEmail  == ''"
          >Set up DNS-records</button> -->
        </div>
      </div>

  </div>
</template>

<script>
import Vue from 'vue';
import MailboxDnsSettings from './MailboxDnsSettings';
Vue.component('mailbox-dns-settings', MailboxDnsSettings)

export default {
  name: 'MailboxAdd',
  props: [
    'createMailbox',
  ],
  data() {
    return {
      frontappToken: '',
      mailboxHash: '',
      incomingEmail: '',
      setDNS: false,
      mailbox: false
    }
  },
  mounted() {
    console.log('Mailbox Add')
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
      this.$parent.emailImportModal = false
    },
    getEmailSettings: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to send us our settings
      var url = this.apiUrl + 'settings/frontapp-token'
      this.$http.get(url).then(response => {
        this.loader.hide()
        this.frontappToken = response.data.email_settings.frontapp_token
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    createMailboxRequest: function () {
      this.createMailbox = true

      var data = {
        'mailbox': this.mailboxHash,
        'incoming_email': this.incomingEmail,
        'frontapp_import': true,
        'frontapp_token': this.frontappToken
      }

      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to create a random mailbox for us
      var url = this.apiUrl + 'user_add_mailbox'
      this.$http.post(url, data).then(response => {
        this.mailboxHash = response.data.name
        this.$parent.createMailbox = false
        this.mailbox = response.data
        // this.setDNS = true
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    completeMailboxRequest: function () {
      this.createMailbox = true
      this.loader = this.$loading.show({zIndex: 30,})
      // confirm that we are using given email
      var url = this.apiUrl + 'user_add_mailbox'
      var data = {
        'mailbox': this.mailboxHash,
        'incoming_email': this.incomingEmail,
        'frontapp_import': true,
        'frontapp_token': this.frontappToken
      }
      this.$http.post(url, data).then(response => {
        console.log('create dns')
        console.log(response.data)
        this.mailbox = response.data
        this.loader.hide()
        this.$parent.createMailbox = false
        this.setDNS = true
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    checkForwarding: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to send a test email to us
      var url = this.apiUrl + 'check-forwarding'
      var data = {
        'mailbox': this.mailboxHash,
        'incoming_email': this.incomingEmail,
        'frontapp_import': true,
        'frontapp_token': this.frontappToken
      }
      this.$http.post(url, data).then(response => {
        console.log('Send test Email')
        console.log(response.data)
        this.loader.hide()
        this.$forceUpdate()
        this.$parent.getMailboxes()
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    }
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