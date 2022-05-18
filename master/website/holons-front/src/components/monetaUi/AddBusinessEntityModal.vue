<template>
  <div id="addNewEntityModal" class="hm modal">
    <div class="content">

      <h2 class="title">add new entity</h2>

      <p>Entity represents an org other than your account
      (or <a class="hm link" target="_blank"
      href="https://odyssey.holons.me/meta/value/personal-brands">personal brand</a>).</p>

                <div class="ui input" style="width:100%">
                  <input
                    id="enterEntityName"
                    type="text"
                    name="business_entity_name"
                    placeholder="Enter business entity name"
                    v-model="businessEntityName"
                  />
                </div>

                <br><br><br>

                <div style="width:100%"
                  class="ui basic button"
                  v-on:click.prevent="createBusinessEntity">
                  + create </div>

                <br><br><br>

              <div class="ui grid">
                <div class="twelve wide column">

                  <h5>Use cases & examples</h5>

                    <ul class="hm ul">
                      <li>An entity has its own P&L <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/moneta">@moneta</a></li>
                      <li>It's possible to <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/prudentia-justice/equity">manage equity and profit rule</a></li>
                      <li>An entity might have a public profile at <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/FORA">FORA Public</a>
                      IF at least one owner has Holons Classic or Gold <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/prudentia-justice/identity">account</a></li>
                      <li>It is used in both <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/fairchild-layers/talent">supply</a> and <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/prudentia-justice/relations">demand relations</a> similar to a company name</li>
                      <li>At <a class="hm link" target="_blank"
                      href="https://odyssey.holons.me/nodes/purpose">@purpose</a> an entity
                      has its own space to run seasons (OKR framework implementation)</li>
                    </ul>

                </div>

              </div>

  </div>
</div>

</template>

<script>



export default {
  name: 'BusinessEntityModal',

  props: [ "businessEntity" ],
  data() {
    return {
      loader: null,
      businessEntityName: '',
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol
          url += '//' + document.location.host.replace('8080', '8000')
          url += '/api/moneta/business-entities'
      return url
    }
  },
  mounted() {},
  methods: {
    refreshOnSave: function () {
      this.$parent.getBusinessEntities()
    },
    createBusinessEntity: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var config = {}
      var data = {
        name: this.businessEntityName,
      }
      this.$http.post(this.apiUrl, data, config).then(response => {
        this.$forceUpdate()
        if(response.data){
          this.closeModal()
        }
        this.$nextTick(async () => {
          await this.refreshOnSave()
          this.loader.hide()
        })
      }).catch(error => {
          console.log('Business Entity api is unavailable at the moment')
          console.log(error)
          this.closeModal()
          this.loader.hide()
      });
    },
    closeModal: function () {
      var jQuery = window.$
      jQuery('#addNewEntityModal')
        .removeClass('active')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
