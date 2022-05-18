<template>
  <div class="email-display" v-hotkey="keymap">
    <div class="ray--campaigns">
      <select
        name="template"
        id="template"
        v-model="selectedTemplate">
        <option
          v-for="template in templates"
          v-bind:key="template.id"
          v-bind:value="template.id"
        >{{ template.title }}</option>
      </select>

      <div class="" v-if="!$parent.isCustom">
        <span
          class="primary bid-button"
          v-bind:href="message.url.replace('?source=rss', '')"
          v-on:click.prevent="placeBid"
          v-if="bidButtonVisible"
          target="_blank"
        >{{ bidTitle }}</span>
      </div>
    </div>

    <div class="thread-working-area__controls">
      <!--<button class="ui icon button"
        v-on:click="messageArchive()"
      >
        <i class="archive icon"></i>
      </button>-->
      <button class="ui icon button"
        v-on:click="messageDelete()"
      >
          <i class="trash alternate outline icon"></i>
      </button>

      <h3 class="thread-working-area__subject">{{ message.title }}</h3>

      <!--<select
        name="owner"
        id="owner_select"
        v-model="selectedUser"
        v-on:change="setUsers()"
      >
        <option selected="selected">Share with</option>
        <option v-for="user in users" v-bind:key="user.id">{{ user.username }}</option>
      </select>-->
    </div>



    <div class="thread-working-area__email" style="margin-top: 0px;">

      <div class="thread-working-area__email--content">

        <div class="ray__meta">
          <div v-if="message.country">
            <b style="text-transform: capitalize">{{ message.country }}</b>
          </div>

            <div v-if="message.budget != '' && message.budget != '0'">
              Budget: <b>${{ message.budget }}</b>
            </div>

            <div
              v-if="message.rate_from != '' && message.rate_from != '0'"
            >
              Hourly range <b>${{ message.rate_from }} - ${{ message.rate_to }}</b>
            </div>

            <div v-if="(message.rate_from == '' && message.rate_from == '0') || (message.budget == '' && message.budget == '0')">
              <del>budget: NA</del>
            </div>

        </div>

        <div class="thread-working-area__email--message" v-html="message.description"></div>
        <!--<div class="thread-working-area__email--message">Proposed: {{ message.is_proposed }}</div>

        <button class="ui icon button thread-working-area__email__extras-two">
          <i class="icon ellipsis horizontal"></i></button>-->

        <div class="ray--timing">
          <div>
            <a
              v-bind:href="this.message.url.replace('?source=rss', '')"
              v-on:click.prevent="goToUrl"
            >Open</a>
            <span style="font-weight: 100;font-size: 12px;"> – or hit 'O'</span>
          </div>
          <div>
            Posted {{ message.pub_date_pretty }}
          </div>

        </div>


      </div>

    </div>

    <div class="activity-log" v-if="ownerUser">
      Assigned to @{{ selectedUser }} by @{{ ownerUser }}
    </div>
  </div>
</template>

<script>

export default {
  name: 'RaysDisplay',
  props: [
    'message',
  ],
  data() {
    return {
      users: [],
      selectedUser: null,
      ownerUser: null,
      selectedTemplate: 0,
      templates: [],
      bidTitle: 'register bid',
      bidButtonVisible: true
    }
  },
  watch: {
    message: function() {
      this.selectedUser = null
      this.ownerUser = null
      // this.getUsers()
    }
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/campaigns/templates'
      return url
    },
    keymap () {
      return {
       'd': this.messageDelete,
       'o': this.goToUrl,
      }
     },
  },
  mounted() {
    this.getUsers()
    this.getTemplates()
  },
  methods: {
    goToUrl() {
      window.open(this.message.url.replace('?source=rss', ''))
    },
    placeBid() {
      if(0 === this.selectedTemplate){
        this.bidTitle = 'Select a template'
      } else {
        for(var el in this.templates){
          if(this.templates[el].id == this.selectedTemplate){
            this.updateTemplateUsage(this.templates[el])
            this.bidButtonVisible = false
            // window.open(this.message.url.replace('?source=rss', ''), '_blank')
            break
          }
        }
      }

    },
    updateTemplateUsage(templateData) {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/update'
      var data = {
        template_id: templateData.id
      }
      this.$http.post(url, data).then(response => {
        console.log(response.data)
        this.messageArchive()
        this.loader.hide()
      }).catch(error => {
        console.log(['Templates api is unavailable at the moment (update usage)', error])
        this.loader.hide()
      });
    },
    getTemplates() {
      // then get fresh data
      this.$http.get(this.apiUrl).then(response => {
        console.log(response.data.templates)
        this.templates = response.data.templates
      }).catch(error => {
        console.log(['Templates api is unavailable at the moment (get campaigns)', error])
        this.loader.hide()
      });
    },
    getUsers() {
      var url = this.$parent.apiUrl + 'users'
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.get(url).then(response => {
        console.log(response.data)
        this.users = response.data.users
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error =>{
        console.log(['Rays api is unavailable at the moment (users)', error])
        this.loader.hide()
      });
    },
    setUsers() {
      var url = this.$parent.apiUrl + 'users'
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.post(url).then(response => {
        this.ownerUser = response.data.owner_user
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error =>{
        console.log(['Rays api is unavailable at the moment (assign user)', error])
        this.loader.hide()
      });
    },
    messageDelete: function () {
      var url = this.$parent.apiUrl + 'message/' + this.message.id
      this.loader = this.$loading.show({zIndex: 30,})
      this.$http.delete(url).then(response => {
        console.log(response.data)
        this.$parent.selectedMessage = null
        this.message = null
        this.$parent.getRays()
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
        this.loader.hide()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (delete message)', error])
        this.loader.hide()
      });
    },
    messageArchive: function () {
      var url = this.$parent.apiUrl + 'message/' + this.message.id
      this.$http.patch(url).then(response => {
        console.log(response.data)
        this.$parent.selectedMessage = null
        this.$parent.getRays()
        if(typeof(this.loader) != 'undefined'){
          this.loader.hide()
        }
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Rays api is unavailable at the moment (archive message)', error])
        this.loader.hide()
      });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .thread-working-area__email__extras a {
    color: #000;
  }
  .thread-working-area__email__extras:hover a {
    color: #fff;
  }

</style>
