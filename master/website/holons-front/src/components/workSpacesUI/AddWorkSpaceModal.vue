<template>
    <div id="addProjectModal" class="hm modal">
      <div class="content">
        <h2 class="title">Add new workspace</h2>

          <div class="ui input" style="width:100%">
              <input
                id="nameNewWorkspaceWillYou"
                type="text"
                name="workspace_name"
                placeholder="Enter workspace name"
                v-model="workspaceName"/>
          </div>

        <br><br><br>

        <div class="actions">
          <!--<div class="ui basic deny button">
            Cancel
          </div>-->
          <div
          style="width:100%"
            class="ui basic button"
            v-on:click.prevent="createWorkspace"
          >
            + CREATE
          </div>

      </div>
    </div>
</template>

<script>



export default {
  name: 'AddWorkSpaceModal',

  props: [
    'tokenValue',
    'parentListId'
  ],
  data() {
    return {
      loader: null,
      workspaceName: '',
      workspaceDescription: '\n',
      apiUrl: 'https://holons.me/boards/api/v1/',
    }
  },
  mounted() {
    // console.log('WorkSpaces modal', this.parentListId)
  },
  methods: {
    refreshOnSave: async function () {
      await this.$parent.getWorkspaces()
      await this.$parent.fetchWorkspaceData()
    },
    createWorkspace: function () {
      const config = {
          headers: {
            Authorization: 'Bearer ' + this.tokenValue,
          }
      };
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl
        url += 'projects'
        delete this.$http.defaults.headers.common['X-CSRFToken']
        var workspaceName = this.workspaceName
        if(this.parentListId !== null && typeof this.parentListId === 'number'){
          workspaceName = this.workspaceName + '__parent_id=' + this.parentListId
        }
        var data = {
          "creation_template": 2,
          "description": this.workspaceDescription,
          "name": workspaceName,
          "is_backlog_activated": true,
          "is_issues_activated": true,
          "is_kanban_activated": true,
          "is_private": true,
          "is_wiki_activated": false,
          "total_milestones": 3,
          "total_story_points": 20.0,
        }
        this.$http.post(url, data, config).then(response => {
        this.$forceUpdate()
        this.$nextTick(async () => {
          await this.refreshOnSave()
          this.loader.hide()
        })
        console.log(response.data)
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
