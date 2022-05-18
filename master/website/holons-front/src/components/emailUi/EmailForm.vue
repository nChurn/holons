<template>
        <div class="write-email-form">
          <div v-if="!$parent.$parent.messageSentSuccess" class="ui grid form"> <!-- /temporary off -->
            <div class="form-row row">
              <div class="column">
                <p><strong>Send email:</strong></p>
                <label>From: <input class="ui field" type="text" v-model="fromEmail"></label>
              </div>
            </div>
            <div class="form-row row">
              <div class="column">
                <label>To: <input class="ui field" type="text" v-model="toEmail"></label>
              </div>
            </div>
            <div class="form-row row">
              <div class="column">
                <label>Subject: <input class="ui field" type="text" v-model="emailSubject"></label>
              </div>
            </div>
            <div class="form-row row">
              <div class="column">
                <label>Message: </label>
                <wysiwyg v-model="sendEmail['message']" />
                <!-- <textarea class="ui field" cols="30" v-model="sendEmail['message']" rows="10"></textarea> -->
              </div>
            </div>
            <div
              class="form-row row"
            >
              <div class="column">
                <button
                  class="ui button"
                  v-on:click.prevent="sendEmailRequest()"
                  v-if="!sendButtonText"
                >Send email</button>
                <button
                  class="ui button"
                  v-on:click.prevent="sendEmailRequest()"
                  v-else
                >{{ sendButtonText }}</button>
              </div>
            </div>
          </div>
          <div
            class="form-row row"
            v-else
          >
          <div class="ui message">
            <div class="header">
              Success
            </div>
            <ul class="list">
              <li>Message sent successfully</li>
            </ul>
          </div>
          </div>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
        </div>
</template>

<script>
import Vue from 'vue'
import wysiwyg from "vue-wysiwyg";
Vue.use(wysiwyg, {});
export default {
  name: 'EmailForm',
  props: [
    'emailSubject',
    'conversationId',
    'inReplyToId',
    'quotedBody',
    'conversation',
    'sendButtonText'
  ],
  data() {
    return {
      sendEmail: {
        from: '',
        to: '',
        subject: '',
        message: '',
      },
    }
  },
  mounted() {
    console.log('Write Email Form')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/mailboxes/'
      return url
    },
    activeMailbox: function () {
        console.log('activeMailbox')
        if (this.$parent.$parent.selectedMailbox.alias === 'all new folder') {
          return this.$parent.$parent.getMailboxByAlias(this.$parent.message.mailbox_alias)
        }
        return this.$parent.$parent.selectedMailbox
    },
    toEmail: function () {
      if (this.$parent.message.outgoing) {
        return this.$parent.message.to_address[0]
      }
      return this.$parent.message.from_address[0]
    },
    fromEmail: function () {
      if (this.$parent.message.outgoing) {
        return this.$parent.message.from_address[0]
      }
      return this.$parent.message.to_address[0]
    }
  },
  methods: {
    sendEmailRequest: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + 'send_email'
      this.sendEmail['from'] = this.fromEmail
      this.sendEmail['to'] = this.toEmail
      this.sendEmail['subject'] = this.emailSubject
      this.sendEmail['mailboxAlias'] = this.activeMailbox.name
      this.sendEmail['conversationId'] = this.conversationId
      this.sendEmail['inReplyToId'] = this.inReplyToId
      this.sendEmail['quotedBody'] = this.quotedBody
      var data = this.sendEmail
      console.log(this.sendEmail)
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        this.loader.hide()
        this.$parent.$parent.emailComposeModal = false

        if (response.data.mailbox) {
          this.selectedMailbox = response.data.mailbox[0]
          this.$parent.$parent.selectMailbox(this.$parent.$parent.selectedMailbox, this.conversationId)
        }
        this.$parent.$parent.messageSentSuccess = true
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Cannot send email. Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .write-email-form {
    margin: 20px;
  }
</style>
