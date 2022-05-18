<template src="./templates/wscreator.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import Workspaces from './WorkSpaces'
import RelationsUi from '../relationsUi/RelationsUiComponent'
import ProspectingComponent from '../relationsUi/ProspectingComponent'
import InboundComponent from '../relationsUi/InboundComponent'
import MeetingsComponent from '../relationsUi/MeetingsComponent'
import CommitmentsComponent from '../relationsUi/CommitmentsComponent'
import InvoicesComponent from '../relationsUi/InvoicesComponent'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'WsCreator',

  components: {
    Workspaces,
    RelationsUi,
    ProspectingComponent,
    InboundComponent,
    MeetingsComponent,
    CommitmentsComponent,
    InvoicesComponent,
  },

  props: {
    wsPrefix: String,
    wsTitle: String,
  },

  data() {
    return {
      loader: null,
      apiUrl: 'https://boards.holons.me/api/v1/',
      userMe: null,
      defaultSelected: false,
      pipelinesSelected: true,
      activeProject: [],
      workspacesAvailable: [],
      workspaceName: [],
      workspacesList: [],
      relationsActive: 'Offers',
      menuActive: {
        parentId: 0,
        childId: null,
      },
      menuItems: [
        {
          id: 1,
          name: '<i class="clock outline icon"></i> Inbound',
          prefix: false,
          title: 'inbound',
          disabled: 'disabled',
          menu: 'left',
        },
        {
          id: 2,
          name: '<i class="clock outline icon"></i> Prospecting',
          prefix: false,
          title: 'prospecting',
          disabled: 'disabled',
          menu: 'left',
        },
        {
          id: 3,
          name: 'Offers',
          prefix: false,
          title: 'New offers',
          url: '/offers',
          menu: 'left',
        },
        {
          id: 4,
          name: 'Commitments',
          prefix: false,
          title: 'Create New Commitments',
          url: '/commitments',
          menu: 'left',
        },
        {
          id: 5,
          name: 'Invoices',
          prefix: false,
          title: 'Create new Invoices',
          url: '/invoices',
          menu: 'left',
        },

        {
          id: 6,
          name: '<i class="clock outline icon"></i> Portfolio',
          prefix: '__portfolio',
          title: 'Create New Portflio',
          url: '/portfolio',
          disabled: 'disabled',
          menu: 'right',
        },
        {
          id: 7,
          name: '<i class="clock outline icon"></i> Address book',
          prefix: '__relations',
          title: 'Create New Relations',
          url: '/relations',
          disabled: 'disabled',
          menu: 'right',
        },
        {
          id: 8,
          name: '<i class="square full icon"></i>the why',
          prefix: false,
          title: 'the why',
          url: 'https://odyssey.holons.me/nodes/prudentia-justice/relations',
          menu: 'right',
        },
        /*{
          id: 8,
          name: '<i class="square full icon"></i>the why',
          prefix: '__relations',
          title: 'Create New Relations',
          url: 'https://odyssey.holons.me/nodes/prudentia-justice/relations',
          menu: 'right',
        },*/
      ],
    }
  },
  computed: {
    token: function () {
      let tokenStorage = window.localStorage
      if (tokenStorage.getItem('token')) {
        return tokenStorage.getItem('token').replace(/['"]+/g, '')
      } else {
        return undefined
      }
    },
    authHeaders: function () {
      return { headers: { Authorization: 'Bearer ' + this.token } }
    },
    wsPrefixLive: function () {
        return this.menuItems[this.menuActive.parentId].prefix
    },
    wsTitleLive: function () {
        return this.menuItems[this.menuActive.parentId].title
    },
    // @todo: MAKE it work to hide
    wsIsOpen: function () {
      if (typeof Vue.prototype.wsIsOpen === 'undefined') {
        Vue.prototype.wsIsOpen = false
      }
      return Vue.prototype.wsIsOpen
    },
  },
  mounted() {
    this.getUsersPrefixedBoards()
    window.selectedProjectType = this.wsPrefixLive
    var locationObject = window.location.pathname.split('/')
    if(locationObject[locationObject.length -1] == 'invoices') {
      this.relationsActive = 'invoices'
      this.menuActive.parentId = 5
    }
    if(locationObject[locationObject.length -1] == 'commitments') {
      this.relationsActive = 'commitments'
      this.menuActive.parentId = 4
    }
    // @todo: check if this switch really working
    if(locationObject[locationObject.length -2] == 'offers') {
      this.relationsActive = 'offers'
      this.menuActive.parentId = 2
      if(typeof(locationObject[locationObject.length -1]) !== 'undefined') {
        this.activateOffer = {
          token: locationObject[locationObject.length -1]
        }
      } else {
        this.activateOffer = {
          token: false
        }
      }
    }
    if(locationObject[locationObject.length -1] == 'offers') {
      this.relationsActive = 'offers'
      this.menuActive.parentId = 2
    }
  },
  methods: {
    activateMenuItem: function (item) {
      this.relationsActive = ''
      if(item.disabled === 'disabled'){
        return
      }
      this.menuActive.parentId = item.id
      if (typeof(item.children) !== 'undefined') {
        this.menuActive.childId = item.children[0].id
        // @todo: level2 menu logic to be here
      }

      this.wsPrefix = false
      this.wsPrefix = this.wsPrefixLive
      this.workspacesList = []

      this.getUsersPrefixedBoards()
      this.changeUrl(item.url)
      if(this.wsPrefixLive == '') {
        this.relationsActive = item.url.replace('/', '')
      } else {
        this.relationsActive = ''
      }
      if (item.url == '/offers') {
        this.relationsActive = 'offers'
      }
      if (item.url == '/meetings') {
        this.relationsActive = 'meetings'
      }
      if (item.url == '/commitments') {
        this.relationsActive = 'commitments'
      }
      if (item.url == '/invoices') {
        this.relationsActive = 'invoices'
      }
      this.$forceUpdate()
    },
    // Show create modal
    openCreatePrefixedBoardModal() {
      var jQuery = window.$
      jQuery('#openCreatePrefixedBoardModal')
        .modal('show')
      ;
    },
    // Refresh workspaces
    refreshOnSave: function () {
      this.getUsersPrefixedBoards()
    },
    /*
      Call API, ask for all __prefixed boards accessible to the user
    */
    async getUsersPrefixedBoards() {
      this.userMe = await this.sendRequest('users/me')
      if (!this.token) {
        return undefined
      }
      // get list of all the boards available
      let getWorkspaces = await this.sendRequest('projects?member=' + this.userMe.id)
      // return only wsPrefix boards
      let filteredWorkspaces = getWorkspaces.map((currentValue) => {
        if (currentValue && currentValue.name.indexOf(this.wsPrefixLive) > 0) {
            currentValue.name = currentValue.name.replace(this.wsPrefixLive, '')
            return currentValue
        } else {
            return false
        }
      });
      this.workspacesList = []
      this.workspacesList = filteredWorkspaces
      this.$forceUpdate()
    },
    /*
      Call API, create a new board with title ending with wsPrefix
    */
    createPrefixedWorkspace: function () {
      const config = {
          headers: {
            Authorization: 'Bearer ' + this.token,
          }
      };
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl
        url += 'projects'
        delete this.$http.defaults.headers.common['X-CSRFToken']
        var data = {
          "creation_template": 2,
          "description": ' ',
          "name": this.workspaceName + this.wsPrefix,
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
          this.refreshOnSave()
          console.log(response.data)
        }).catch(error => {
          console.log('Workspaces/Boards api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
    async sendRequest(url = 'get') {
      delete this.$http.defaults.headers.common['X-CSRFToken'] // remove CSRF in order to access API by a separate API token
      let prop

      await this.$http.get(this.apiUrl + url, this.authHeaders)
        .then((response) => {
          prop = response.data
        })
        .catch(error => this.handleError(error, url))
      return prop
    },
    changeUrl(urlPart) {
      const url = location.origin + '/relations'  + urlPart
      window.history.replaceState({}, '', url)
    },
  },
}
</script>

<style lang="css">
.ui.input>input {
  font-weight: inherit;
}
.ws-actions {
  overflow: hidden;
}
</style>
