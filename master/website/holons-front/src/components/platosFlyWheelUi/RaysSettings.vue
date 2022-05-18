<template>
  <div class="hm modal platos active" v-on-modal-close="closeModal">
    <div class="content">
      <h2 class="title">settings</h2>

      <div class="ui secondary menu secondary-navigation pdng0"
        style="margin-bottom:2rem !important">

          <a class="item active" data-tab="inrays">
            settings
          </a>


          <!--
          <a class="item" href="" target="_blank">
            <i class="square full icon"></i>the why
          </a>-->

          <div class="right menu">
            <a class="item disabled">
              <i class="clock outline icon"></i> stats
            </a>
          </div>
      </div>

      <div class="form">

          <div class="flex">
            <h5>name</h5>
            <p class="muted">
              items are sorted alpabetically</p>
          </div>

          <div class="input fluid ui">
            <input
              type="text"
              name="short-name"
              v-model="shortName"
              class="ui input fluid"
            />
          </div>

        <!--<div class="form-row">
          <label for="source-url">RSS source url: </label><br />
          <div class="input fluid ui">
            <input
              type="text" name="source-url"
              v-model="sourceUrl"
              class="ui input fluid"
            />
          </div>
        </div>-->

          <div class="flex" style="margin-top: 2rem">
            <h5>Countries to include</h5>
            <p class="muted">leave empty to include all</p>
          </div>
          <div class="input fluid ui">
            <input
              type="text"
              name="source-url"
              v-model="includeCountries"
              class="ui input fluid"
            />
          </div>


        <div class="grid ui">

          <!-- budget settings -->
          <div class="eight wide column">
            <h5>Filter by budget</h5>
            <div class="input fluid ui">
              <div class="ui label">
                <label for="budget-set">Minimal rate: </label>
              </div>
              <input
                type="text"
                name="budget-rate" v-model="budgetRate"
                class="ui input fluid"
              />
            </div>
            <div class="input fluid ui">
              <div class="ui label">
                <label for="budget-fixed">Min. fixed price: </label>
              </div>
              <input
                type="text"
                name="budget-fixed" v-model="budgetFixed"
                class="ui input fluid"
              />
            </div>
          </div>
          <!-- budget settings end -->

          <div class="eight wide column">
            <h5>Assign</h5>
            [ address book module to assign people ]
          </div>
        </div>

        <div class="form-row">
          <div class="four wide column">
            <div class="checkbox ui">
              <input
                type="checkbox"
                name="budget-set" v-model="budgetEmpty"
                class="ui input"
              />
              <label for="budget-set">Display items with no budget info</label>
            </div>
          </div>
        </div>

        <!--<div class="form-row">
          <div class="four wide column">
            <div class="checkbox ui">
              <input
                type="checkbox"
                name="budget-set"
                v-model="isActive"
                class="ui input"
              />
              <label for="budget-set">This ray is active (if not checked, ray is ignored)</label>
            </div>
          </div>
        </div>-->

        <div>
          <button
            v-on:click.prevent="updateRaySettings(ray)"
            v-bind:disabled="shortName == ''"
            class="ui positive basic button"
          >
            Save
          </button>

          <button
            v-on:click.prevent="deleteRay(ray)"
            class="ui negative basic button right floated"
          >
            Delete this ray
          </button>
          <button
            v-on:click.prevent="closeModal()"
            class="ui basic button right floated"
          >
            Cancel
          </button>

        </div>
      </div>

      <div class="form-row">
        <label for="source-url">Comma separated list of words to look for in title: </label><br />
        <div class="input fluid ui">
          <input
            type="text"
            name="source-url"
            v-model="titleFilter"
            class="ui input fluid"
          />
        </div>
      </div>
      <div class="form-row">
        <label for="source-url">Skills to look for: </label><br />
        <div class="input fluid ui">
          <input
            type="text"
            name="source-url"
            v-model="skillsFilter"
            class="ui input fluid"
          />
        </div>
      </div>
      <div class="form-row">
        <label for="source-url">Categories to look for: </label><br />
        <div class="input fluid ui">
          <input
            type="text"
            name="source-url"
            v-model="categoryFilter"
            class="ui input fluid"
          />
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'RaysAdd',
  props: [
    'ray',
  ],
  data() {
    return {
      shortName: '',
      sourceUrl: '',
      includeCountries: '',
      skillsFilter: '',
      categoryFilter: '',
      titleFilter: '',
      isActive: true,
      budgetEmpty: false,
      budgetRate: 0,
      budgetFixed: 0
    }
  },
  mounted() {
    console.log('Rays Add')
    this.shortName = this.ray.short_name
    this.sourceUrl = this.ray.url
    this.isActive = this.ray.is_active
    this.includeCountries = this.ray.key_words
    this.skillsFilter = this.ray.skills_filter
    this.categoryFilter = this.ray.category_filter
    this.titleFilter = this.ray.title_filter
    this.budgetEmpty = this.ray.budget_empty
    this.budgetRate = this.ray.budget_rate
    this.budgetFixed = this.ray.budget_fixed
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/rays/'
      return url
    }
  },
  methods: {
    closeModal: function () {
      this.$parent.raysSettingsModal = false
    },
    deleteRay (ray) {
      var url = this.apiUrl += ray.id
      this.$http.delete(url).then(response => {
        console.log('Delete ray')
        console.log(response.data)
        this.$parent.getRays()
        this.closeModal()
        this.loader.hide()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (Delete ray)', error])
        this.closeModal()
        this.loader.hide()
      });
    },
    updateRaySettings (ray) {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl += ray.id
      var data = {ray: ray}
      data.ray.short_name = this.shortName
      data.ray.title = this.shortName
      data.ray.link = this.sourceUrl
      data.ray.key_words = this.includeCountries
      data.ray.is_active = this.isActive
      data.ray.title_filter = this.titleFilter
      data.ray.skills_filter = this.skillsFilter
      data.ray.category_filter = this.categoryFilter
      data.ray.budget_empty = this.budgetEmpty
      data.ray.budget_rate = this.budgetRate
      data.ray.budget_fixed = this.budgetFixed


      this.$http.post(url, data).then(response => {
        console.log('Update ray settings')
        console.log(response.data)
        this.closeModal()
        this.loader.hide()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (Update ray settings)', error])
        this.closeModal()
        this.loader.hide()
      });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .modal {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,.3);
    z-index: 9999;
  }
  .settings {
    background: #fff;
    padding: 20px;
    top: 12%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
</style>
