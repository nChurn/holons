<template src='./templates/mailbox-messages.html' />

<script>
import Vue from 'vue'
import MainTools from './threads/MainTools'
Vue.component('main-tools', MainTools)
import MessagesShared from './threads/MessagesShared'
Vue.component('shared-messages', MessagesShared)
import MessagesThreadShared from './threads/MessagesThreadShared'
Vue.component('shared-messages-thread', MessagesThreadShared)
import Messages from './threads/Messages'
Vue.component('messages', Messages)
import MessagesThreads from './threads/MessagesThreads'
Vue.component('messages-threads', MessagesThreads)

export default {
  name: 'MailboxMessages',
  props: [
    'mailbox',
  ],
  data() {
    return {
      showOpen: true,
      showArchived: false,
      showDeleted: false,
      showSnoozed: false
    }
  },
  mounted() {
    console.log('Mailbox messages UI')
  },
}
</script>

<style scoped>
  .thread-previews__item {
    cursor: pointer;
  }
  .thread-previews__item.active {
    background: #fff;
  }
  .conversations-wrap {
    /* padding-bottom: 1000px; */
  }
  .mailbox-messages {
    padding-bottom: 2000px;
  }
  .thread-previews__item {
    height: auto !important;
  }
  .shared {
    color: red;
  }
</style>
