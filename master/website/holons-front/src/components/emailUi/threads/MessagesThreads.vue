<template>
  <div class="conversations-wrap">
    <div class="conversation"
      v-for="conversation in mailbox.conversations"
      v-bind:key="conversation.id"
    >
      <div
        v-if="$parent.showOpen && conversation[0].status != 'archived' && conversation[0].status != 'deleted'"
        class="message-wrap">
        <div class="thread-previews__item"
          v-on:click="$parent.$parent.setActiveConversation(conversation)"
          v-bind:class="{ active: $parent.selectedConversation == conversation }"
        >
          <div class="thread-previews__item--name"><strong>{{ conversation[0].from_address[0] }}</strong></div>
          <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
        </div>
      </div>
      <div
        v-if="$parent.showDeleted && conversation[0].status == 'deleted'"
        class="message-wrap">
        <div class="thread-previews__item"
          v-on:click="$parent.$parent.setActiveConversation(conversation)"
        >
          <div class="thread-previews__item--name"><strong>{{ conversation[0].from_address[0] }}</strong></div>
          <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
        </div>
      </div>
      <div
        v-if="$parent.showArchived && conversation[0].status == 'archived' &&  conversation[0].status != 'deleted'"
        class="message-wrap">
        <div class="thread-previews__item"
          v-on:click="$parent.$parent.setActiveConversation(conversation)"
        >
          <div class="thread-previews__item--name"><strong>{{ conversation[0].from_address[0] }}</strong></div>
          <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessagesThreads',
  props: [
   'mailbox',
  ],
  methods: {
  },
}
</script>

<style scoped>
.thread-previews__item {
  border-left: 4px solid #ccc;
}
</style>
