<template src="./templates/relations-ui.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import OffersComponent from './OffersComponent'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'RelationsUiComponent',

  components: {
    OffersComponent
  },

  props: {
    relationsType: {
      type: String
    },
    activateOffer: {
      type: Object
    }
  },

  data() {
    return {
      relations: []
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/relations'
      return url
    }
  },

  mounted() { },

  methods: {
    getRelations: function () {
      console.log('Get relations')
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(this.apiUrl).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          // await this.refreshOnSave()
          this.relations = response.data.data
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Relations api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  }
}
</script>

<style lang="css">
</style>
