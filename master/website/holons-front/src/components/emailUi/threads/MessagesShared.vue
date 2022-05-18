<template>
  <div>
    <div class="message-wrap"
        v-for="message in mailbox.shared.shared_messages"
        v-bind:key="message.id"
    >
      {{ message.from_address }}
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showOpen && message.status != 'archived' && message.status != 'deleted'"
        v-bind:class="{ active: $parent.$parent.selectedMessage.id == message.id }"
      >
        <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showArchived && message.status == 'archived'"
      >
        <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
      <div class="thread-previews__item"
        v-on:click="$parent.$parent.setActiveMessage(message)"
        v-if="$parent.showDeleted && message.status == 'deleted'"
      >
        <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ message.from_address[0] }}</strong></div>
        <div class="thread-previews__item--subject">{{ message.subject }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessagesShared',
  props: [
   'mailbox',
  ],
}
</script>
