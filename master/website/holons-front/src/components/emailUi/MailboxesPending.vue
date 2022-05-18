<template>
  <div class="attached-mailboxes">
    <div class="email-inboxes__item"
          v-for="mailbox in mailboxes.pending"
          v-bind:key="mailbox.id"
        >
          <div
            class="mailbox__settings not_receiving"
            v-on:click.prevent="$parent.showForwardingSettingsModal(mailbox)"
          >
              &nbsp;
          </div>
          <div class="thread-previews__item--name">
            <strong>{{ mailbox.alias }}</strong>
            @{{ mailbox.domain }}
          </div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'MailboxesPending',
  props: [ 
    'mailboxes',
  ],
  data() {
    return {
      mailboxesValidityStatus: {}
      //
    }
  },
  mounted() {
    console.log('Mailboxes Pending UI')
    // this.$parent.getMailboxes()
  },
  methods: {
    // 
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .mailbox__settings {
    display: block;
    position: absolute;
    top: 19px;
    left: 0;
    border-radius: 50%;
    width: 10px;
    height: 10px;
    background: #FFCF4A;
    cursor: pointer;
  }
  .mailbox__settings.not_receiving {
    background: red;
  }
</style>