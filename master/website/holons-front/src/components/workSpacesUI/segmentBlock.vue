<template>
  <div class="card-prop-segments">
    <div
      v-for="prop in propsToDisplay"
      :key="prop"
      :class="`segment-blocks__prop ${prop}`"
    >
      <sui-segment
        v-if="!!card[prop] && card[prop] !== null && card[prop].length !== 0"
      >
        <sui-label class="segment-label" attached="top">
          {{ prop.replace('_', ' ') }}
        </sui-label>
        <!-- <pre>{{ prop }}</pre> -->
        <div v-if="prop === 'due_date'" class="due-date-span">
          <sui-checkbox
            :label="customDateFormatter(card.due_date)"
            v-model="isFinished"
            class="due-date"
            :class="{
              'closed': isFinished
            }"
          />
          <div>
            <a
              v-if="isFinished"
              class="due-date-closed"
              is="sui-label"
            >
              closed
            </a>
            <a
              v-else-if="card.due_date_status !== 'set' && card.due_date_status !== 'not_set'"
              class="due-date-status"
              :color="card.due_date_status === 'due_soon' ? 'orange' : 'red'"
              is="sui-label"
            >
              {{ card.due_date_status.replace('_', ' ') }}
            </a>
            <sui-icon class="control-icon" name="close" @click="setDate(null, 'due_date');"/>
          </div>
        </div>
        <div v-else-if="prop === 'attachments'" class="array-span">
          <a
            v-for="item in card[prop]"
            :key="item"
            class="property"
            is="sui-label"
          >
            {{item}}
            <span @click="delValue(prop, item)">×</span>
          </a>
        </div>
        <div v-else-if="prop === 'tasks'" class="task-span">
          <div v-for="(task, taskIndex) in card.tasks" :key="taskIndex" class="task-list">
            <div class="task-base-info">
              <sui-checkbox v-model="task.is_closed" class="task-list__checkbox" @click="switchFinishDate($event, task)"/>
              <textarea-autosize
                v-model="task.subject"
                :key="taskIndex"
                rows="1"
                placeholder="Task name"
                class="task-list__input"
                :class="{'closed': task.is_closed}"
                @blur="saveTask(task, ['subject'])"
                @keyup.enter="$event.target.blur()"
              />
              <sui-icon
                v-if="task.assigned_to == null"
                class="control-icon"
                name="user plus"
                @click="assignUser(task.subject)"
              />
              <div v-else class="task-extra-info__assigned">
                <div
                  v-for="(user, uId) in getUserInfo([task.assigned_to])"
                  :key="uId"
                  class="task-extra-info__assigned-inner"
                  :style="`background-color:${user.color}`"
                  @click="assignUser(task.subject)"
                >
                  <img v-if="user.photo != null" :src="user.photo" :alt="user.fullName">
                  <span v-else>{{ user.shortName }}</span>
                </div>
              </div>
              <sui-icon
                v-if="task.due_date == null"
                class="control-icon"
                name="calendar alternate outline"
                @click="toggleDatePicker(task)"
              />
              <div v-else class="task-extra-info__due">
                <a
                  is="sui-label"
                  :color="getDueColor(task)"
                  :title="getDueTitle(task)"
                  @click="toggleDatePicker(task)"
                >
                  {{ customDateFormatter(task.due_date, true) }}
                </a>
              </div>
              <sui-icon class="control-icon" name="close" @click="deleteTask(task.id)"/>
              <div v-if="chooseTaskUser === task.subject" class="task-options users">
                <sui-checkbox
                  v-for="user in usersToAssign"
                  v-model="task.assigned_to"
                  radio
                  :value="user.id"
                  :key="user.username"
                  :label="`${user.full_name_display}`"
                  :title="
                    `${user.full_name_display}${user.me ? ' (Me)' : ''}\n(${
                      user.username
                    })`
                  "
                  class="task-options__user-checkbox"
                  :class="{
                    me: user.me,
                  }"
                  @click="closeUsers($event, task, user)"
                />
              </div>
              <div v-if="chooseTaskDate === task.subject" class="task-options">
                <datepicker
                  v-model="subtaskDueDate"
                  name="task_due_date"
                  placeholder="Change Task Due Date"
                  inline
                  monday-first
                  clear-button
                  @selected="subtask = task"
                />
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="prop === 'assigned_users'" class="users-span">
          <div
            v-for="(user, uId) in getUserInfo(card[prop])"
            :key="uId"
          >
            <user-block
              :user="user"
              :with-details="true"
              :show-controls="true"
              :show-name="false"
              :control-function="'remove'"
              :add-value="addValue"
              :del-value="delValue"
            />
          </div>
          <div class="users-span__user add-new" @click="switchOptions('Members')">
            <span>&#43;</span>
          </div>
        </div>
        <div v-else-if="prop === 'tags'" class="array-span">
          <a
            v-for="item in card[prop]"
            :key="item[0]"
            class="property"
            is="sui-label"
            :color="getTagColor(item[1])"
            :tag="prop === 'tags'"
          >
            {{
              item[0]
            }}
            <span @click="delValue(prop, item[0])">×</span>
          </a>
        </div>
        <div v-else class="array-span">
          <a
            v-for="item in card[prop]"
            :key="item"
            class="property"
            is="sui-label"
            :color="activeProject.tags_colors[item] || ''"
            :tag="prop === 'tags'"
          >
            {{
              item.name || item
            }}
            <span @click="delValue(prop, item)">×</span>
          </a>
        </div>
      </sui-segment>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker';
import UserBlock from './userBlock';

export default {
  components: {
    Datepicker,
    UserBlock
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
    propsToDisplay: {
      type: Object,
      default: () => []
    },
    addValue: {
      type: Function,
      default: () => {},
    },
    delValue: {
      type: Function,
      default: () => {},
    },
    customDateFormatter: {
      type: Function,
      default: () => {},
    },
    sendRequest: {
      type: Function,
      default: () => {}
    },
    getUserInfo: {
      type: Function,
      default: () => []
    },
    switchOptions: {
      type: Function,
      default: () => {}
    },
    setFocus: {
      type: Function,
      default: () => []
    },
    activeProject: {
      type: Object,
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
    usersToAssign: {
      type: Object,
      default: () => []
    },
    getTagColor: {
      type: Function,
      default: () => null
    },
    setDate: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      newTextValue: null,
      chooseTaskDate: null,
      chooseTaskUser: null,
      isFinished: this.card.finish_date != null,
      subtaskDueDate: null,
      subtask: null,
    }
  },
  methods: {
    toggleDatePicker(task) {
      this.chooseTaskUser = null
      this.chooseTaskDate = this.chooseTaskDate === task.subject ? null : task.subject
      this.subtaskDueDate = task.due_date ? new Date(task.due_date) : null
    },
    closeDatePicker(task, date) {
      if (date != null) {
        task.due_date = date.toISOString().substring(0, 10)
      } else {
        task.due_date = null
      }
      this.chooseTaskDate = null
      this.subtask = null
      this.saveTask(task, ['due_date'])
    },
    assignUser(subject) {
      this.chooseTaskDate = null
      this.chooseTaskUser = this.chooseTaskUser === subject ? null : subject
    },
    closeUsers(evt, task, user) {
      if (['LABEL', 'I'].indexOf(event.target.tagName) >= 0) {
        if (user.id < 0) {
          task.assigned_to = null
          task.assigned_to_extra_info = {}
        } else {
          task.assigned_to = user.id
          task.assigned_to_extra_info = {
            big_photo: user.big_photo,
            full_name_display: user.full_name_display,
            gravatar_id: user.gravatar_id,
            id: user.id,
            is_active: user.is_active,
            photo: user.username,
            username: user.username
          }
        }
        this.chooseTaskUser = null
        this.saveTask(task, ['assigned_to'])
      }
    },
    getSelectedUsers(uIds) {
      let users = this.usersList.filter(u => uIds.indexOf(u.id) >= 0)
      return users
    },
    async switchFinishDate(event, task) {
      if (event.target.tagName == 'LABEL') {
        let statuses = await this.sendRequest('task-statuses?project=' + this.activeProject.id)
        let closed = await statuses.find(s => s.slug === 'closed')
        let progress = await statuses.find(s => s.slug === 'in-progress')
        task.status = task.is_closed ? closed.id : progress.id
        this.saveTask(task, ['status'])
      }
    },
    async saveTask(task, props) {
      let payload = {}
      for (const prop of props) {
        payload[prop] = task[prop]
      }
      payload.version = task.version
      let savedTask = await this.sendRequest('tasks/' + task.id, 'patch', payload)
      this.card.tasks = await this.card.tasks.filter(t => t.id !== task.id)
      this.card.tasks.push(savedTask)
      this.card.tasks.sort((a,b) => a.id - b.id)
    },
    deleteTask(taskId) {
      this.card.tasks = this.card.tasks.filter(task => task.id !== taskId)
      this.sendRequest('tasks/' + taskId, 'delete')
    },
    getDueColor(task) {
      if (task.is_closed) {
        return 'green'
      } else if (task.due_date_status === 'due_soon') {
        return 'orange'
      } else if (task.due_date_status === 'past_due') {
        return 'red'
      } else {
        return 'blue'
      }
    },
    getDueTitle(task) {
      if (task.is_closed) {
        return 'Closed'
      } else if (task.due_date_status === 'due_soon') {
        return 'Due Soon'
      } else if (task.due_date_status === 'past_due') {
        return 'Past Due'
      }
    },
  },
  watch: {
    isFinished: {
      handler() {
        this.setDate(this.isFinished ? new Date() : null, 'finish_date');
      }
    },
    subtaskDueDate: {
      handler() {
        this.closeDatePicker(this.subtask, this.subtaskDueDate)
      }
    }
  },
}
</script>
