<template>
    <div
      style="width:100%;margin-bottom:1rem"
      class="ui basic button tiny"
      v-on:click.prevent="openModal"
    >
      + workspace
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
  name: 'AddWorkSpaceButton',
  props: {
    openModal: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      loader: null,
    }
  },
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
</style>
