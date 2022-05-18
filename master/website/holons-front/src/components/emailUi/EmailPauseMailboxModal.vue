<template>
  <div class="mailbox-add modal">
      <div
        class="settings"
        v-if="!mailbox.is_paused"
      >
        <h1>Pause mailbox {{ mailbox.alias }}@{{ mailbox.domain }}</h1>
        <div class="field">
          <button
            v-on:click.prevent="closeModal()"
            class="ui button cancel"
          >Cancel</button>
          <button
            v-on:click.prevent="pauseMailbox()"
            class="ui button"
          >Pause this mailbox</button>
        </div>
      </div>
      <div
        class="settings"
        v-else
      >
        <h1>Re-enable mailbox {{ mailbox.alias }}@{{ mailbox.domain }}</h1>
        <div class="field">
          <button
            v-on:click.prevent="closeModal()"
            class="ui button cancel"
          >Cancel</button>
          <button
            v-on:click.prevent="reEnableMailbox()"
            class="ui button"
          >Re-Enable this mailbox</button>
        </div>
      </div>
  </div>
</template>

<script>
  export default {
    name: 'EmailPauseMailboxModal',
    props: [
      'mailbox'
    ],
    data() {
      return {
      }
    },
    mounted() {
      console.log('Email Pause Mailbox Modal')
    },
    computed: {
      apiUrl: function () {
        var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
            url += '/api/mailboxes/'
        return url
      }
    },
    methods: {
      pauseMailbox: function () {
        console.log('Pause mailbox')
        this.loader = this.$loading.show({zIndex: 30,})
        // ask backend to create a random mailbox for us
        var url = this.apiUrl + 'pause'
        var data = this.mailbox
        this.$parent.selectedMailbox.is_paused = true
        this.$http.post(url, data).then(response => {
          console.log(response.data)
          this.$parent.selectedMailbox.is_paused = true
          this.$parent.emailPauseMailboxModal = false
          this.loader.hide()
          this.$forceUpdate()
        }).catch(error => {
          console.log(['Cannot pause mailbox. Mailbox api is unavailable at the moment', error])
          this.$parent.emailPauseMailboxModal = false
          this.loader.hide()
        });
      },
      reEnableMailbox: function () {
        console.log('Re-enable mailbox')
        this.loader = this.$loading.show({zIndex: 30,})
        // ask backend to create a random mailbox for us
        var url = this.apiUrl + 'reenable'
        var data = this.mailbox
        this.$http.post(url, data).then(response => {
          console.log(response.data)
          this.$parent.selectedMailbox.is_paused = false
          this.$parent.emailPauseMailboxModal = false
          this.loader.hide()
          this.$forceUpdate()
        }).catch(error => {
          console.log(['Cannot reenable mailbox. Mailbox api is unavailable at the moment', error])
          this.$parent.emailPauseMailboxModal = false
          this.loader.hide()
        });
      },
      closeModal: function () {
        this.$parent.emailPauseMailboxModal = false
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
    top: 10%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
  .field {
    margin-bottom: 10px;
  }
</style>
