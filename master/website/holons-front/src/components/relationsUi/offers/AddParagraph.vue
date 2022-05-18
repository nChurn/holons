<template>
<div class="paragraphs">
  <div
    class="row"
    v-for="(paragraph, index) in paragraphs"
    v-bind:key="index"
  >
    <wysiwyg
      v-if="!preview"
      v-model="paragraphs[index]" />
    <div
      v-else
      v-html="paragraphs[index]"
    >
    </div>
  </div>
  <div style="text-align:right">
    <a
      class="hm link"
      v-html="label"
      v-on:click.prevent="add"
    ></a>
  </div>
</div>
</template>


<script>
import Vue from 'vue'
import wysiwyg from 'vue-wysiwyg'
Vue.use(wysiwyg, {
    hideModules: {
      "image": true,
      "code": true,
      "table": true,
      "headings": true,
      "removeFormat": true,
      "separator": true,
    },
})

export default {
  name: 'AddParagraph',
  props: {
    preview: {
      type: Boolean,
      default: function () { 
        return false
      }
    },
    label: {
      type: String,
      default: function () {
        return '+ paragraph'
      }
    },
    jsonKey: {
      type: String,
      default: function () {
        return 'paragraph-1'
      }
    }
  },
  data() {
    return {
      paragraphs: [],
      paragraph: '',
    }
  },
  watch: {
    paragraphs: function(oldValue, newValue){
      this.$emit(
        'append-paragraph',
        {
          'key': this.jsonKey,
          'paragraph': newValue
        }
      )
    }
  },
  mounted() {},
  methods: {
    add: function() {
      this.paragraphs.push(this.paragraph)
    },
  }
}
</script>
