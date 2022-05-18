<template>
  <div class="subscription-holder">
    <div
      v-if="!paymentActive"
    >
      <button
        class="ui button"
        v-on:click.prevent="activatePaymentForm"
      >
        Subscribe
      </button>
      <p>for Plato's Flywheel $15 monthly payment</p>
      <p>
        <span
          class="ui button"
          v-on:click.prevent="activateEarlyAdopterModal"
        >
          Become early adopter $240
        </span>
      </p>
    </div>
    <div
      v-bind:class="{'hidden': !paymentActive}"
      v-if="!paymentSuccess"
    >
      <h3 style="width: 100%; clear: both">Subscription payment</h3>  
      <p>Monthly price 15 USD</p>
      <form id="payment-form">
        <div id="card-element">
          <!-- Elements will create input elements here -->
        </div>

        <!-- We'll put the error messages in this element -->
        <div id="card-errors" role="alert"></div>

        <button
          id="card-button"
          v-on:click.prevent="submit"
        >Submit Payment</button>
      </form>
    </div>
    <div v-else >
      <h3>Subscription successful</h3>
    </div>

    <div
      id="early-adopter-modal"
      class="hm modal"
      v-bind:class="{'active': showEarlyAdopterModal}"
    >
      <div class="content">
          <h2>
          Become early adopter
          </h2>
          <button
            class="ui button"
            v-on:click.prevent="showLogin = true"
          >
            Login and pay
          </button>
          <div
            v-if="showLogin"
            class="login">
              <div
                    class=""
                  >
                  <div class="">
                      <form
                        class="ui form"
                        id="login-form"
                        autocomplete="off"
                      >

                          <label
                            for="#"
                            class="phone_field"
                            autocomplete="off"
                          >

                              <input
                                type="text"
                                placeholder="phone number in internationnaal format w/o pllus sign :D"
                                autocomplete="off"
                                name="phone"
                                v-if="!codeInputActive"
                                v-model="phoneNumber"
                              >

                          </label>
                          <label
                            for="#"
                            class="code_field"
                            autocomplete="off"
                          >
                              <input
                                v-if="codeInputActive"
                                type="text"
                                name="code"
                                placeholder="code from SMS"
                                v-model="confirmationCode"
                              />

                          </label>

                          <br>

                          <div class="ui field">
                          <button
                            class="auth-btn btn ui basic button"
                            name="code"
                            v-if="!codeInputActive"
                            v-bind:disabled="phoneNumber == ''"
                            v-on:click.prevent="getConfirmationCode"
                          >ok.go</button>
                          </div>
                          <div class="ui field">
                          <button
                            class="auth-btn btn ui basic button"
                            name="confirm"
                            v-if="codeInputActive"
                            v-bind:disabled="confirmationCode == ''"
                            v-on:click.prevent="confirmAccount"
                          >let.me.in</button>
                          </div>
                      </form>
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

Vue.use(Loading, {
    zIndex: 9999,
})

export default {
  name: 'SubscriptionApp',
  data() {
    return{
      loader: null,
      customerId: null,
      clientSecret: '',
      subscriptionId: '',
      stripe: null,
      card: null,
      elements: null,
      paymentActive: false,
      paymentSuccess: false, 
      showEarlyAdopterModal: false,
      productId: '',
      showLogin: '',
    }
  },
  computed: {
    csrfToken: function () { return window.csrftoken },
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/subscribe'
      return url
    },
  },
  mounted() {
    // this.getSecret()
    this.createCustomer()
  },
  methods: {
    /*
    getSecret() {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/secret'
      this.$http.post(url).then(response => {
        this.clientSecret = response.data.client_secret
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Subscription api is unavailable at the moment', error])
      });
      this.loader.hide()
    },
    */
    activatePaymentForm() {
      this.paymentActive = true
      this.createCustomer()
      var style = {
        base: {
          color: "#32325d",
        }
      };
      this.stripe = Stripe('pk_test_51Id0AKL8b8L0s6Ju6j7Mzj1gkNcH1yObWYDH5UcjSLH0fGzqyZ26Moq6sHUV13txiuMi4LqFMLWpmAtnDhlW8sWF00ERn97Eso')
      this.elements = this.stripe.elements();
      this.card = this.elements.create("card", { style: style });
      this.renderForm()
    },
    renderForm() {
        this.card.mount("#card-element");
        this.card.on('change', ({error}) => {
          let displayError = document.getElementById('card-errors');
          if (error) {
            displayError.textContent = error.message;
          } else {
            displayError.textContent = '';
          }
        });
    },
    createEarlyAdopter() {
      var url = this.apiUrl + '/create-early-adopter'
      this.$http.post(url).then(response => {
        this.clientId = response.data.client_id
        this.clientSecret = response.data.client_secret
        this.productId = response.data.product_id
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Payment api is unavailable at the moment', error])
      });
    },
    createCustomer() {
      var url = this.apiUrl + '/create-customer'
      this.$http.post(url).then(response => {
        this.clientId = response.data.client_id
        this.clientSecret = response.data.client_secret
        this.subscriptionId = response.data.subscription_id
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Subscription api is unavailable at the moment', error])
      });
    },
    submit () {
      this.loader = this.$loading.show({zIndex: 30,})
      this.stripe.confirmCardPayment(this.clientSecret, {
        payment_method: {
          card: this.card,
          billing_details: {
            name: window.handle,
          }
        },
        setup_future_usage: 'off_session'
      }).then(result => {
        if (result.error) {
          // Show error to your customer (e.g., insufficient funds)
          console.log(result.error.message);
        } else {
          // The payment has been processed!
          if (result.paymentIntent.status === 'succeeded') {
            // Show a success message to your customer
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            console.log('success')
            this.paymentSuccess = true
          }
        }
        this.loader.hide()
      });
    },
    activateEarlyAdopterModal () {
      this.showEarlyAdopterModal = true
      // this.createEarlyAdopter()
    }
  }
};
</script>

<style scoped>
  .subscription-holder {
    width: 400px;
  }
  .hidden {
    display: none !important;
  }
</style>
