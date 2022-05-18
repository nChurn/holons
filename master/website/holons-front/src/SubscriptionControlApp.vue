<template>
  <div id="subscriptionControl" class="hm modal">
      <div class="content">
        <h3>Your subscriptions</h3>
        <table class="ui table">
          <tr
            v-for="item in subscriptions"
            v-bind:key="item.id"
          >
            <td>{{ item.id }}</td>
            <td>{{ item.subscription_type }}</td>
            <td>{{ item.expires_at }}</td>
            <td>
              <button
                class="ui button"
                v-on:click.prevent='confirmCancelSubscription(item.id)'
                v-if="confirmCancelId != item.id"
              >&times;&nbsp;cancel</button>
              <span
                v-else
              >
              Are you sure you want to cancel? 
              <button class="mini ui button red"
                v-on:click.prevent='cancelSubscription(item.id)'
              >
                Yes
              </button>
              <button
                class="mini ui button"
                v-on:click.prevent='confirmCancelId = null'
              >
                no
              </button>
              </span>
            </td>
              
          </tr>
        </table>
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
  name: 'SubscriptionControlApp',
  data() {
    return{
      loader: null,
      showModal: false,
      subscriptions: [],
      confirmCancelId: null,
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
    this.getSubscriptions()
  },
  methods: {
    getSubscriptions() {
      // this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/all'
      this.$http.get(url).then(response => {
        this.subscriptions = response.data.subscriptions
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Subscription api is unavailable at the moment', error])
      });
      // this.loader.hide()
    },
    confirmCancelSubscription(itemId) {
      this.confirmCancelId = itemId
    },
    cancelSubscription(itemId) {
      this.loader = this.$loading.show({zIndex: 30,})
      var url = this.apiUrl + '/cancel/' + itemId
      this.$http.post(url).then(response => {
        console.log(response.data)
        this.getSubscriptions()
        this.confirmCancelId = null
        this.loader.hide()
        this.$forceUpdate()
      }).catch(error => {
        console.log(['Subscription api is unavailable at the moment', error])
      });
      this.loader.hide()

    }
  }
};
</script>

<style scoped>
</style>
