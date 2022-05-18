<template>
    <div @click="() => { this.$parent.editFixedCost = null }" v-if="toEdit" class="hm modal fixed-cost-modal">
        <div @click.stop="" class="content">
            <h2 class="title">log new fixed cost</h2>
            <input class="hm field" type="text" placeholder="name" v-model="toEdit.name"><br><br>
            <input class="hm field" type="number" placeholder="amount" min="0" v-model="toEdit.amount">$<br><br>
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

            <button :disabled="!(this.toEdit.name && this.toEdit.amount)" @click="saveCost" class="ui basic button">ok. log</button>
        </div>
    </div>
</template>

<script>
import TagsInput from '@johmun/vue-tags-input';

export default {
    components: {
        TagsInput
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
            return this.$parent.activeTags.sort((a, b) => a.uses_count - b.uses_count).map(t => ({text: t.name, id: t.id}))
        },
        filteredItems() {
            return this.existedTags.filter(i => i.text.toLowerCase().includes(this.tag.toLowerCase()));
        },
    },
    methods: {
        saveCost(){
            const dataToSend = {}
            const fields = ['name', 'amount', 'tags', 'context_id']
            fields.forEach(p => { dataToSend[p] = this.toEdit[p] })
            dataToSend.tags = typeof(dataToSend.tags) == 'object' ?  dataToSend.tags.map(t => t.id) : null

            fetch(this.$parent.apiUrl + `/fixed-costs${this.toEdit.id ? '/' + this.toEdit.id : ''}`, {
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

                this.$parent.getFixedCosts()
            })
            .catch(console.log)
            .finally(() => this.$parent.editFixedCost = null)
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
                // evt.addTag()
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
            const tagInput = document.querySelector('.fixed-cost-modal .ti-new-tag-input');
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