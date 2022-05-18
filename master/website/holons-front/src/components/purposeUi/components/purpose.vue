<template>
    <div class="purpose" v-if="purpose">
        <KeyResultModal v-if="editKeyResult" :toEdit="editKeyResult"></KeyResultModal>

        <!--<h1 class="purpose__status">{{ purpose.status }}</h1>-->
        <br><br>
        <div class="flex purpose__title">
            <input
                @change="changePurpose"
                placeholder="state your purpose"
                class="hm field big purpose-working__input"
                v-model="purpose.title"
                v-if="purpose && purpose.status == 'draft'"
            >

            <h1 v-if="purpose && purpose.status != 'draft'">{{ purpose.title }}</h1>
        </div>

        <p v-if="purpose && purpose.status == 'draft'"
        class="muted" style="margin: 2rem 0">
            Add objectives and corresponding key results.
            They say, there should be up to 5 objectives with 3-4 results each. <br>
            You may read <a href="https://odyssey.holons.me/en/nodes/purpose" class="hm link">about the framework</a>
            if you're not sure what's going on.
        </p>


            <button
                v-if="purpose && purpose.status == 'draft'"
                @click="() => { $parent.editObjective = {new: true, purpose_id: purpose.id, title: ''} }"
                class="ui basic button" style="width:100%"
            >+ objective</button>

            <br><br>

            <div
                class="objective"
                v-for="objective in purpose.objectives"
                :key="objective.id"
            >
                <!-- objective title -->
                <div class="flex">
                    <h2 class="objective__title">
                        {{ objective.title }}
                    </h2>
                    <div v-if="purpose && purpose.status == 'draft'">
                        <a
                            class="hm link"
                            @click.stop="function(){ $parent.editObjective = objective }"
                        >edit</a>
                        \
                        <a
                            class="hm link"
                            @click.stop="() => deleteObjective(objective)"
                        ><i class="trash alternate outline icon"></i></a>

                        <br><br>
                        <button
                            v-if="purpose && purpose.status == 'draft'"
                            class="ui basic button" style="width:100%"
                            @click.stop="function(){ editKeyResult = {new: true, objective_id: objective.id, type: {id: 2, name: 'number'}, title: '', target_value: 0} }"
                        >+ key result</button>
                    </div>
                </div>
                <!-- objective title ends -->

                <div class="key-result__container">
                    <table class="hm ui table">
                        <thead>
                            <tr>
                                <td style="padding-left: 0">owner</td>
                                <td></td>
                                <td v-if="purpose && purpose.status != 'draft'">fact</td>
                                <td>plan</td>
                            </tr>
                        </thead>
                    </table>
                        <!-- key result starts -->
                        <KeyResult v-for="keyResult in objective.key_results" :key="keyResult.id" :keyResult="keyResult"></KeyResult>
                        <!-- key result ends -->

            </div>
        </div>
        <DatePicker
            v-model="purpose.plan_end_date"
            @change="changePurpose"
            v-if="purpose && purpose.status == 'draft'"
        ></DatePicker>
        <div class="purpose__date" v-else>
            End date: 
            {{ 
                purpose.plan_end_date ? 
                Intl.DateTimeFormat('en', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(purpose.finish_at || purpose.plan_end_date) : 
                '' 
            }}
            </div>
        <div class="purpose__btns" v-if="$parent.isActiveContextMy">
            <button @click="endPurpose" style="width:100%"
            class="ui basic button" v-if="purpose &&  purpose.status == 'start'">end season</button>
            <!-- <button @click="deletePurpose" class="button ui red" v-if="purpose && purpose.status == 'draft'">delete draft</button> -->
            <button
                @click="startPurpose" style="width:100%"
                class="hm button core"
                v-if="purpose && purpose.status == 'draft' && !$parent.activeContextPurposes.filter(p => p.status == 'start').length"
                :disabled="!purpose || !purpose.objectives || !purpose.objectives.length || !purpose.title"
            >launch season</button>
            <h2 v-else-if="purpose && purpose.status == 'draft'" class="muted">end the current season before you can launch a new one</h2>
        </div>
    </div>
</template>

<script>
import KeyResultModal from './keyResultModal.vue'
import KeyResult from './keyResult.vue'

import DatePicker from 'vue2-datepicker'

export default {
    name: 'Purpose',
    components:{
        KeyResultModal: KeyResultModal,
        KeyResult: KeyResult,
        DatePicker: DatePicker
    },
    props: {
        purpose: {
            required: true
        }
    },
    data() {
        return {
            activeObjective: null,

            keyResults: null,
            editKeyResult: null
        }
    },
    methods:{
        changePurpose(){
            const dataToSend = {
                title: this.purpose.title
            }

            if(this.purpose.plan_end_date){
                dataToSend.plan_end_date = this.purpose.plan_end_date
            }

            fetch(this.$parent.apiUrl + this.purpose.id, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            })
            .then(res => res.json())
            .then(res => {
                if(!res || !res.success) return

                this.$parent.getPurposes()
            })
        },
        startPurpose(){
            fetch(this.$parent.apiUrl + this.purpose.id, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ start_at: (new Date()).toISOString() })
            })
            .then(res => res.json())
            .then(res => {
                if(!res || !res.success) return

                this.$parent.activePurpose = null
                this.$parent.getPurposes()
            })
        },
        endPurpose(){
            fetch(this.$parent.apiUrl + this.purpose.id, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ finish_at: true })
            })
            .then(res => res.json())
            .then(res => {
                if(!res || !res.success) return

                this.$parent.getPurposes()
                this.$parent.openFinish()
            })
        },
        deletePurpose(){
            fetch(this.$parent.apiUrl + this.purpose.id, {
                method: 'DELETE' ,
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                },
            })
            .then(res => res.json())
            .then(res => {
                if(!res || !res.success) return

                this.$parent.getPurposes()
                this.$parent.activePurpose = null
            })
        },

        switchObjective(objective, forceOpen=false){
            if(typeof(objective) == 'number')
                objective = this.purpose.objectives.find(o => o.id == objective)

            if(this.activeObjective == objective && !forceOpen){
                this.activeObjective = null
                this.keyResults = null
                return
            }

            this.activeObjective = objective

            if(!objective || !objective.id) return

            fetch(this.$parent.apiUrl + `objectives/${objective.id}`)
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return;

                this.keyResults = res.key_results
            })
            .catch(err => console.log('Err while loading objective info: ' + err))
        },
        deleteObjective(objective){
            fetch(this.$parent.apiUrl + `objectives/${objective.id}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                }
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res || !res.success) return


                this.$parent.getPurposes()
                this.activeObjective = null
            }).catch(err => console.log('Err while deleting objective: ' + err))
        },

        changeKeyResultValue(kr, evt){
            kr.current_value = evt.target.value

            fetch(this.$parent.apiUrl + `keyresults/${kr.id}`, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_value: evt.target.value
                })
            })
        },
        deleteKeyResult(keyResult){
            fetch(this.$parent.apiUrl + `keyresults/${keyResult.id}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                }
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res || !res.success) return

                // this.switchObjective(this.activeObjective, true)
                let keyResults = this.purpose.objectives.find(o => o.id == keyResult.objective_id).key_results
                // keyResults = keyResults.filter(kr => kr.id != keyResult.id)

                this.purpose.objectives.find(o => o.id == keyResult.objective_id).key_results.splice(keyResults.indexOf(keyResult), 1)
            }).catch(err => console.log('Err while deleting key result: ' + err))
        }
    },
    beforeUpdate(){
        if(this.purpose && typeof(this.purpose.plan_end_date) == 'string'){
            this.purpose.plan_end_date = new Date(this.purpose.plan_end_date)
        }
        if(this.purpose && typeof(this.purpose.finish_at) == 'string'){
            this.purpose.finish_at = new Date(this.purpose.finish_at)
        }
    }
}
</script>
