<template>
    <div class="address-book-holder" v-if="isLoaded">
        <div class="item user" v-if="selectedUser && selectedUser.user_id">
            <div>Selected:</div>
            <div class="flex">
                <img class="ab__userpic" width="40px" :src="selectedUser.userpic">
                <div class="vaHack">
                    <p>
                        <span>{{ selectedUser.username || '' }}</span>&nbsp;
                        <span style="opacity: .5;">{{ selectedUser.user_phone || '' }}</span>
                    </p>
                </div>
            </div>
        </div>

        <div v-if="users.length && !disabled">
            <div class="ui input" v-if="users.length < 1">
                <select
                    class="hm legal"
                    id="name"
                    @change="selectUser"
                    v-model="selectedUser"
                >
                    <option v-for="user in users" :key="user.user_id" :value="user">{{ user.username }}</option>
                    <!--
                    TODO otherwise just let user type in the name instead
                    TODO do we re-use address book component here?
                    -->
                </select>
            </div>
            <div v-else class="ui large icon input search" style="width:100%">
                <Autocomplete
                    :items="usersToSelect" 
                    v-model="selectedUser" 
                    :wait="100"
                    :min-len="0"
                    :component-item="userTemplate"
                    :input-attrs="{ placeholder: 'Search people...' }"
                    :get-label="user => user && user.username"
                    @input="selectUser"
                    @update-items="updateUsersToSelect"
                ></Autocomplete>
                <i class="search icon"></i>
            </div>
        </div>
        <div class="explanation" v-else-if="explanationIfEmpty">
            <p class="muted">It's possible to (assign) people that
                you have a working relationship with.
            </p>
            <p class="muted">So, you either hire them, they hire you, or you're connected
                through some org (e.g. have the same employer)
            </p>
            <p style="text-align:right;">
                <a style="margin:2rem 0;" class="hm link">comb employment offer</a>
            </p>
        </div>
    </div>
</template>

<script>
import Autocomplete from 'v-autocomplete'
import 'v-autocomplete/dist/v-autocomplete.css'
import UserInList from './UserInList.vue'

export default {
    name: 'AddressBook',
    components: {
        Autocomplete
    },
    props: {
        explanationIfEmpty: {
            type: Boolean
        },
        user: {
            type: Object
        },
        disabled: {
            type: Boolean
        }
    },
    data() {
        return {
            users: [],
            usersToSelect: [],
            selectedUser: this.user || {
                user_id: window.user_id,
                username: window.username,
                handle: window.handle,
                userpic: window.userpic
            },
            isLoaded: false,

            userTemplate: UserInList
        }
    },
    computed: {
        csrfToken: function () { return window.csrftoken },
        apiUrl: function () {
            return window.location.origin + '/api/social'
        }
    },
    methods: {
        selectUser(){
            if(this.selectedUser && this.selectedUser.user_id){
                this.$emit('select', { user: this.selectedUser, me: this.selectedUser.handle == window.handle })
                this.$emit('input', this.selectedUser.user_id)
            }else{
                this.$emit('select', {})
                this.$emit('input', null)
            }
        },
        updateUsersToSelect(text){
            this.usersToSelect = this.users.filter(u => typeof(u.username) == 'string' && u.username.includes(text))
        }
    },
    mounted(){        
        fetch(this.apiUrl + '/address-book')
        .then(res => res.ok && res.json())
        .then(res => {
            if(!res) return

            this.users = this.usersToSelect = res
            this.isLoaded = true
        })
    }
}
</script>

<style>
.v-autocomplete{
    width: 100%;
}
.v-autocomplete-input{
    width: 100% !important;
}
.v-autocomplete-list{
    background-color: #fff !important;
    z-index: 10 !important;
}
</style>
