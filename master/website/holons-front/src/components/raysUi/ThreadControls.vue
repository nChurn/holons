<template src="./templates/thread-controls.html" /> 

<script>
export default {
  name: 'ThreadControls',
  data() {
    return {
    }
  },
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
