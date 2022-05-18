<template>
<div id="purposeWrap">
  <ObjectiveModal v-if="editObjective" :toEdit="editObjective"></ObjectiveModal>

  <div class="ui secondary menu secondary-navigation">

        <!--<h3 class="item vip-title" style="padding-left: 0; margin-left: 0">
          Audits</h3>-->

          <Context
            :context="{ id: 0, type: 'all mine', foreign: {name: 'all mine'}, owner: {user_id: me.user_id} }"
            :isActive="activeContext && (activeContext.id === 0 || activeContext.type == 'all mine')"
            @select="switchContext"
          ></Context>

          <Context
            @select="switchContext"
            v-for="context in contexts.filter(c => c.type.includes('user'))"
            :key="context.id"
            :context="context"
            :isActive="activeContext && activeContext.id == context.id"
          ></Context>



        <div class="right menu">

          <Context
            @select="switchContext"
            v-for="context in contexts.filter(c => !c.type.includes('user'))"
            :key="context.id"
            :context="context"
            :isActive="activeContext && activeContext.id == context.id"

          ></Context>

        </div>
  </div>
    <div style="background: #23272B;margin-top:5rem"
    class="ui secondary menu secondary-navigation inverted">
        <a @click="openCurrent" :class="['item', {'active': tab == 'current'}]">current season</a>
        <div class="right menu" v-if="isActiveContextMy">
            <a :class="['item', {'active': tab == 'draft'}]" @click="openDraft">next season draft</a>
            <a :class="['item', {'active': tab == 'finish'}]" @click="openFinish">days of past glory</a>
        </div>
    </div>

  <div style="margin:2rem">

        <!-- <h1 style="max-width:700px;font-size:300%;text-shadow: 1px 1px 1px #23272B">
            current purpose season boldly stated
        </h1> -->

        <AllMineKRs
            v-if="activeContext && activeContext.type == 'all mine'"
            :filter="tab"
        ></AllMineKRs>
        <PurposeList
            v-if="!activePurpose && tab == 'finish'"
            @select="switchPurpose"
            :purposes="activeContextPurposes.filter(p => p.status == 'finish')"
        ></PurposeList>
        <Purpose :purpose="activePurpose"></Purpose>
        <div v-if="tab == 'current' && !activePurpose && activeContext && activeContext.id" class="no-current">No current season</div>

  </div>

</div>
</template>

<script>
import 'vue-loading-overlay/dist/vue-loading.css'
import Context from './components/context.vue'
import Purpose from './components/purpose.vue'
import PurposeList from './components/purposeList.vue'
import ObjectiveModal from './components/objectiveModal.vue'
import AllMineKRs from './AllMineKRs.vue'

export default {
    name: 'PurposeUiComponent',

    components: {
        Context: Context,
        Purpose: Purpose,
        PurposeList: PurposeList,
        ObjectiveModal: ObjectiveModal,
        AllMineKRs: AllMineKRs
    },
    data(){
        return {
            loader: null,

            contexts: [],
            activeContext: null,

            purposes: [],
            activePurpose: null,

            editObjective: null,

            tab: 'current',

            me: {
                user_id: window.user_id
            }
        }
    },
    computed: {
        apiUrl() {
            return window.location.origin + '/api/purpose/'
        },
        activeContextPurposes(){
            return this.activeContext ? this.purposes.filter(p => p.context.id == this.activeContext.id) : []
        },
        isActiveContextMy(){
            return !this.activeContext || !this.activeContext.owner || this.activeContext.owner.user_id == this.me.user_id
        }
    },
    methods: {
        getContexts(){
            return new Promise((resolve, rej) => {
                fetch(this.apiUrl + 'contexts')
                .then(res => res.ok && res.json())
                .then(res => {
                    if(!res) return
    
                    this.contexts = res
                    this.activeContext = res.find(c => c.foreign.name == window.handle)
                    this.activeContext.foreign.name = 'professional'
    
                    this.$forceUpdate()

                    resolve()
                })
                .catch(err => { console.log('Err while loading contexts: ' + err); rej(err)})
            })

        },
        switchContext(newCtx){
            this.activeContext = newCtx
            this.activePurpose = null
            this.openCurrent()

            if(!this.activePurpose && this.activeContext.id){
                this.openDraft()
            }
        },
        getPurposes(id = this.activePurpose && this.activePurpose.id){
            return new Promise((resolve, reject) => {
                fetch(this.apiUrl)
                .then(res => res.ok && res.json())
                .then(res => {
                    if(!res) return

                    this.purposes = res

                    if(id){
                        this.activePurpose = this.purposes.find(p => p.id == id)
                        this.activeContext = (
                            this.activePurpose ? 
                            this.contexts.find(c => c.id  == this.activePurpose.context.id) : 
                            this.contexts.find(c => c.foreign.name == window.handle)
                        )
                    }

                    this.$forceUpdate()
                    
                    if(!this.activePurpose){
                        this.openCurrent() || this.openDraft()
                    }else{
                        this.tab = this.activePurpose.status == 'start' ? 'current' : this.activePurpose.status
                    }
                    
                    console.log('from getPurposes', this.activeContext);
                    resolve()
                })
                .catch(err => console.log('Err while loading purposes: ' + err))
            })
        },
        openCurrent(){
            this.tab = 'current'
            this.activePurpose = this.activeContextPurposes.find(p => p.status == 'start')

            return this.activePurpose
        },
        openDraft(){
            if(!this.isActiveContextMy) return

            this.tab = 'draft'
            this.activePurpose = this.activeContextPurposes.find(p => p.status == 'draft')
            if(!this.activePurpose && this.activeContext && this.activeContext.id){
                fetch(this.apiUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        context_id: this.activeContext.id,
                    })
                })
                .then(res => res.json())
                .then(res => {
                    if(!res || !res.success) return

                    if(this.tab =='draft') this.getPurposes(res.id)
                })
            }
        },
        openFinish(){
            if(!this.isActiveContextMy) return
            this.activePurpose = null
            this.tab = 'finish'
        },
        switchPurpose(newPurpose){
            this.activePurpose = newPurpose
        },
        getCookie(name) {
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;
        }
    },
    mounted() {
        const purposeId = (new URLSearchParams(window.location.search)).get('purposeId')

        this.getContexts()
        .then(() => purposeId ? this.getPurposes(purposeId) : this.getPurposes())
        .then(() => {
            history.pushState(null, null, window.location.origin + window.location.pathname)
            
            if(this.purposes.filter(p => p.status == 'start').length > 2){
                this.activeContext = { type: 'all mine', id: 0, foreign: { name: 'all mine' } }
                this.activePurpose = null
            }
        })
    },
}
</script>

<style scoped>
  .active{
    z-index: 10;
  }
</style>
