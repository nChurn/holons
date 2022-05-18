<template>
  <div class="email_compose_modal modal">
    <div class="settings">
      <div class="email_compose ui grid">
          <div class="fourteen wide column">
            <h1>New message</h1>
            <p>For now you can edit *from* and *to* addresses manually</p>
              <div class="field">
                <label for="select_mailbox"></label>
                <select
                  v-model="fromEmail"
                  v-on:change="selectMailbox"
                >
                  <option value="">Select a mailbox</option>
                  <option 
                    v-for="mailbox in mailboxes"
                    v-bind:key="mailbox.id"
                    v-bind:value="mailbox.alias + '@' + mailbox.domain"
                    >
                    {{ mailbox.alias }}@{{ mailbox.domain }}
                  </option>
                </select>
              </div>
              <email-form
                v-bind:mailboxEmail="fromEmail"
                v-bind:toEmail="toEmail"
                v-bind:emailSubject="emailSubject"
                v-bind:mailboxAlias="selectedMailbox"
                v-bind:quotedBody="quotedBody"
                v-bind:conversation="''"
                v-bind:sendButtonText="'Send and close'"
              />
          </div>
          <div class="two wide right aligned column">
            <span
                v-on:click.prevent="closeModal()"
                class="ui cancel"
              ><i class="window close icon"></i>
            </span>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'EmailComposeModal',
  data() {
    return {
      mailboxes: [],
      fromEmail: '',
      selectedMailbox: ''
    }
  },
  mounted() {
    console.log('Email Compose Modal')
    this.getMailboxesAddresses()
  },
  methods: {
    closeModal: function () {
      this.$parent.emailComposeModal = false
    },
    getMailboxesAddresses: function () {
      this.mailboxes = this.$parent.mailboxes.active
      this.selectMailbox()
    },
    selectMailbox: function() {
      for(var m in this.mailboxes){
        // console.log(this.mailboxes[m].name + ' ' + this.mailboxes[m].alias + '@' + this.mailboxes[m].domain)
        if(this.mailboxes[m].alias + '@' + this.mailboxes[m].domain == this.fromEmail){
          this.selectedMailbox = this.mailboxes[m].name
        }
      }
    } 
        
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
    top: 2%;
    margin: 0 auto;
    position: relative;
    width: 70%;
  }
  .field {
    margin-bottom: 10px;
  }
  .cancel {
    cursor: pointer; 
  }
</style>