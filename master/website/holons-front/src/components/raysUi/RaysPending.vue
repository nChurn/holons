<template>
  <div class="attached-mailboxes">
    <div class="email-inboxes__item"
          v-for="ray in rays.pending"
          v-bind:key="ray.id"
        >
            <div class="thread-previews__item--name">
              <strong>{{ ray.alias }}</strong>
            </div>
      </div>
  </div>
</template>

<script>

export default {
  name: 'RaysPending',
  props: [ 
    'rays',
  ],
  data() {
    return {
      //
    }
  },
  mounted() {
    console.log('Rays Pending UI')
    // this.$parent.getRays()
  },
  methods: {
    // 
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>