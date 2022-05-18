<template src="./templates/rays-write-new-modal.html"></template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
import AddressBook from '../addressBookComponent/index.vue'

Vue.use(Loading, { zIndex: 9999, })

export default {
  name: 'RaysWriteNewModal',
  components: {
    AddressBook: AddressBook
  },
  data() {
    return {
      loader: null,
      addressSelected: null,
      addressBook: [],
      messageSubject: '',
      messageBody: ''
    }
  },
  mounted() {
    console.log('Rays: write new ray message')
    this.getAddressBook()
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/direct'
      return url
    },
    contactsUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/accounts/address-book'
      return url
    }
  },
  methods: {
    getAddressBook: function () {
      console.log('Get address book')
      const loader = this.$loading.show({zIndex: 30,})
      
      fetch(window.location.origin + '/api/social/address-book')
      .then(res => res.ok && res.json())
      .then(res => {
        if(!res) return

        this.addressBook = res
        this.$forceUpdate()
        loader.hide()
      })
    },
    sendRaysMessage: function () {
      console.log('Send message')
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/send/'
      var data = {
        'to': this.addressSelected,
        'subject': this.messageSubject,
        'message_body': this.messageBody
      }
      this.$http.post(url, data).then(response => {
        this.refreshRays()
        this.loader.hide()
        this.$forceUpdate()
        console.log(response.data)
      }).catch(error => {
        console.log(['Contacts api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    refreshRays: function () {
      var jQuery = window.$
      jQuery('#raysWriteMessageModal')
        .modal('hide')
      this.addressSelected = null
      this.messageSubject = ''
      this.messageBody = ''
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.wrapper {
  padding: 30px;
}
textarea {
  width: 100%;
}
</style>
