<template>
  <div class="mailbox-add modal">
    <div class="settings">
      <h1>Add a ray</h1>
      <div class="form">
        <div class="form-row">
          <label for="source-url">Short name for the ray: </label>
          <div class="input fluid ui">
            <input type="text"
              name="short-name"
              v-model="shortName"/>
          </div>
        </div>
        <div class="form-row">
          <label for="source-url">RSS source url: </label>
          <div class="input fluid ui">
            <input type="text"
              name="source-url"
              v-model="sourceUrl"/>
          </div>
        </div>
        <div class="form-row">
          <label for="source-url">Comma separated list of countries to include, leave empty to include all: </label>
          <div class="input fluid ui">
            <input type="text"
              name="source-url"
              v-model="exludeCountries"/>
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
        <div class="form-row">
          &nbsp;<br /><br />
        </div>
        <div class="form-row grid ui">
          <div class="seven wide column">
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
          </div>
          <div class="seven wide column">
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
        </div>
        <div class="form-row">
          &nbsp;<br /><br />
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
        <div class="form-row">
          &nbsp;<br /><br />
        </div>
        <div class="form-row">
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
        </div>
        <div class="form-row">
          &nbsp;<br /><br />
        </div>
        <div class="form-row">
          <div class="input ui">
            <button
              v-on:click.prevent="createRayRequest()"
              v-bind:disabled="shortName == '' && sourceUrl == ''"
              class="button ui"
            >
              Add
            </button>
            <button
              v-on:click.prevent="closeModal()"
              class="button ui"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RaysAdd',
  data() {
    return {
      shortName: '',
      sourceUrl: '#',
      exludeCountries: 'india, pakistan, nigeria, thailand, kuwait, zambia, malaysia, argentina, ghana, panama, hong kong, croatia, poland, italy, slovakia, qatar, france, poland, bulgaria, romania, United Arab Emirates, estonia, latvia, saudi arabia, brazil, morocco, dropshipping, drop shipping, simple, dropshipping, drop shipping, simplebubble, bubble.io, t shirt, t shirts, t-shirts, tshirt, Tunisia, Germany, Bahrain, Webflow, Portugal, Singapore, Spain, Kenya, Vietnam, Austria, Jamaica, Egypt, Ukraine, Vietnam, Philippines, China, Honduras, Montenegro, Hungary, Puerto Rico, Albania, wix, mexico, bangladesh, squarespace, Ecuador, Elementor, Gibraltar, Greece, Uganda, Moldova, Slovenia, Taiwan, Sri Lanka',
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
      this.$parent.raysModal = false
    },
    createRayRequest: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      // ask backend to create a ray for us
      // @todo: duplicate code from RaySettings, move it to a single component
      var url = this.apiUrl
      var data = {ray: {}}
      data.ray.title = this.shortName
      data.ray.link = this.sourceUrl
      data.ray.is_active = this.isActive
      data.ray.stop_words = this.exludeCountries
      data.ray.skills_filter = this.skillsFilter
      data.ray.category_filter = this.categoryFilter
      data.ray.title_filter = this.titleFilter
      data.ray.budget_empty = this.budgetEmpty
      data.ray.budget_rate = this.budgetRate
      data.ray.budget_fixed = this.budgetFixed

      this.$http.post(url, data).then(response => {
        console.log(response)
        this.shortName = ''
        this.sourceUrl = ''
        this.exludeCountries = ''
        this.$parent.raysModal = false
        this.$parent.getRays()
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment', error])
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
