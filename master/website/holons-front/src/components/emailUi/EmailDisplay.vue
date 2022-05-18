<template src="./templates/email-display.html" />

<script>

import Vue from 'vue'
import VueLuxon from "vue-luxon"
Vue.use(VueLuxon)
import EmailForm from './EmailForm'
import EmailMoveThread from './EmailMoveThread'
Vue.component('email-form', EmailForm)
Vue.component('email-move-thread', EmailMoveThread)

export default {
  name: 'EmailDisplay',
  props: [
    'message',
    'conversation'
  ],
  data() {
    return {
      users: [],
      selectedUser: null,
      ownerUser: null,
      showEmailForm: false
    }
  },
  computed: {
    emailSubject: function() {
      var messageSubject = ''
      if (this.message) {
        messageSubject = this.message.subject
      }
      for (var messageId in this.conversation) {
        var message = this.conversation[messageId]
        messageSubject = message.subject
      }
      return ('Re: ' + messageSubject)
    },
    fromEmail: function() {
      return (this.$parent.selectedMailbox.alias + '@' + this.$parent.selectedMailbox.domain)
    },
    toEmail: function() {
      var toAddress = 'to@address'
      if (this.message) {
        toAddress = this.message.to_address
      }
      for (var messageId in this.conversation) {
        var message = this.conversation[messageId]
        if (
            message.from_address[0] != this.$parent.selectedMailbox.alias + '@' + this.$parent.selectedMailbox.domain
            ) {
          toAddress = message.from_address[0]
        } else {
          toAddress =  message.to_address[0]
        }
      }
      return toAddress
    },
    isPaused: function () {
      return this.$parent.selectedMailbox.is_paused
    },
    availableMailboxes: function () {
      let filteredMailboxes = this.$parent.mailboxes.active.map((el) => {
        if (el && !el.is_paused) {
            return el
        } else {
            return false
        }
      }).filter(function (el) {
        return el != false;
      });
      return filteredMailboxes
    }
  },
  watch: {
    message: function() {
      this.selectedUser = null
      this.ownerUser = null
      // this.getUsers()
    },
    conversation: function(){
      console.log(this.conversation[0])
    }
  },
  mounted() {
    console.log('Email Display UI')
  },
  methods: {
    getUsers() {
      var url = this.$parent.apiUrl + 'users'
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(url).then(response => {
        console.log(response.data)
        this.users = response.data.users
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error =>{
        console.log(['Mail api is unavailable at the moment (users)', error])
        this.loader.hide()
      });
    },
    setUsers() {
      var url = this.$parent.apiUrl + 'users'
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.post(url).then(response => {
        this.ownerUser = response.data.owner_user
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error =>{
        console.log(['Mail api is unavailable at the moment (assign user)', error])
        this.loader.hide()
      });
    },
    messageDelete: function () {
      console.log('Delete message')
      var status
      if(this.$parent.$refs.mailboxMessages.showOpen){ status = null }
      if(this.$parent.$refs.mailboxMessages.showArchived){ status = 'archived' }
      if(this.$parent.$refs.mailboxMessages.showDeleted){ status = 'deleted' }

      this.$parent.selectedMessage.status = 'deleted'

      let statusMessages = this.$parent.selectedMailbox.messages.map((el) => {
        if (el.id === this.message.id) {
            return el
        }
        if (el && (el.status === status || el.id !== this.message.id)) {
            return el
        } else {
            return false
        }
      }).filter(function (el) {
        return el != false;
      });


      var url = this.$parent.apiUrl + 'message/' + this.message.id
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.delete(url).then(response => {
        console.log(response.data)
        this.$parent.selectedMessage = null
        for(var m in statusMessages){
          if(statusMessages[m].id == this.message.id){
            this.$parent.selectedMessageKey = statusMessages[m].id
            this.$parent.setActiveMessageByKey(statusMessages[m].id)
            break
          }
        }
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (delete message)', error])
        this.loader.hide()
      });
    },
    messageArchive: function () {
      console.log('Archive message')
      var status
      if(this.$parent.$refs.mailboxMessages.showOpen){ status = null }
      if(this.$parent.$refs.mailboxMessages.showArchived){ status = 'archived' }
      if(this.$parent.$refs.mailboxMessages.showDeleted){ status = 'deleted' }

      this.$parent.selectedMessage.status = 'archived'

      let statusMessages = this.$parent.selectedMailbox.messages.map((el) => {
        if (el.id === this.message.id) {
            return el
        }
        if (el && (el.status === status || el.id !== this.message.id)) {
            return el
        } else {
            return false
        }
      }).filter(function (el) {
        return el != false;
      });

      var stopWord = false
      for(var m in statusMessages){
        if(stopWord){
          this.$parent.selectedMessage = statusMessages[m]
          this.$parent.selectedMessageKey = statusMessages[m].id
          break
        }
        if(statusMessages[m].id == this.message.id){
          stopWord = true
        }
      }
      var url = this.$parent.apiUrl + 'message/' + this.message.id
      this.$http.patch(url).then(response => {
        console.log(response.data)
        this.$parent.selectedMessage = null
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (archive message)', error])
        this.loader.hide()
      });
    },
    showReplyForm: function(message) {
      this.showEmailForm = true
      this.inReplyToId = message.id
      this.quotedBody = message.html
    }
  }
}
</script>

<style scoped>
  .thread-working-area__email--pic {
    width: 40px;
    height: 40px;
    border: 2px solid #ccc;
    background: #eee;
  }
  .move_thread__button {
    position: relative !important;
  }
</style>
