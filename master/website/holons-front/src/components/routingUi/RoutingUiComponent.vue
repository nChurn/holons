<template src="./templates/routing-ui.html"></template>

<script>
import Vue from 'vue'
import wysiwyg from 'vue-wysiwyg'
import WrenchMenuComponent from './WrenchMenuComponent'
Vue.use(wysiwyg, {})
Vue.component('wrench-menu', WrenchMenuComponent)
export default {
  name: 'RoutingUiComponent',
  data() {
    return {
      activeScope: 'rays',
      activeMenu: {},
      addNew: false,
      templateName: '',
      templateBody: '',
      templateId: null, 
      cannedRays: [],
    }
  },

  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/routes/'
      return url
    },
  },

  mounted() {
    console.log('Routing UI')
    this.getRayCanned()
  },
  methods: {
    addRayTeplate() {
      this.addNew = true
      this.templateBody = ''
      this.templateName = ''
      this.templateId = null
    },
    addMailTeplate() {
      this.addNew = true
    },
    deleteTemplate(itemId){
      var url = this.apiUrl + 'delete/' + itemId
      this.$http.delete(url).then(response => {
        if(response.data){
          this.templateBody = ''
          this.templateName = ''
          this.templateId = null
          this.getRayCanned()
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays routes templates api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    openEditModal(item) {
        this.addNew = true
        this.templateName = item.title
        this.templateBody = item.body
        this.templateId = item.id
    },
    editTemplate() {
      var url = this.apiUrl + 'update'
      var data = {
        'title': this.templateName,
        'body': this.templateBody,
        'id': this.templateId,
      }
      this.$http.patch(url, data).then(response => {
        if(response.data){
          this.addNew = false
          this.templateBody = ''
          this.templateName = ''
          this.getRayCanned()
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays routes templates api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    createTemplate() {
      this.addNew = false
      var url = this.apiUrl + 'create'
      var data = {
        'title': this.templateName,
        'body': this.templateBody,
      }
      this.$http.post(url, data).then(response => {
        if(response) {
          this.addNew = false
          this.templateBody = ''
          this.templateName = ''
          this.templateId = null
          this.getRayCanned()
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays routes templates api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    cancelCreateTemplate() {
      this.addNew = false
      this.templateBody = ''
      this.templateName = ''
      this.templateId = null
    },
    getRayCanned() {
      var url = this.apiUrl
      this.$http.get(url).then(response => {
        if(response) {
          this.cannedRays = response.data
          this.$forceUpdate()
        }
      }).catch(error => {
        console.log(['Rays routes templates api is unavailable at the moment', error])
        this.loader.hide()
      });
    }
  }
}
</script>
