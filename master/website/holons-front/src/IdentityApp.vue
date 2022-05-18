<template src="./templates/identity.html" />

<script>

import Cropper from 'cropperjs'
import FileUpload from 'vue-upload-component'

export default {
  name: 'IdentityApp',
  components: {
    FileUpload,
  },
  data() {
    return {
      loader: null,
      files: [],
      edit: false,
      cropper: false,
      username: '',
      handle: '',
      updateProfile: false,
    }
  },
  computed: {
    csrfToken: function () {
      return window.csrftoken
    },
    apiUrl: function () {
      var url = document.location.protocol + '//' + document.location.host.replace('8080', '8000')
          url += '/api/accounts/'
      return url
    },
    defaultUserpic: function () {
      if(window.userpic != ''){
        return window.userpic
      } else {
        return 'https://www.gravatar.com/avatar/default?s=200&r=pg&d=mm'
      }
    },
    defaultUsername: function () {
      return window.username
    },
    defaultHandle: function () {
      return window.handle
    },
  },
  watch: {
    edit(value) {
      if (value) {
        this.$nextTick(function () {
          if (!this.$refs.editImage) {
            return
          }
          let cropper = new Cropper(this.$refs.editImage, {
            aspectRatio: 1 / 1,
            viewMode: 2,
            responsive: true,
          })
          this.cropper = cropper
        })
      } else {
        if (this.cropper) {
          this.cropper.destroy()
          this.cropper = false
        }
      }
    },
    handle(newValue, oldValue){
      if(newValue != oldValue && newValue != this.defaultHandle){
        if(!this.updateProfile){
          this.updateProfile = setTimeout(this.updatePData, 1000)
        }
      }
    }
  },
  mounted() {
    this.username = this.defaultUsername
    this.handle = this.defaultHandle
  },
  methods: {
    updatePData() {
      this.saveProfile(false)
      clearTimeout(this.updateProfile)
      this.updateProfile = false
    },
    saveProfile(closeModal=true) {
      if(closeModal){
        this.loader = this.$loading.show({zIndex: 30,})
      }
      var url = this.apiUrl + 'edit'
      var data = {
        username: this.username,
        handle: this.handle
      }
      this.$http.post(url, data).then(response => {
        if(response){
          this.handle = response.data.user.handle
          if(closeModal){
            this.loader.hide()
          }
          this.$forceUpdate()
          var jQuery = window.$
          jQuery('.username_str').text(this.username)
          if(closeModal){
            jQuery('#identitySettings').removeClass('active')
          }
        }
      }).catch(error => {
        console.log(['Accounts api is unavailable at the moment', error])
        this.loader.hide()
      });
    },
    editSave() {
      this.edit = false
      let oldFile = this.files[0]
      let binStr = atob(this.cropper.getCroppedCanvas().toDataURL(oldFile.type).split(',')[1])
      let arr = new Uint8Array(binStr.length)
      for (let i = 0; i < binStr.length; i++) {
        arr[i] = binStr.charCodeAt(i)
      }
      let file = new File([arr], oldFile.name, { type: oldFile.type })
      this.$refs.upload.update(oldFile.id, {
        file,
        type: file.type,
        size: file.size,
        active: true,
      })
    },
    inputFile(newFile, oldFile, prevent) {
      console.log(prevent)
      if (newFile && !oldFile) {
        this.$nextTick(function () {
          this.edit = true
        })
      }
      if (!newFile && oldFile) {
        this.edit = false
      }
      if (newFile && newFile.success) {
        var jQuery = window.$
        console.log(this.$refs.upload.files[0])
        console.log(this.$refs.upload.files[0].response)
        console.log(this.$refs.upload.files[0].response['image-src'])
        jQuery('.sidebar .identity__img').attr('src', this.$refs.upload.files[0].response['image-src'])
      }

    },
    inputFilter(newFile, oldFile, prevent) {
      if (newFile && !oldFile) {
        if (!/\.(gif|jpg|jpeg|png|webp)$/i.test(newFile.name)) {
          return prevent()
        }
      }
      if (newFile && (!oldFile || newFile.file !== oldFile.file)) {
        newFile.url = ''
        let URL = window.URL || window.webkitURL
        if (URL && URL.createObjectURL) {
          newFile.url = URL.createObjectURL(newFile.file)
        }
      }
    },
  }
}
</script>

<style>
.avatar .avatar-upload .rounded-circle {
  width: 200px;
  height: 200px;
}
.avatar .text-center .btn {
  margin: 0 .5rem
}
.avatar .avatar-edit-image {
  max-width: 100%
}
.avatar .drop-active {
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 9999;
  opacity: .6;
  text-align: center;
  background: #000;
}
.avatar .drop-active h3 {
  margin: -.5em 0 0;
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
  font-size: 40px;
  color: #fff;
  padding: 0;
}
</style>
