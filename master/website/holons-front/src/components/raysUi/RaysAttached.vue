<template src="./templates/rays-attached.html" />

<script>
export default {
  name: 'RaysAttached',
  props: ['rays'],
  methods: {
    switchRay: function(ray) {
     this.$parent.selectedRay = ray
     this.$parent.selectedThread = null
     this.$parent.messageSent = false
    },
  }
}
</script>

<style scoped>
  .email-inboxes__item {
    cursor: pointer;
  }
  .ray__settings {
    display: none;
    position: absolute;
    top: 14px;
    left: 0px;
    width: 16px;
    height: 16px;
    font-size: 12px;
    cursor: pointer;
  }
  .email-inboxes__item:hover .ray__settings {
    display: block;
  }
  .notifications-count {
    background: #fff;
  }
  .item__special {
    min-height: 42px;
  }
  .item__special img {
      position: absolute;
      top: 7px;
      left: 5px;
      width: 35px;
      height: auto;
    }
  .item__special__moneta img,
  .item__special__fora img {
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
