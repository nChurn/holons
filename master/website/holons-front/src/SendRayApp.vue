<template src="./templates/send-ray-app.html" />

<script>

import Vue from 'vue'
import wysiwyg from "vue-wysiwyg";
Vue.use(wysiwyg, {
    hideModules: {
      "image": true,
      "code": true,
      "table": true,
      "headings": true,
      "removeFormat": true,
      "separator": true,
    },
});

export default {
  name: 'SendRayApp',
  data() {
    return {
      loader: null,
      message: '',
      messageSent: false,
      showLogin: false,
      codeInputActive: false,
      regCodeInputActive: false,
      confirmationCode: '',
      regConfirmationCode: '',
      regPhoneNumber: '',
      regName: '',
      newCsrf: ''
    }
  },
  computed: {
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/routes/reply'
      return url
    },
    itemTitle: function () { return window.itemTitle },
    itemBody: function () { return this.htmlDecode(window.itemBody) },
    itemId: function () { return window.itemId },
    userIsLoggedin: function () { return (window.user_is_anonymous === 'False') },
  },
  mounted() {
    console.log('send ray app')
  },
  methods: {
    postNewMessage() {
      if(this.newCsrf != ''){
        this.$http.defaults.headers.common['X-CSRFToken'] = this.newCsrf
      }
      var url = this.apiUrl
      var data = {
        'id': this.itemId,
        'message': this.message,
      }
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        this.messageSent = true
        window.location.href = "/subscribe/ok"
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays routes templates api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    getConfirmationCode: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/login'
        var data = {'phone_number': this.phoneNumber}
        this.$http.post(url, data).then(response => {
        this.searchResults = response.data
        this.loader.hide()
        this.codeInputActive = true
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    confirmAccount: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/confirmation'
        var data = {
          'phone_number': this.phoneNumber,
          'confirmation_code': this.confirmationCode
        }
        this.$http.post(url, data).then(response => {
          this.loader.hide()
          var tokenStorage
          var wsUserMeta = response.data['workspaces_user_meta']
          tokenStorage = window.localStorage
          tokenStorage.setItem('token', '"' + wsUserMeta['auth_token'] + '"')
          tokenStorage.setItem('userInfo', JSON.stringify(wsUserMeta))

          this.invitationActive = true
          this.codeInputActive = false
          this.storeTeleportToken(response.data['teleport_user_meta'])
          this.newCsrf = response.data['csrf_token']
          this.postNewMessage()
          //document.location.href="/?" + document.location.href.split('?')[1]
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    storeTeleportToken: function (teleportData) {
      // set localStorage items
      var tokenStorage
      tokenStorage = window.localStorage;
      tokenStorage.setItem('mx_access_token', teleportData.access_token);
      tokenStorage.setItem('mx_user_id', teleportData.user_id);
      tokenStorage.setItem('mx_crypto_initialised', 'false');
      tokenStorage.setItem('mx_device_id', teleportData.device_id);
      tokenStorage.setItem('mx_hs_url', 'https://' + teleportData.home_server);
      tokenStorage.setItem('mx_is_guest', 'false');
      tokenStorage.setItem('mx_is_url', 'https://' + teleportData.home_server);
      tokenStorage.setItem('mxjssdk_memory_filter_FILTER_SYNC_' + teleportData.user_id, '0');
      console.log(teleportData)
      return
    },
    // utility function to convert encoded html to a renderable html
    htmlDecode: function (input){
      var doc = new DOMParser().parseFromString(input, "text/html");
      return doc.documentElement.textContent;
    }
  }
}
</script>

<style>
</style>

