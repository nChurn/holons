<template lang="html">
        <div class="content">
          <h2 class="title">add new custom field</h2>
        <div class="ui form">
          <div class="fields">
            <div class="four wide field">
              <label>name</label>
              <input 
                type="text"
                placeholder="dev hours estimate"
                v-model="name"
              >
            </div>
            <div class="six wide field">
              <label>description</label>
              <input
                type="text"
                placeholder="Middle Name"
                v-model="description"  
              >
            </div>
            <div class="four wide field">
              <label>type</label>
              <select
                class="ui fluid search dropdown"
                v-model="type"
              >
                  <option value="text">
                    <i class="star outline icon"></i> do some math here, bitch
                  </option>
                 <option value="text">plain text line</option>
                 <option value="multiline">textarea</option>
                 <option value="richtext">rich text area w/ formatting</option>
                 <option value="date">date</option>
                 <option value="url">URL</option>
                 <option value="dropdown">dropdown</option>
                 <option value="checkbox">checkbox</option>
                 <option value="number">number</option>
               </select>
            </div>
            <div class="two wide field">
              <button class="ui basic button" @click="create">
              + add</button>
            </div>
          </div>
          <div class="fields">
            <div class="field" v-if="scope === 'userstory'">
              <div class="ui checkbox">
                <input id="__cfbtn_display" type="checkbox" tabindex="0" class="hidden" v-model="displayOnFront">
                <label for="__cfbtn_display">display on card's front</label>
              </div>
            </div>
            <div class="field">
              <div class="ui checkbox">
                <input id="__cfbtn_require" type="checkbox" tabindex="1" class="hidden" v-model="requireCf">
                <label for="__cfbtn_require">require</label>
              </div>
            </div>
          </div>
          <div v-if="type === 'dropdown'">
            <div class="fields" v-for="(option, index) in extra" v-bind:key="index">
              <div class="field">
                <label>Option {{index + 1}}</label>
                <input
                  type="text"
                  v-model="extra[index]"  
                >
              </div>
            </div>
            <div class="fields">
              <div class="two wide field">
                <button class="ui basic button" @click="extra.push('')">
                + add option</button>
            </div>
          </div>
        </div>
        <div class="CFList">
          <sui-label for="CFTable">Custom fields</sui-label>
          <table id="CFTable" v-if="fields.length">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Type</th>
              <th>Options</th>
              <th />
            </tr>
            <tr v-for="field in fields" v-bind:key="field.id">
              <td class="cf-name">{{field.name}}</td>
              <td class="cf-desc">{{field.description.substr(0, field.description.length - 3)}}</td>
              <td class="cf-type">{{field.type}}</td>
              <td class="cf-Options">
                <span v-if="displayFields.has(field.id)">display on card</span>
                <select
                class="ui fluid search dropdown"
                v-if="field.type === 'dropdown'"
                >
                  <option v-for="option in field.extra" v-bind:key="option">{{option}}</option>
                </select>
              </td>
              <td>
                <span
                  @click="deleteCF(scope, field.id)"
                  class="cf-delete"
                >
                  X
                </span>
              </td>
              
            </tr>
          </table>
          <!-- if no custom fields yet-->
          <p v-else>no custom fields yet</p>
        </div>
    </div>
</template>

<script>
const defaults = {
  name: "",
  description: "",
  type: "text",
  extra: [""],
  displayOnFront: false,
  requireCf: false
}

export default {
    name: 'CfModal',

    data() {
        return defaults
    },

    props: {
      createCF: {
        type: Function,
        default: () => {}
      },
      scope: {
        type: String,
        default: "userstory"
      },
      updateCFList: {
        type: Function,
        default: () => {}
      },
      fields: {
        type: Object,
        default: () => []
      },
      displayFields: {
        type: Object,
        default: () => {}
      },
      deleteCF: {
        type: Function,
        default: () => {}
      }
    },

    methods: {
      async create() {
        document.getElementById('cfModal-' + this.scope).classList.remove('active');
        const newCF = await this.createCF(
          this.name,
          this.addSettings(this.description),
          this.type,
          this.scope,
          this.type === 'dropdown' ? this.extra : null
        );
        for (const key of Object.keys(defaults)) {
          this[key] = defaults[key]
        }
        this.updateCFList(newCF, this.scope)
      },
      addSettings(text) {
        let settings = "___";
        if (this.displayOnFront) settings = "__d";
        return text + settings;
      }
    }
}
</script>

<style scoped lang="css">

</style>
