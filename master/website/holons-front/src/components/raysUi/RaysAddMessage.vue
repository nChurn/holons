<template>
    <div
      class="mailbox-add modal"
      >
      <div class="settings">
        <h1>New message</h1>
        <div class="form ui">
<!--           <div class="form-row">
            <div class="field">
              <select v-model="selectedRay">
                <label>Ray: </label><br />
                <option
                  v-for="item in raysList"
                  v-bind:key="item"
                  v-bind:value="item"
                >
                 {{ item }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-row">
            &nbsp;<br /><br />
          </div>
 -->
          <div class="form-row">
            <label for="source-url">Title: </label><br />
            <div class="input fluid ui">
              <input
                type="text"
                name="short-name"
                v-model="messageTitle"
                class="ui input fluid"
              />
            </div>
          </div>
          <div class="form-row">
            &nbsp;<br /><br />
          </div>
          <div class="form-row">
            <label for="source-url">Description: </label><br />
            <div class="field ui">
              <textarea class="input fluid ui" v-model="messageDescription" id="" cols="30" rows="10"></textarea>
            </div>
          </div>
          <div class="form-row">
            &nbsp;<br /><br />
          </div>
          <div class="form-row ui field input">
            <button
              v-on:click.prevent="saveMessage(ray)"
              class="button ui"
            >
              Save
            </button>
            <button
              v-on:click.prevent="closeModal()"
              class="button ui"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
  name: 'RaysAddMessage',
  data() {
    return {
      selectedRay: '',
      raysList: [
        'Mercury',
        'Odysseus',
        'Athena',
        'Talant',
        'Moneta',
        'Fora',
        '@grintender'
      ],
      messageTitle: '',
      messageDescription: '',
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/'
      return url
    }
  },
  mounted() {
    this.selectedRay = this.$parent.selectedFixedRay.short_name
    console.log('Rays add message UI')
  },
  methods: {
    saveMessage: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl += 'message/add'
      var data = {}
      data.title = this.messageTitle
      data.description = this.messageDescription
      data.ray_source = this.$parent.selectedFixedRay.short_name

      this.$http.post(url, data).then(() => {
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment', error])
        this.loader.hide()
      });
      this.$parent.addMessageModal = false
    },
    closeModal: function () {
      this.$parent.addMessageModal = false
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.3);
    z-index: 9999;
  }
  .settings {
    background: #fff;
    padding: 20px;
    top: 12%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
</style>
