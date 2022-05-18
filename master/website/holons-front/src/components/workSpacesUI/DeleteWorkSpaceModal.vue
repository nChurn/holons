<template>
    <div id="deleteWorkspaceModal" class="ui modal">
      <i class="close icon"></i>
      <div class="header">
        Think twice.
      </div>
      <div class="content">
        <div class="description">
          <div class="ui header">Do you really want to completely destroy this workspace?</div>
        </div>
      </div>
      <div class="actions">
        <div class="ui black deny button">
          Cancel
        </div>
        <div
          class="ui red right labeled icon button"
          v-on:click.prevent="deleteWorkspace"
        >
          Delete this workspace
          <i class="trash icon"></i>
        </div>
      </div>
    </div>
</template>

<script>



export default {
  name: 'DeleteWorkSpaceModal',

  props: [
    'tokenValue',
    'workspaceId'
  ],
  data() {
    return {
      loader: null,
      apiUrl: 'https://holons.me/boards/api/v1/',
    }
  },
  mounted() {
    console.log('Delete WorkSpace modal', this.parentListId)
  },
  methods: {
    refreshOnSave: function () {
      this.$parent.getUsersBoards()
    },
    deleteWorkspace: function () {
      const config = {
          headers: {
            Authorization: 'Bearer ' + this.tokenValue,
          }
      };
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl
        url += 'projects' + '/' + this.workspaceId
        delete this.$http.defaults.headers.common['X-CSRFToken']
        this.$http.delete(url, config).then(response => {
        console.log(response.data)
        window.location.href="/layers"
      }).catch(error => {
          console.log('Boards api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
