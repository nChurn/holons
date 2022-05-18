<template>
  <div class="ui padded grid no-gutter">

    <div class="column eight wide">
      <div class="container">
          <div class="box">

              <div class="title">
                  <h1>Sign in</h1>
              </div>
              <PhoneInput
                @update="updateLoginPhone"
                v-model="localPhoneNumber"
                fetch-country="false"
                no-flags="false"
                size="sm"
                v-if="!codeInputActive"
              ></PhoneInput>
              <form id="login-form" autocomplete="off">

                  <label for="#" class="email_field" autocomplete="off">

                      <!-- <input
                        type="text"
                        placeholder="phone"
                        autocomplete="off"
                        name="phone"
                        v-if="!codeInputActive"
                        v-model="phoneNumber"
                      > -->

                      <input
                        v-if="codeInputActive"
                        type="text"
                        name="code"
                        placeholder="code from SMS"
                        v-model="confirmationCode"
                      />

                  </label>

                  <button
                    class="auth-btn"
                    name="code"
                    v-if="!codeInputActive"
                    v-bind:disabled="phoneNumber == ''"
                    v-on:click.prevent="getConfirmationCode"
                  >ok. go</button>
                  <button
                    class="auth-btn"
                    name="confirm"
                    v-if="codeInputActive"
                    v-bind:disabled="confirmationCode == ''"
                    v-on:click.prevent="confirmAccount"
                  >let me in</button>
              </form>

          </div>
      </div>
    </div>


    <div class="column eight wide">
      <div class="container">
          <div class="box">

              <div class="title">
                  <h1>Sign up</h1>
              </div>

              <form  autocomplete="off">
                  <label for="#" class="email_field" autocomplete="off">
                      <input
                        type="text"
                        placeholder="name"
                        autocomplete="off"
                        v-if="!regCodeInputActive"
                        v-model="regName"
                      >
                      <input
                        v-if="regCodeInputActive"
                        type="text"
                        name="code"
                        placeholder="code from SMS"
                        v-model="regConfirmationCode"
                      />
                  </label>

                  <PhoneInput
                    @update="updatRegPhone"
                    v-model="regLocalPhoneNumber"
                    fetch-country="false"
                    no-flags="false"
                    size="sm"
                    v-if="!regCodeInputActive"
                  ></PhoneInput>

                  <label
                    for="#"
                    class="email_field"
                    autocomplete="off"
                    v-if="!regCodeInputActive"
                  >
                      <input
                        type="text"
                        placeholder="phone"
                        autocomplete="off"
                        v-model="regPhoneNumber"
                      >

                  </label>


                  <button
                    class="auth-btn"
                    name="code"
                    v-if="!regCodeInputActive"
                    v-bind:disabled="regPhoneNumber == ''"
                    v-on:click.prevent="getRegConfirmationCode"
                  >ok. go</button>
                  <button
                    class="auth-btn"
                    name="confirm"
                    v-if="regCodeInputActive"
                    v-bind:disabled="regConfirmationCode == ''"
                    v-on:click.prevent="regConfirmAccount"
                  >let me in</button>

              </form>

          </div>
      </div>
    </div>

  </div>
</template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
import VuePhoneNumberInput from 'vue-phone-number-input'
import 'vue-phone-number-input/dist/vue-phone-number-input.css'

Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'LoginForm',
  components:{
    PhoneInput: VuePhoneNumberInput
  },
  data() {
    return {
      loader: null,

      codeInputActive: false,
      invitationActive: false,

      phoneNumber: '',
      localPhoneNumber: '',
      confirmationCode: '',
      country: '',

      regActive: false,
      regCodeInputActive: false,
      regConfirmationCode: '',
      regPhoneNumber: '',
      regLocalPhoneNumber: '',
      regName: '',
      regCountry: '',
      
      countries: []
    }
  },
  mounted() {
    fetch(window.location.origin + '/static/app/countries.json')
    .then(res => res.ok && res.json())
    .then(res => { this.countries = res ? res : [] })
  },
  methods: {
    getConfirmationCode: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/login'
        var data = {
          phone_number: this.phoneNumber,
          country: this.country
        }
        this.$http.post(url, data).then(response => {
        this.searchResults = response.data
        this.loader.hide()
        this.codeInputActive = true
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    confirmAccount: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/confirmation'
        var data = {
          'phone_number': this.phoneNumber,
          'confirmation_code': this.confirmationCode
        }
        this.$http.post(url, data).then(response => {
          this.loader.hide()
          var tokenStorage
          var wsUserMeta = response.data['workspaces_user_meta']
          tokenStorage = window.localStorage
          tokenStorage.setItem('token', '"' + wsUserMeta['auth_token'] + '"')
          tokenStorage.setItem('userInfo', JSON.stringify(wsUserMeta))

          this.invitationActive = true
          this.codeInputActive = false
          this.storeTeleportToken(response.data['teleport_user_meta'])
          document.location.href="/?" + document.location.href.split('?')[1]
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    getRegConfirmationCode: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/login'
        var data = {
          'user_name': this.regName,
          'phone_number': this.regPhoneNumber
        }
        this.$http.post(url, data).then(response => {
        this.searchResults = response.data
        this.loader.hide()
        this.regCodeInputActive = true
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    regConfirmAccount: function () {
        this.loader = this.$loading.show({zIndex: 30,})
        var url = document.location.protocol + '//'
            url += document.location.host.replace('8080', '8000')
            url += '/api/accounts/confirmation'
        var data = {
          'phone_number': this.regPhoneNumber,
          'confirmation_code': this.regConfirmationCode
        }
        this.$http.post(url, data).then(response => {
          this.loader.hide()
          var tokenStorage
          var userMeta = response.data['user_meta']
          tokenStorage = window.localStorage
          tokenStorage.setItem('token', '"' + userMeta['auth_token'] + '"')
          tokenStorage.setItem('userInfo', JSON.stringify(userMeta))

          this.regCodeInputActive = true
          this.invitationActive = false
          document.location.href="/email"
        }).catch(error => {
            console.log('Login api is unavailable at the moment')
            console.log(error)
            this.loader.hide()
        });
    },
    storeTeleportToken: function (teleportData) {
      // set localStorage items
      var tokenStorage
      tokenStorage = window.localStorage;
      tokenStorage.setItem('mx_access_token', teleportData.access_token);
      tokenStorage.setItem('mx_user_id', teleportData.user_id);
      tokenStorage.setItem('mx_crypto_initialised', 'false');
      tokenStorage.setItem('mx_device_id', teleportData.device_id);
      tokenStorage.setItem('mx_hs_url', 'https://' + teleportData.home_server);
      tokenStorage.setItem('mx_is_guest', 'false');
      tokenStorage.setItem('mx_is_url', 'https://' + teleportData.home_server);
      tokenStorage.setItem('mxjssdk_memory_filter_FILTER_SYNC_' + teleportData.user_id, '0');
      // fill Session storage in Indexed DB
      // window.indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB;
      // window.IDBTransaction = window.IDBTransaction || window.webkitIDBTransaction || window.msIDBTransaction || {READ_WRITE: "readwrite"};
      // window.IDBKeyRange = window.IDBKeyRange || window.webkitIDBKeyRange || window.msIDBKeyRange;
      // var request = window.indexedDB.open("matrix-js-sdk:riot-web-sync", 3);
      // console.log(request)
      // request = window.indexedDB.open("matrix-js-sdk:crypto", 3);
      // console.log(request)
      /* */
      console.log(teleportData)
      return
    },
    updateLoginPhone(data) {
      if(data.countryCallingCode && data.phoneNumber){
        this.phoneNumber = data.countryCallingCode + data.nationalNumber

        const countryObj = this.countries.find(c => `+${data.countryCallingCode}` == c.dial_code)
        this.country = countryObj ? countryObj.name : ''
      }
    },
    updateRegPhone(data){
      if(data.countryCallingCode && data.phoneNumber){
        this.regPhoneNumber = data.countryCallingCode + data.nationalNumber
        
        const countryObj = this.countries.find(c => `+${data.countryCallingCode}` == c.dial_code)
        this.regCountry = countryObj ? countryObj.name : ''
      }
    }
  }
}
</script>

<style scoped>
  .no-gutter {
    padding: 0 !important;
  }
  .no-gutter .column {
    padding: 0 !important;
  }
  .phone-input__cont *{
    width: unset !important;
  }
  .country-selector__list{
    overflow: auto;
    max-height: 150px;
  }
  .country-selector__input{
    width: 40px;
  }
</style>
