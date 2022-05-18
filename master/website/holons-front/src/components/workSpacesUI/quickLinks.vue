<template>
  <div class="project-header__quick-links">
    <div class="quick-links__links">
      <sui-label v-for="link in links" :key="link.name" class="quick-links__link">
        <a :href="link.url" target="_blank" rel="noopener noreferrer">
          {{ link.name }}
        </a>
        <span class="quick-links__del" @click="deleteLink(link)">×</span>
        <span class="quick-links__link--icon"><i class="linkify icon"></i></span>
      </sui-label>
      <sui-button size="mini" @click="addNew = true" class="ui basic button">+ quick link</sui-button>
      <div v-if="addNew" class="quick-links__close-overlay" @click="addNew = false"></div>
      <div v-if="addNew" class="quick-links__add-link">
        <sui-input v-model="newLinkName" placeholder="Link name" />
        <sui-input v-model="newLinkURL" placeholder="Link URL" />
        <div class="quick-links__spacer">
          <span v-if="addError" class="add-link__error">Please enter link name and URL</span>
        </div>
        <sui-button @click="addNewLink">Add Link</sui-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    activeProject: {
      type: Object,
      default: () => {}
    },
    sendRequest: {
      type: Function,
      default: () => {}
    },
  },
  data() {
    return {
      links: this.getLinks(),
      addNew: false,
      newLinkName: '',
      newLinkURL: '',
      addError: false
    }
  },
  methods: {
    getLinks() {
      const linksArr = this.activeProject.description.split('\n').filter(l => l !== '')
      return linksArr.map(l => {
        const lArr = l.split('+')
        return {
            name: lArr[0],
            url: lArr[1]
          }
      })
    },
    addNewLink() {
      if (this.newLinkName === '' && this.newLinkURL === '') {
        this.addError = true
        setTimeout(() => {
          this.addError = false
        }, 2000);
      } else {
        this.activeProject.description = this.activeProject.description + '\n' + this.newLinkName + '+' + this.newLinkURL
        this.update()
        this.newLinkName = ''
        this.newLinkURL = ''
        this.addNew = false
      }
    },
    deleteLink(link) {
      let name = link.name || ''
      let url = link.url ? '+' + link.url : ''
      let deleteString = name + url
      let newDesc = this.activeProject.description.replace(deleteString, '')
      if (newDesc === '') {
        newDesc = '\n'
      }
      this.activeProject.description = newDesc
        this.update()
    },
    update() {
      this.links = this.getLinks()
      this.sendRequest('projects/' + this.activeProject.id, 'patch', {
        description: this.activeProject.description
      })
    }
  },
  watch: {
    'activeProject.description': {
      handler() {
        this.links = this.getLinks()
      }
    }
  },
}
</script>
