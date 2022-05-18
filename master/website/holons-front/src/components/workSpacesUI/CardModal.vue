<template>
  <div class="card-modal-bg">
    <div class="card-modal-overlay" @click="close" @keyup:escape="close"></div>
    <sui-card class="card-modal">
      <sui-card-content>
        <sui-card-header>

          <sui-grid>
            <sui-grid-row style="padding:0">

              <sui-grid-column :width="16">
                <sui-input
                  v-model="card.subject"
                  class="card-header"
                  transparent
                  fluid
                  @blur="saveCard(card, { subject: card.subject })"
                  @keyup.enter="$event.target.blur()"
                />

                <div class="ws-card-meta">
                  <sui-header-subheader class="subheader">
                    in list
                    <span class="parent">{{ getCurrentList(card.status).name }}</span>
                    &nbsp;
                    <span v-if="card.is_watcher" class="is-watching"><sui-icon name="eye"/></span>
                  </sui-header-subheader>

                </div>


              </sui-grid-column>

              <!--<sui-grid-column :width="8">
                TODO
                <div class="ws-card--tags">
                  <span class="label-text">test #2</span>
                  <span class="label-text">example 2</span>
                  <sui-button class="ui button mini"
                  icon="bullseye">Tags</sui-button>
                </div>
              </sui-grid-column>-->

              <!--<sui-grid-column :width="5">
                <div class="ws-card--controls">
                  <sui-button class="ui button mini"
                  icon="bullseye">Move</sui-button>
                  <sui-button class="ui button mini"
                  icon="bullseye">Copy</sui-button>
                  <sui-button class="ui button mini"
                  icon="bullseye">Archive</sui-button>
                  <sui-button class="ui button mini"
                  icon="bullseye">Share</sui-button>
                  <sui-button class="ui button mini"
                  icon="bullseye">Watch</sui-button>
                  <sui-button class="ui button mini"
                  icon="bullseye">Delete</sui-button>
                </div>
              </sui-grid-column>-->



            <!--<sui-grid-column :width="3">
              <sui-button class="ui button mini"
              icon="bullseye">Assign owner</sui-button>
              <sui-button class="ui button mini"
              icon="bullseye">Set due date</sui-button>
            </sui-grid-column>-->

            </sui-grid-row>
          </sui-grid>

        </sui-card-header>

      </sui-card-content>

      <sui-card-content>
        <sui-grid>
          <sui-grid-row style="padding:0">

            <!-- description column -->
            <sui-grid-column :width="7" style="padding:0">

              <!--<sui-header size="small">Description</sui-header>-->
              <textarea
                class="ui field textarea card-modal__description-textarea"
                v-model="card.description"
                placeholder="Enter description"
                cols="30"
                rows="10"
                @blur="saveCard(card, { description: card.description })"
              ></textarea>

              <!--<button class="ui button">add checklist</button>
              <button class="ui button">start timer</button>-->
              <div v-if="customFields.userstory.length">
                <sui-label class="segment-label" attached="top">
                  Custom Fields
                </sui-label>
                <drop-down-container>
                <CustomField 
                  v-for="field in customFields.userstory"
                  v-bind:key="field.id"
                  v-bind:field="field"
                  v-bind:value="cfValues.attributes_values[field.id]"
                  v-bind:saveField="saveField"
                 />
                </drop-down-container>
              </div>

              <segmentBlock
                :card="card"
                :item="item"
                :props-to-display="propsToDisplay"
                :add-value="addValue"
                :del-value="delValue"
                :active-project="activeProject"
                :users-list="usersList"
                :user-me="userMe"
                :users-to-assign="usersToAssign"
                :custom-date-formatter="customDateFormatter"
                :send-request="sendRequest"
                :set-date="setDate"
                :get-tag-color="getTagColor"
                :switch-options="switchOptions"
                :get-user-info="getUserInfo"
                :set-focus="setFocus"
              />



            </sui-grid-column>

            <!-- timeline + comments -->
            <sui-grid-column :width="7">

              <!--<sui-header size="small">timeline</sui-header>-->

              <sui-input
                v-model="card.comment"
                :transparent="card.comment != null && card.comment !== '' && original.comment === card.comment"
                placeholder="write a comment..."
                fluid
                @blur="saveCard(card, { comment: card.comment })"
                @keyup.enter="$event.target.blur()"
              />

              <!--<div>-->
                <timeLine
                  v-if="timeline"
                  :get-user-info="getUserInfo"
                  :filter-time-line="filterTimeLine(timeline)"
                  :custom-date-formatter="customDateFormatter"
                />
              <!--</div>-->

            </sui-grid-column>

            <!--

            TODO: refactor & brin back later on
            <sui-grid-column :width=5>

              <div class="ui secondary menu secondary-navigation" style="overflow: hidden">
                  <a href="#" class="item active">Activity</a>
                  <a href="#" class="item">Comments</a>
                  <a href="#" class="item">Custom fields</a>
                  <a href="#" class="item">Linked items</a>
              </div>

            </sui-grid-column>-->

            <sui-grid-column :width="2" id="card-modal-controls">


                <!--<div class="segment-label ui top attached label"> Log $$ </div>-->
                <div id="controlsMembers" class="ui segment segment-controls">
                  <button class="card-button ui basic button">
                    <i class="dollar sign icon"></i>expense</button>
                  <button class="card-button ui basic button">
                    <i class="clock outline icon"></i>start timer</button>
                </div>


              <!--<button class="ui button">add attachment</button>-->

              <div v-if="true">
              <sui-segment v-for="segment in cardControls" :key="segment.name" class="control-segments">
                <sui-label class="segment-label" attached="top">
                  {{ segment.name }}
                </sui-label>
                <segmentControls
                  v-for="item in segment.content"
                  :key="item.name"
                  :card="card"
                  :item="item"
                  :add-value="addValue"
                  :del-value="delValue"
                  :all-projects="allProjects"
                  :get-current-list="getCurrentList"
                  :project-columns="projectColumns"
                  :project-archive="projectArchive"
                  :users-list="usersList"
                  :user-me="userMe"
                  :new-tag-color-options="newTagColorOptions"
                  :get-tag-color="getTagColor"
                  :set-date="setDate"
                  :active-project="activeProject"
                  :save-card="saveCard"
                  :send-request="sendRequest"
                  :archived-col-id="archivedColId"
                  :reorder-rows="reorderRows"
                  :add-row="addRow"
                  :delete-card="deleteCard"
                  :show-options="showOptions"
                  :switch-options="switchOptions"
                  :get-user-info="getUserInfo"
                  :set-focus="setFocus"
                />
              </sui-segment></div>
            </sui-grid-column>

          </sui-grid-row>
        </sui-grid>
      </sui-card-content>
    </sui-card>
  </div>
</template>

<script>
import DropDownContainer from '../App/dropDownContainer.vue';
import CustomField from './card/customField.vue';
import segmentBlock from './segmentBlock';
import segmentControls from './segmentControls';
import timeLine from './timeLine';

export default {
  components: {
    segmentBlock,
    segmentControls,
    timeLine,
    CustomField,
    DropDownContainer
  },
  props: {
    card: {
      type: Object,
      default: () => {}
    },
    closeCard: {
      type: Function,
      default: () => {}
    },
    getCurrentList: {
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
    saveCard: {
      type: Function,
      default: () => {}
    },
    deepCopy: {
      type: Function,
      default: () => {}
    },
    sendRequest: {
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
    activeProject: {
      type: Object,
      default: () => {}
    },
    projectColumns: {
      type: Object,
      default: () => {}
    },
    projectArchive: {
      type: Object,
      default: () => {}
    },
    allProjects: {
      type: Object,
      default: () => {}
    },
    authHeaders: {
      type: Object,
      default: () => {}
    },
    usersList: {
      type: Object,
      default: () => []
    },
    userMe: {
      type: Object,
      default: () => null
    },
    currentTasks: {
      type: Object,
      default: () => null
    },
    timeline: {
      type: Object,
      default: () => null
    },
    archivedColId: {
      type: Number,
      default: NaN
    },
    showOptions: {
      type: String,
      default: ''
    },
    customFields: {
      type: Object,
      default: () => {}
    },
    updateField: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      apiUrl: 'https://holons.me/boards/api/v1/',
      original: {},
      cardControls: [
        {
          name: 'Add to card',
          content: [
            {
              name: 'assign',
              icon: 'users',
              property: 'assigned_users',
            },
            {
              name: 'tag',
              icon: 'tags',
              property: 'tags',
            },
            {
              name: 'task',
              icon: 'tasks',
              property: 'tasks',
            },
            {
              name: 'Due Date',
              icon: 'calendar alternate outline',
              property: 'due_date',
            },
            {
              name: 'attach',
              icon: 'paperclip',
              property: 'attachments',
            },
          ]
        },
        {
          name: 'Actions',
          content: [
            {
              name: 'Move',
              icon: 'exchange',
              action: 'move'
            },
            {
              name: 'Copy',
              icon: 'copy outline',
              action: 'copy'
            },
            {
              name: 'Watch',
              icon: 'eye'
            },
            {
              name: 'divider'
            },
            {
              name: 'Archive',
              icon: 'archive'
            },
            {
              name: 'Share',
              icon: 'share'
            },
            {
              name: 'Delete',
              icon: 'delete',
              action: 'delete'
            },
          ]
        },
      ],
      propsToDisplay: ['assigned_users', 'tags', 'tasks', 'due_date', 'attachments'],
      usersToAssign: [],
      newTagColorOptions: [],
      tagPossibleColors: [
        { name: 'fancy green', col: '#7b8f50'},
        { name: 'fancy black', col: '#23272B'},
        { name: 'trendy blue', col: '#4E7D96'},
        { name: 'humble pink', col: '#FCC7D0'},
        { name: 'pale green', col: '#7DA199'},
        { name: 'frienly yellow', col: '#F4BE2A'},
        { name: 'white-ish', col: '#828382'},
        { name: "queen's red", col: '#AE4952'},
        { name: 'fancy blue', col: '#344563'},

      ],
      cfValues: {attributes_values: {}, version: 0}
    }
  },
  async created() {
    this.original = { ...this.card }
    this.getTagColors()

    this.usersToAssign = [
      {
        id: -1,
        username: 'No one',
        full_name_display: 'No one'
      },
      ...this.usersList
    ]
    this.cfValues = await this.getCFValues(this.card.id);
  },
  methods: {
    close(evt, save = true) {
      if (!save) {
        this.deepCopy(this.card, this.original)
      }
      this.original = {}
      this.showOptions = ''
      this.closeCard()
    },
    addValue(property, value) {
      // console.log('add property, value :>> ', property, value);
      if (!this.card[property]) {
        this.card[property] = []
      }
      if (value === null || value === '' || this.card[property].filter(_t => _t == value).length) {
        console.log('stop');
        return
      }
      this.card[property].push(value)
      this.$forceUpdate()
    },
    delValue(property, value) {
      // console.log('del property, value :>> ', property, value);
      if (property === 'tags') {
        this.card[property] = this.card[property].filter(_t => _t[0] != value)
      } else {
        this.card[property] = this.card[property].filter(_t => _t != value)
      }
      this.$forceUpdate()
    },
    async getTagColors() {
      let nocolor = {
          text: 'No color',
          value: '',
          label: { empty: true, circular: true },
        }
      let colors = await this.tagPossibleColors.map(color => {
        return {
          text: color.name,
          value: color.col,
          label: { color: color.name.replace(' ', '-').replace('\'', ''), empty: true, circular: true },
        }
      })

      this.newTagColorOptions = [nocolor, ...colors]
    },
    customDateFormatter(date, short = false) {
      let d = new Date(date)
      let options = short ? {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      } : {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        weekday: 'short',
        hour: '2-digit',
        minute: '2-digit',
      }
      return d.toLocaleDateString('en-US', options)
    },
    async setDate(date, prop) {
      if (date != null) {
        if (prop === 'due_date') {
          this.card[prop] = date.toISOString().substring(0, 10)
        } else {
          this.card[prop] = date.toISOString()
        }
      } else {
        this.card[prop] = date
      }
      this.card = await this.beforeSave(prop)
    },
    isEqual(array1, array2) {
      return array1.length === array2.length && array1.every((value, index) => {
        return value === array2[index]
      })
    },
    getTagColor(color) {
      if (color == null) {
        return null
      } else {
        let current = this.newTagColorOptions.find(_col => _col.value === color)
        return current ? current.text.replace(' ', '-').replace('\'', '') : null
      }
    },
    async filterTimeLine(timeline) {
      let cardTimeline = await timeline.filter(tl => {
        if (tl.data && tl.data.userstory) {
          return tl.data.userstory.id === this.card.id
        } else if (tl.data && tl.data.task && tl.data.task.userstory) {
          return tl.data.task.userstory.id === this.card.id
        }
      })
      return cardTimeline
    },
    async beforeSave(prop) {
      let payload = {}
      if (prop !== '') {
        payload[prop] = this.card[prop]
      }
      payload.status = this.card.status
      payload.project = this.card.project
      return await this.saveCard(this.card, payload)
    },
    async getCFValues(id) {
      return await this.sendRequest("userstories/custom-attributes-values/" + id)
    },
    async saveField(id, value) {
      this.cfValues.attributes_values[id] = value;
      this.updateField(this.card.id, id, value);
      return await this.sendRequest(
        "userstories/custom-attributes-values/" + this.card.id,
        "patch",
        this.cfValues
      )
    }
  },
  watch: {
    card: {
      async handler() {
        console.log('card changed'); // TEMP
      },
      deep: true,
    },
    'card.assigned_users': {
      async handler(old, nw) {
        if (!this.isEqual(old, nw)) {
          this.card = await this.beforeSave('assigned_users')
        }
      },
      deep: true,
    },
    'card.is_closed': {
      async handler() {
        this.card = await this.beforeSave('is_closed')
      }
    },
    'card.status': {
      async handler() {
        this.card = await this.beforeSave('')
      }
    },
    'card.project': {
      async handler() {
        this.card = await this.beforeSave('')
      }
    },
    'card.tags': {
      async handler() {
        this.card = await this.beforeSave('tags')

        let payload = {
          tags: this.activeProject.tags
        }
        this.sendRequest('projects/' + this.activeProject.id, 'patch', payload)
      }
    },
  },
}
</script>

<style lang="css">
.card-modal-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* display: flex; */
  overflow-y: scroll;
  z-index: 10;
}
.card-modal-overlay {
  position: fixed;
  width: 100%;
  height: 100%;
  background: #000a;
  z-index: 10;
}
.card-modal-bg .card-modal {
  position: relative;
  margin: 5rem;
  width: calc(100% - 10rem);
  background: #F7F8FA;
  border-radius: 5px;
  z-index: 100;
}
.ui.card:last-child {
  margin-bottom: 5rem;
}
.ui.input.card-header {
  font-weight: 900;
  font-size: 2rem;
}
.subheader {
  font-weight: 100;
  font-size: 1rem;
  color: #777;
}
.parent {
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}
.ui.button.card-button {
  width: 100%;
  font-size: 1rem;
  margin: 0.7rem 0;
  display: flex;
}
.ui.styled.accordion {
  width: 100%;
}
.ui.label.property,
.ui.label.property:last-child,
.ui.label.property:first-child {
  margin: .25rem;
}
.ui.tag.property.label {
  margin: 0.3rem 0.75rem;
}
.ui.label.segment-label {
  text-transform: uppercase;
  text-align: center;
  background: none;
  position: inherit;
  text-align: center;
  padding: 0

}
.add-new-input>.ui.input>input {
  margin-top: 0.5rem;
}
.option-section__current {
  margin: 0.5rem 0;
}
.option-section__current:first-child {
  margin-top: 0;
}
span.vdp-datepicker__clear-button {
  font-size: 1.4rem;
}
span.vdp-datepicker__clear-button span i span::after {
  content: ' clear date';
}

.ui.top.attached.label:first-child+:not(.attached) {
  margin-top: 0 !important
}

.control-segments {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  padding: 0 !important
}
</style>
