<template>
  <div>
    <div class="message-wrap"
        v-for="message in mailbox.messages"
        v-bind:key="message.id"
    >
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showOpen && message.status != 'archived' && message.status != 'deleted'"
        v-bind:class="{ active: $parent.$parent.selectedMessage.id == message.id }"
      >
        <div class="thread-previews__item--name"><strong>{{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showArchived && message.status == 'archived'"
      >
        <div class="thread-previews__item--name"><strong>{{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showDeleted && message.status == 'deleted'"
      >
        <div class="thread-previews__item--name"><strong>{{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Messages',
  props: [
   'mailbox',
  ],
  mounted() {
    console.log('messages')
    console.log(this.mailbox)

  },
  methods: {
  },
}
</script>
