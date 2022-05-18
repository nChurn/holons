<template src="./templates/workspaces.html" lang="html"></template>

<script>
import Vue from 'vue'
import * as queryString from 'query-string';
import Loading from 'vue-loading-overlay'
import draggable from 'vuedraggable'
import 'vue-loading-overlay/dist/vue-loading.css'
import AddWorkSpaceButton from './AddWorkSpaceButton'
import AddWorkSpaceModal from './AddWorkSpaceModal'
import DeleteWorkSpaceModal from './DeleteWorkSpaceModal'
import CardModal from './CardModal'
import UserBlock from './userBlock'
import QuickLinks from './quickLinks'
import DropDownContainer from '../App/dropDownContainer'
import CfModal from './cfModal'

Vue.use(Loading, {
  zIndex: 9999,
})

export default {
  name: 'WorkSpaces',

  components: {
    draggable,
    AddWorkSpaceButton,
    AddWorkSpaceModal,
    DeleteWorkSpaceModal,
    CardModal,
    UserBlock,
    QuickLinks,
    DropDownContainer,
    CfModal
  },

  props: {
    selectedId: {
      type: Number,
      required: false
    }
  },

  data() {
    return {
      loader: null,
      workspacesLoaded: false,
      columnsLoaded: false,
      apiUrl: 'https://boards.holons.me/api/v1/',
      layouts: [
        'kanban',
        'vertical',
        'table'
      ],
      kanbanVertical: false,
      kanbanTable: false,
      workspacesAvailable: [],
      activeProject: null,
      activeProjectColumns: [],
      activeProjectArchive: [],
      workspaceTasks: [],
      dragColumn: false,
      dragRow: false,
      newColumn: false,
      newRow: false,
      reColumn: false,
      newColumnName: '',
      newRowName: '',
      newRowColumnId: NaN,
      cardToOpen: null,
      draggedElement: null,
      rowsOrdering: false,
      cardUpdating: false,
      rowsOrderTimeout: null,
      updateCardTimeout: null,
      archivedColId: null,
      usersList: [],
      userMe: null,
      currentTasks: null,
      timeline: null,
      cardKey: 0,
      showCardOptions: '',
      inviteModal: false,
      parentProjects: [],
      showProjDetails: false,
      parentListId: null,
      breadCrumbs: [],
      nestedUrlId: '__parent_id=',
      inviteMail: '',
      inviteRole: 0,
      inviteLink: '',
      inviteError: false,
      linkCopied: false,
      projectsRoles: [],
      customFields: {
        task: [],
        userstory: []
      },
      cardDisplayCF:{},
      fieldsToDisplay: {},
      displayFieldsMap: new Map()
    }
  },
  computed: {
    token: function() {
      let tokenStorage = window.localStorage
      if (tokenStorage.getItem('token')) {
        return tokenStorage.getItem('token').replace(/['"]+/g, '')
      } else {
        return undefined
      }
    },
    authHeaders: function() {
      return {headers: {Authorization: 'Bearer ' + this.token}}
    },
    holonsApiUrl: function() {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
      return url
    },
    selectedProjectType: function() {
      return window.selectedProjectType
    },
  },
  async created() {
    // get logged in user info so that we could filter projects by member-id
    this.userMe = await this.sendRequest('users/me')
    await this.checkInvite()
    await this.getWorkspaces()
    if (this.workspacesAvailable.length) {
      await this.readParams()
    }
    this.workspacesLoaded = true
    console.log('WorkSpaces loaded')
  },
  methods: {
    /*
      Call API, ask for all boards accessible to the user
    */
    async getWorkspaces() {
      if (!this.token) {
        return undefined
      }
      // get list of all the boards available
      let getProjects = await this.sendRequest('projects?member=' + this.userMe.id)
      if (this.selectedProjectType) {
        getProjects = getProjects.map((currentValue) => {
          if (currentValue && currentValue.name.indexOf(this.selectedProjectType) > 0) {
              currentValue.name = currentValue.name.replace(this.selectedProjectType, '')
              return currentValue
          } else {
              return false
          }
        })
        getProjects = getProjects.filter(function (el) {
          return el != false;
        });
      }

      this.workspacesAvailable = getProjects ? getProjects : []
      this.parentProjects = await this.workspacesAvailable.filter(p => {
        let result = true
        let nameArr = p.name ? p.name.split(this.nestedUrlId) : []
        if (nameArr.length > 1) {
          result = false
        }
        return result
      })
    },
    /*
      Call API, ask for a single given board
    */
    async getBoardData(boardId) {
      if (!this.loader) {
        this.loader = this.$loading.show({zIndex: 30,})
      }
      if (this.workspacesLoaded) {
        this.changeParams({
          project: boardId
        })
      }
      this.activeProject = await this.workspacesAvailable.find(w => w.id === boardId)
      if (!this.activeProject) {
          this.loader.hide()
          return
      }
      var url = window.location.href.split('=')[0] + '=' + this.activeProject.id
      this.breadCrumbs.push({
        id: this.activeProject.id,
        name: this.cropProjectName(this.activeProject.name),
        url: url
      })

      await this.fetchWorkspaceData()
      this.columnsLoaded = true
      this.loader.hide()

      Vue.prototype.wsIsOpen = true
      this.$forceUpdate()
      this.getData()
    },
    async fetchWorkspaceData() {
      if (this.activeProject) {
        // get all cards in the board
        this.workspaceTasks = await this.fetchTasks(this.activeProject.id)
        // get all columns in the board
        this.activeProjectColumns = await this.fetchColumns(this.activeProject.id)
        await this.arrangeCards(this.activeProjectColumns)
        //get all custom fields in the board
        this.customFields = await this.fetchCustomFields(this.activeProject.id)
        this.fieldsToDisplay = this.customFields.userstory.filter(field => {
          return field.description.substr(-3) === '__d'
        })
        this.fieldsToDisplay.forEach(field => this.displayFieldsMap.set(field.id, field.name))
        for (const clmn of this.activeProjectColumns) {
          for (const card of clmn.cards) {
            this.cardDisplayCF[card.id] = []
            const cardCFValues = await this.sendRequest("userstories/custom-attributes-values/" + card.id);
            for (const field of this.fieldsToDisplay) {
              if  (cardCFValues.attributes_values[field.id]) {
                this.cardDisplayCF[card.id][field.id] = {
                  name:field.name,
                  value: cardCFValues.attributes_values[field.id]
                }
              }
            }
          }
        }
      }
    },
    async getData() {
      if (!this.loader) {
        this.loader = this.$loading.show({zIndex: 30,})
      }
      this.usersList = await this.sendRequest('users')
      this.userMe = await this.sendRequest('users/me')
      this.currentTasks = await this.sendRequest('tasks')
      this.timeline = await this.sendRequest('timeline/project/' + this.activeProject.id)
      const roles = await this.sendRequest('roles?project=' + this.activeProject.id)
      this.projectsRoles = roles
        .map(role => ({
          text: role.name,
          value: role.id,
        }))
      this.sendRequest('tasks')
      this.loader.hide()
    },
    async readParams() {
      const parsed = queryString.parse(location.search)
      if (parsed.project && !parsed.card) {
        this.getBoardData(parseInt(parsed.project, 10))
      } else if (parsed.project && parsed.card) {
        await this.getBoardData(parseInt(parsed.project, 10))
        this.openCard(parseInt(parsed.card, 10))
      }
    },
    async checkInvite() {
      const parsed = queryString.parse(location.search)
      if (parsed.project && parsed.invite) {
        await this.activateToken(parsed.invite)
      }
    },
    async activateToken(invite) {
      var membershipId = await this.sendRequest('invitations/' + invite)
      await this.sendRequest(
        'memberships/' + membershipId.id,
        'patch', 
        {"user": this.userMe.id}
      ) 
    },
    changeParams(paramsObj) {
      const params = queryString.stringify(paramsObj);
      const title = this.activeProject != null ?
          (this.cardToOpen != null ?
            (this.activeProject.name + ' - ' + this.cardToOpen.subject) :
            this.activeProject.name
          ) :
          'Workspaces'
      const url = location.pathname + '?' + params
      var elem = document.querySelector('#hiding-nav');
      if (elem !== null) {
        elem.style.display = 'none';
      }
      window.history.pushState(paramsObj, title, url)
    },
    replaceQueryParam(param, newval, search) {
      var regex = new RegExp("([?;&])" + param + "[^&;]*[;&]?");
      var query = search.replace(regex, "$1").replace(/&$/, '');

      return (query.length > 2 ? query + "&" : "?") + (newval ? param + "=" + newval : '');
    },
    switchOptions(name) {
      this.showCardOptions = this.showCardOptions !== name ? name : ''
    },
    arrangeCards(columns) {
      columns.forEach(col => {
        let nested = this.nestedProjects(col.id).map(nested => ({ ...nested, type: 'nested'}))
        let own = this.filterCards(col.id).map(card => ({ ...card, type: 'card'}))
        if (col.is_archived) {
          this.archivedColId = col.id
        }

        col.cards = [ ...nested, ...own]
      })
    },
    filterCards(columnId) {
      return this.workspaceTasks.filter(t => t.status === columnId).sort((a, b) => a.kanban_order - b.kanban_order)
    },
    renameColumn: function(column) {
      this.reColumn = false
      this.sendRequest('userstory-statuses/' + column.id, 'patch', column)
    },
    async addList(projectId) {
      let block = document.querySelector('.columns-list')
      let order = this.activeProjectColumns.length + 1
      let newList = {
        name: this.newColumnName.length ? this.newColumnName : 'List ' + order,
        project: projectId,
        order: order
      }
      this.newColumn = false
      this.newColumnName = ''
      let list = await this.saveList(newList, true)
      this.$nextTick(() => {
        list.cards = []
        this.activeProjectColumns.push(list)
        block.scrollLeft = block.scrollWidth
      })
    },
    async addRow(column, orgn = null, order = column.cards.length) {
      if (!column.cards) {
        column.cards = []
      }
      let newCard = {
        subject: this.newRowName.length ? this.newRowName : 'New card',
        project: this.activeProject.id,
        status: column.id
      }
      this.newRow = false
      this.newRowName = ''
      let row = await this.saveCard(orgn == null ? newCard : orgn)
      this.$nextTick(async () => {
        column.cards.splice(order, 0, row)
        this.workspaceTasks.push(row)
        this.activeProjectColumns = await this.fetchColumns(this.activeProject.id)
        if (orgn == null) {
          await this.arrangeCards(this.activeProjectColumns)
        }
        this.reorderRows(this.activeProjectColumns)
      })
    },
    async openCard(cardId) {
      if (this.workspacesLoaded && this.activeProject != null) {
        this.changeParams({
          project: this.activeProject.id,
          card: cardId
        })
      }
      let _tasks = await this.sendRequest('tasks') || []
      this.cardToOpen = await this.sendRequest('userstories/' + cardId)
      this.showProjDetails = false
      console.log('this.cardToOpen :>> ', this.cardToOpen);
      this.cardToOpen.tasks = _tasks.filter(_t =>  _t.user_story === cardId)
    },
    closeCard() {
      this.changeParams({
        project: this.activeProject.id
      })
      this.cardToOpen = null
    },
    getCurrentList(listId) {
      return this.activeProjectColumns.find(list => list.id === listId) || {}
    },
    setFocus(ref, refs = this.$refs) {
      this.$nextTick(() => {
        let el = refs[ref][0] ? refs[ref][0] : refs[ref]
        if (el) {
          el.focus() // ser focus on imput
        }
      })
    },
    async checkMove(evt){
      let newId = evt.to.id.replace('column', '')
      this.draggedElement = evt.draggedContext.element
      if (this.draggedElement && this.draggedElement.type === 'card') {
        this.draggedElement.status = parseInt(newId)
        this.saveCard(this.draggedElement, { status: parseInt(newId) })
      } else if (this.draggedElement && this.draggedElement.type === 'nested') {
        this.draggedElement.name = await this.renameNestedProject(this.draggedElement, newId)
      }
    },
    trackDrag(event, type) {
      if (type.indexOf('column') >= 0) {
        this.dragColumn = false
        this.$nextTick(() => {
          this.reorderColumns()
        })
      } else {
        this.dragRow = false
        this.$nextTick(() => {
          this.reorderRows()
        })
      }
    },
    startDrag(event, type) {
      if (type.indexOf('column') >= 0) {
        this.dragColumn = true
      } else {
        this.dragRow = true
      }
    },
    async updateCard() {
      if (this.cardUpdating) {
        clearTimeout(this.updateCardTimeout)
        this.updateCardTimeout = setTimeout(() => {
          this.updateCard()
        }, 2000);
      } else {
        this.cardUpdating = true
        this.cardKey++
        await this.arrangeCards(this.activeProjectColumns)
        this.updateTimeline()
        this.cardUpdating = false
      }
    },
    async saveCard(task, payload = null) {
      if (!task) {
        return
      }
      let newCard = null
      if (payload == null) {
        newCard = await this.sendRequest('userstories', 'post', task)
      } else {
        payload.version = task.version++
        newCard = await this.sendRequest('userstories/' + task.id, 'patch', payload)
        if (newCard.due_date_status) {
          task.due_date_status = newCard.due_date_status
        }
      }
      this.$nextTick(async () => {
        this.workspaceTasks = await this.fetchTasks(this.activeProject.id)
        this.updateCard()
      })
      return newCard ? newCard : {}
    },
    async saveList(list, isNew = false) {
      let newList = null
      if (isNew) {
        newList = await this.sendRequest('userstory-statuses', 'post', list)
      } else {
        newList = await this.sendRequest('userstory-statuses/' + list.id, 'patch', list)
      }
      this.cardKey++
      return newList ? newList : {}
    },
    async deleteCard(cardId) {
      this.closeCard()
      this.workspaceTasks = await this.workspaceTasks.filter(card => card.id !== cardId)
      this.activeProjectColumns = [...this.activeProjectColumns]
      this.arrangeCards(this.activeProjectColumns)
      this.sendRequest('userstories/' + cardId, 'delete')
    },
    async deleteList(listId) {
      this.activeProjectColumns = await this.activeProjectColumns.filter(list => list.id !== listId)
      this.arrangeCards(this.activeProjectColumns)
      this.sendRequest('userstory-statuses/' + listId, 'delete')
    },
    reorderColumns() {
      this.activeProjectColumns.forEach((col, i) => {
        if (col.order !== (1 + i)) {
          col.order = (1 + i)
          this.saveList(col)
        }
      })
    },
    async reorderRows() {
      if (this.rowsOrdering) {
        clearTimeout(this.rowsOrderTimeout)
        this.rowsOrderTimeout = setTimeout(() => {
          this.reorderRows()
        }, 2000);
      } else {
        this.rowsOrdering = true
        let inc = 0
        for (const col in this.activeProjectColumns) {
          if (this.activeProjectColumns[col] && this.activeProjectColumns[col].cards) {
            for (let card of this.activeProjectColumns[col].cards) {
              if (card.type !== 'nested') {
                if (card.kanban_order !== inc) {
                  card = await this.saveCard(card, { kanban_order: inc })
                }
                inc++
              }
            }
          }
          inc++
        }
        this.rowsOrdering = false
      }
    },
    deepCopy(recepient, obj) {
      for (let prop in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, prop)) {
          recepient[prop] = obj[prop]
        }
      }
    },
    async updateTimeline() {
      let timeLineUrl = 'timeline/project/' + this.activeProject.id
      this.timeline = await this.sendRequest(timeLineUrl)
    },
    async fetchTasks(boardId) {
      const tasks_url = 'userstories?project=' + boardId
      let fetchedTasks = await this.sendRequest(tasks_url)

      return fetchedTasks.sort((a, b) => a.kanban_order - b.kanban_order)
    },
    async fetchColumns(boardId) {
      const columns_url = 'userstory-statuses?project=' + boardId
      let fetchedColumns = await this.sendRequest(columns_url)
      this.activeProjectArchive = fetchedColumns.filter(col => col.is_archived)

      return fetchedColumns.sort((a, b) => a.order - b.order)
    },
    async sendRequest(url, type = 'get', payload = {}) {
      delete this.$http.defaults.headers.common['X-CSRFToken'] // remove CSRF in order to access API by a separate API token
      let prop

      this.authHeaders.headers['x-disable-pagination'] = true

      if (type === 'post') {
        await this.$http
          .post(this.apiUrl + url, payload, this.authHeaders)
          .then((response) => {
            prop = response.data
          })
          .then(() => {
            // feed WS token to Holons invitations repository
            this.$http.defaults.headers.common['X-CSRFToken'] = window.csrftoken
            var inviteUrl = '/invitation/generate-layers-invite'
            this.$http.post(this.holonsApiUrl + inviteUrl, {'token': prop.token})
            .then((holonsResponse) => {
              console.log('Holons response:', holonsResponse.data)
            })
          }
          )
          .catch(error => this.handleError(error, url))

      } else if (type === 'patch') {
        await this.$http
          .patch(this.apiUrl + url, payload, this.authHeaders)
          .then((response) => {
            prop = response.data
          })
          .catch(error => this.handleError(error, url))
      } else if (type === 'put') {
        await this.$http
          .put(this.apiUrl + url, payload, this.authHeaders)
          .then((response) => {
            prop = response.data
          })
          .catch(error => this.handleError(error, url))

      } else if (type === 'delete') {
        await this.$http
            .delete(this.apiUrl + url, this.authHeaders)
            .catch(error => this.handleError(error, url))

      } else {
        await this.$http
          .get(this.apiUrl + url, this.authHeaders)
          .then((response) => {
            prop = response.data
          })
          .catch(error => this.handleError(error, url))
      }
      return prop
    },
    handleError(error, type) {
      console.error([
        type + ' api is unavailable at the moment',
        error,
      ])
    },
    getShortName(name) {
      let nameArr = name.split(' ')
      for (let i = 0; i < nameArr.length; i++) {
          const n = nameArr[i];
          nameArr[i] = n[0].toUpperCase()
      }
      return nameArr.join('')
    },
    getUserInfo(idsArr) {
      let userObj = {}
      for (let i = 0; i < idsArr.length; i++) {
        const userId = idsArr[i];
        if (userId >= 0) {
          let user = this.usersList.find(u => u.id === userId)
          let fullName = user.full_name !== '' ? user.full_name : user.full_name_display
          let shorName = this.getShortName(fullName !== '' ? fullName : user.username)
          userObj[userId] = {
            id: userId,
            username: user.username,
            color: user.color,
            fullName: fullName,
            shortName: shorName,
            photo: user.photo
          }
        }
      }
      return userObj
    },
    openNewProjectModal(listId = null) {
      this.parentListId = listId
      var jQuery = window.$
      jQuery('#addProjectModal')
        .modal('show')
      ;
    },
    openDeleteWorkspaceModal() {
      var jQuery = window.$
      jQuery('#deleteWorkspaceModal')
        .modal('show')
      ;
    },
    nestedProjects(colId) {
      let arr = this.workspacesAvailable.filter(p => {
        let result = false
        let nameArr = p.name ? p.name.split(this.nestedUrlId) : []
        if (nameArr.length > 1) {
          result = nameArr[nameArr.length - 1] == colId
        }
        return result
      })
      return arr
    },
    getCardName(card, column) {
      return card.type === 'nested'
              ? card.name.replace(this.nestedUrlId + column.id, '')
              : card.subject
    },
    cropProjectName(name) {
      let arr = name.split(this.nestedUrlId)
      return arr[0]
    },
    async renameNestedProject(nestedProject, newParentId) {
      let newName = (await this.cropProjectName(nestedProject.name)) + this.nestedUrlId + newParentId
      await this.sendRequest('projects/' + nestedProject.id, 'patch', {
        name: newName
      })
      this.workspacesAvailable = await this.getWorkspaces()
      return newName
    },
    // This is a cut and paste from CardModal.vue
    // @todo: Mabe centralize this and use parental method in Modal?
    customDateFormatter(date, short = false, human = false) {
      let d = new Date(date)
      let options = {}
      if (short) {
        options = {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        }
      } else {
        options = {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          weekday: 'short',
          hour: '2-digit',
          minute: '2-digit',
        }
      }
      if (human) {
        options = {
          month: 'short',
          day: 'numeric',
        }
      }
      return d.toLocaleDateString('en-US', options)
    },
    changeLayout(layout) {
      if (layout === 'vertical') {
        this.kanbanVertical = true
        this.kanbanTable = false
      } else if (layout === 'table') {
        this.kanbanVertical = false
        this.kanbanTable = true
      } else {
        this.kanbanVertical = false
        this.kanbanTable = false
      }
    },
    async getInvite() {
      let inviteResponse
      if (this.inviteMail === '' || this.inviteRole === 0) {
        this.inviteError = true
      } else {
        inviteResponse = await this.sendRequest('memberships', 'post', {
          project: this.activeProject.id,
          role: this.inviteRole,
          username: this.inviteMail
        })

        this.inviteLink = location.href + '&invite=' + inviteResponse.token
      }
    },
    copyLink(ev) {
      this.linkCopied = true
      setTimeout(() => {
        this.linkCopied = false
      }, 3000);
      ev.target.select();
      document.execCommand('copy');
    },
    async fetchCustomFields(boardId) {
      return {
        task: await this.fetchTaskCF(boardId),
        userstory: await this.fetchUserstoryCF(boardId)
      }
    },
    async fetchTaskCF(boardId) {
      const f_url = 'task-custom-attributes?project=' + boardId
      let fetched = await this.sendRequest(f_url)

      return fetched;
    },
    async fetchUserstoryCF(boardId) {
      const f_url = 'userstory-custom-attributes?project=' + boardId
      let fetched = await this.sendRequest(f_url)

      return fetched;
    },
    async createCF(name, description, type, scope, extra) {
      const url = `${scope}-custom-attributes`
      let field = {
        name, description, type,
        project: this.activeProject.id
      };
      if (extra) {
        field.extra = extra
      }
      return await this.sendRequest(url, 'post', field)
    },
    deleteCF(scope, id) {
      const url = `${scope}-custom-attributes/${id}`
      this.sendRequest(url, 'delete')
      this.customFields[scope] = this.customFields[scope].filter(a => a.id !== id);
    },
    addCF(cf, scope) {
      this.customFields[scope].push(cf);
      this.displayFieldsMap.set(cf.id, cf.name)
    },
    updateDisplayCF(cardId, fieldId, value) {
      if (this.displayFieldsMap.has(fieldId)) {
        if (this.cardDisplayCF[cardId][fieldId])
        this.cardDisplayCF[cardId][fieldId].value = value;
      else {
        this.cardDisplayCF[cardId][fieldId] = {
          value,
          name: this.displayFieldsMap.get(fieldId)
        }
      }
      }
      
    }
  },
  watch: {
    newColumn: function() {
      if (this.newColumn) {
        this.setFocus('newColumnRef')
      }
    },
    reColumn: function() {
      if (this.reColumn) {
        this.setFocus('renameColumnRef')
      }
    },
    newRow: function() {
      if (this.newRow) {
        this.setFocus('newRowRef' + this.newRowColumnId)
      }
    },
  },
}
</script>

<style lang="css">
.ui.input>input {
  font-weight: inherit;
}
.task-extra-info__assigned-inner.member {
  padding: 10px;
  text-transform: uppercase;
  border-radius: 50%;
  display: inline-block;
  height: 28px !important;
  width: 28px !important;
}
</style>
