<template>
    <div
        @click="() => ($parent.editKeyResult = null)"
        @keypress.esc="() => ($parent.editKeyResult = null)"
        class="hm modal"
    >
        <div @click.stop="" class="new-key-result content">
            <h2 class="title">
                {{ toEdit.new ? "add new" : "edit" }} key result
            </h2>

            <input
                type="text"
                class="hm field big"
                v-model="toEdit.title"
                id="new-key-result-title"
                placeholder="key result..."
                style="margin-bottom: 2rem"
            />

            <div class="ui grid">

                <div class="eight wide column">
                  <h5>type</h5>
                    <div class="form__radios">
                        <div v-for="t in types" :key="t.id" class="form__radio">
                            <label :for="'krType-' + t.id">{{ t.name }}</label>
                            <input
                                :id="'krType-' + t.id"
                                name="type"
                                type="radio"
                                :value="{ id: t.id, name: t.name }"
                                v-model="toEdit.type"
                                :checked="toEdit.type && t.id == toEdit.type.id"
                            />
                        </div>

                        <p class="muted" style="margin:1rem">
                            Types below will pull data
                            automatically in real time. Otherwise the data is updated manually on check-ins.</p>

                        <div style="opacity: 0.5;" class="form__radio"> <!-- V2 Moneta: entities’ profit -->
                            <label for="krType-5">Profit booked @moneta</label>
                            <input disabled id="krType-5" name="type" type="radio" value="">
                        </div>

                        <div style="opacity: 0.5;" class="form__radio">
                            <label for="krType-4">Commitments made @relations</label>
                            <input disabled id="krType-4" name="type" type="radio" value="">
                        </div>

                        <div style="opacity: 0.5;" class="form__radio">
                            <label for="krType-4">Revenue collected @relations</label>
                            <input disabled id="krType-4" name="type" type="radio" value="">
                        </div>

                        <div style="opacity: 0.5;" class="form__radio"> <!-- V2 Meet: number of meetings -->
                            <label for="krType-6">Meetings done @meet</label>
                            <input disabled id="krType-6" name="type" type="radio" value="">
                        </div>

                        <div style="opacity: 0.5;" class="form__radio disabled">
                            <label for="krType-7">Hosting feature</label>
                            <input disabled id="krType-7" name="type" type="radio">
                        </div>
                    </div>
                </div>

                <div class="eight wide column" v-if="!isYesNoType">
                    <h5>target value</h5>
                        <input
                            type="number"
                            class="hm field big"
                            style="text-align:center"
                            v-model="toEdit.target_value"
                            id="new-key-result-target"
                        />

                    <br>
                    <h5>check-in rhythm</h5>
                    <p>
                        Every X weeks the owner will get status update request.
                        Responses are attached to key results of currently active season
                    </p>
                    <div class="ui input">
                        <input type="number" placeholder="Inteval (weeks)" v-model="toEdit.interval">
                    </div>

                    <div v-if="!isPersonalContext">
                        <h5>owner</h5>
                        <!-- TODO:
                        1. if social graph count less than X don't show search
                        2. v2: live typing would be nice -->

                        <br><br>

                        <div class="hm list" style="margin:0 -3px">
                            <div 
                                v-for="user in users" 
                                :key="user.user_id" 
                                :class="[{active: toEdit.owner && user.user_id == toEdit.owner.user_id},'item', 'user']"
                            >
                                <div class="flex">
                                    <img class="ab__userpic" width="40px" :src="user.userpic">
                                    <div class="vaHack">
                                        <h5>{{ user.username }}</h5>
                                        <p>{{ user.user_phone }}</p>
                                    </div>
                                    <!--<p class="vaHack">$15 \ hour</p>-->

                                </div>
                                <button 
                                    type="button"
                                    class="ui basic button mrgn0"
                                    @click="() => { toEdit.owner = user; toEdit.owner_id = user.user_id; $forceUpdate() }"
                                >assign</button>
                            </div>

                            <!--<h2 style="padding:2rem 0; margin-top:2rem;border-top:30px solid #23272B">
                                Talent Augmentation Broker</h2>-->

                            <div class="item">
                                <div class="flex">
                                <img class="ab__userpic" width="40px"
                                src="https://holons.me/scaled/resize/100x100//usg/usg/soulspics/fNii1u_phsk.jpg">
                                <div class="vaHack">
                                    <h5>Athena</h5>
                                    <p>Executive Assistant</p>
                                </div>
                                <!--<p class="vaHack">$15 \ hour</p>-->

                                </div>
                                <button type="button"
                                class="ui basic button mrgn0">schedule a discovery call</button>
                            </div>
                            <div class="item">
                                <div class="flex">
                                    <img class="ab__userpic" width="40px"
                                    src="https://holons.me/scaled/resize/100x100//usg/usg/soulspics/fNii1u_phsk.jpg">
                                    <div class="vaHack">
                                        <h5>Talant</h5>
                                        <p>Talent Augmentation Broker</p>
                                    </div>
                                </div>
                                <button 
                                    type="button"
                                    class="ui basic button mrgn0"
                                >chat</button>
                            </div>
                        </div> <!-- list ends -->
                    </div>
                </div>
            </div>

            <div class="btns">
                <button
                    @click="saveKeyResult"
                    class="ui button black"
                    :disabled="(
                        !toEdit.title || !toEdit.target_value || 
                        !toEdit.type || !toEdit.type.id || 
                        !toEdit.owner_id && !isYesNoType && !isPersonalContext
                    )"
                >{{ toEdit.new ? 'add' : 'edit' }} key result</button>
                <button
                    @click="cancelEdit"
                    class="button ui"
                >cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';
Vue.use(Loading, { zIndex: 9999, })

import AddressBook from '../../addressBookComponent'
export default {
    name: "KeyResultModal",
    components: {
        AddressBook
    },
    props: {
        toEdit: {
            required: true,
        },
    },
    data() {
        return {
            types: [],
            beforeEdit: Object.assign({}, this.toEdit),
            users: []
        };
    },
    computed: {
        isYesNoType() {
            return (this.toEdit.type.name && this.toEdit.type.name.toLowerCase() == "yes/no")
        },
        isPersonalContext(){
            return this.$parent.purpose && this.$parent.purpose.context.type == 'user_personal'
        }
    },
    methods: {
        saveKeyResult() {
            const dataToSend = {
                type_id: this.toEdit.type.id,
            }

            for(let prop of ['title', 'owner_id', 'interval', 'target_value', 'objective_id']){
                if(typeof(this.toEdit[prop]) != 'undefined') dataToSend[prop] = +this.toEdit[prop] || this.toEdit[prop]
            }

            fetch(this.$parent.$parent.apiUrl + `keyresults/${this.toEdit.id ? this.toEdit.id : ""}`, {
                method: this.toEdit.id ? "PATCH" : "POST",
                body: JSON.stringify(dataToSend),
                headers: {
                    "X-CSRFToken": this.$parent.$parent.getCookie("csrftoken"),
                    "Content-Type": "application/json",
                },
            })
            .then(async res => {
                try{
                    res = await res.json();

                    if (!res.success) return console.log(res.message);

                    if(this.toEdit.new){
                        this.toEdit.id = res.id
                        this.toEdit.creator = {
                            userpic: window.userpic,
                            user_id: window.user_id,
                            username: window.username,
                            handle: window.handle
                        }
                        this.$parent.purpose.objectives.find(o => o.id == this.toEdit.objective_id).key_results.push(this.toEdit)
                    }
                    delete this.toEdit.new

                    this.$parent.$forceUpdate()

                    this.$parent.editKeyResult = null
                }catch(err){
                    console.log(err)
                }
            })
        },
        cancelEdit(){
            for(let prop in this.toEdit){
                this.toEdit[prop] = this.beforeEdit[prop] || null
            }

            this.$parent.editKeyResult = null
        }
    },
    mounted() {
        fetch(this.$parent.$parent.apiUrl + "keyresults/types")
        .then((res) => res.ok && res.json())
        .then((res) => {
            if (!res) return

            this.types = res

            return new Promise((resolve, rej) => resolve())
        })
        .then(() => fetch(window.location.origin + '/api/social/address-book'))
        .then(res => res.ok && res.json())
        .then(res => {
            if(!res) return

            this.users = res
        })
    },
    beforeUpdate() {
        if (this.toEdit && this.toEdit.type.name == "yes/no") {
            this.toEdit.target_value = 1
            this.toEdit.owner = null
            this.toEdit.owner_id = null
            this.toEdit.interval = null
        }
    },
};
</script>

<style scoped>
.modal {
    position: fixed !important;
    display: unset !important;
}
.new-key-result__item {
    margin: 5px 0;
}
.user.active{
    border: 1px black solid;
    border-radius: 3px;
}
</style>
