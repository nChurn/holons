<template>
    <tr>
        <td >
            <div class="ui dropdown icon item">
                <i class="wrench icon"></i>
                <div @click.self="() => null" class="menu">
                    <div @click.self="function(){ $parent.editFixedCost = cost }" class="item">
                        edit
                    </div>
                    <div v-if="!cost.finished_at" @click.self="stopLoging" class="item">
                        stop logging from now on
                    </div>
                    <div @click.self="deleteCost" class="item">
                        delete from logs
                    </div>
                </div>
            </div>
        </td>
        <td>{{ cost.name }}</td>
        <td>${{ cost.amount }}</td>
        <td><span class="cost-tag" v-for="tag in cost.tags" :key="tag.id">{{ tag.name }}</span></td>
    </tr>
</template>

<script>
export default {
    props:{
        cost: {
            type: Object,
            required: true
        }
    },
    methods: {
        stopLoging(){
            fetch(this.$parent.apiUrl + `/fixed-costs/${this.cost.id}`, {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    finish: true
                })
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.$parent.getFixedCosts()
            })
        },
        deleteCost(){
            fetch(this.$parent.apiUrl + `/fixed-costs/${this.cost.id}`, {
                method: 'DELETE',
                headers:{
                    'X-CSRFToken': this.$parent.getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(res => res.ok && res.json())
            .then(res => {
                if(!res) return

                this.$parent.getFixedCosts()
            })
        }
    },
    mounted(){
        $('.ui.dropdown').dropdown()
    }
}
</script>