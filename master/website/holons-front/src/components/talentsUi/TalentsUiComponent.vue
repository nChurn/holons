<template>
  <div class="talents-wrapper">
    <div class="">
      <div class="row">
        <div class="column">
          <h1>Talents search</h1>
        </div>
      </div>
      <form id="search_talents" class="">
        <div class="row">
          <div class="column ui">
            <div class="ui field">
              <label for="search_string">Whom do you want to find:</label>
            </div>
          </div>
          <div class="column ui">
            <div class="ui field input">
              <input id="search_string" type="text" v-model="searchString" />
            </div>
          </div>
        </div>
        <div class="row">
          <div class="two wide column ui">
            <small>e.g. Designer, accountant, Jane Doe, founder</small>
          </div>
        </div>
        <div class="row">
          <div class="column ui">
            <div class="ui field">
              <label for="geo_string">Where:</label>
            </div>
          </div>
          <div class="ui field input">
              <input id="geo_string" type="text" v-model="geoString" />
          </div>
        </div>
        <div class="row">
          <div class="two wide column ui">
            <small>location e.g. New York, London, Gothenburg</small>
          </div>
        </div>
        <div class="row">
          <div class="ui field input">
              <button
                class="ui button"
                v-bind:disabled="searchString == ''"
                v-on:click.prevent="searchTalents()"
              >Search</button>
          </div>
        </div>
      </form>
    </div>
    <div class="results-holder"
        v-if="talents.length > 0"
    >
      <div class="ui grid">
      <div class="row">
        <div class="column">
          <h1>What we found</h1>
        </div>
      </div>
      <div class="row">
        <div class="column">
          <table class="ui celled table">
            <thead>
              <tr>
                <th>Name</th>
                <th>-</th>
                <th>Job</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="talent in talents"
                v-bind:key="talent.id"
              >
                <td data-label="Name">{{ talent.name }}</td>
                <td data-label="Locations">{{ talent.location }}</td>
                <td data-label="summary">{{ talent.summary }}</td>
              </tr>
            </tbody>
          </table>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';


Vue.use(Loading, { zIndex: 9999, })

export default {
  name: 'TalentsUiComponent',
  data() {
    return {
      loader: null,
      talents: [],
      searchString: '',
      geoString: ''
    }
  },
  mounted() {
    console.log('Talents UI')
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/talents/'
      return url
    }
  },
  methods: {
    searchTalents: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + 'search'
      var data = {
        'search_string': this.searchString,
        'geo_string': this.geoString
      }
      this.$http.post(url, data).then(response => {
        console.log('Search talents')
        console.log(response.data)
        this.talents = response.data.talents
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Talents api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .talents-wrapper {
    margin-top: 100px;
    padding-left: 50px;
    overflow-y: auto !important;
  }
  #parent {
    overflow: auto !important;
  }
</style>