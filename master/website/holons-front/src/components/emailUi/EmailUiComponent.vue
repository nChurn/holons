<template src="./templates/email-ui.html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'

import EmailComposeModal from './EmailComposeModal'
import MailboxesAttached from './MailboxesAttached'
import MailboxesPending from './MailboxesPending'
import MailboxMessages from './MailboxMessages'
import MailboxAdd from './MailboxAdd'
import MailboxImport from './MailboxImport'
import EmailDisplay from './EmailDisplay'
import EmailThreadDisplay from './EmailThreadDisplay'
import EmailSettings from './EmailSettings'
import EmailPauseMailboxModal from './EmailPauseMailboxModal'

Vue.component('email-compose-modal', EmailComposeModal)
Vue.component('mailboxes-attached', MailboxesAttached)
Vue.component('mailboxes-pending', MailboxesPending)
Vue.component('mailbox-messages', MailboxMessages)
Vue.component('mailbox-add', MailboxAdd)
Vue.component('mailbox-import', MailboxImport)
Vue.component('email-settings', EmailSettings)
Vue.component('email-pause-mailbox-modal', EmailPauseMailboxModal)
Vue.component('email-display', EmailDisplay)
Vue.component('email-thread-display', EmailThreadDisplay)

Vue.use(Loading, { zIndex: 9999, })

export default {
  name: 'EmailUiComponent',
  data() {
    return {
      loader: null,
      mailboxes: {
        active: [],
        pending: []
      },
      sendEmail: {
        from: '',
        to: '',
        message: ''
      },
      createMailbox: false,
      incomingEmail: '',
      mailboxesValidityStatus: {},
      selectedMailbox: {},
      selectedMessageKey: 0,
      selectedMessage: { id: 0 },
      unreadMessages: null,
      unreadMessagesCount: null,
      selectedConversation: null,
      emailModal: false,
      emailImportModal: false,
      emailSettingsModal: false,
      emailComposeModal: false,
      emailPauseMailboxModal: false,
      showDnsSettings: false,
      showForwardingSettings: false,
      showFrontAppSettings: false,
      searchString: '',
      searchActive: false,
      messageSentSuccess: false,
    }
  },
  mounted() {
    console.log('Email UI')
    this.getAllUnreadMessages()
    this.getMailboxesList()
    this.setAccordion()
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/mailboxes/'
      return url
    }
  },
  watch: {
    selectedMailbox: function(newValue) {
      console.log('selectedMailbox')
      for (var i in newValue.messages) {
        if(newValue.messages[i].status == null){
          this.selectedMessage = newValue.messages[i]
          break
        }
      }
    },
  },
  methods: {
    setAccordion: function () {
      var jQuery = window.$
      jQuery('.ui.accordion')
        .accordion()
    },
    getAllUnreadMessages: function () {
      var url = this.apiUrl + 'user_get_all_unread_messages'
      console.log('getAllUnreadMessages')
      this.$http.get(url).then(response => {
        // this.mailboxes = response.data.mailboxes
        this.unreadMessages = response.data.messages
        this.unreadMessagesCount = response.data.messages_count
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment (getAllUnreadMessages)', error])
        this.loader.hide()
      });
    },
    getMailboxesList: function (selectedMailboxHashname) {
      /*
        Get only mailboxes, without messages
      */
      console.log('getMailboxesList')
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + 'user_mailboxes_list'
      if(this.searchString != ''){
        url += '?search_string=' + this.searchString
      }
      this.$http.get(url).then(response => {
        this.mailboxes = response.data.mailboxes
        if(selectedMailboxHashname != ''){
          for (var i in this.mailboxes.active) {
            if (this.mailboxes.active[i].name == selectedMailboxHashname) {
              this.selectedMailbox = this.mailboxes.active[i]
              this.emailModal = false
              this.$forceUpdate()
            }
          }
        }
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Mailbox api is unavailable at the moment (getMailboxesList)', error])
        this.loader.hide()
      });
    },
    openEmailModal: function () {
      this.emailModal = true
      this.showDnsSettings = false
      this.showForwardingSettings = false
      this.showFrontAppSettings = false
    },
    openEmailImportModal: function () {
      this.emailImportModal = true
      this.showFrontAppSettings = true
      this.showForwardingSettings = false
      this.showDnsSettings = false
      this.showForwardingSettings = false
    },
    openEmailSettingsModal: function () {
      this.emailSettingsModal = true
      this.showDnsSettings = false
      this.showForwardingSettings = false
    },
    showPauseModal: function (mailbox) {
      this.emailPauseMailboxModal = true
      this.selectedMailbox = mailbox
    },
    sendEmailRequest: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to create a random mailbox for us
      var url = this.apiUrl + 'send_email'
      var data = this.sendEmail
      console.log(this.sendEmail)
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Cannot send email. Mailbox api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    showForwardingSettingsModal: function (mailbox) {
      console.log('Show forwarding settings')
      this.emailModal = true
      this.selectedMailbox = mailbox
      this.showDnsSettings = false
      this.showForwardingSettings = true
      this.showFrontAppSettings = false
    },
    showDnsSettingsModal: function (mailbox) {
      console.log('Show DNS settings')
      this.emailModal = true
      this.selectedMailbox = mailbox
      this.showDnsSettings = true
      this.showForwardingSettings = false
      this.showFrontAppSettings = false
    },
    selectFolder: function (folderType) {
      if (folderType == 'all-unread') {
        this.selectedMailbox = {
          alias: "all new folder",
          conversations: {},
          dns: {},
          domain: 'global',
          id: '',
          incoming_email: '',
          messages: this.unreadMessages,
          messages_count: this.unreadMessagesCount,
          name: '',
          status: '',
          shared: {
            shared_messages: [],
            shared_threads: [],
          },
        }

      }
    },
    selectMailbox: function (mailbox, conversation = '') {
      console.log('Mailbox selected:')
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + 'user_get_mailbox_messages'
      if(this.searchString != ''){
        url += '?search_string=' + this.searchString
      }
      var data = { 'mailbox_name': mailbox.name }
      // I know we should use GET here, but backend needs POST
      this.$http.post(url, data).then(response => {
        console.log('Messages loaded:')
        console.log(response.data)
        this.selectedMailbox = response.data.mailbox[0]
        this.loader.hide()
        if (conversation != '') {
          console.log('Conversation loaded:')
          var activeConversation = this.selectedMailbox.conversations[conversation]
          this.setActiveConversation(activeConversation)
        } else {
          console.log('Set default conversation')
          var status
          if(this.$refs.mailboxMessages.showOpen){ status = null }
          if(this.$refs.mailboxMessages.showArchived){ status = 'archived' }
          if(this.$refs.mailboxMessages.showDeleted){ status = 'deleted' }

          var conversations = this.selectedMailbox.conversations

          for(var c in conversations){
            var currentConversation = conversations[c]
            for(var m in currentConversation){
              if (status == currentConversation[m].status) {
                console.log('status: ' + currentConversation[m].status + ' : ' + status + ' :  ' + currentConversation[m].from_address + ' ' + currentConversation[m].subject)
                this.setActiveConversation(currentConversation)
                return
              }
            }
          }
        }
        this.$forceUpdate()
      })
    },
    setActiveMessageByKey: function (messageId) {
      this.messageSentSuccess = false
      this.$refs.showsinglemessage.showEmailForm = false
      this.selectedConversation = null
      for(var m in this.selectedMailbox.messages){
        if(this.selectedMailbox.messages[m].id == messageId){
          this.selectedMessage = this.selectedMailbox.messages[m]
          break
        }
      }
      // this.selectedMessage = message
      this.$forceUpdate()
    },
    setActiveMessage: function (message) {
      this.messageSentSuccess = false
      this.$refs.showsinglemessage.showEmailForm = false
      this.selectedConversation = null
      this.selectedMessage = message
      this.$forceUpdate()
    },
    setActiveConversation: function (conversation) {
      this.messageSentSuccess = false
      this.selectedConversation = conversation
      // this.$refs.showthreads.showEmailForm = false
      this.selectedMessage = false
      this.$forceUpdate()
    },
    setActiveMailbox: function(mailboxHash) {
      console.log('Set active mailbox')
      console.log(this.selectedMailbox)
      this.selectedMailbox = {}
      for (var i in this.mailboxes.active) {
        if (this.mailboxes.active[i].name == mailboxHash) {
          this.selectedMailbox = this.mailboxes.active[i]
          console.log(this.selectedMailbox)
          this.$refs.mailboxMessagesComponent.childComponent.hideComponent()
          this.$refs.mailboxMessagesComponent.childComponent.showComponent()
          this.emailModal = false
          this.$forceUpdate()
        }
      }
      this.$forceUpdate()
    },
    startSearch: function () {
      console.log('Searching: ' + this.searchString)
      this.getMailboxesList()
    },
    getMailboxByAlias: function (mailboxHash) {
      for (var i in this.mailboxes.active) {
        if (this.mailboxes.active[i].name == mailboxHash) {
          console.log(this.mailboxes.active[i])
          return this.mailboxes.active[i]
        }
      }
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #parent {
    overflow: auto !important;
  }
  .email {
    font-family: sans-serif;
  }
  #email-inboxes {
    padding-bottom: 3000px;
  }
  .email-inboxes__item {
    cursor: pointer;
  }
  input.thread-control {
    cursor: pointer;
    margin-left: 7px;
  }
</style>
