<template>
    <div class="conversations-wrap-shared"
      v-if="mailbox.shared"
    >
      <div class="conversation"
        v-for="conversation in mailbox.shared.shared_threads"
        v-bind:key="conversation.id"
      >
        <div
          v-if="$parent.showOpen && conversation[0].status != 'archived' && conversation[0].status != 'deleted'"
          class="message-wrap">
          <div class="thread-previews__item"
            v-on:click="$parent.$parent.setActiveConversation(conversation)"
            v-bind:class="{ active: $parent.$parent.selectedConversation == conversation }"
          >
            <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ conversation[0].from_address[0] }}</strong></div>
            <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
          </div>
        </div>
        <div
          v-if="$parent.showDeleted && conversation[0].status == 'deleted'"
          class="message-wrap">
          <div class="thread-previews__item"
            v-on:click="$parent.$parent.setActiveConversation(conversation)"
          >
            <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ conversation[0].from_address[0] }}</strong></div>
            <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
          </div>
        </div>
        <div
          v-if="$parent.showArchived && conversation[0].status == 'archived' &&  conversation[0].status != 'deleted'"
          class="message-wrap">
          <div class="thread-previews__item"
            v-on:click="$parent.$parent.setActiveConversation(conversation)"
          >
            <div class="thread-previews__item--name"><strong><span class="shared">Shared:</span> {{ conversation[0].from_address[0] }}</strong></div>
            <div class="thread-previews__item--subject">{{ conversation[0].subject }}</div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'MessagesThreadShared',
  props: [
   'mailbox',
  ],
  methods: {
  },
}
</script>
