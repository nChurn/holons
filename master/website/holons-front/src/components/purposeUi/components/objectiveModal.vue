<template>
    <div
        @click="() => $parent.editObjective = null"
        @keydown.esc="() => $parent.editObjective = null"
        class="hm modal"
    >
        <div @click.stop="" class="new-objective content">
            <h2 class="title">{{ toEdit.new  ? 'add new' : 'edit' }} objective</h2>

            <input type="text"
            class="hm field big" v-model="toEdit.title"
            :value="title" id="new-objective-title"
            placeholder="do smth great...">
            <div class="btns" style="margin-top:2rem">
                <button @click.prevent="saveObjective" class="button ui black" :disabled="!toEdit.title">{{ toEdit.new  ? 'add' : 'edit' }} objective</button>
                <button @click.prevent="cancelEdit" class="button ui">cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ObjectiveModal',
    props: {
        toEdit: {
            type: Object
        }
    },
    data(){
        return {
            beforeEdit: Object.assign({}, this.toEdit)
        }
    },
    methods: {
        saveObjective(){
            const dataToSend = {
                title: this.toEdit.title,
                purpose_id: this.toEdit.purpose_id
            }

            fetch(this.$parent.apiUrl + `objectives/${this.toEdit.id ? this.toEdit.id : ''}`, {
                method: this.toEdit.id ? 'PATCH' : 'POST',
                body: JSON.stringify(dataToSend),
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            }).then(async res => {
                try{
                    res = await res.json()

                    if(!res.success) console.log(res.message)

                    this.$parent.getPurposes()
                    this.$parent.editObjective = null
                }catch(err){
                    console.log(err)
                }
            })
        },
        cancelEdit(){
            for(let prop in this.toEdit){
                this.toEdit[prop] = this.beforeEdit[prop] || null
            }

            this.$parent.editObjective = null
        }
    }
}
</script>
<style scoped>
.modal{
    display: unset !important;
    position: fixed !important;
}
</style>
