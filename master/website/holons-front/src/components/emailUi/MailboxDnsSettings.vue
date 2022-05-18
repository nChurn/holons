<template>
  <div>
      <table class="ui celled table">
        <thead>
        <tr>
          <th>Status</th>
          <th>Type</th>
          <th>Host</th>
          <th>Value</th>
        </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <span v-if="mailboxesValidityStatus.validity_status.validation_results.mail_cname.valid">OK</span>
              <span v-else>N/A</span>
            </td>
            <td>CNAME</td>
            <td>{{ mailbox.dns.mail_cname }}</td>
            <td>{{ mailbox.dns.mail_cname_data }}</td>
          </tr>
          <tr>
            <td v-if="mailboxesValidityStatus.mailbox == mailbox.name">
              <span v-if="mailboxesValidityStatus.validity_status.validation_results.dkim1.valid">OK</span>
              <span v-else>N/A</span>
            </td>
            <td v-else>
                <span>N/A</span>
            </td>
            <td>CNAME</td>
            <td>{{ mailbox.dns.dkim1 }}</td>
            <td>{{ mailbox.dns.dkim1_data }}</td>
          </tr>
          <tr>
            <td v-if="mailboxesValidityStatus.mailbox == mailbox.name">
              <span v-if="mailboxesValidityStatus.validity_status.validation_results.dkim2.valid">OK</span>
              <span v-else>N/A</span>
              </td>
              <td v-else><span>N/A</span>
            </td>
            <td>CNAME</td>
            <td>{{ mailbox.dns.dkim2 }}</td>
            <td>{{ mailbox.dns.dkim2_data }}</td>
          </tr>
        </tbody>
      </table>
      <button class="ui button" v-on:click.prevent="closeModal()">Close</button>
      <button class="ui button" v-on:click.prevent="validateDNS($parent.mailbox.name)">Check DNS records</button>
  </div>
<!--   <div>
    444
    <div v-if="!mailbox.is_verified">
      <table class="ui celled table">
        <thead>
        <tr>
          <th>Status</th>
          <th>Type</th>
          <th>Host</th>
          <th>Value</th>
        </tr>
        </thead>
        <tbody>
        <tr>
          <td v-if="mailbox.name == mailbox.name">
            <span v-if="mailboxesValidityStatus.validity_status.validation_results.mail_cname.valid">OK</span>
            <span v-else>N/A</span>
          </td>
          <td v-else>
            <span>N/A</span>
          </td>
          <td>CNAME</td>
          <td>{{ mailbox.dns.mail_cname }}</td>
          <td>{{ mailbox.dns.mail_cname_data }}</td>
        </tr>
        <tr>
          <td v-if="mailboxesValidityStatus.mailbox == mailbox.name">
            <span v-if="mailboxesValidityStatus.validity_status.validation_results.dkim1.valid">OK</span>
            <span v-else>N/A</span>
          </td>
          <td v-else>
              <span>N/A</span>
          </td>
          <td>CNAME</td>
          <td>{{ mailbox.dns.dkim1 }}</td>
          <td>{{ mailbox.dns.dkim1_data }}</td>
        </tr>
        <tr>
          <td v-if="mailboxesValidityStatus.mailbox == mailbox.name">
            <span v-if="mailboxesValidityStatus.validity_status.validation_results.dkim2.valid">OK</span>
            <span v-else>N/A</span>
            </td>
            <td v-else><span>N/A</span>
          </td>
          <td>CNAME</td>
          <td>{{ mailbox.dns.dkim2 }}</td>
          <td>{{ mailbox.dns.dkim2_data }}</td>
        </tr>
        </tbody>
      </table>

      <button class="ui button" v-on:click.prevent="closeModal()">Close</button>
      <button class="ui button" v-on:click.prevent="validateDNS($parent.mailbox.name)">Check DNS records</button>
    </div>
    <div v-else>
      The mailbox is verified, DNS-records look OK.
      <button class="ui button" v-on:click.prevent="closeModal()">Close</button>
    </div>
  </div> -->
</template>

<script>
export default {
  name: 'MailboxDnsSettings',
  props: [
    'mailbox',
    'forceCheckDns'
  ],
  data() {
    return {
      mailboxesValidityStatus: false
    }
  },
  mounted() {
    console.log('Mailbox Dns Settings')
    this.validateDNS(this.mailbox.name)
  },
  computed: {
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/mailboxes/'
      return url
    }
  },
  methods: {
    closeModal: function () {
      this.$parent.closeModal()
    },
     validateDNS: function () {
        var mailboxName = this.mailbox.name
        console.log('Check DNS')
        console.log(mailboxName)
        this.loader = this.$loading.show({zIndex: 30,})
        // ask backend to validate a mailbox for us
        var url = this.apiUrl + 'user_validate_mailbox/' + mailboxName
        this.$http.get(url).then(response => {
          // this.mailbox = response.data
          this.mailboxesValidityStatus = response.data
          console.log('validity check')
          console.log(response.data)
          this.loader.hide()
          this.$forceUpdate()
        }).catch(error => {
          console.log(['Mailbox api is unavailable at the moment', error])
          this.loader.hide()
        });
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>