<template>
    <div @click="() => { this.$parent.editVariableCost = null }" v-if="toEdit" class="hm modal variable-cost-modal">
        <div @click.stop="" class="content">
            <h2 class="title">log new variable cost</h2> 
            <input type="text" placeholder="name" v-model="toEdit.name"><br><br>
            <input type="number" placeholder="amount, $$" min="0" v-model="toEdit.amount"><br><br>
            <TagsInput
                v-model="tag"
                :tags="tags"
                :autocomplete-items="filteredItems"
                @tags-changed="newTags => tags = newTags"
                :add-on-key="[13, ';', ',', '.', ':']"
                :autocomplete-min-length="isTagsFocused ? 0 : 1"
                placeholder="tags"
                @before-adding-tag="addTag"
                @before-deleting-tag="deleteTag"
            ></TagsInput><br>
            
            <DatePicker
                v-model="toEdit.date"
            ></DatePicker><br><br>

            <button :disabled="!(this.toEdit.name && this.toEdit.amount && this.toEdit.date)" @click="saveCost" class="ui basic button">ok. log</button>
        </div>
    </div>
</template>

<script>
import TagsInput from '@johmun/vue-tags-input'

import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'

export default {
    components: {
        TagsInput,
        DatePicker
    },
    props: {
        toEdit: {}
    },
    data() {
        return {
            tag: '',
            tags: [],
            isTagsFocused: false
        }   
    },
    computed: {
        existedTags(){
            return this.$parent.activeTags.sort((a, b) => a.uses_count - b.uses_count).map(t => {
                t.text = t.name
                return t
            })
        },
        filteredItems() {
            return this.existedTags.filter(i => i.text.toLowerCase().includes(this.tag.toLowerCase()));
        },
        
    },
    methods: {
        saveCost(){
            const dataToSend = {}
            const fields = ['name', 'amount', 'tags', 'context_id', 'date']
            fields.forEach(p => { dataToSend[p] = this.toEdit[p] })
            dataToSend.tags = this.tags.map(t => t.id)

            fetch(this.$parent.apiUrl + `/variable-costs${this.toEdit.id ? '/' + this.toEdit.id : ''}`, {
                method: this.toEdit.new ? 'POST' : 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.$parent.getVariableCosts()
            })
            .catch(console.log)
            .finally(() => this.$parent.editVariableCost = null)
        },
        addTag(evt){
            if(evt.tag.id){
                this.toEdit.tags.push(evt.tag)

                return evt.addTag()
            }

            fetch(this.$parent.apiUrl + '/tags', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: evt.tag.text,
                    context_id: this.$parent.activeContext.id
                })
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                evt.tag = {
                    id: res.id,
                    name: evt.tag.text,
                    text: evt.tag.text,
                    context_id: this.$parent.activeContext.id,
                    uses_count: 0
                }
                this.$parent.activeTags.push(evt.tag)
                this.toEdit.tags.push(evt.tag)
                this.tag = ''
            })
        },
        deleteTag(evt){
            this.toEdit.tags.splice(this.toEdit.tags.findIndex(t => t.id == evt.tag.id), 1)
            evt.deleteTag()
        }
    },
    mounted(){
        setTimeout(() => {
            const tagInput = document.querySelector('.variable-cost-modal .ti-new-tag-input');
            if(tagInput){
                tagInput.onfocus = () => { this.isTagsFocused = true }
                tagInput.onblur = () => { this.isTagsFocused = false }
            }
        }, 0)
    },
    beforeUpdate(){
        if(this.toEdit){
            const newTags = this.toEdit.tags.filter(toEditTag => !this.tags.find(t => t.id == toEditTag.id))
            if(newTags.length) this.tags.push(...newTags.map(t => { t.text = t.name; return t }))

            if(this.toEdit.date && typeof(this.toEdit.date) != 'object'){
                this.toEdit.date = new Date(this.toEdit.date)
            }
        }else{
            this.tags = []
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