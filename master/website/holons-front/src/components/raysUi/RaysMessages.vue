<template>

  <div class="thread-previews eight wide column" id="thread-previews" style="overflow-y: scroll;">
  <div
      class="thread-previews__controls"
      v-if="ray.messages"
  >
      <div class="ui secondary menu thread-previews--filters" style="overflow: hidden">
          <a class="item"
            v-bind:class="{'active': showOpen}"
            v-on:click.prevent="activateOpenMessages()"
          >Open</a>
          <a class="item"
            v-bind:class="{'active': showArchived}"
            v-on:click.prevent="activateArchivedMessages()"
          >Bids</a>
          <!-- <a class="item"
            v-bind:class="{'active': showArchived}"
            v-on:click.prevent="activateArchivedMessages()"
          >Archived</a> -->
          <a class="item"
            v-bind:class="{'active': showDeleted}"
            v-on:click.prevent="activateDeletedMessages()"
          >Trash</a>
          <!-- <a class="item"
            v-bind:class="{'active': showSnoozed}"
            v-on:click.prevent="activateSnoozedMessages()"
          >Snoozed</a> -->
        </div>
    </div>
    <div class="mailbox-messages">
      <div
        class="custom-wrap"
        v-if="$parent.isCustom">
        <div class="mailbox-messages">
          <div class="message-wrap"
            v-on:click="addCustomMessage()"
          >
            <div class="thread-previews__item">
              <div class="thread-previews__item--name"><span>+ Add new message</span></div>
            </div>
          </div>
          <div class="message-wrap"
              v-for="message in $parent.selectedFixedRay.messages"
              v-bind:key="message.id"
          >
            <div class="thread-previews__item"
              v-on:click="$parent.selectedMessage = message"
              v-bind:class="{ active: $parent.selectedMessage == message}"
            ><div class="thread-previews__item--name"><span v-html="message.title"></span></div>
          </div>
        </div>
        </div>
      </div>
      <div class="message-wrap"
          v-for="message in ray.messages"
          v-bind:key="message.id"
      >
        <div class="thread-previews__item"
          v-on:click="$parent.selectedMessage = message"
          v-if="showOpen && message.archived == false && message.deleted == false"
          v-bind:class="{ active: $parent.selectedMessage == message}"
        ><div class="thread-previews__item--name"><span v-html="message.title"></span></div>
        </div>
        <div class="thread-previews__item"
          v-on:click="$parent.selectedMessage = message"
          v-if="showArchived && message.archived == true && message.deleted == false"
          v-bind:class="{ active: $parent.selectedMessage == message}"
        ><div class="thread-previews__item--name"><span v-html="message.title"></span></div>
        </div>
        <div class="thread-previews__item"
          v-on:click="$parent.selectedMessage = message"
          v-if="showDeleted && message.deleted == true"
          v-bind:class="{ active: $parent.selectedMessage == message}"
        ><div class="thread-previews__item--name"><span v-html="message.title"></span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'RaysMessages',
  props: [
    'ray',
  ],
  data() {
    return {
      showOpen: true,
      showArchived: false,
      showDeleted: false,
      showSnoozed: false,
      addMessageModal: false,
    }
  },
  mounted() {
    console.log('Rays messages UI')
  },
  methods: {
    refreshRays: function () {
      this.$parent.refreshRays()
    },
    activateOpenMessages: function () {
      console.log('activateOpenMessages')
      this.showOpen = true
      this.showArchived = false
      this.showDeleted = false
      this.showSnoozed = false
    },
    activateArchivedMessages: function () {
      console.log('activateArchivedMessages')
      this.showOpen = false
      this.showArchived = true
      this.showDeleted = false
      this.showSnoozed = false
    },
    activateDeletedMessages: function () {
      console.log('activateDeletedMessages')
      this.showOpen = false
      this.showArchived = false
      this.showDeleted = true
      this.showSnoozed = false
    },
    activateSnoozedMessages: function () {
      console.log('activateSnoozedMessages')
      this.showOpen = false
      this.showArchived = false
      this.showDeleted = false
      this.showSnoozed = true
    },
    addCustomMessage: function () {
      // console.log(this.$parent.selectedFixedRay.short_name)
      this.$parent.addMessageModal = true
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .thread-previews__item.active {
    background: #fff;
  }
  .message-wrap {
    cursor: pointer;
  }
  .modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.3);
    z-index: 9999;
  }
  .settings {
    background: #fff;
    padding: 20px;
    top: 12%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
  .thread-previews__item {
    height: auto !important;
  }
</style>
