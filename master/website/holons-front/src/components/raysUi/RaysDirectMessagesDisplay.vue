<template src="./templates/rays-direct-messages-display.html" />

<script>

import Vue from 'vue'
import wysiwyg from "vue-wysiwyg";
Vue.use(wysiwyg, {});

export default {
  name: 'RaysDirectMessagesDisplay',
  props: [
    'mThread',
  ],
  data() {
    return {
      users: [],
      selectedUser: null,
      ownerUser: null,
      userFrom: '',
      userTo: '',
      messageBody: '',
      messageReplyToId: null
    }
  },
  watch: {
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//'
          + document.location.host.replace('8080', '8000')
          url += '/api/rays/direct/'
      return url
    },
    myHandle: function () {
      return window.handle
    },
  },
  mounted() {
    console.log('Rays Direct Messages Display UI')
  },
  methods: {
    messageDelete: function () {
      var url = this.$parent.apiUrl + '/thread/' + this.mThread.id + '/delete'
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.delete(url).then(response => {
        if(response.data){
          this.$parent.selectedMessage = null
          this.message = null
          this.$parent.getRays()
          if(typeof(this.loader) != 'undefined'){
            this.loader.hide()
          }
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (delete message)', error])
        this.loader.hide()
      });
    },
    messageArchive: function () {
      var url = this.$parent.apiUrl + '/thread/' + this.mThread.id + '/archive'
      this.$http.patch(url).then(response => {
        if(response.data){
          this.$parent.selectedMessage = null
          this.$parent.getRays()
          if(typeof(this.loader) != 'undefined'){
            this.loader.hide()
          }
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (archive message)', error])
        this.loader.hide()
      });
    },
    sendRaysMessage: function () {
      if(this.messageReplyToId === null){
        var replyId = this.mThread.messages[this.mThread.messages.length -1].id
        this.messageReplyToId = replyId
      }
      var url = this.apiUrl + 'message'
      var data = {
        'message_body': this.messageBody,
        'reply_to_id': this.messageReplyToId,
      }
      var message = {
        body: this.messageBody,
        id:0,
        is_archived:false,
        is_deleted:false,
        provider:"holons",
        pub_date:"just now",
        subject:this.mThread.messages[0].subject,
      }
      this.mThread.messages.push(message)
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        // this.$parent.selectedMessage = null
        // this.$parent.getRays()
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (archive message)', error])
        this.loader.hide()
      });
    },
    messageReplyModalOpen: function (messageId) {
      this.messageReplyToId = messageId
      var jQuery = window.$
      jQuery('#raysWriteReplyMessageBlock').show()
    },
    openRaysProfile: function () {
      var jQuery = window.$
      jQuery('#raysProfileModal').show()
    },
    closeRaysProfile: function () {
      var jQuery = window.$
      jQuery('#raysProfileModal').hide()
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .reply-button {
    cursor: pointer;
  }
  .wrapper {
    padding: 30px;
  }
  textarea {
    width: 100%;
  }
  .thread-working-area__email__extras a {
    color: #000;
  }
  .thread-working-area__email__extras:hover a {
    color: #fff;
  }
</style>
