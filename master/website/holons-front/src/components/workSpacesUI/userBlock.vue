<template>
  <div class="users-span__user">
    <div
      class="users-span__user-frame"
      :style="`background-color:${user.color}`"
      @click="showUserInfo(user)"
    >
      <img width="100%"
      v-if="user.photo != null" :src="user.photo" :alt="user.fullName" />
      <span v-else>{{ user.shortName }}</span>
    </div>
    <div
      v-if="showName"
      class="users-span__user-name"
      @click="showUserInfo(user)"
    >
      {{ user.fullName }}
    </div>
    <div
      class="users-span__details"
      v-if="withDetails && fullUserInfo && fullUserInfo.id === user.id"
      tabindex="0"
      :ref="`userInfo${user.id}`"
    >
      <div
        v-if="fullUserInfo != null"
        class="users-span__user-frame"
        :style="`background-color:${user.color}`"
      >
        <img
          v-if="fullUserInfo.photo != null"
          :src="fullUserInfo.photo"
          :alt="fullUserInfo.fullName"
        />
        <span v-else>{{ fullUserInfo.shortName }}</span>
      </div>
      <div v-if="fullUserInfo != null" class="users-span__user-info">
        <span>{{
          fullUserInfo.fullName +
            (userMe && user.id === userMe.id ? ' (me)' : '')
        }}</span>
        <button
          v-if="showControls && controlFunction === 'remove'"
          @click="delValue('assigned_users', user.id)"
        >
          Remove from card
        </button>
        <button
          v-if="showControls && controlFunction === 'add'"
          @click="addValue('assigned_users', user.id)"
        >
          Add to card
        </button>
      </div>
      <sui-icon
        class="users-span__details-close"
        name="close"
        @click="showUserInfo(null)"
      />
    </div>
    <div
      v-if="fullUserInfo && fullUserInfo.id === user.id"
      class="user-close-overlay"
      @click="showUserInfo(null)"
    ></div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {},
    },
    withDetails: {
      type: Boolean,
      default: false,
    },
    showControls: {
      type: Boolean,
      default: false,
    },
    showName: {
      type: Boolean,
      default: false,
    },
    controlFunction: {
      type: String,
      default: '',
    },
    addValue: {
      type: Function,
      default: () => {},
    },
    delValue: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      fullUserInfo: null,
    }
  },
  methods: {
    showUserInfo(user) {
      this.fullUserInfo = user
    },
  },
}
</script>

<style lang="css">
.users-span__user {
  position: relative;
  margin-right: 0.5rem;
  font-weight: 900;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.users-span__user-frame,
.users-span__user.add-new {
  height: 2.5rem;
  width: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  overflow: hidden;
}
.users-span__user-name {
  margin-left: 0.5rem;
}
.users-span__user.add-new {
  margin-right: 0;
  background-color: #eee;
  font-size: 1.8rem;
}
.users-span__details {
  display: flex;
  padding: 1rem 2.5rem 1rem 1rem;
  width: max-content;
  position: absolute;
  top: 105%;
  left: 0;
  background-color: #fff;
  border: 1px solid #999;
  border-radius: 5px;
}
.project-header__project-users .users-span__details {
  left: unset;
  right: 0;
}
.users-span__details:focus {
  outline: none;
}
.users-span__details .users-span__user-frame {
  min-width: 2.5rem;
}
.users-span__user-info {
  margin-left: 1rem;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.users-span__details-close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}
.user-close-overlay {
  position: fixed;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  z-index: 1;
}
.users-span__details,
.users-span__user-frame {
  z-index: 10;
}
</style>
