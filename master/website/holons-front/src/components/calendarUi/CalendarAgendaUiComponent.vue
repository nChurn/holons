<template src="./templates/calendar-agenda-ui.html" lang="html"></template>

<script>
import Vue from 'vue'
import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
// import listWeek from '@fullcalendar/list'
// import listDay from '@fullcalendar/list'
// import list from '@fullcalendar/list'
import interactionPlugin from '@fullcalendar/interaction'


Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'CalendarAgendaUiComponent',

  components: {
    FullCalendar 
  },

  data() {
    return {
      loader: null,
      calendarOptions: {
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          interactionPlugin 
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        initialView: 'timeGridWeek',
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        // dateClick: this.handleDateClick,
        events: '/calendar/events'

      }
    }
  },
  mounted() {
    console.log('Calendar loaded')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/calendar/events'
      return url
    },
  },
  methods: {
    //
  }
}
</script>


<style scoped>
</style>

