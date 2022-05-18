<template src="./templates/commitments-tr.html"></template>

<script>
import CommitmentsMainWrenchMenu from './CommitmentsMainWrenchMenu'

export default {
  name: 'CommitmentsTr',

  components: {
    CommitmentsMainWrenchMenu,
  },
  props: ['item', 'showMenu'],
  methods: {
    createInvoice: function () {
      this.$emit('show-create-invoice-modal', this.item)
    },
  }

}
</script>
