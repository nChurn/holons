<template>
  <div class="attached-mailboxes" >

    <div v-if="rays.active">
        <div class="item__wrapper"
            v-for="ray in rays.active"
            v-bind:key="ray.id"
        >
          <div class="email-inboxes__item"
            v-if="ray.short_name != 'Upwork'"
            v-bind:class="{ active: $parent.selectedRay == ray }"
          >
                <!--<img class="platos-ray__owner"
                src="https://holons.me/usg/usg/soulspics/__a0_c2c8XI.jpg">-->
                <div
                    class="ray__settings button"
                    v-on:click.prevent="$parent.showRaySettingsModal(ray)"
                >
                  <i class="wrench icon button"></i>
                </div>
              <div class="thread-previews__item--name"
              style="padding-right: 20px"
                v-on:click.prevent="$parent.selectedRay = ray; $parent.isCustom = false; $parent.selectedFixedRay = {}"
              >
                {{ ray.short_name }}
                <span
                  v-if="ray.total_count > 0"
                  class="platos-ray__notifications-count"
                >{{ ray.total_count }}</span>

              </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PlatosRaysAttached',
  props: [
    'rays',
  ],
  data() {
    return {
      //
    }
  },
  mounted() {
    console.log('Rays Attached UI')
  },
  methods: {
    selectFixedRay: function(rayName) {
      if (rayName !== 'upwork') {
        console.log(rayName)
        var ray = rayName
        this.$parent.selectedRay = {}
        this.$parent.selectedFixedRay.short_name = ray
        this.$parent.isCustom = true
        this.$parent.selectedFixedRay.messages = []
        for(var ray_id in this.rays.fixed){
          if (Object.keys(this.rays.fixed[ray_id])[0] == ray.toLowerCase()){
            var messages = this.rays.fixed[ray_id][Object.keys(this.rays.fixed[ray_id])[0]]
            for (var message in messages) {
              this.$parent.selectedFixedRay.messages.push(messages[message])
            }
          }
        }
        this.$forceUpdate()
      }
      if (rayName === 'upwork') {
        this.$parent.selectedRay = this.rays.active[this.rays.active.length - 1]
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .email-inboxes__item {
    cursor: pointer;
  }
  .ray__settings {
    display: none;
    position: absolute;
    right: 5px;
    width: 16px;
    height: 16px;
    font-size: 18px;
    cursor: pointer;
    color:rgba(0, 0, 0, 0.35)
  }
  .ray__settings:hover { color: #23272B }
  .email-inboxes__item:hover .ray__settings {
    display: block;
  }
  .email-inboxes__item:hover .platos-ray__notifications-count { display: none }
  .notifications-count {
    background: #fff;
  }
  .item__special {
    min-height: 42px;
    /*border-top: none;*/
    /*border-bottom: 2px solid black;*/
  }
  .item__special img {
      position: absolute;
      top: 7px;
      left: 5px;
      width: 35px;
      height: auto;
    }
  .item__special__moneta img, .item__special__fora img {
    top: 7px;
  }
  .item__special .thread-previews__item--name {
    padding: 0 0 0 30px;
  }
  .item__special img {
    position: absolute;
    top: 7px;
    left: 5px;
    width: 35px;
    height: auto;
  }
  .identity__img {
      border-radius: 50%;
  }
</style>
