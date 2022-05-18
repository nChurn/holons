<template>
  <div class="attached-mailboxes">
    <div v-if="mailboxes.active">
        <div class="mailbox-wrap"
          v-for="mailbox in mailboxes.active"
          v-bind:key="mailbox.id"
        >
          <div
            class="email-inboxes__item"
            v-bind:class="{ active: $parent.selectedMailbox.id == mailbox.id}"
          >
              <div
                  class="mailbox__settings okay"
                  v-if="mailbox.status && !mailbox.is_paused && mailbox.is_verified"
                  v-on:click.prevent="$parent.showPauseModal(mailbox)"
              >&nbsp;</div>
              <div
                  class="mailbox__settings"
                  v-on:click.prevent="$parent.showDnsSettingsModal(mailbox)"
                  v-else-if="mailbox.status && !mailbox.is_paused"
              >&nbsp;</div>
              <div
                  class="mailbox__settings paused"
                  v-on:click.prevent="$parent.showPauseModal(mailbox)"
                  v-else-if="mailbox.status && mailbox.is_paused"
              >&nbsp;</div>
              <div
                class="mailbox__settings not_receiving"
                v-on:click.prevent="$parent.showForwardingSettingsModal(mailbox)"
                v-else
              >&nbsp;</div>
              <div class="thread-previews__item--name"
                v-on:click.prevent="$parent.selectMailbox(mailbox)"
                v-bind:id="'mailbox_id_' + mailbox.id"
              >
                <strong>{{ mailbox.alias }}</strong>@{{ mailbox.domain }}
                <span
                  v-if="mailbox.messages_count != 0"
                  class="notifications-count inverted">
                  {{ mailbox.messages_count }}
                </span>

              </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MailboxesAttached',
  props: [
    'mailboxes',
  ],
  data() {
    return {
      //
    }
  },
  mounted() {
    console.log('Mailboxes Attached UI')
  },
  methods: {
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
  .mailbox__settings.okay {
    background: green;
  }
  .mailbox__settings.paused {
    background: teal;
  }
  .mailbox-wrap {
    cursor: pointer;
  }
</style>
