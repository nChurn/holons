<template>
  <div class="vld-parent gsap-container" v-if="active">
      <div class="cir"></div>
      <div class="cir"></div>
      <div class="cir"></div>
      <div class="cir"></div>
      <div class="cir"></div>

      <div id="logo">
        <h2 id="logoText">holons.me</h2>
      </div>
  </div>
</template>

<script>
import gsap from "gsap";

export default {
  props: {
    entry: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      timeline: gsap.timeline(),
      active: true,
    };
  },
  mounted() {
    let overlay = document.querySelector('.vld-overlay')
    overlay.style.backgroundColor = '#fff'
    overlay.style.opacity = '1'

    this.timeline.set(".cir", {
      scale: 0,
      transformOrigin: "center",
    })
      .set("#logo", {
        scale: 0.27,
        transformOrigin: "center",
        opacity: 0,
      })
      .to(".cir", {
        ease: "back.out(3)",
        duration: 4,
        scale: gsap.utils.distribute({
          base: 1,
          amount: 3,
          from: "end",
        }),
        stagger: {
          each: 0.4,
        },
      })
      .to(
        "#logo",
        {
          scale: 0.3,
          transformOrigin: "center",
          opacity: 1,
          duration: 3,
        },
        "-=1.5"
      );

    if(this.active){
      setTimeout(() => {
        this.fade()
      }, 5500);
    }
  },
  methods: {
    fade() {
      let bg = document.querySelector('.vld-background')
      let overlay = document.querySelector('.vld-overlay')

      bg.style.opacity = 0;
      overlay.style.opacity = 0
    }
  },
};
</script>

<style lang="css" scoped> 
.gsap-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.vld-parent {
  background: #fff !important;
  opacity: 1 !important;
}

/*#logo {
  width: 100px;
  height: 100px;
  opacity: 0;
   background: red;
} */
#logoText {
  color: #23272B;
  font-size: 7rem
}

.cir {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  box-shadow: 10px 10px 10px 10px rgba(136, 165, 191, 0.1) inset,
    inset -10px -10px 10px #ffffff;
}
</style>
