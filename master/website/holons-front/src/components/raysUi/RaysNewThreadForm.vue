<template src="./templates/rays-new-thread-form.html"></template>

<script>
import Vue from 'vue'
import wysiwyg from "vue-wysiwyg";
Vue.use(wysiwyg, {});

export default {
  name: 'RaysNewThreadForm',
  props: ['from', 'to', 'toUsername'],
  data() {
    return {
      messageSubject: '',
      messageBody: '',
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//'
          + document.location.host.replace('8080', '8000')
          url += '/api/rays/direct/'
      return url
    },
  },
  mounted() {},
  methods: {
    sendRaysMessage: function () {
      var url = this.apiUrl + 'message'
      var data = {
        'message_body': this.messageBody,
        'subject': this.messageSubject,
        'from': this.from,
        'to': this.to,
      }
      this.$http.post(url, data).then(response => {
        if(response.data){
          if(typeof(this.loader) != 'undefined'){
            this.loader.hide()
          }
          this.messageSubject = ''
          this.messageBody = ''
          this.$forceUpdate()
          this.$parent.getRays()
          this.$parent.messageSent = true
        }
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (archive message)', error])
        this.loader.hide()
      });
    },
  },
}

</script>
<style scoped>
  h4 {
    margin-top: 3em;
  }
</style>
