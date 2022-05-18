<template src='./templates/email-thread-display.html'/>

<script>

import Vue from 'vue'

import VueLuxon from "vue-luxon"
Vue.use(VueLuxon)

import EmailForm from './EmailForm'
import EmailMoveThread from './EmailMoveThread'
Vue.component('email-form', EmailForm)
Vue.component('email-move-thread', EmailMoveThread)

export default {
  name: 'EmailThreadDisplay',
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
      for (var message in this.conversation){
        var url = this.$parent.apiUrl + 'message/' + this.conversation[message].id
        // this.loader = this.$loading.show({zIndex: 30,})
        this.$http.delete(url).then(response => {
          console.log(response.data)
        }).catch(error => {
          console.log(['Rays api is unavailable at the moment (delete message)', error])
          this.loader.hide()
        });
          this.$parent.selectMailbox(this.$parent.selectedMailbox)
      }
    },
    messageArchive: function () {
      console.log('Archive message')
      for (var message in this.conversation){
        var url = this.$parent.apiUrl + 'message/' + this.conversation[message].id
        this.$http.patch(url).then(response => {
          console.log(response.data)
          this.$parent.selectedMessage = null
        }).catch(error => {
          console.log(['Rays api is unavailable at the moment (archive message)', error])
          this.loader.hide()
        });
      }
      if(typeof(this.loader) != 'undefined'){
        this.loader.hide()
      }
      this.$parent.selectMailbox(this.$parent.selectedMailbox)
    },
    showReplyForm: function(message) {
      this.showEmailForm = true
      this.inReplyToId = message.id
      this.quotedBody = message.html
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #email-thread-content {
    top: 0;
    bottom: 0;
    overflow-y: scroll;
    overflow-x: hidden;
    min-height: 100px;
    max-height: 800px;
    height: 100%;
  }
  blockquote,
  .gmail_quote {
    display: none !important;
  }
  .thread-working-area__email {
    margin-bottom: 16px;
  }
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
