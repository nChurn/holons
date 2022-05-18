<template>
  <div id="thread-previews__controls">
      <div class="ui secondary menu thread-previews--filters" style="overflow: hidden">
          <a class="item"
            v-bind:class="{'active': $parent.showOpen}"
            v-on:click.prevent="activateOpenMessages()"
          >Open</a>
          <a class="item"
            v-bind:class="{'active': $parent.showArchived}"
            v-on:click.prevent="activateArchivedMessages()"
          >Archived</a>
          <a class="item"
            v-bind:class="{'active': $parent.showDeleted}"
            v-on:click.prevent="activateDeletedMessages()"
          >Trash</a>
          <a class="item"
            v-bind:class="{'active': $parent.showSnoozed}"
            v-on:click.prevent="activateSnoozedMessages()"
          >Snoozed</a>
      </div>
  </div>
</template>

<script>
export default {
  name: 'MainTools',
  methods: {
    activateOpenMessages: function () {
      this.$parent.showOpen = true
      this.$parent.showArchived = false
      this.$parent.showDeleted = false
      this.$parent.showSnoozed = false
    },
    activateArchivedMessages: function () {
      this.$parent.showOpen = false
      this.$parent.showArchived = true
      this.$parent.showDeleted = false
      this.$parent.showSnoozed = false
    },
    activateDeletedMessages: function () {
      this.$parent.showOpen = false
      this.$parent.showArchived = false
      this.$parent.showDeleted = true
      this.$parent.showSnoozed = false
    },
    activateSnoozedMessages: function () {
      this.$parent.showOpen = false
      this.$parent.showArchived = false
      this.$parent.showDeleted = false
      this.$parent.showSnoozed = true
    },
  }
}
</script>
