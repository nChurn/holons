<template v-else>
  <div id="app">
    <login-form v-if="showLogin"></login-form>
    <moneta-ui v-if="showMoneta" />
    <ws-creator v-if="showWsCreator" v-bind:ws-prefix="wsPrefix" v-bind:ws-title="wsTitle" />
    <work-spaces v-if="showWorkspaces" />
    <campaigns-ui v-if="showCampaigns"></campaigns-ui>
    <email-ui v-if="showEmailUi"></email-ui>
    <rays-ui v-if="showRaysUi"></rays-ui>
    <platos-flywheel-ui v-if="showPlatosFlywheel"></platos-flywheel-ui>
    <talents-ui v-if="showTalentsUi"></talents-ui>
    <calendar-ui v-if="showCalendarUi"></calendar-ui>
    <purpose-ui v-if="showPurposeUi"></purpose-ui>
    <registration-form v-if="showLogin"></registration-form>
    <timetracker-ui v-if="timeTrackerUiIsActive"></timetracker-ui>
    <button
      class="hotkeys-handler"
      v-shortkey="{
        agenda: ['a'],
        agendaCyr: ['ф'],
        relations: ['r'],
        relationsCyr: ['к'],
        layers: ['l'],
        layersCyr: ['д'],
        moneta: ['m'],
        monetaCyr: ['ь'],
        identity: ['i'],
        identityCyr: ['ш'],
        faith: ['v'],
        faithCyr: ['м'],
        broker: ['b'],
        brokerCyr: ['и'],
        purpose: ['p'],
        purposeCyr: ['з'],
        rays: ['1'],
        teleport: ['2'],
        email: ['3'],
        schedule: ['4'],
        magic: ['5'],
        //xo: ['5'],
        platos: ['6'],
        //outreach:['7'],
        //dial: ['8'],
        //digest: ['9'],
        //hearsay: ['0'],
        fullscreen: ['f'],
        fullscreenCyr: ['а'],
      }"
      @shortkey="shortkeyGoTo"
    />
  <custom-loader v-if="false" />
  </div>
</template>

<script>
import CustomLoader from './components/CustomLoader'

export default {
  name: 'App',
  components: {
    CustomLoader
  },
  data() {
    return {
      loader: null,
      showLogin: false,
      showWorkspaces: false,
      showCampaigns: false,
      showEmailUi: false,
      showRaysUi: false,
      showPlatosFlywheel: false,
      showRegistration: false,
      fullTemplate: false,
      showTalentsUi: false,
      showWsCreator: false,
      showAgenda: false,
      showMoneta: false,
      wsPrefix: '',
      wsTitle: '',
      timeTrackerUiIsActive: '',
      showCalendarUi: false,
      showPurposeUi: false,
      magicLink: 'https://magic1.teleport.holons.me/' + this.$generateRandomPhrase()
    }
  },
  async created() {
    this.loader = this.$loading.show({
      zIndex: 90,
    },{
      default: this.$createElement('CustomLoader', {
        props: {
          entry: 'created'
        }
      }),
    })
    await this.checkUrl()
    setTimeout(() => {
      this.loader.hide()
    }, 7000);
  },
  mounted() {
    const magicLinkElement = document.getElementById("magic1_start_link");
    if (magicLinkElement) {
      magicLinkElement.href = this.magicLink;
      magicLinkElement.addEventListener('click',  event => {
        event.preventDefault()
        location.href = this.copyMagicLink(this.magicLink) + '#copied';
      })
    }
  },
  methods: {
    checkUrl: function () {
        var location = window.location
        if (location.href.indexOf('login') > 0) {
            this.showLogin = true
        }
        if (location.href.indexOf('auth') > 0) {
            this.showLogin = true
        }
        if (location.href.indexOf('relations') > 0) {
            this.showWsCreator = true
            this.wsPrefix = '__crm'
            this.wsTitle = 'Create New CRM'
        }
        if (window.relationsIsActive) {
            this.showWsCreator = true
            this.wsPrefix = '__crm'
            this.wsTitle = 'Create New CRM'
        }
        if (location.href.indexOf('workspaces') > 0) {
            this.showWorkspaces = true
        }
        if (location.href.indexOf('campaigns') > 0) {
            this.showCampaigns = true
        }
        if (location.href.indexOf('email') > 0) {
            this.showEmailUi = true
        }
        if (location.href.indexOf('rays') > 0) {
            this.showRaysUi = true
        }
        if (location.href.indexOf('platos-flywheel') > 0) {
            this.showPlatosFlywheel = true
        }
        if (location.href.indexOf('talent') > 0) {
            this.showTalentsUi = true
        }
        if (location.href.indexOf('finish-account-setup') > 0) {
            this.showRegistration = true
        }
        // @todo: maybe get rid of url-related checks and switch to something like this?
        // looks more comfortable
        if (window.layersIsActive) {
            this.showWorkspaces = true
        }
        if (window.agendaIsActive) {
            this.showAgenda = true
        }
        if (window.monetaIsActive) {
            this.showMoneta = true
        }
        if (window.calendarIsActive) {
            this.showCalendarUi = true
        }
        if (window.timeTrackerUiIsActive) {
            this.timeTrackerUiIsActive = true
        }
        if (window.purposeIsActive) {
            this.showPurposeUi = true
        }
    },
    copyMagicLink (link) {
      const pathName = document.createElement("input");
      pathName.type = "text";
      pathName.value = link;
      document.body.appendChild(pathName);
      pathName.focus();
      pathName.select();
      document.execCommand('copy');
      document.body.removeChild(pathName);
      return link;
    },
    shortkeyGoTo(event) {
      switch (event.srcKey) {
        case 'fullscreen':
        case 'fullscreenCyr':
          var screenfull = window.screenfull
          if (screenfull.isEnabled) {
            screenfull.request();
          }
          break
        case 'agenda':
        case 'agendaCyr':
          location.pathname = '/'
          break
        case 'relations':
        case 'relationsCyr':
          location.pathname = '/relations'
          break
        case 'layers':
        case 'layersCyr':
          location.pathname = '/layers'
          break
        case 'moneta':
        case 'monetaCyr':
          location.pathname = '/moneta'
          break
        case 'purpose':
        case 'purposeCyr':
          location.pathname = '/purpose/';
          break;
        case 'identity':
        case 'identityCyr':
          location.pathname = '/identity'
          break
        case 'broker':
        case 'brokerCyr':
          location.pathname = '/broker'
          break
        case 'faith':
        case 'faithCyr':
          location.pathname = '/faith';
          break;
        case 'rays':
          location.pathname = '/rays'
          break
        case 'teleport':
          location.href = 'https://teleport.holons.me/auth/'
          break
        case 'magic':
          location.href = this.copyMagicLink(this.magicLink) + '#copied';
          break
        case 'email':
          location.pathname = '/email'
          break
        case 'schedule':
          location.pathname = '/schedule'
          break
        case 'xo':
          location.pathname = '/xo'
          break
        case 'platos':
          location.pathname = '/platos-flywheel'
          break
        case 'outreach':
          location.pathname = '/outreach'
          break
        case 'dial':
          location.pathname = '/dial'
          break
        case 'digest':
          location.pathname = '/digest'
          break
        case 'hearsay':
          location.pathname = '/hearsay'
          break
      }
    },
  }
}
</script>

<style>
  .hotkeys-handler {
    opacity: 0;
  }
  .white-block {
    overflow: hidden;
  }
  .finish-account-setup {
    color: rgba(255, 255, 255, 0.35);
  }
  .finish-account-setup:hover {
    color: rgba(255, 255, 255, 0.35);
  }
</style>
