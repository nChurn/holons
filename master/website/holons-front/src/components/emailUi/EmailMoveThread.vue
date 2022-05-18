<template>
  <!-- thread moving tools -->
  <div class="ui grid">
    <div class="ui five wide column thread-moving-tools">
      <select
        id="selected-mailbox"
        v-model="selectedMailbox"
      >
        <option
          selected="selected"
          disabled="disabled"
        >
        Select mailbox
        </option>
        <option
          v-for="singleMailbox in availableMailboxes"
          :value="singleMailbox.name"
          :key="singleMailbox.id"
        >{{ singleMailbox.alias }}@{{ singleMailbox.domain }}</option>
      </select>
    </div>
    <div class="ui nine wide column thread-moving-tools">
      <div
        class="thread-control thread-working-area__email__extras move_thread__button"
        v-on:click.prevent="moveThread()"
      >
        Continue using selected mailbox
      </div>
    </div>
  </div>
  <!-- /thread moving tools -->
</template>

<script>
export default {
  name: 'EmailMoveThread',
  props: [
    'message'
  ],
  data() {
    return {
      selectedMailbox: {},
      selectedMessage: {}
    }
  },
  mounted() {
    console.log('Email Move Thread')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/mailboxes'
      return url
    },
    availableMailboxes: function () {
      let filteredMailboxes = this.$parent.$parent.mailboxes.active.map((el) => {
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
  methods: {
    moveThread: function () {
      var data = {}
      var url = this.apiUrl + '/move_thread'
      var loader = this.$parent.$parent.$loading.show()
      data.message_id = this.message.id
      data.mailbox_from = this.$parent.$parent.selectedMailbox.name
      data.mailbox_to = this.selectedMailbox
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        loader.hide()
        // this.selectedMailbox = response.data.mailbox[0]
        // this.$parent.$parent.selectMailbox(this.$parent.$parent.selectedMailbox, this.conversationId)
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Cannot move thread. Mailbox api is unavailable at the moment', error])
        loader.hide()
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
