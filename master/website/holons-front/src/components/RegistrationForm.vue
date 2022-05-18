<template>
  <div class="login">
    <h1>Account setup</h1>
    <form id="login-form" class="ui form">
        <div class="field" v-if="!codeInputActive && !success">
          <label>
            Your mobile phone number
          </label>
          <div class="ui input">
            <input
              type="text"
              name="phone"
              v-model="phoneNumber"
              placeholder="digits only"
            />
          </div>
        </div>
        <div class="field" v-if="!codeInputActive && !success">
          <label>
            Enter your desired username
          </label>
          <div class="ui input">
            <input
              type="text"
              name="username"
              v-model="userName"
            />
          </div>
        </div>
        <div class="field">
        <div class="code"
          v-if="codeInputActive && !success"
        >
          <label>Enter the code we've just sent you via SMS</label>
          <div class="ui input">
            <input
              type="text"
              name="code"
              v-model="confirmationCode"
            />
          </div>
        </div>
        <div class="get-code"
          v-if="!codeInputActive && !success">
          <button
            name="code"
            class="ui button"
            v-bind:disabled="phoneNumber  == '' || userName == ''"
            v-on:click.prevent="getConfirmationCode">
            Get confirmation code
          </button>
        </div>
        <div class="get-code"
          v-if="codeInputActive && !success">
          <button
            name="confirm"
            class="ui button"
            v-on:click.prevent="confirmAccount">Confirm your account
          </button>
        </div>
        <div class="success"
          v-if="success">
          You're successully logged in.
        </div>
      </div>

    </form>
  </div>
</template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'RegistrationForm',
  data() {
    return {
      loader: null,
      codeInputActive: false,
      invitationActive: false,
      phoneNumber: '',
      userName: '',
      confirmationCode: '',
      success: false
    }
  },
  mounted() {
    //
  },
  methods: {
    getConfirmationCode: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/accounts/login'
        this.$http.post(url, {'phone_number': this.phoneNumber, 'username': this.userName}).then(response => {
        this.searchResults = response.data
        this.loader.hide()
        this.codeInputActive = true
      }).catch(error => {
          console.log('Login api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
      console.log(url)
    },
    confirmAccount: function () {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/accounts/confirmation'
        this.$http.post(url, {'phone_number': this.phoneNumber, 'confirmation_code': this.confirmationCode}).then(response => {
        this.loader.hide()
        this.invitationActive = true
        this.codeInputActive = false
        this.success = true

        console.log(response.data)
        var tokenStorage
        tokenStorage = window.localStorage;
        tokenStorage.setItem('token', '"' + response.data['user_meta']['auth_token'] + '"');
        tokenStorage.setItem('userInfo', JSON.stringify(response.data['user_meta']));
        document.location.href="/"

      }).catch(error => {
          console.log('Login api is unavailable at the moment')
          console.log(error)
          this.loader.hide()
      });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login {
    padding: 3em;
  }
  .vld-background,
  .vld-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  .vld-icon {
    position: absolute;
    top: 50%;
    left: 50%;
  }
  .code,
  .field {
    margin-bottom: 10px;
  }
</style>
