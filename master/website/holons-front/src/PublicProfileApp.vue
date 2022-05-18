<template src="./templates/public-profile.html" />

<script>

import Vue from 'vue'
import wysiwyg from "vue-wysiwyg"
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
  name: 'PublicProfileApp',
  data() {
    return {
      loader: null,
      edit: false,
      username: '',
      handle: '',
      profileBio: '',
      maxLengthError: false, 
    }
  },
  computed: {
    csrfToken: function () {
      return window.csrftoken
    },
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/accounts/'
      return url
    },
    defaultBio: function () {
      return window.profileBio
    }
  },
  watch: {
    profileBio: function (oldVal, newVal) {
      if(newVal.length > 450){
        this.profileBio = oldVal
        this.maxLengthError = true
      } else {
        this.maxLengthError = false
      }
    },
  },
  mounted() {
    console.log('public profile edit')
    this.profileBio = this.defaultBio
  },
  methods: {
    saveProfile() {
      if (this.maxLengthError) { return }
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + 'edit'
      var data = {
        bio: this.profileBio
      }
      this.$http.post(url, data).then(response => {
        console.log(response)
        this.edit = false
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Accounts api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
  }
}
</script>

<style>
</style>
