<template>
  <div v-if="timeLine.length">
    <div v-for="event in timeLine" :key="event.id" class="timeline-entry">


      <table v-if="event.data" class="timeline-entry-table">
        <tr>
          <td class="timeline__meta">
            <span v-if="event.data.user">
              <user-block
                v-for="(user, uId) in getUserInfo([event.data.user.id])"
                :key="uId"
                class="timeline-entry__user"
                :user="user"
                :with-details="true"
                :show-controls="false"
                :show-name="true"
              />
            </span>
          </td>
          <td rowspan="2">

            <div v-if="event.data.comment == ''"
            class="timeline-entry__info">

              <span
                class="timeline-entry__event-type"
                is="sui-span"
                :color="eventType(event.event_type, event.data).color"
              >
                {{ eventType(event.event_type, event.data).type }}
              </span>
              <span v-if="event.data.task" class="timeline-entry__task">
                Task:&nbsp;
                <a class="timeline-entry__task-name" is="sui-span" color="pink">
                  {{ event.data.task.subject }}
                </a>
                &nbsp;in&nbsp;
              </span>
              <span v-if="event.data.userstory" class="timeline-entry__card">
                Card:&nbsp;
                <a class="timeline-entry__card-name" is="sui-span" color="yellow">
                  {{ event.data.userstory.subject }}
                </a>
                &nbsp;in&nbsp;
              </span>
              <!--<span v-if="event.data.project" class="timeline-entry__project">
                Project:&nbsp;
                <a
                  class="timeline-entry__project-name"
                  is="sui-label"
                  color="orange"
                >
                  {{ event.data.project.name }}
                </a>
              </span>-->
            </div>

            <div
              v-if="event.data.comment !== ''"
              class="timeline-entry_diff"
            >
              <sui-segment>
                <span>{{ event.data.comment }}</span>
              </sui-segment>
            </div>
          </td>

        </tr>
        <tr>
          <td class="timeline__meta">
            <div class="timeline-entry__gd">
            {{ customDateFormatter(event.created) }} | XX days delta
            </div>
          </td>
        </tr>
      </table>


      <!-- <pre>{{event.data}}</pre> -->

      <!--
      <div v-if="event.data">

        <div
          v-if="
            event.data.values_diff && event.event_type.indexOf('change') >= 0
          "
          class="timeline-entry_diff"
        >
          <div
            v-if="event.data.values_diff.description_diff"
            class="timeline-entry_diff-entry"
          >
            {{ event.data.values_diff.description_diff }}
          </div>
          <div v-else>
            <div
              v-for="(prop, i) in event.data.values_diff"
              :key="i"
              class="timeline-entry_diff-entry"
            >
              <span class="timeline-entry_diff-prop">
                {{ i }}
              </span>
              :&nbsp;
              <span class="timeline-entry_diff-value">
                <a
                  class="timeline-entry__project-name"
                  is="sui-label"
                  color="grey"
                >
                  {{ prop[0] || 'None' }}
                </a>
                &nbsp;>>>&nbsp;
                <a
                  class="timeline-entry__project-name"
                  is="sui-label"
                  color="black"
                >
                  {{ prop[1] || 'None' }}
                </a>
              </span>
            </div>
          </div>
        </div>


      </div>-->
    </div>
  </div>
</template>

<script>
import UserBlock from './userBlock';

export default {
  components: {
    UserBlock
  },
  props: {
    filterTimeLine: {
      type: Function,
      default: () => {},
    },
    getUserInfo: {
      type: Function,
      default: () => {},
    },
    customDateFormatter: {
      type: Function,
      default: () => {},
    },
  },
  data() {
      return {
          timeLine: []
      }
  },
  async created() {
    this.timeLine = await this.filterTimeLine
  },
  methods: {
    eventType(event_type, data) {
      let typeArr = event_type.split('.')
      let type = typeArr[typeArr.length - 1]
      if (data.comment !== '') {
        type = 'comment'
      }
      let color = this.colorEvent(type)

      return {
        type: type,
        color: color
      }
    },
    colorEvent(type) {
      if (type === 'create') {
        return 'blue'
      } else if (type === 'delete') {
        return 'red'
      } else if (type === 'comment') {
        return 'brown'
      } else {
        return 'teal'
      }
    }
  },
}
</script>

<style lang="css">
.timeline-entry {
  padding: 5px 0;
  font-size: .8rem;
  border-bottom: 1px solid #ddd;
}
.timeline-entry__info {
  display: flex;
  align-items: baseline;
}
.timeline-entry_diff {
  padding: 0.5rem 0.5rem 0;
}
.timeline-entry_diff-entry {
  margin-bottom: 0.5rem;
}
.timeline-entry_diff-entry:last-child {
  margin-bottom: 0;
}
.timeline-entry__event-type,
.timeline-entry__task-name,
.timeline-entry__card-name,
.timeline-entry__project-name {
  margin: 0 0.5rem;
}
.timeline-entry_diff-prop {
  text-decoration: underline;
}
.timeline-entry__created {
  font-weight: bold;
  color: #999;
}

.timeline-entry-table {width: 100% !important}

.timeline__meta {
  width: 105px;
}
</style>
