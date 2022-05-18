<template>
  <div :id="'controls' + item.name" class="segment-controls">
    <div v-if="showOptions === item.name" class="options-close-overlay" @click="switchOptions('')"></div>
    <sui-divider v-if="item.name == 'divider'" />
    <sui-button
      v-else-if="item.name == 'Watch'"
      class="card-button basic"
      :content="item.name"
      :icon="watchCard ? item.icon : item.icon + ' slash'"
      :positive="watchCard"
      @click="setWatch"
    />
    <sui-button
      v-else-if="item.name == 'Archive'"
      class="card-button basic"
      :content="item.name"
      :icon="item.icon"
      :color="archived ? 'orange' : null"
      @click="setArchived"
    />
    <sui-button
      v-else-if="item.name == 'Delete'"
      class="card-button basic"
      :content="item.name"
      :icon="item.icon"
      @click="deleteCard(card.id)"
    />
    <sui-button
      v-else
      class="card-button basic"
      :content="item.name"
      :icon="item.icon"
      @click="switchOptions(item.name)"
    />
    <sui-segment
      v-if="showOptions === item.name"
      class="segment-controls__option"
    >
      <!-- <sui-label class="segment-label" attached="top">
          {{ item.name }}
      </sui-label> -->
      <div v-if="item.property" class="segment-controls__option-section">
        <datepicker
          v-if="item.name == 'Due Date'"
          v-model="dueDate"
          name="due_date"
          placeholder="Change Due Date"
          inline
          monday-first
        />
        <div v-else>
          <div class="option-section__add">
            <div v-if="item.name === 'assign'">
              <sui-checkbox
                v-for="user in usersList"
                v-model="card.assigned_users"
                :value="user.id"
                :key="user.id"
                :label="`${user.full_name_display}`"
                :title="
                  `${user.full_name_display}${userMe && (user.id === userMe.id) ? ' (Me)' : ''}\n(${
                    user.username
                  })`
                "
                class="user-checkbox"
                :class="{
                  me: userMe && (user.id === userMe.id),
                }"
              />
            </div>
            <div v-else-if="item.name === 'tag'">
              <div v-if="addNewTagSwitch">
                <div class="add-new-input">
                  <sui-dropdown
                    text="Choose tag color"
                    button
                    selection
                    :options="newTagColorOptions"
                    v-model="newTagColor"
                  />
                  <sui-input
                    v-model="newTagName"
                    ref="newTagRef"
                    placeholder="Enter tag"
                    fluid
                  />
                  <sui-input
                    v-model="searchString"
                    ref="searchStringRef"
                    placeholder="Search projects"
                    fluid
                  />
                </div>
                <div style="margin-bottom: .5rem;">&nbsp;</div>
                <div
                  id="search-results"
                  v-if="searchResults.length > 0"
                >
                  <ul>
                    <li
                      v-for="result in searchResults"
                      :key="result.id"
                      class="result-item"
                    >
                    <a
                      v-bind:href="'/workspaces?card=' + result.card + '&project=' + result.project"
                      target="_blank"
                    >
                      {{ result.title }}
                    </a>
                    <button
                      role="button"
                      class="ui button mini"
                      @click="addDynamicTag(result)"
                      >
                      <i class="plus icon"></i>link
                    </button>
                    </li>
                  </ul>
                </div>
                <div style="margin-bottom: .5rem;">&nbsp;</div>
                <sui-button fluid success @click="startSearch">Search for cards</sui-button>
                <div style="margin-bottom: .5rem;">&nbsp;</div>
                <sui-button fluid success @click="addNewTag">Add Tag</sui-button>
              </div>
              <div v-else>
                <div v-if="activeProject && activeProject.tags.length" class="option-section__current">
                  Project Tags <br>
                  <a
                    v-for="tag in activeProject.tags"
                    :key="tag"
                    class="property tag"
                    is="sui-label"
                    :color="getTagColorFromProject(tag)"
                    tag
                    @click="switchCardTag('tags', tag)"
                  >
                    {{ tag }}
                  </a>
                </div>
                <div v-else class="option-section__current">
                  No project tags
                </div>
                <sui-button fluid success @click="addNewTagSwitch = true">Add New Tag</sui-button>
              </div>
            </div>
            <div v-else-if="item.name === 'task'">
              <sui-input
                v-model="newTask"
                ref="newTask"
                placeholder="New Task"
                transparent
                fluid
                @blur="addNewTask"
                @keyup.enter="$event.target.blur()"
              />
            </div>
            <div v-else-if="item.name === 'attach'">
              <div class="upload upload-label">
                <label class="ui label" for="upload-file">Upload file</label>
                <input id="upload-file" type="file" ref="file" @change="selectFile" />
              </div>
              <span>or</span>
              <div class="add-new-input">
                <sui-input
                  v-model="newAttachLink"
                  ref="newAttachLink"
                  placeholder="Attach Link"
                  transparent
                  fluid
                  @blur="
                    addValue(item.property, newAttachLink), (newAttachLink = null)
                  "
                  @keyup.enter="$event.target.blur()"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="item.action && item.action !== 'delete'" class="segment-controls__option-action">
        <sui-input
          v-if="item.action === 'copy'"
          v-model="nameToCopy"
          ref="copyRef"
          class="option-action"
          placeholder="Enter copy name"
          fluid
        />
        <sui-dropdown
          class="option-action"
          :text="'Project to ' + item.action"
          selection
          :options="allProjectsOptions"
          v-model="moveCopyProject"
        />
        <sui-dropdown
          class="option-action"
          :text="'Where to ' + item.action"
          selection
          :options="boardList"
          v-model="currentList"
        />
        <sui-dropdown
          class="option-action"
          text="Select order"
          selection
          :options="orderList"
          v-model="currentOrder"
        />
        <sui-button
          class="option-action"
          positive
          fluid
          @click="performAction(item.action)"
        >
          {{ item.name }}
        </sui-button>
      </div>
      <div v-else-if="item.name === 'Share'" class="segment-controls__option-action">
        <sui-label class="segment-label" attached="top">
          Link to this card
        </sui-label>
        <div class="ui input option-action__share">
          <input
            class="option-action__share-input"
            type="text"
            readonly
            autofocus
            v-model="shareLink"
            @click="copyLink"
          >
          <sui-button
            positive
            :content="`${ linkCopied ? 'Copied!' : 'Copy'}`"
            @click="copyLink"
          />
          <sui-label
            class="option-action__share-label"
            :style="`opacity: ${ linkCopied ? '1' : '0'}`"
            pointing
          >Copied!</sui-label>
        </div>
      </div>
    </sui-segment>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'

export default {
  components: {
    Datepicker,
  },
  props: {
    card: {
      type: Object,
      default: () => {}
    },
    item: {
      type: Object,
      default: () => {}
    },
    addValue: {
      type: Function,
      default: () => {},
    },
    delValue: {
      type: Function,
      default: () => {},
    },
    allProjects: {
      type: Object,
      default: () => {}
    },
    getCurrentList: {
      type: Function,
      default: () => {}
    },
    sendRequest: {
      type: Function,
      default: () => {}
    },
    saveCard: {
      type: Function,
      default: () => {}
    },
    reorderRows: {
      type: Function,
      default: () => {}
    },
    addRow: {
      type: Function,
      default: () => {}
    },
    deleteCard: {
      type: Function,
      default: () => {}
    },
    switchOptions: {
      type: Function,
      default: () => {}
    },
    getUserInfo: {
      type: Function,
      default: () => []
    },
    setFocus: {
      type: Function,
      default: () => []
    },
    projectColumns: {
      type: Object,
      default: () => []
    },
    projectArchive: {
      type: Object,
      default: () => []
    },
    getTagColor: {
      type: Function,
      default: () => null
    },
    usersList: {
      type: Object,
      default: () => []
    },
    userMe: {
      type: Object,
      default: () => []
    },
    newTagColorOptions: {
      type: Object,
      default: () => []
    },
    activeProject: {
      type: Object,
      default: () => null
    },
    setDate: {
      type: Function,
      default: () => {}
    },
    archivedColId: {
      type: Number,
      default: NaN
    },
    showOptions: {
      type: String,
      default: ''
    },
  },
  data() {
    return {
      newTask: null,
      addNewTagSwitch: false,
      newTagName: null,
      searchString: null,
      searchResults: [],
      newTagColor: '#00B5AD',
      boardList: [],
      orderList: [],
      currentList: null,
      currentOrder: 0,
      nameToCopy: '',
      moveCopyProject: this.activeProject,
      allProjectsOptions: [],
      newAttachLink: null,
      currentFile: undefined,
      shareLink: location.href,
      linkCopied: false,
      watchCard: this.card.is_watcher,
      dueDate: this.card.due_date,
      archived: this.archivedColId === this.card.status,
    }
  },
  created() {
    if (this.item.action) {
      this.getLists()
    }
  },
  methods: {
    async setWatch() {
      this.watchCard = !this.watchCard
      this.card.is_watcher = !this.card.is_watcher
      let watchUrl = 'userstories/' + this.card.id + (this.watchCard ? '/watch' : '/unwatch')
      this.sendRequest(watchUrl, 'post')
    },
    async setArchived() {
      this.archived = !this.archived
      if (this.archived) {
        this.card.status = this.archivedColId
        this.projectArchive.forEach(a => {
          a.cards.push(this.card)
        })
        this.setDate(new Date(), 'finish_date');
      } else {
        this.card.status = this.projectColumns[0].id
        this.projectArchive.forEach(a => {
          a.cards = a.cards.filter(c => c.id !== this.card.id)
        })
        this.setDate(null, 'finish_date');
      }
    },
    async getLists() {
      this.currentList = await this.getCurrentList(this.card.status)
      this.allProjectsOptions = await this.allProjects.map((p) => {
        return {
          text: p.name,
          value: p,
        }
      })

      this.boardList = await this.projectColumns.map((p) => {
        return {
          text: p.name,
          value: p,
        }
      })
      this.orderList = await this.getOrderList()
    },
    getOrderList() {
      if (this.currentList.cards && this.currentList.cards.length) {
        this.currentOrder = this.currentList.cards.indexOf(this.card) >= 0 ? this.currentList.cards.indexOf(this.card) : this.currentList.cards.length
        let arr = this.currentList.cards.map(c => {
          let index = this.currentList.cards.indexOf(c)
          return {
            text: index + 1,
            value: index
          }
        })
        return [...arr, {
            text: arr.length + 1,
            value: arr.length
        }]
      } else {
        this.currentOrder = 0
        return [{
          text: 1,
          value: 0
        }]
      }
    },
    performAction(action) {
      if (action === 'move') {
        this.moveCard(this.currentList, this.currentOrder)
      } else if (action === 'copy') {
        this.copyCard(this.currentList, this.currentOrder)
      }
    },
    copyCard(list, order) {
      let toCopy = {...this.card}
      toCopy.subject = this.nameToCopy.length ? this.nameToCopy : 'New card'
      toCopy.status = list.id
      this.addRow(list, toCopy, order)
    },
    moveCard(list, order) {
      this.card.status = list.id
      if (list.cards && list.cards.length) {
        list.cards.splice(order, 0, this.card)
      }
      this.reorderRows(this.projectColumns)
    },
    // This is Alex speaking, here's a POC Fuzzy Search across projects
    // @todo: rewrite in more consistent way if necessary
    async startSearch() {
      let projectList = await this.sendRequest('projects', 'get')
      for (var projectItem in projectList) {
        var searchResult = await this.sendRequest('search?'
          + 'project=' + projectList[projectItem].id
          + '&text=' + this.searchString, 'get')
        if (searchResult.userstories.length > 0) {
          for (var card in searchResult.userstories) {
            this.searchResults.push({
                id: searchResult.userstories[card].id,
                project: projectList[projectItem].id,
                card: searchResult.userstories[card].id,
                title: searchResult.userstories[card].subject
              }
            )
          }
        }
      }
      console.log(this.searchResults)
    },
    // 'Dynamic tag' is a tag with __link_projectId:cardId added to the tagName
    addDynamicTag(cardDetails) {
      this.newTagName = cardDetails.title + '__link_' + cardDetails.project + ':' + cardDetails.card
      this.addNewTag()
    },
    addNewTag() {
      if (this.newTagName === null || this.newTagName === '' || this.activeProject.tags.indexOf(this.newTagName) >= 0) {
        return
      }
      let newTag = [
        this.newTagName,
        this.newTagColor
      ]
      this.activeProject.tags_colors[this.newTagName] = this.newTagColor
      this.activeProject.tags.push(this.newTagName)
      this.addValue('tags', newTag)
      this.newTagColor = ''
      this.newTagName = null
      this.addNewTagSwitch = false
    },
    getTagColorFromProject(tag) {
      let projColor = this.activeProject.tags_colors[tag]
      if (projColor === undefined) {
        return null
      } else {
        return this.getTagColor(projColor)
      }
    },
    async addNewTask() {
      if (this.newTask === null || this.newTask === '' || this.card.tasks.find(t => t.subject === this.newTask)) {
        return
      }
      let task = {
          project: this.card.project,
          subject: this.newTask,
          user_story: this.card.id,
          is_closed: false,
          assigned_to: null,
          assigned_to_extra_info: {},
          due_date: null
      }
      let savedTask = await this.sendRequest('tasks', 'post', task)
      this.addValue('tasks', savedTask)
      this.newTask = null
    },
    switchCardTag(property, tag) {
      let tagArr = [
        tag,
        this.activeProject.tags_colors[tag]
      ]
      let exist = this.card[property].find(_t => {
        return _t[0] === tag
      })
      if (exist) {
        this.delValue(property, tag)
      } else {
        this.addValue(property, tagArr)
      }
    },
    selectFile() {
      this.currentFile = this.$refs.file.files;
      this.addValue('attachments', this.currentFile)
      console.log('this.selectedFiles :>> ', this.selectedFiles);
    },
    copyLink(ev) {
      this.linkCopied = true
      setTimeout(() => {
        this.linkCopied = false
      }, 3000);
      ev.target.select();
      document.execCommand('copy');
    },
  },
  watch: {
    dueDate() {
      this.setDate(this.dueDate, 'due_date');
    },
    currentList: {
      async handler() {
        this.orderList = this.getOrderList()
      }
    },
    moveCopyProject: {
      async handler() {
        let newList = await this.sendRequest('userstory-statuses?project=' + this.moveCopyProject.id)
        this.boardList = newList.map((p) => {
        return {
          text: p.name,
          value: p,
        }
      })
      }
    }
  },
}
</script>

<style lang="css">
.segment-controls {
  position: relative;
}
.ui.segment.segment-controls__option {
  margin: 0;
  position: absolute;
  z-index: 100;
  min-width: 100%;
}
.segment-label {
  text-transform: uppercase;
}
.segment-controls__option-section {
  word-break: break-all;
}
.ui.checkbox.user-checkbox {
  position: relative;
  font-size: 0.9rem;
}
.ui.checkbox.user-checkbox.me {
  margin-right: 12px;
}
.ui.checkbox.user-checkbox.me::after {
  content: '(me)';
  position: absolute;
  top: 0;
  left: calc(100% + 3px);
  font-size: 0.7rem;
  color: #00000099;
  width: 2rem;
}
.upload-label {
  margin-bottom: .5rem;
}
#upload-file {
  opacity: 0;
  position: absolute;
  z-index: -1;
}
.ui.input.option-action__share {
  position: relative;
  display: flex;
  justify-content: center;
  word-break: normal;
  z-index: 1000;
}
.ui.pointing.label.option-action__share-label {
  top: 100%;
  position: absolute;
  transition: opacity .5s;
  box-shadow: 0px 1px 2px 0px #0008;
}
.option-action {
  margin-top: .5rem;
  margin-bottom: .5rem;
}
.option-action:first-child {
  margin-top: 0;
}
.option-action:last-child {
  margin-bottom: 0;
}
.options-close-overlay {
  position: fixed;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  z-index: 10;
}
</style>
